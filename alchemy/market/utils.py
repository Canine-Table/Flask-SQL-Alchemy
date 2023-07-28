import json
import os

def string_to_dict(string):
    new_dict = {}
    for pairs in string.split(','):
        new_list = str(pairs).split(':')
        new_dict[new_list[0]] = new_list[1]
    return new_list


def after_create_item_table(*args,**kwargs):
    file_dump = os.path.join(os.path.realpath('./alchemy'),'static','json','items.json')
    with open(str(file_dump), 'r') as f:
        json_object = json.loads(f.read())
        for kw in json_object:
            yield kw
