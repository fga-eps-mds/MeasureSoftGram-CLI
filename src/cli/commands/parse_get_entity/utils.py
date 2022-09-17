entities_keys = {
    'metrics': 'metric_id',
    'measures': 'measure_id',
    'characteristics': 'characteristic_id',
    'subcharacteristics': 'subcharacteristic_id',
}


def get_entity(response, entity_name, entity_id, history):
    if entity_id:
        extracted_data, headers, data = \
            get_entity_id(response, entity_name, history)
    else:
        extracted_data, headers, data = \
            get_without_entity_id(response, entity_name, history)

    return extracted_data, headers, data


def get_entity_id(response, entity_name, history):
    extracted_data = []

    if history:
        data = response.json().get("history")
        headers = ['Id', 'History Id', 'Value', 'Created at']
        for entity_data in data:
            extracted_data.append([
                entity_data[entities_keys[entity_name]],
                entity_data['id'],
                entity_data['value'],
                entity_data['created_at'],
            ])
    else:
        data = response.json()
        headers = ['Name', 'Value', 'Created at']
        extracted_data = [[
            data['name'],
            data['latest']['value'],
            data['latest']['created_at'],
        ]]

    return extracted_data, headers, data


def get_without_entity_id(response, entity_name, history):
    extracted_data = []

    if history:
        headers = ['Id', 'History Id', 'Name', 'Created at']
        data = response.json().get("results")
        for entity_data in data:
            for history_data in entity_data["history"]:
                extracted_data.append([
                    history_data[entities_keys[entity_name]],
                    history_data['id'],
                    history_data['value'],
                    history_data['created_at'],
                ])

    else:
        headers = ['Name', 'Value', 'Created at']
        data = response.json().get("results")
        for entity_data in data:
            extracted_data.append([
                entity_data['name'],
                entity_data['latest']['value'],
                entity_data['latest']['created_at'],
            ])

    return extracted_data, headers, data
