import pprint
import json


def print_data():
    pp = pprint.PrettyPrinter(indent=4)

    with open('data.json', 'r') as f:
        cmd_dict = json.load(f)
        f.close()

    pp.pprint(cmd_dict)


def info_reload(data):
    sys_keys = list(data['info']['do']['sys-list'])
    api_keys = list(data['info']['do']['api-list'])
    pil_keys = list(data['info']['do']['pil-list'])

    data['info']['do']['all'] = sys_keys + api_keys + pil_keys

    return data


def load_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
        f.close()

    return data


def dump_data(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, separators=(', \n\t', ': '))
        f.close()


if __name__ == '__main__':
    data_path = 'data.json'

    data_dict = load_data(data_path)
    data_dict = info_reload(data_dict)

    dump_data(data_dict, data_path)
    print_data()
