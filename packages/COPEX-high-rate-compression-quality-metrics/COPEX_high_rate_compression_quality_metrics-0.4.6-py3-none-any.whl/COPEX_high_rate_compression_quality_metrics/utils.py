import glob
import os
import re
from datetime import datetime
from typing import List, Optional, Dict, Any

import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.enums import Resampling

lib_version = ("0.4.6")


def get_lib_version():
    return lib_version


compressed_folder_name = "compressed"
decompressed_folder_name = "decompressed"
original_folder_name = "original"
algorithm_colors = {
    "JJ2000": "green",
    "HiFiC": "green",
    # Ajoute d'autres algorithmes et leurs couleurs ici
}
thematics_dictionary = {

}
metrics_dictionary = {
    "LPIPS":{
        "min":0,
        "max":1
    },
    "SSIM":{
        "min":0.995,
        "max":1
    },
    "RMSE":{
        "min":0,
        "max":650
        #Pourquoi 650 ? , avec 40db comme valeure d'appuis on a :
        #PSNR = 20.log10(MAX) - 10.log10(MSE)
        #5,6329598612473982468396446311838 = log10(MSE)
        #MSE = 429519
        #RMSE = 655,3769
    },
    "PSNR":{
        "min":40,
        "max":100
    }
}
data_range_for_compression = {
    "min" : 0,
    "max" : 1000
}
bands_per_satellite_type = {
    "S2_L1C":{
        1:"B01",
        2:"B02",
        3:"B03",
        4:"B04",
        5:"B05",
        6:"B06",
        7:"B07",
        8:"B08",
        9:"B09",
        10:"B10",
        11:"B11",
        12:"B12",
        13:"B8A"
    },
"S1_GRD":{
        1:"VV",
        2:"VH",
    }

}
summary_output_folder_name = "summary"
summary_output_csv_folder_name = "csv"
summary_output_png_folder_name = "png"

def get_product_name_from_final_folder_path(original_folder_path, num_de_dossier_en_partant_de_la_fin=-2):
    """
        Extrait l'avant-dernier dossier dans un chemin donné et isole la partie spécifique du nom de dossier.

        Args:
            path (str): Le chemin de fichier complet.
            num_de_dossier_en_partant_de_la_fin(int) : de combien on recule pour prendre le  nom de dossier, -2 = on regule de 1

        Returns:
            tuple: (avant_dernier_dossier, partie_extraite)
        """
    # Récupérer l'avant-dernier dossier du chemin
    # print("getting product name from ",original_folder_path)
    path_parts = original_folder_path.split(os.sep)  # Divise le chemin en parties
    if len(path_parts) < 2:
        raise ValueError("Le chemin n'a pas suffisamment de dossiers.")

    avant_dernier_dossier = path_parts[num_de_dossier_en_partant_de_la_fin]  # Avant-dernier dossier
    # print("avant_dernier_dossier = ",avant_dernier_dossier)
    # Isoler la partie avant ']_' du dossier
    # match = re.search(r'^(\[.*?\])', avant_dernier_dossier)
    if avant_dernier_dossier:
        product_name = avant_dernier_dossier.split(']_')[1][1:]  # Enlever les crochets []
    else:
        product_name = None  # Aucun match trouvé

    return avant_dernier_dossier, product_name


