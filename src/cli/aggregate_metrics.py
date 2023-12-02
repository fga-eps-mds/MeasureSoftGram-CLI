import os
import json

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

def read_msgram(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_metrics(file_name, metrics):
    output_file_path = file_name.replace('.msgram', '.metrics')
    with open(output_file_path, 'w') as output_file:
        json.dump(metrics, output_file, indent=2)
    print(f'Metrics saved to: {output_file_path}')

def main():
    # Get all .msgram files in the current directory
    msgram_files = [file for file in os.listdir() if file.endswith('.msgram')]

    # Identify GitHub files based on the file name prefix
    github_files = [file for file in msgram_files if file.startswith('github_')]

    # Check if at least one GitHub file was found
    if github_files:
        print(f'GitHub metrics found in: {", ".join(github_files)}')

        # Iterate through remaining files
        for file in msgram_files:
            if file not in github_files:
                print(f'Processing {file}')
                file_content = read_msgram(file)

                # Extract GitHub metrics from the GitHub files
                github_metrics = [
                    {"metric": metric, "value": next((m["value"] for m in read_msgram(github_file)['nlohmann/json'] if m["metric"] == metric), None)}
                    for github_file in github_files
                    for metric in metrics["github"]
                ]

                # Extract the list of metrics from the current file
                current_metrics = file_content.get('fga-eps-mds_2022-2-MeasureSoftGram-CLI', [])

                # Add GitHub metrics to the list
                current_metrics += github_metrics

                # Update the original dictionary with the modified list of metrics
                file_content['fga-eps-mds_2022-2-MeasureSoftGram-CLI'] = current_metrics

                # Save the modified content to the file
                save_metrics(file, file_content)

    else:
        print('GitHub files not found in the current directory.')


if __name__ == "__main__":
    main()
