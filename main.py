import ast
import my_nodes
from astpretty import pprint


if __name__ == '__main__':
    with open('for_parse.py', 'r') as source:
        tree = ast.parse(source.read())
    pprint(tree)
    visitor = my_nodes.MyVisitor()
    visitor.visit(tree)