def create_folder_if_do_not_exist(folder_path):
    """
    Crée un dossier s'il n'existe pas déjà.

    :param folder_path: Chemin du dossier à créer.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Dossier créé : {folder_path}")
    else:
        return
        # print(f"Le dossier existe déjà : {folder_path}")


def resample_band(input_path, output_path, scale_factor=2, resampling_method=Resampling.bilinear):
    """
    Fonction pour rééchantillonner une bande d'image raster en utilisant le
    facteur d'échelle spécifié (2 = on multiplie par 2 le nombre de pixels de l'image en x et y).
     Le rééchantillonnage est, par défaut, fait en
    utilisant la méthode du plus proche voisin, mais peut être modifié via le paramètre.

    Args:
        input_path (str): Chemin du fichier raster d'entrée.
        output_path (str): Chemin du fichier raster de sortie.
        scale_factor (float, optional): Facteur par lequel redimensionner l'image.
                                        Par défaut, le facteur est 2.
        resampling_method (rasterio.enums.Resampling, optional): Méthode de rééchantillonnage.
                                        Par défaut, la méthode du plus proche voisin (nearest ou bilinear).

    Returns:
        None. Le fichier rééchantillonné est écrit dans output_path.

    Exemple:
        resample_band("input.tif", "output.tif", scale_factor=3, resampling_method=Resampling.bilinear)
    """
    with rasterio.open(input_path) as src:
        # Récupérer les métadonnées
        profile = src.profile

        # Calculer les nouvelles dimensions
        new_width = int(src.width * scale_factor)
        new_height = int(src.height * scale_factor)

        # Mettre à jour le profil pour le fichier de sortie
        profile.update(
            width=new_width,
            height=new_height,
            transform=src.transform * src.transform.scale(
                (src.width / new_width),
                (src.height / new_height)
            )
        )

        # Rééchantillonner l'image
        data = src.read(
            out_shape=(src.count, new_height, new_width),
            resampling=resampling_method
        )

        # Écrire les données rééchantillonnées
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(data)

    print(f"{input_path} rééchantillonné et sauvegardé sous {output_path}")


def get_nn_vv_ppp_from_full_nnvvppp_algo_name(nnvvppp_algo_name: str) -> str:
    """
    Extrait la partie NN-VV-PPP du nom complet de l'algorithme.

    Args:
        nnvvppp_algo_name (str): Le nom complet de l'algorithme au format 'NN-VV-PPP_suffixedetails'.

    Returns:
        str: La partie NN-VV-PPP extraite du nom complet de l'algorithme.

    Raises:
        ValueError: Si le nom de l'algorithme ne contient pas de séparateur '_' ou si la partie avant le premier '_'
                    est trop courte pour être valide.
    """
    split_list = nnvvppp_algo_name.split("_")[0]
    if len(split_list) < 2:
        raise ValueError(
            f"Le chemin spécifié '{nnvvppp_algo_name}' n'est pas un nom valide, avoir un format nnvvppp_algoname.")
    return nnvvppp_algo_name.split("_")[0]


def get_product_path_list_from_path(path: str) -> List[str]:
    """
    Récupère tous les fichiers TIFF (.tif et .tiff) présents dans le dossier spécifié.

    Args:
        path (str): Le chemin du dossier à explorer.

    Returns:
        List[str]: Une liste des chemins complets des fichiers TIFF trouvés dans le dossier.
    """
    # Liste pour stocker les chemins des fichiers TIFF
    tiff_files = []

    # Vérifier si le chemin spécifié est un dossier
    if not os.path.isdir(path):
        raise ValueError(f"Le chemin spécifié '{path}' n'est pas un dossier valide.")

    # Lister tous les fichiers dans le dossier
    for file_name in os.listdir(path):
        # Construire le chemin complet du fichier
        file_path = os.path.join(path, file_name)

        # Vérifier si c'est un fichier
        if os.path.isfile(file_path):
            # Extraire l'extension du fichier
            _, ext = os.path.splitext(file_name)

            # Vérifier si l'extension est .tif ou .tiff
            if ext.lower() in {'.tif', '.tiff'}:
                tiff_files.append(file_path)

    return tiff_files


def add_data_to_dict(base_dict: Dict[str, Any], data_to_add: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ajoute des données au dictionnaire de base de manière modulaire.

    Args:
        base_dict (Dict[str, Any]): Le dictionnaire de base auquel les données seront ajoutées.
        data_to_add (Dict[str, Any]): Les données à ajouter au dictionnaire de base.

    Returns:
        Dict[str, Any]: Le dictionnaire mis à jour avec les nouvelles données.
    """
    for key, value in data_to_add.items():
        if isinstance(value, dict):
            # Si la valeur est un dictionnaire, on fusionne les dictionnaires récursivement
            base_dict[key] = add_data_to_dict(base_dict.get(key, {}), value)
        else:
            # Sinon, on ajoute ou remplace la valeur dans le dictionnaire de base
            base_dict[key] = value

    return base_dict


