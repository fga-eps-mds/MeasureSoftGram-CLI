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
        "resolved_issues",
        "total_issues",
        "sum_ci_feedback_times",
        "total_builds",
    ]

    # Métricas que o parâmetro é extraído do UTS
    uts_values = ["test_execution_time", "tests"]
    response_data = {}

    # Para todos os arquivos extraídos
    for path_readed in extracted.values():
        # Para cada métrica dentro das medidas
        for metric in path_readed:
            # Check if metric is a dictionary
            if isinstance(metric, dict):
                metric_name = metric.get("metric")
                metric_value = metric.get("value")

                # Se ela for "agregada", olho apenas arquivos FIL,
                # se não, salvo somente a última.
                all_value_list = listed_values + uts_values
                if metric_name in all_value_list:
                    response_data.setdefault(metric_name, []).append(metric_value)
                else:
                    response_data[metric_name] = metric_value

    return response_data
