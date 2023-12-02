import json

def read_msgram(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_metrics(file_name, metrics):
    output_file_path = file_name.split('.')[0] + '.metrics'
    with open(output_file_path, 'w') as output_file:
        json.dump(metrics, output_file, indent=2)
    print(f'Metrics saved to: {output_file_path}')

def main():
    file1_path = 'fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram'
    file2_path = 'github_nlohmann-json-19-11-2023-12-53-58-extracted.msgram'

    file1_content = read_msgram(file1_path)
    file2_content = read_msgram(file2_path)


    resolved_issues_metric = next((metric['value'] for metric in file2_content['nlohmann/json'] if metric['metric'] == 'resolved_issues'), None)
    total_issues_metric = next((metric['value'] for metric in file2_content['nlohmann/json'] if metric['metric'] == 'total_issues'), None)

    # Extract the list of metrics from the first file
    file1_metrics = file1_content['fga-eps-mds_2022-2-MeasureSoftGram-CLI']

    # Add new metrics to the list
    file1_metrics += [
        {"metric": "resolved_issues", "value": resolved_issues_metric},
        {"metric": "total_issues", "value": total_issues_metric}
    ]

    # Update the original dictionary with the modified list of metrics
    file1_content['fga-eps-mds_2022-2-MeasureSoftGram-CLI'] = file1_metrics

    # Save the modified content to the file
    save_metrics(file1_path, file1_content)


if __name__ == "__main__":
    main()