def get_product_name_list_from_path(path: str) -> List[str]:
    """
    Récupère tous les fichiers TIFF (.tif et .tiff) présents dans le dossier spécifié.

    Args:
        path (str): Le chemin du dossier à explorer.

    Returns:
        List[str]: Une liste des chemins complets des fichiers TIFF trouvés dans le dossier.
    """
    # Liste pour stocker les chemins des fichiers TIFF
    tiff_files = []

    # Vérifier si le chemin spécifié est un dossier
    if not os.path.isdir(path):
        raise ValueError(f"Le chemin spécifié '{path}' n'est pas un dossier valide.")

    # Lister tous les fichiers dans le dossier
    for file_name in os.listdir(path):
        # Construire le chemin complet du fichier
        file_path = os.path.join(path, file_name)

        # Vérifier si c'est un fichier
        if os.path.isfile(file_path):
            # Extraire l'extension du fichier
            _, ext = os.path.splitext(file_name)

            # Vérifier si l'extension est .tif ou .tiff
            if ext.lower() in {'.tif', '.tiff'}:
                tiff_files.append(os.path.basename(file_path))

    return tiff_files


def get_test_case_number_str(number) -> str:
    """
        Convertit un nombre entier en une chaîne de caractères sur 3 digits.

        Args:
            number: Le nombre à convertir.

        Returns:
            str: Le nombre formaté en chaîne de caractères sur 3 digits (par exemple, 1 -> '001').
        """
    if type(number) == int:
        return f"{number:03d}"
    else:
        return number


def get_compression_factor_from_compressed_folder_name(folder_name):
    bracket_content = get_bracket_content(folder_name, 2)
    return bracket_content.split("x")[-1]


def get_compressed_folder_name() -> str:
    """
    Retourne le nom du dossier contenant les fichiers compressés.

    Returns:
        str: Le nom du dossier compressé.
    """
    return compressed_folder_name


def get_decompressed_folder_name() -> str:
    """
    Retourne le nom du dossier contenant les fichiers décompressés.

    Returns:
        str: Le nom du dossier décompressé.
    """
    return decompressed_folder_name


def get_original_folder_name() -> str:
    """
    Retourne le nom du dossier contenant les fichiers originaux.

    Returns:
        str: Le nom du dossier original.
    """
    return original_folder_name


def find_matching_file(image_full_name, folder_path):
    """
    Trouve le fichier correspondant dans le répertoire donné qui commence par le nom de base spécifié.

    Args:
        image_full_name (str): Nom de base du fichier (sans extension).
        folder_path (str): Le chemin vers le répertoire où chercher les fichiers.

    Returns:
        str: Le chemin complet du fichier trouvé ou None si aucun fichier correspondant n'est trouvé.
    """
    # Construire le motif de recherche pour les fichiers qui commencent par image_full_name

    base_name = os.path.splitext(image_full_name)[0]
    # Lister tous les fichiers dans le dossier
    all_files = os.listdir(folder_path)

    # Chercher un fichier qui contient le base_name dans son nom
    for file_name in all_files:
        if base_name in file_name and file_name.endswith(('.tif', '.tiff')):
            return os.path.join(folder_path, file_name)
    return None


def get_algorithm_results_full_path(root_directory: str, dataset_name: str, test_case_number,
                                    nnvvppp_algoname: str, verbose=False) -> str:
    """
    Construit le chemin complet vers les résultats d'un algorithme spécifique pour un test donné.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.
        nnvvppp_algoname (str): Le nom de l'algorithme dans le format NN VV PPP_algo.

    Returns:
        str: Le chemin complet vers les résultats de l'algorithme.
    """
    if verbose : print("-- get_algorithm_results_full_path -- getting algo result folder full path 1...")
    test_case_folder = get_use_case_folder(root_directory, dataset_name, get_test_case_number_str(test_case_number),verbose=verbose)
    if verbose : print("-- get_algorithm_results_full_path -- test_case_folder = ", test_case_folder)

    decompressed_folder_name = get_decompressed_folder_name()
    if verbose : print("-- get_algorithm_results_full_path -- decompressed_folder_name = ", decompressed_folder_name)

    algorithm_results_folders = get_algorithm_results_folder(root_directory, dataset_name,
                                                             get_test_case_number_str(test_case_number),
                                                             nnvvppp_algoname, verbose=verbose)
    if verbose : print("-- get_algorithm_results_full_path -- algorithm_results_folders = ", algorithm_results_folders)
    if algorithm_results_folders :

        final_path = os.path.join(root_directory,
                                  dataset_name,
                                  test_case_folder,
                                  decompressed_folder_name,
                                  algorithm_results_folders
                                  )
        if verbose : print("final path = ", final_path)
        return final_path
    else :
        return None

