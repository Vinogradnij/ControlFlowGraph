from ast import *
from astpretty import pprint
from typing import Any
from functools import singledispatch


class MyVisitor(NodeVisitor):

    def visit_Assign(self, node: Assign) -> Any:
        targets = parse_expression(node.targets)
        value = parse_expression(node.value)
        result = f'{targets} = {value}'
        print(result)
        print()
        self.generic_visit(node)


def parse_expression(node):
    if isinstance(node, Name):
        return parse_name(node)
    elif isinstance(node, Constant):
        return parse_constant(node)
    elif isinstance(node, Attribute):
        return parse_attribute(node)
    elif isinstance(node, List) or isinstance(node, Tuple) or isinstance(node, Set) or isinstance(node, Dict)\
            or isinstance(node, list):
        return parse_collection(node)
    elif isinstance(node, Call):
        return parse_call(node)


def parse_name(node: Name):
    return node.id


def parse_constant(node: Constant):
    return str(node.value)


def parse_attribute(node: Attribute):
    return f'{parse_name(node.value)}.{node.attr}'


@singledispatch
def parse_collection(collection):
    print('normal col')
    content = []
    for argument in collection:
        content.append(parse_expression(argument))
    return ",".join(content)


@parse_collection.register(List)
@parse_collection.register(Tuple)
@parse_collection.register(Set)
def _(collection):
    content = []
    for argument in collection.elts:
        content.append(parse_expression(argument))
    if isinstance(collection, List):
        print('List ast col')
        return f'[{",".join(content)}]'
    elif isinstance(collection, Tuple):
        print('Tuple ast col')
        return f'({",".join(content)})'
    else:
        print('Set ast col')
        return f'{{{",".join(content)}}}'


@parse_collection.register(Dict)
def _(collection):
    content = []
    for key, value in collection.keys, collection.values:
        content.append(f'"{parse_expression(key)}":{parse_expression(value)}')
    print('list col')
    return f'{{{",".join(content)}}}'


def parse_call(node: Call):
    return f'{parse_attribute(node.func)}({parse_collection(node.args)})'
