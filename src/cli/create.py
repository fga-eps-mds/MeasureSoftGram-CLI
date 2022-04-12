import inquirer
from inquirer.themes import GreenPassion

VALID_WEIGHT_SUM_ADVISE = "the sum of the weights must be 100"
INVALID_WEIGHT_SUM_ERROR = "Invalid weights, " + VALID_WEIGHT_SUM_ADVISE

VALID_WEIGHT_ADVISE = "the weight must be between 0 and 100"
INVALID_WEIGHT_VALUE = "Invalid weight, " + VALID_WEIGHT_ADVISE

VALID_CHECKBOX_ERROR = "Select at least one Check-Box"


def define_weight(data_key, data_name):
    while True:
        weights = [
            inquirer.Text(
                data_key,
                message="Enter the weight of "
                + data_name
                + f" ({VALID_WEIGHT_SUM_ADVISE})",
            )
        ]
        defined_weight = inquirer.prompt(
            weights, theme=GreenPassion(), raise_keyboard_interrupt=True
        )
        if validate_weight_value(float(defined_weight[data_key])):
            break
        print(INVALID_WEIGHT_VALUE)

    return defined_weight


def validate_weight_sum(items):
    sum = 0
    for x in items:
        for v in x.values():
            sum += float(v)

    if 0 < round(100 - sum, 2) <= 0.01:
        sum = 100
    return sum == 100


def validate_weight_value(weight):
    return 0 < weight <= 100


def validate_check_box_input(selected):
    return selected > 0


def validate_preconfig_post(status_code, response):
    if status_code == 201:
        print(
            f"\nYour Pre Configuration was created with sucess!\nPre Configuration ID: {response['_id']}"
        )
    else:
        print(
            f"\nThere was an ERROR while creating your Pre Configuration:  {response['error']}"
        )


def print_error_message(message, is_input_valid):
    if not is_input_valid:
        print(message)


def sublevel_cli(level_name, level_alias, sublevels, available_pre_config):
    reverse_sublevel = {v["name"]: k for k, v in available_pre_config.items()}

    sublevels_answer = [
        inquirer.Checkbox(
            "sublevels",
            message="Choose the " + level_alias + " for " + level_name,
            choices=[available_pre_config[x]["name"] for x in sublevels],
        )
    ]
    user_sublevels = inquirer.prompt(
        sublevels_answer, theme=GreenPassion(), raise_keyboard_interrupt=True
    )

    user_sublevels = [reverse_sublevel[x] for x in user_sublevels["sublevels"]]

    return user_sublevels


def define_characteristic(available_pre_config):
    characteristics = available_pre_config["characteristics"]

    if len(characteristics) == 1:
        user_characteristics = list(characteristics.keys())
        characteristics_weights = [{user_characteristics[0]: 100}]
        return user_characteristics, characteristics_weights

    user_characteristics = select_characteristics(characteristics)

    if len(user_characteristics) == 1:
        print("\nOnly one characteristic selected, no need to define weights")
        characteristics_weights = [{user_characteristics[0]: 100}]
        return user_characteristics, characteristics_weights

    characteristics_weights = input_weights(characteristics, user_characteristics)

    return user_characteristics, characteristics_weights


def select_characteristics(characteristics):
    reversed_characteristics = {v["name"]: k for k, v in characteristics.items()}

    def body_func():
        characteristics_answer = [
            inquirer.Checkbox(
                "characteristics",
                message="Choose the characteristics",
                choices=[x["name"] for x in characteristics.values()],
            )
        ]

        return inquirer.prompt(
            characteristics_answer,
            theme=GreenPassion(),
            raise_keyboard_interrupt=True,
        )

    def validation_func(values):
        return validate_check_box_input(len(values["characteristics"]))

    user_characteristics = generic_valid_input(
        validation_func,
        body_func,
        VALID_CHECKBOX_ERROR,
        {"characteristics": []},
    )

    user_characteristics = [
        reversed_characteristics[x] for x in user_characteristics["characteristics"]
    ]

    return user_characteristics


def select_sublevels(available_pre_config, level_key, sublevel_key, current_level):
    def body_func():
        return sublevel_cli(
            available_pre_config[level_key][current_level]["name"],
            sublevel_key,
            available_pre_config[level_key][current_level][sublevel_key],
            available_pre_config[sublevel_key],
        )

    def validation_func(values):
        return validate_check_box_input(len(values))

    return generic_valid_input(
        validation_func,
        body_func,
        VALID_CHECKBOX_ERROR,
    )


def generic_valid_input(
    validation_function, body_function, error_message, initial_value=None
):
    values = [] if initial_value is None else initial_value
    valid_input = validation_function(values)

    while not valid_input:
        values = body_function()

        valid_input = validation_function(values)

        print_error_message(error_message, valid_input)

    return values


def input_weights(sublevels_config, user_sublevels):
    def body_func():
        sublevels_weights = []
        for x in user_sublevels:
            sublevels_weights.append(define_weight(x, sublevels_config[x]["name"]))
        return sublevels_weights

    def validation_func(values):
        return validate_weight_sum(values)

    return generic_valid_input(
        validation_func, body_func, INVALID_WEIGHT_SUM_ERROR, [{"empty": 0}]
    )


def has_one_sublevel(available_pre_config, level_key, sublevel_key, current_level):
    return len(available_pre_config[level_key][current_level][sublevel_key]) == 1


def print_no_need_define_weights_msg(sublevel_key, key_value):
    print(
        f"\nOnly one {sublevel_key} {key_value} selected, no need to define weights\n"
    )


def define_sublevel(user_levels, available_pre_config, level_key, sublevel_key):
    sublevels = available_pre_config[sublevel_key]

    if len(sublevels) == 1:
        user_sublevels = list(sublevels.keys())
        sublevels_weights = [{user_sublevels[0]: 100}]

        return user_sublevels, sublevels_weights

    selected_sublevels = []
    sublevels_weights = []

    for x in user_levels:
        if has_one_sublevel(available_pre_config, level_key, sublevel_key, x):
            local_selected_sublevels = available_pre_config[level_key][x][sublevel_key]
            local_selected_weights = [{local_selected_sublevels[0]: 100}]

            print_no_need_define_weights_msg(
                sublevel_key,
                available_pre_config[sublevel_key][local_selected_sublevels[0]]["name"],
            )

        else:
            local_selected_sublevels = select_sublevels(
                available_pre_config, level_key, sublevel_key, x
            )

            if len(local_selected_sublevels) == 1:
                local_selected_weights = [{local_selected_sublevels[0]: 100}]

                print_no_need_define_weights_msg(
                    sublevel_key,
                    available_pre_config[sublevel_key][local_selected_sublevels[0]][
                        "name"
                    ],
                )

            else:
                local_selected_weights = input_weights(
                    available_pre_config[sublevel_key], local_selected_sublevels
                )

        selected_sublevels.extend(local_selected_sublevels)
        sublevels_weights.extend(local_selected_weights)

    return selected_sublevels, sublevels_weights
