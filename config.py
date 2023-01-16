import json
import os.path


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')


app_id: int
api_hash: str
phone_number: int


_config_structure = {
    'app_id': 100500,
    'api_hash': 'sample_text',
    'phone_number': 88005553535
}


try:
    with open(CONFIG_PATH) as file:
        data = json.load(file)
except FileNotFoundError:
    with open(CONFIG_PATH, 'w') as file:
        data = json.dump(_config_structure, file, indent=4)

    print(f'Создан конфигурационный файл "{CONFIG_PATH}"')

    import sys; sys.exit()


for key in _config_structure:
    if key not in data:
        raise ValueError('В конфигурационном файле '
                        f'отсутствует необходимый параметр: "{key}"')


for key, value in data.items():
    if key not in _config_structure:
        raise ValueError('Неизвестный параметр в '
                        f'конфигурационном файле: "{key}"')

    expected_type = type(_config_structure[key])
    if expected_type != type(value):
        raise ValueError(f'Неверный тип параметра "{key}": '
                         f'ожидал {expected_type}, получил {type(value)}')

    globals()[key] = value
