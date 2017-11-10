#!/usr/bin/env python

def _get_path(nested_dict, attr_path):
    cur_attr = nested_dict
    for attr in attr_path:
        if attr in cur_attr:
            cur_attr = cur_attr[attr]
        else:
            cur_attr = None
            break
    return cur_attr

def group_by_attr(array, path):
    result = {}
    attr_path = path.split('.')
    for x in array:
        node = _get_path(x, attr_path)
        if node not in result:
            result[node] = []
        result[node].append(x)
    return result

def map_attr(array, path):
    result = []
    attr_path = path.split('.')
    for x in array:
        node = _get_path(x, attr_path)
        if node is not None:
            result.append(node)
    return result

class FilterModule(object):
    def filters(self):
        return {
        'group_by_attr': group_by_attr,
        'map_attr': map_attr
        }
        