def get_original_full_path(root_directory: str, dataset_name: str, test_case_number: int) -> str:
    """
    Construit le chemin complet vers les fichiers originaux pour un test donné.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        str: Le chemin complet vers les fichiers originaux.
    """
    return os.path.join(
        root_directory,
        dataset_name,
        get_use_case_folder(root_directory, dataset_name, get_test_case_number_str(test_case_number)),
        get_original_folder_name()
    )


def get_use_case_full_path(root_directory: str, satellite_type: str, test_case_number: int) -> str:
    """
    Construit le chemin complet vers les fichiers originaux pour un test donné.

    Args:
        satellite_type (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        str: Le chemin complet vers les fichiers originaux.
    """
    return os.path.join(
        root_directory,
        satellite_type,
        get_use_case_folder(root_directory, satellite_type, get_test_case_number_str(test_case_number)))

# Fonction pour récupérer le dernier fichier JSON dans un dossier donné
def get_latest_json_file_path(folder_path: str) -> Optional[str]:
    """
    Récupère le dernier fichier JSON dans un dossier donné, en se basant sur la date dans le nom du fichier.

    :param folder_path: Chemin du dossier où rechercher les fichiers JSON.
    :return: Chemin complet du dernier fichier JSON basé sur la date, ou None si aucun fichier n'est trouvé.
    """
    # Liste tous les fichiers dans le dossier qui ont une extension ".json"
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    # Si aucun fichier JSON n'est trouvé, renvoie None
    if not json_files:
        return None
    # Trie les fichiers JSON par date d'analyse (extraite du nom de fichier) en ordre décroissant
    json_files.sort(
        key=lambda f: datetime.strptime(f.split('[')[-1].replace('].json', ''), "%Y%m%d_%H%M%S"),
        reverse=True
    )

    # Retourne le chemin complet du dernier fichier JSON
    return os.path.join(folder_path, json_files[0])

def get_latest_json_summary_file_path(folder_path: str) -> Optional[str]:
    """
    Récupère le dernier fichier JSON summary dans un dossier donné, en se basant sur la date dans le nom du fichier.

    :param folder_path: Chemin du dossier où rechercher les fichiers JSON.
    :return: Chemin complet du dernier fichier JSON basé sur la date, ou None si aucun fichier n'est trouvé.
    """
    # Liste tous les fichiers dans le dossier qui ont une extension ".json"
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    # Si aucun fichier JSON n'est trouvé, renvoie None
    if not json_files:
        return None
    # Trie les fichiers JSON par date d'analyse (extraite du nom de fichier) en ordre décroissant
    json_files.sort(
        key=lambda f: datetime.strptime(f.split('[')[-2].replace(']_', ''), "%Y%m%d_%H%M%S"),
        reverse=True
    )

    # Retourne le chemin complet du dernier fichier JSON
    return os.path.join(folder_path, json_files[0])
def get_decompressed_folder_path(root_directory: str, dataset_name: str, test_case_number, verbose=False) -> \
Optional[str]:
    """
    Retourne le chemin du dossier decompressed ou peut se trouver le json summary

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        Optional[str]: Le chemin du decompressed folder,
        ou None si aucun dossier ne correspond.
    """
    if verbose : print("--- get_algorithm_results_folders --- starting ...")
    test_case_folder_name = get_use_case_folder(root_directory, dataset_name,
                                                get_test_case_number_str(test_case_number),verbose=verbose)
    if verbose : print("---- test case folder name = ",test_case_folder_name)
    # print("test_case_folder_name = ",test_case_folder_name)
    root_dir = os.path.join(root_directory, dataset_name, test_case_folder_name,decompressed_folder_name)
    return root_dir
