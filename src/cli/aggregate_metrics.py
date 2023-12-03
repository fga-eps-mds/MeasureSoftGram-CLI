import os
import json

from src.cli.utils import print_error, print_info

metrics = {}
metrics["sonar"] = ['tests',
                    'test_failures',
                    'test_errors',
                    'coverage',
                    'test_execution_time',
                    'functions',
                    'complexity',
                    'comment_lines_density',
                    'duplicated_lines_density']

metrics["github"] = ['resolved_issues', 'total_issues']

measures = {}
measures["sonar"] = ['passed_tests',
                    'test_builds',
                    'test_errors',
                    'test_coverage',
                    'non_complex_file_density',
                    'commented_file_density',
                    'duplication_absense']

measures["github"] = ['team_throughput']

def should_process_sonar_metrics(config):
    # Check if any Sonar measures are present in the config file
    for characteristic in config.get("characteristics", []):
        for subcharacteristic in characteristic.get("subcharacteristics", []):
            for measure in subcharacteristic.get("measures", []):
                if measure.get("key") in measures["sonar"]:
                    return True
    return False

def should_process_github_metrics(config):
    # Check if any GitHub measures are present in the config file
    for characteristic in config.get("characteristics", []):
        for subcharacteristic in characteristic.get("subcharacteristics", []):
            for measure in subcharacteristic.get("measures", []):
                if measure.get("key") in measures["github"]:
                    return True
    return False


def read_msgram(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except IsADirectoryError:
        return False

def list_msgram_files(folder_path):
    try:
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"{folder_path} is not a directory.")
        
        msgram_files = [file for file in os.listdir(folder_path) if file.endswith('.msgram')]
        return msgram_files
    
    except NotADirectoryError as e:
        print(f"Error: {e}")

def save_metrics(file_name, metrics):
    # Extract the directory path from the file_name
    directory = os.path.dirname(file_name)

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Save the metrics file
    output_file_path = os.path.join(directory, os.path.basename(file_name).replace('.msgram', '.metrics'))
    with open(output_file_path, 'w') as output_file:
        json.dump(metrics, output_file, indent=2)
    
    print_info('> [blue] Metrics saved to: {output_file_path}\n')


def process_sonar_metrics(folder_path, msgram_files, github_files):
    processed_files = []

    for file in msgram_files:
        if file not in github_files:
            print_info('> [blue] Processing {file}')
            sonar_metrics_dict = read_msgram(os.path.join(folder_path, file))

            if not sonar_metrics_dict:
                print_error('> [red] Error to read sonar metrics in: {folder_path}\n')
                return False
            
            processed_files.append((file, sonar_metrics_dict))

    return processed_files


def process_github_metrics(folder_path, github_files, metrics):
    # Check if no GitHub files were found
    if not github_files:
        print_error('> [red] GitHub files not found in the directory: {folder_path}\n')
        return False 

    print_info('> [blue] GitHub metrics found in: {", ".join(github_files)}\n')

    # Extract key for GitHub metrics from the first GitHub file
    first_github_file = read_msgram(os.path.join(folder_path, github_files[0]))

    if not first_github_file:
        print_error('> [red] Error to read github metrics in: {folder_path}\n')
        return False
    
    github_key = next(iter(first_github_file.keys() - metrics["sonar"]), '')

    # Extract GitHub metrics from the GitHub file
    github_metrics = [
            {
                "metric": metric,
                "value": next(
                    (m["value"] for m in first_github_file[github_key] if m["metric"] == metric),
                    None
                )
            }
            for metric in metrics["github"]
        ]


    return (github_files[0],github_metrics)


def aggregate_metrics(folder_path, config: json):

    # Get all .msgram files in the specified directory
    msgram_files = list_msgram_files(folder_path)

    if not msgram_files:
        print_error('> [red]Error: Can not read msgram files in provided directory')
        return False


    # Identify GitHub files based on the file name prefix
    github_files = [file for file in msgram_files if file.startswith('github_')]

    file_content = {}
    
    github_metrics = []

    have_metrics = False

    # Check if GitHub metrics should be processed based on the config file
    if should_process_github_metrics(config):
        
        # Process GitHub metrics and check the length of the result
        file,github_metrics = process_github_metrics(folder_path, github_files, metrics)
        # Check that the result always has exactly one file and file_content
        if not github_metrics:  
            # Handle the case where the result does not have exactly one file and file_content
            print_error('> [red]Error: Unexpected result from process_github_metrics')
            return False
        
        have_metrics = True
            

    if should_process_sonar_metrics(config):
        result = process_sonar_metrics(folder_path, msgram_files, github_files)

        # Check that the result always has exactly one file and file_content
        if not result or len(result) != 1:  
            # Handle the case where the result does not have exactly one file and file_content
            print_error('> [red]Error: Unexpected result from process_sonar_metrics')
            return False
        
        have_metrics = True
        file, file_content = result[0]
    
    all_metrics = github_metrics

    if not have_metrics:
        print_error('> [red]Error: No metrics where found in the .msgram files')
        return False

    file_content["github_metrics"] = all_metrics

    save_metrics(os.path.join(folder_path, file), file_content)

    # Return True after processing all files
    return True
