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

    def visit_If(self, node: If) -> Any:
        test = parse_expression(node.test)
        print(test)
        print()
        self.generic_visit(node)

    def visit_Expr(self, node: Expr) -> Any:
        print(parse_expression(node))
        self.generic_visit(node)

    def visit_Delete(self, node: Delete) -> Any:
        print(parse_expression(node))
        self.generic_visit(node)

    def visit_Call(self, node: Call) -> Any:
        print(parse_expression(node))
        self.generic_visit(node)


def parse_expression(node):
    if isinstance(node, Name):
        return parse_name(node)
    elif isinstance(node, Constant):
        return parse_constant(node)
    elif isinstance(node, Attribute):
        return parse_attribute(node)
    elif isinstance(node, List) or isinstance(node, Tuple) or isinstance(node, Set) or isinstance(node, Dict) \
            or isinstance(node, list) or isinstance(node, tuple):
        return parse_collection(node)
    elif isinstance(node, Call):
        return parse_call(node)
    elif isinstance(node, UnaryOp):
        return parse_unary_op(node)
    elif isinstance(node, BinOp):
        return parse_binary_op(node)
    elif isinstance(node, BoolOp):
        return parse_bool_op(node)
    elif isinstance(node, Compare):
        return parse_compare(node)
    elif isinstance(node, FormattedValue):
        return parse_formatted_value(node)
    elif isinstance(node, JoinedStr):
        return parse_joined_str(node)
    elif isinstance(node, Expr):
        return parse_expr(node)
    elif isinstance(node, Delete):
        return parse_delete(node)
    elif isinstance(node, Starred):
        return parse_starred(node)
    elif isinstance(node, keyword):
        return parse_keyword(node)
    elif isinstance(node, IfExp):
        return parse_if_exp(node)
    elif isinstance(node, NamedExpr):
        return parse_name_expr(node)

def parse_name(node: Name):
    return node.id


def parse_constant(node: Constant):
    return str(node.value)


def parse_attribute(node: Attribute):
    return f'{parse_expression(node.value)}.{node.attr}'


@singledispatch
def parse_collection(collection):
    content = []
    for argument in collection:
        content.append(parse_expression(argument))
    if isinstance(collection, tuple):
        return "".join(content)
    else:
        return ", ".join(content)


@parse_collection.register(List)
@parse_collection.register(Tuple)
@parse_collection.register(Set)
def _(collection):
    content = []
    for argument in collection.elts:
        content.append(parse_expression(argument))
    if isinstance(collection, List):
        return f'[{",".join(content)}]'
    elif isinstance(collection, Tuple):
        return f'({",".join(content)})'
    else:
        return f'{{{",".join(content)}}}'


@parse_collection.register(Dict)
def _(collection):
    content = []
    for key, value in collection.keys, collection.values:
        content.append(f'"{parse_expression(key)}":{parse_expression(value)}')
    return f'{{{",".join(content)}}}'


def parse_call(node: Call):
    args = parse_expression(node.args + node.keywords)
    return f'{parse_expression(node.func)}({args})'


def parse_unary_op(node: UnaryOp):
    operand = parse_expression(node.operand)
    if isinstance(node.op, UAdd):
        op = '+'
    elif isinstance(node.op, USub):
        op = '-'
    elif isinstance(node.op, Not):
        op = 'not '
    else:
        op = '~'
    return op + operand


def parse_binary_op(node: BinOp):
    left = parse_expression(node.left)
    right = parse_expression(node.right)
    if isinstance(node.op, Add):
        op = '+'
    elif isinstance(node.op, Sub):
        op = '-'
    elif isinstance(node.op, Mult):
        op = '*'
    elif isinstance(node.op, FloorDiv):
        op = '//'
    elif isinstance(node.op, Mod):
        op = '%'
    elif isinstance(node.op, Pow):
        op = '**'
    elif isinstance(node.op, LShift):
        op = '<<'
    elif isinstance(node.op, RShift):
        op = '>>'
    elif isinstance(node.op, BitOr):
        op = '|'
    elif isinstance(node.op, BitAnd):
        op = '&'
    else:
        op = '^'
    return f'{left} {op} {right}'


def parse_bool_op(node: BoolOp):
    if isinstance(node.op, And):
        op = ' and '
    else:
        op = ' or '
    content = []
    for operand in node.values:
        content.append(parse_expression(operand))
    return op.join(content)


def parse_compare(node: Compare):
    content = []
    left = parse_expression(node.left)
    content.append(left)

    for operand, comparator in zip(node.ops, node.comparators):
        if isinstance(operand, Eq):
            op = '=='
        elif isinstance(operand, NotEq):
            op = '!='
        elif isinstance(operand, Lt):
            op = '<'
        elif isinstance(operand, LtE):
            op = '<='
        elif isinstance(operand, Gt):
            op = '>'
        elif isinstance(operand, GtE):
            op = '>='
        elif isinstance(operand, Is):
            op = 'is'
        elif isinstance(operand, IsNot):
            op = 'is not'
        elif isinstance(operand, In):
            op = 'in'
        else:
            op = 'not in'
        content.append(op)
        content.append(parse_expression(comparator))
    return ' '.join(content)


def parse_formatted_value(node: FormattedValue):
    return f'{{{parse_expression(node.value)}}}'


def parse_joined_str(node: JoinedStr):
    collection_without_separator = tuple(node.values)
    return f'f"{parse_expression(collection_without_separator)}"'


def parse_expr(node: Expr):
    return parse_expression(node.value)


def parse_delete(node: Delete):
    return f'del {parse_expression(node.targets)}'


def parse_starred(node: Starred):
    return f'*{parse_expression(node.value)}'


def parse_keyword(node: keyword):
    if hasattr(node, 'arg') and node.arg is not None:
        return f'{node.arg}={parse_expression(node.value)}'
    else:
        return f'**{parse_expression(node.value)}'


def parse_if_exp(node: IfExp):
    return f'{parse_expression(node.body)} if {parse_expression(node.test)} else {parse_expression(node.orelse)}'


def parse_name_expr(node: NamedExpr):
    return f'({parse_expression(node.target)} := {parse_expression(node.value)})'