def get_algorithm_results_folder(root_directory: str, dataset_name: str, test_case_number, nnvvpp_algoname: str, verbose=False) -> \
Optional[str]:
    """
    Retourne le nom du dossier contenant les résultats d'un algorithme spécifique.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.
        nnvvpp_algoname (str): Le nom de l'algorithme dans le format NN VV PPP_algo.

    Returns:
        Optional[str]: Le nom du dossier contenant les résultats de l'algorithme,
        ou None si aucun dossier ne correspond.
    """
    if verbose : print("--- get_algorithm_results_folders --- starting ...")
    test_case_folder_name = get_use_case_folder(root_directory, dataset_name,
                                                get_test_case_number_str(test_case_number),verbose=verbose)
    if verbose : print("---- test case folder name = ",test_case_folder_name)
    # print("test_case_folder_name = ",test_case_folder_name)
    root_dir = os.path.join(root_directory, dataset_name, test_case_folder_name,decompressed_folder_name)
    if verbose : print("--- get_algorithm_results_folders --- root dir = ",root_dir)

    result = list_matching_folders(root_dir=root_dir, search_str=nnvvpp_algoname, bracket_num=0, verbose=verbose).pop(0)
    if verbose : print("--- get_algorithm_results_folders --- list of matching folders = ", list_matching_folders(root_dir=root_dir, search_str=nnvvpp_algoname, bracket_num=0, verbose=verbose))

    return result



def get_use_case_folder(root_directory: str, dataset_name: str, test_case_number, verbose=False) -> Optional[str]:
    """
    Retourne le nom du dossier contenant les données pour un test donné.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        Optional[str]: Le nom du dossier de test case, ou None si aucun dossier ne correspond.
    """
    test_case_root_folder = os.path.join(root_directory, dataset_name)
    if verbose : print("get_use_case_folder ----> test_case_root_folder = ",test_case_root_folder)
    result = list_matching_folders(test_case_root_folder, get_test_case_number_str(test_case_number), 0, verbose=verbose).pop(0)
    if verbose : print("get_use_case_folder ----> result = ",result)
    return result


def get_bracket_content(folder_name: str, bracket_num: int) -> str:
    """
    Extrait le Nième champ entre crochets dans une chaîne de caractères et vérifie s'il contient une sous-chaîne spécifique.

    Args:
        folder_name (str): Le nom du dossier au format [001]_[1c_256_256]_[1]..[] ou chempin du dossier
        (si c est un chemin de dossier, alors on le découpera et regardera uniquement le dernier dossier.
        search_str (str): La sous-chaîne à rechercher dans le champ extrait.
        bracket_num (int): Le numéro du champ entre crochets à extraire (commençant à 0).

    Returns:
        bool: True si le Nième champ contient la sous-chaîne, False sinon.
    """
    # Extraire tous les champs entre crochets
    # print("checking bracket contents for ",search_str,"...")
    # Vérifier si folder_name est un chemin complet et extraire le nom du dernier dossier
    if os.path.sep in folder_name:
        folder_name = os.path.basename(folder_name)

    fields = folder_name.split('[')[1:]  # Diviser la chaîne et ignorer tout avant le premier crochet ouvrant
    # print("fields = ",fields)
    fields = [field.split(']')[0] for field in fields]  # Extraire les contenus des crochets
    # print("fields = ",fields)

    # Vérifier que le numéro de champ demandé est valide
    if 0 <= bracket_num <= len(fields):
        # Extraire le Nième champ
        selected_field = fields[bracket_num]

        return selected_field
    else:
        # Si le numéro de champ est invalide, retourner False
        raise ValueError("Si le numéro de champ est invalide ou le champs n'existe pas")


def check_bracket_content(folder_name: str, search_str: str, bracket_num: int, verbose = False) -> bool:
    """
    Extrait le Nième champ entre crochets dans une chaîne de caractères et vérifie s'il contient une sous-chaîne spécifique.

    Args:
        folder_name (str): Le nom du dossier au format [001]_[1c_256_256]_[1]..[].
        search_str (str): La sous-chaîne à rechercher dans le champ extrait.
        bracket_num (int): Le numéro du champ entre crochets à extraire (commençant à 0).

    Returns:
        bool: True si le Nième champ contient la sous-chaîne, False sinon.
    """
    # Extraire tous les champs entre crochets
    # print("checking bracket contents for ",search_str,"...")
    # Vérifier si folder_name est un chemin complet et extraire le nom du dernier dossier
    if verbose : print("---- check_bracket_content ---- trying to find ",folder_name," in ",folder_name," at bracket number ",bracket_num," ...")
    if os.path.sep in folder_name:
        folder_name = os.path.basename(folder_name)

    fields = folder_name.split('[')[1:]  # Diviser la chaîne et ignorer tout avant le premier crochet ouvrant
    if verbose : print("---- check_bracket_content ---- Diviser la chaîne et ignorer tout avant le premier crochet ouvrant = ",fields)

    fields = [field.split(']')[0] for field in fields]  # Extraire les contenus des crochets
    if verbose : print("---- check_bracket_content ---- Extraire les contenus des crochets = ",fields)

    # print("fields = ",fields)

    # Vérifier que le numéro de champ demandé est valide

    if 0 <= bracket_num <= len(fields) and len(fields) !=0 :
        # Extraire le Nième champ
        selected_field = fields[bracket_num]
        # Vérifier si la sous-chaîne est présente
        # print(search_str in selected_field)
        if verbose:
            print("---- check_bracket_content ---- selected_field = ",selected_field)
            print("---- check_bracket_content ---- search_str in selected_field = ", search_str in selected_field)
        return search_str in selected_field
    else:
        # Si le numéro de champ est invalide, retourner False
        if verbose: print("---- check_bracket_content ---- Si le numéro de champ est invalide, retourner False ")

        return False


