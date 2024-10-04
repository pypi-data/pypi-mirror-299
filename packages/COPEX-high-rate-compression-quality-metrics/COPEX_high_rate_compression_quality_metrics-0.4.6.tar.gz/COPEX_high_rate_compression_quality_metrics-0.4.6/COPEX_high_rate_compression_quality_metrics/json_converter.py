# module permettant la conversion, le passage de json a des graphs de visualisation par exemple
import json
import csv
import os.path
import utils
import json_builder


def json_to_csv_band_and_metric(json_input_path: str, csv_output_path: str, band: str, metric: str, verbose=False,
                                show_output=False):
    """
    Prend un fichier JSON, récupère les informations spécifiques à une bande et une métrique,
    et les ordonne dans un fichier CSV.

    :param json_input_path: Chemin vers le fichier JSON d'entrée.
    :param csv_output_path: Chemin vers le fichier CSV de sortie.
    :param band: Bande spécifique à récupérer (par exemple : "B01", "B02", "VV").
    :param metric: Métrique spécifique à récupérer (par exemple : "SSIM", "PSNR", "RMSE", "LPIPS").
    """
    if verbose: print("json_to_csv_band_and_metric ...")

    # Ouvre le fichier JSON et le charge en tant que dictionnaire
    with open(json_input_path, 'r') as json_file:
        data = json.load(json_file)
    if verbose: print(json_input_path, "loaded ...")

    # Vérifie si la métrique existe dans les données
    if metric not in data['metrics']:
        raise ValueError(f"La métrique '{metric}' n'existe pas dans le fichier JSON.")

    # Récupère les données de la métrique demandée
    metric_data = data['metrics'][metric]['per_band']
    if verbose: print("metric_data = [", metric_data, "] ...")

    # Filtre les données pour ne garder que celles concernant la bande spécifique
    filtered_band_data = {}
    for band_key in metric_data:
        if band in band_key:
            filtered_band_data = metric_data[band_key]
            break

    # Si aucune bande n'a été trouvée, lever une erreur
    if not filtered_band_data:
        raise ValueError(f"La bande '{band}' n'a pas été trouvée dans le fichier JSON.")

    # Liste pour stocker les données avant le tri
    data_list = []

    # Récupère les informations de chaque algorithme, sa métrique et son facteur de compression
    for algorithm, value in filtered_band_data.items():
        # Récupère le facteur de compression associé à l'algorithme
        if algorithm in data['compression_algorithms']:
            compression_factor = data['compression_algorithms'][algorithm]['compression_factor']
        else:
            compression_factor = float(
                'inf')  # Si le facteur est manquant, utiliser 'inf' pour éviter les erreurs lors du tri

        # Ajoute les informations sous forme de tuple : (algorithme, valeur de la métrique, facteur de compression)
        data_list.append((algorithm, value, compression_factor))

    # Trie la liste par facteur de compression (du plus petit au plus grand)
    data_list_sorted = sorted(data_list, key=lambda x: x[2])

    # Crée une liste avec les en-têtes pour le CSV
    csv_header = ['Algorithm', metric, 'Compression Factor']

    # Écrit les données dans un fichier CSV
    with open(csv_output_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Écrire l'en-tête
        writer.writerow(csv_header)

        # Écrire les données triées par facteur de compression
        for algorithm, value, compression_factor in data_list_sorted:
            # Écrire la ligne avec l'algorithme, la métrique et le facteur de compression
            writer.writerow([algorithm, value, compression_factor])

    print(f"Les données ont été exportées dans le fichier CSV '{csv_output_path}'.")


def json_to_csv_band_all_metrics(json_input_path: str, csv_output_path: str, band: str, verbose=False):
    """
    Prend un fichier JSON, récupère les informations spécifiques à une bande pour toutes les métriques,
    et les ordonne dans un fichier CSV.

    :param json_input_path: Chemin vers le fichier JSON d'entrée.
    :param csv_output_path: Chemin vers le fichier CSV de sortie.
    :param band: Bande spécifique à récupérer (par exemple : "B01", "B02", "VV").
    :param verbose: Affiche des informations supplémentaires si True.
    """
    if verbose: print("json_to_csv_band_all_metrics ...")

    # Ouvre le fichier JSON et le charge en tant que dictionnaire
    with open(json_input_path, 'r') as json_file:
        data = json.load(json_file)
    if verbose: print(f"{json_input_path} loaded ...")

    # Récupère toutes les métriques disponibles dans le JSON
    available_metrics = data['metrics'].keys()
    if verbose: print(f"Métriques disponibles : {available_metrics}")

    # Filtre les données pour ne garder que celles concernant la bande spécifique
    band_data_per_metric = {}
    for metric in available_metrics:
        metric_data = data['metrics'][metric]['per_band']
        for band_key in metric_data:
            if band in band_key:
                if metric not in band_data_per_metric:
                    band_data_per_metric[metric] = {}
                band_data_per_metric[metric] = metric_data[band_key]
                break

    # Si aucune bande n'a été trouvée, lever une erreur
    if not band_data_per_metric:
        raise ValueError(f"La bande '{band}' n'a pas été trouvée dans le fichier JSON.")

    # Liste pour stocker les données avant le tri
    data_list = []

    # Pour chaque algorithme, collecte toutes les métriques disponibles
    for algorithm in data['compression_algorithms']:
        row = [algorithm]
        compression_factor = data['compression_algorithms'][algorithm]['compression_factor']
        row.append(compression_factor)

        # Récupère la valeur de chaque métrique pour l'algorithme et la bande
        for metric in available_metrics:
            if metric in band_data_per_metric:
                metric_value = band_data_per_metric[metric].get(algorithm, None)
                row.append(metric_value)
            else:
                row.append(None)

        # Ajoute la ligne complète (algorithme, facteur de compression, valeurs des métriques)
        data_list.append(row)

    # Trie la liste par facteur de compression (du plus petit au plus grand)
    data_list_sorted = sorted(data_list, key=lambda x: x[1])

    # Crée une liste avec les en-têtes pour le CSV
    csv_header = ['Algorithm', 'Compression Factor'] + list(available_metrics)

    # Écrit les données dans un fichier CSV
    with open(csv_output_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Écrire l'en-tête
        writer.writerow(csv_header)

        # Écrire les données triées par facteur de compression
        for row in data_list_sorted:
            writer.writerow(row)

    print(f"Les données ont été exportées dans le fichier CSV '{csv_output_path}'.")


def get_csv_name_from_wanted_band_and_wanted_metric(wanted_band, wanted_metric):
    return str(wanted_band) + "_" + str(wanted_metric) + ".csv"
def get_csv_name_from_wanted_band(wanted_band):
    return str(wanted_band) + ".csv"

def make_csv_from_decompressed_folder_metrics_separated(root_directory: str, dataset_name: str, test_case_number,
                                      create_json_summary_if_do_not_exist=False, verbose=True):
    """

    """
    decompressed_folder_path = utils.get_decompressed_folder_path(root_directory, dataset_name, test_case_number,
                                                                  verbose=verbose)
    json_summary_path = utils.get_latest_json_summary_file_path(decompressed_folder_path)
    print(json_summary_path)
    if json_summary_path == None:
        print(
            "no json summary path found, try to make one before using make_csv_from_decompressed_folder or use proper root directory, dataset name and test case number, or put create_json_summary_if_do_not_exist to true")
        if create_json_summary_if_do_not_exist:
            json_builder.create_summary_json_from_use_case_path(root_directory, dataset_name, test_case_number)
            json_summary_path = utils.get_latest_json_summary_file_path(decompressed_folder_path)
    output_folder_path = os.path.join(decompressed_folder_path, utils.summary_output_folder_name,
                                      utils.summary_output_csv_folder_name)
    utils.create_folder_if_do_not_exist(output_folder_path)
    for band_number, band_name in utils.bands_per_satellite_type[dataset_name].items():
        print(band_name)
        for metric_name, _ in utils.metrics_dictionary.items():
            print(metric_name)
            output_csv_path = os.path.join(output_folder_path,
                                           get_csv_name_from_wanted_band_and_wanted_metric(band_name, metric_name))
            json_to_csv_band_and_metric(json_summary_path, output_csv_path, band_name, metric_name,verbose=verbose)
def make_csv_from_decompressed_folder(root_directory: str, dataset_name: str, test_case_number,
                                      create_json_summary_if_do_not_exist=False, verbose=True):
    """

    """
    decompressed_folder_path = utils.get_decompressed_folder_path(root_directory, dataset_name, test_case_number,
                                                                  verbose=verbose)
    json_summary_path = utils.get_latest_json_summary_file_path(decompressed_folder_path)
    print(json_summary_path)
    if json_summary_path == None:
        print(
            "no json summary path found, try to make one before using make_csv_from_decompressed_folder or use proper root directory, dataset name and test case number, or put create_json_summary_if_do_not_exist to true")
        if create_json_summary_if_do_not_exist:
            json_builder.create_summary_json_from_use_case_path(root_directory, dataset_name, test_case_number)
            json_summary_path = utils.get_latest_json_summary_file_path(decompressed_folder_path)
    output_folder_path = os.path.join(decompressed_folder_path, utils.summary_output_folder_name,
                                      utils.summary_output_csv_folder_name)
    utils.create_folder_if_do_not_exist(output_folder_path)
    for band_number, band_name in utils.bands_per_satellite_type[dataset_name].items():
        print(band_name)
        output_csv_path = os.path.join(output_folder_path,
                                       get_csv_name_from_wanted_band(band_name))
        json_to_csv_band_all_metrics(json_summary_path, output_csv_path, band_name, verbose=True)

"""root_directory = os.path.join("..","test","data")
dataset_name = "S2_L1C"
test_case_number = 1
make_csv_from_decompressed_folder(root_directory,dataset_name,test_case_number,verbose=True)
"""
# Exemple d'utilisation :
"""print("os gcwd = ", os.getcwd())
input_summary = os.path.join("..", "test", "data", "S2_L1C",
                             "[001]_[S2A_MSIL1C_20200111T105421_N0208_R051_T29NNJ_20200111T123505]_[Mt_Nimba]",
                             "decompressed", "[S2_L1C]_[001]_[20240926_153321]_[sum].json")
wanted_band = "B08"
wanted_metric = "SSIM"
output_csv_name = wanted_band + ".csv"
json_to_csv_band_all_metrics(input_summary, output_csv_name, wanted_band, verbose=True)"""
