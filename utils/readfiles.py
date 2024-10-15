import os
import json


# we need to define a class

# this will solve the problem of calling lazy_load on the first execution pipeline

# this function is used to change attributes of the class
def change_attribute(instance, attribute, new_value):
    if hasattr(instance, attribute):
        setattr(instance, attribute, new_value)
    else:
        raise ValueError(f'type: {type(instance)} has no attribute: {attribute}')


def changes_attributes(instance, attributes: dict):
    for old_attr, new_attr in attributes:
        setattr(instance, old_attr, new_attr)


def lazy_load_func(json_filename) -> list:
    json_file = os.path.join('../', json_filename)
    lazy_load_log = []
    with open(json_file, 'r') as jsonFile:  # read all things that have errors and put them in a list
        intermediate = json.load(jsonFile)

        for elem in intermediate:
            if elem['compile_status'] == 'failure':
                lazy_load_log.append(elem['name'][0])
    return lazy_load_log