def list_matching_folders(root_dir: str, search_str: str, bracket_num: int, verbose = False) -> List[str]:
    """
    Liste les sous-dossiers d'un répertoire racine et vérifie si le Nième champ
    entre crochets dans leur nom contient une sous-chaîne spécifique.

    Args:
        root_dir (str): Le chemin du répertoire racine.
        search_str (str): La sous-chaîne à rechercher dans le Nième champ.
        bracket_num (int): Le numéro du champ entre crochets à vérifier (commençant à 1).

    Returns:
        List[str]: Une liste de chemins complets des sous-dossiers correspondants.
    """
    if verbose : print("list_matching_folders --> matching folders from ",root_dir,", trying to find ",search_str," in bracket number ",bracket_num,"...")
    matching_folders = []
    list_of_dirs = os.listdir(root_dir)
    # Lister tous les sous-dossiers dans le répertoire racine
    if verbose:
        print("list_matching_folders --> LIST OF DIRS : ",list_of_dirs)

    for folder_name in list_of_dirs:
        if verbose :
            print("list_matching_folders --> folder name [",folder_name,"]...")
        folder_path = os.path.join(root_dir, folder_name)

        # Vérifier si l'élément est bien un dossier
        if os.path.isdir(folder_path):
            # Utiliser check_bracket_content pour vérifier le contenu du Nième champ
            is_content_found = check_bracket_content(folder_name, search_str, bracket_num, verbose=verbose)
            if verbose:
                print("list_matching_folders --> is_content_found = ", is_content_found, "")

            if is_content_found:
                if verbose :
                    print("list_matching_folders --> folder FOUND [", folder_name, "].")

                # Si trouvé, ajouter le chemin complet du dossier à la liste
                matching_folders.append(folder_name)

    if verbose : print("list_matching_folders --> returns : ",matching_folders,".")
    return matching_folders


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize the image for display, regardless of the value range.

    This function adjusts the image data to a standard range for display purposes.
    It handles different data types and scales the image values accordingly.

    Args:
        image (np.ndarray): The input image as a NumPy array.

    Returns:
        np.ndarray: The normalized image.
    """
    # Check the data type and normalize accordingly
    if image.dtype == np.uint16:
        # For 16-bit unsigned integer images, scale to the range [0, 1]
        image = image.astype(np.float32) / 65535.0
    elif image.dtype == np.float32:
        # For floating-point images, clip values to the range [0, 1]
        image = np.clip(image, 0, 1)
    else:
        # For other data types, normalize to the range [0, 1]
        image = image.astype(np.float32)
        image_min = np.min(image)
        image_max = np.max(image)
        # Avoid division by zero if the image has a uniform value
        if image_max > image_min:
            image = (image - image_min) / (image_max - image_min)
        else:
            image = np.zeros_like(image)

    return image


def display_multiband_tiffs(image1: np.ndarray, image2: np.ndarray) -> None:
    """
    Display two TIFF images with appropriate normalization and visualization.

    This function displays two images side by side. It handles different numbers of channels and normalizes
    the images for better visualization. It supports single-channel, multi-channel (e.g., RGB), and images
    with more than three channels.

    Args:
        image1 (np.ndarray): The first image as a NumPy array (HxWxC or HxW).
        image2 (np.ndarray): The second image as a NumPy array (HxWxC or HxW).

    Returns:
        None
    """
    plt.figure(figsize=(10, 5))

    # Normalize images for display
    image1 = normalize_image(image1)
    image2 = normalize_image(image2)

    plt.subplot(1, 2, 1)
    plt.title('Image 1')
    if image1.ndim == 3:
        if image1.shape[2] == 1:
            # Display single-channel image as grayscale
            plt.imshow(image1[:, :, 0], cmap='gray')
        if image1.shape[2] == 2:
            # Display  a two-channel image
            plt.imshow(image1[:, :, :1])
        elif image1.shape[2] == 3:
            # Display RGB image
            plt.imshow(image1)
        else:
            # Display the first three channels of an image with more than 3 channels
            img_to_show = image1[:, :, :3]
            # Normalize data for better visualization
            img_to_show = (img_to_show - np.min(img_to_show)) / (np.max(img_to_show) - np.min(img_to_show))
            plt.imshow(img_to_show)
    elif image1.ndim == 2:
        # Display grayscale image
        plt.imshow(image1, cmap='gray')
    plt.axis('off')

    # Display Image 2
    plt.subplot(1, 2, 2)
    plt.title('Image 2')
    if image2.ndim == 3:
        if image2.shape[2] == 1:
            # Display single-channel image as grayscale
            plt.imshow(image2[:, :, 0], cmap='gray')
        if image2.shape[2] == 2:
            # Display a two-channel image
            plt.imshow(image2[:, :, :1])
        elif image2.shape[2] == 3:
            # Display RGB image
            plt.imshow(image2)
        else:
            # Display the first three channels of an image with more than 3 channels
            img_to_show = image2[:, :, :3]
            # Normalize data for better visualization
            img_to_show = (img_to_show - np.min(img_to_show)) / (np.max(img_to_show) - np.min(img_to_show))
            plt.imshow(img_to_show)
    elif image2.ndim == 2:
        # Display grayscale image
        plt.imshow(image2, cmap='gray')
    plt.axis('off')

    plt.show()


def reformat_date(input_date: str) -> str:
    """
    Reformate une chaîne de date au format 'YYYYMMDD_HHMMSS' en 'YYYY-MM-DD HH:MM:SS'.

    :param input_date: La chaîne de date à reformater.
    :return: La chaîne de date reformée.
    """
    # Vérifie que la chaîne a la longueur attendue
    if len(input_date) != 15 or input_date[8] != '_':
        raise ValueError("La date doit être au format 'YYYYMMDD_HHMMSS'")

    # Sépare la date et l'heure
    date_part = input_date[:8]  # 'YYYYMMDD'
    time_part = input_date[9:]  # 'HHMMSS'

    # Reformate la date
    reformatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]} {time_part[:2]}:{time_part[2:4]}:{time_part[4:]}"

    return reformatted_date


def list_directories(base_path="decompressed"):
    """
    Liste tous les dossiers dans un répertoire donné.

    Args:
        base_path (str): Le chemin du dossier à inspecter (par défaut "decompressed").

    Returns:
        list: Une liste des noms de dossiers trouvés dans le répertoire spécifié.
    """
    try:
        # Vérifie si le chemin spécifié existe
        if not os.path.exists(base_path):
            print(f"Le dossier '{base_path}' n'existe pas.")
            return []

        # Liste des dossiers
        directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

        return directories

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return []


def list_csv_files(directory_path: str):
    """
    Liste tous les fichiers CSV dans un dossier donné.

    Parameters:
    directory_path (str): Le chemin vers le dossier où chercher les fichiers CSV.

    Returns:
    list: Une liste contenant les noms de fichiers CSV.
    """
    # Vérifie que le dossier existe
    if not os.path.exists(directory_path):
        print(f"Le dossier {directory_path} n'existe pas.")
        return []

    # Liste tous les fichiers dans le dossier et filtre uniquement ceux avec l'extension .csv
    csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

    return csv_files

def list_tiff_files(directory_path: str):
    """
    Liste tous les fichiers tiff dans un dossier donné.

    Parameters:
    directory_path (str): Le chemin vers le dossier où chercher les fichiers CSV.

    Returns:
    list: Une liste contenant les noms de fichiers CSV.
    """
    # Vérifie que le dossier existe
    if not os.path.exists(directory_path):
        print(f"Le dossier {directory_path} n'existe pas.")
        return []

    # Liste tous les fichiers dans le dossier et filtre uniquement ceux avec l'extension .csv
    csv_files = [file for file in os.listdir(directory_path) if file.endswith('.tiff')]

    return csv_files

