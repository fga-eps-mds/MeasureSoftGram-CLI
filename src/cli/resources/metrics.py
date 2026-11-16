def get_metric_value(extracted):
    """
    Função que recupera o valor mais recente da métrica
    """
    # Métricas que o parâmetro é uma lista de valores
    listed_values = [
        "coverage",
        "complexity",
        "functions",
        "comment_lines_density",
        "duplicated_lines_density",
        "sqale_debt_ratio",
        "security_rating",
        "security_review_rating",
        "resolved_issues",
        "total_issues",
        "sum_ci_feedback_times",
        "total_builds",
        "security_alerts_open",
        "security_alerts_closed",
    ]

    # Métricas que o parâmetro é extraído do UTS
    uts_values = ["test_execution_time", "tests"]

    # Métricas pareadas por arquivo: só entram dos arquivos que têm todas elas
    paired_values = ["vulnerabilities", "ncloc"]
    all_value_list = listed_values + uts_values + paired_values
    response_data = {}

    # Para todos os arquivos extraídos
    for path_readed in extracted.values():
        # Para cada métrica dentro das medidas
        for metric in _metrics_of_path(path_readed, paired_values):
            metric_name = metric.get("metric")
            metric_value = metric.get("value")

            # Se ela for "agregada", olho apenas arquivos FIL,
            # se não, salvo somente a última.
            if metric_name in all_value_list:
                response_data.setdefault(metric_name, []).append(metric_value)
            else:
                response_data[metric_name] = metric_value

    return response_data


def _metrics_of_path(path_readed, paired_values):
    metrics = [metric for metric in path_readed if isinstance(metric, dict)]
    if set(paired_values) <= {metric.get("metric") for metric in metrics}:
        return metrics
    return [metric for metric in metrics if metric.get("metric") not in paired_values]
