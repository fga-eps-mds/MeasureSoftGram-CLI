import json
import requests
import sys
from datetime import datetime

TODAY = datetime.now()

METRICS_SONAR = [
    'files',
    'functions',
    'complexity',
    'comment_lines_density',
    'duplicated_lines_density',
    'coverage',
    'ncloc',
    'tests',
    'test_errors',
    'test_failures',
    'test_execution_time',
    'security_rating',
    'test_success_density',
    'reliability_rating',
]

BASE_URL_SONAR = 'https://sonarcloud.io/api/measures/component_tree?component=fga-eps-mds_'
OWNER = "fga-eps-mds"

def save_sonar_metrics(tag):
    response = requests.get(f'{BASE_URL_SONAR}{REPO}&metricKeys={",".join(METRICS_SONAR)}&ps=500')

    j = json.loads(response.text)

    print("Extração do Sonar concluída.")

    file_path = f'./analytics-raw-data/fga-eps-mds-{REPO}-{TODAY.strftime("%m-%d-%Y-%H-%M-%S")}-{tag}.json'

    with open(file_path, 'w') as fp:
        fp.write(json.dumps(j))
        fp.close()

    return

def all_request_pages(data):
    total_runs = data["total_count"]
    pages = (total_runs // 100) + (1 if total_runs % 100 > 0 else 0)
    for i in range(pages+1):
        if i == 0 or i == 1:
            continue
        api_url_now = api_url_runs + "?page=" + str(i)
        response = requests.get(api_url_now)
        for j in ((response.json()['workflow_runs'])):
            data['workflow_runs'].append(j)
    return data

def filter_request_per_date(data, date):
    data_filtered = []
    for i in data["workflow_runs"]:
        if datetime.strptime(i["created_at"][:10],"%Y-%m-%d").strftime("%Y-%m-%d") == date:
            data_filtered.append(i)
    return {"workflow_runs": data_filtered}

def save_github_metrics_runs():
    response = requests.get(api_url_runs, params={'per_page': 100,})

    data = response.json()

    # date = datetime.strptime("2023-03-23","%Y-%m-%d").strftime("%Y-%m-%d")
    data = all_request_pages(data)

    print("Quantidade de workflow_runs: " + str(len(data["workflow_runs"])))

    file_path = f'./analytics-raw-data/GitHub_API-Runs-fga-eps-mds-{REPO}-{TODAY.strftime("%m-%d-%Y-%H-%M-%S")}.json'

    # Salva os dados em um json file
    with open(file_path, 'w') as fp:
        fp.write(json.dumps(data))
        fp.close()

    return

def save_github_metrics_issues():
    issues = []
    page = 1

    while True:
        response = requests.get(api_url_issues, params={'state': 'all', 'per_page': 100, 'page': page})

        if response.status_code != 200:
            print(f"Erro na API do GitHub (status {response.status_code}): {response.json()}")
            break

        page_issues = response.json()

        if not isinstance(page_issues, list) or not page_issues:
            break

        issues.extend(page_issues)
        print(f"Página {page}: {len(page_issues)} issues carregadas.")

        page += 1

    print("Quantidade total de issues: " + str(len(issues)))

    file_path = f'./analytics-raw-data/GitHub_API-Issues-fga-eps-mds-{REPO}.json'

    # Salvar todas as issues em um arquivo JSON
    with open(file_path, 'w') as fp:
        json.dump(issues, fp, indent=4)

if __name__ == '__main__':

    REPO = sys.argv[1]
    RELEASE_VERSION = sys.argv[2]

    api_url_runs = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"
    api_url_issues = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

    save_sonar_metrics(RELEASE_VERSION)
    save_github_metrics_issues()
    save_github_metrics_runs()
