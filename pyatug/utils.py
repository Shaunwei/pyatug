import re
import ast
import unittest
import mock
from exceptions import *

##
# >>> s = args:[type value@ str]  [params value@= random input]
# >>> re.findall(RE_ARSER, s)
# [('type', 'value', '', 'str'), ('params', 'value', '=', 'random input')]
# >>> s = 'args: [return@= 123]'
# [('return', '', '=', '123')]
RE_PARSER = re.compile(r"\[(?P<type>\w+) ?(?P<key>\w+)?\@(?P<equal>\=?) (?P<value>[\w ]+)\]")

def get_ast_from(file_name):
    '''
    type filename: str
    params: given source file name return ast
    '''
    with open(file_name) as f:
        source_ast = ast.parse(''.join(f.readlines()))

    return source_ast


def get_docs_key_value_pairs(val_list):
    # TODO: the failure path is not generated.
    '''
    type val: list
    params: form dictionary from val based on seperator
    space will NOT be removed
    >>>l=['- abc: [type @123]', '- bcd: [value @1334]', ]
    >>>get_key_value_pairs_by(l)
    {'abc': ' 123', 'bcd': ' 1334'}
    '''
    if not isinstance(val_list, list):
        raise WrongTypeError('Input should be list type.')

    _str_list = ''.join(val_list).split('- ')
    dic = {}
    for element in _str_list:
        e = element.strip()
        if not e:
            continue
        key, value = e.split(':')
        dic[key] = re.findall(RE_PARSER, value)
    else:
        return dic

    if not dic:
        raise EmptyValueError('No docstrings found.')


def parse_pass_conditions(ast_node):
    '''
    type ast_node: ast.AST
    params: 
    '''
    pass


def get_supported_funcs_map_dict(cls):
    '''
    type cls: class
    params: unittest.TestCase or mock.MagicMock
    get needed funcs from cls
    >>> l = ['assertDictEqual','assertEqual']
    >>> get_supported_funcs_map_dict(unittest.TestCase)
    {'dictequal': 'assertDictEqual', 'equal':'assertEqual'}
    '''
    dic = {}
    if issubclass(cls, unittest.TestCase):
        keys = cls.__dict__.keys()
        # assertEqual[6:] == Equal
        method_names = (name for name in keys if 'assert' in name)
        for name in method_names:
            key_name = name[6:]
            if len(key_name) == 1:
                # del 'assert_'
                continue
            dic[key_name.lower()] = name
    elif issubclass(cls, mock.MagicMock):
        methods = dir(cls)
        method_names = (name for name in methods if not name.startswith('_'))
        for name in method_names:
            # not modify mock method name yet
            dic[name] = name
    else:
        raise AutoUnitGeneratorBaseException('Not dic has valid value.')

    return dic


### helpers
def get_test_data():
    '''
    generate dummy paths data for test use
    example data:
        {
            <_ast.ClassDef>: [
                (<_ast.FunctionDef>, [
                    [<_ast.Assign>,]),
                (<_ast.FunctionDef>, [
                    [<_ast.If>, <_ast.Print>, <_ast.Return>],
                    [<_ast.If>, <_ast.If>, <_ast.Print>, <_ast.Return>],
                    [<_ast.If>, <_ast.If>, <_ast.Expr>]])
            ]
        }
    '''
    dic = {}

    astree = get_ast_from('NewA.py')
    # magic matching func
    class_node = astree.body[-1]
    func_node = class_node.body[-1]

    l0 = []
    for node in class_node.body[0].body:
        l0.append(node)

    l1 = []
    l1.append(func_node.body[0])
    for node in func_node.body[0].body:
        l1.append(node)

    l2 = []
    l2.append(func_node.body[0])
    l2.append(func_node.body[0].orelse[0])
    for node in func_node.body[0].orelse[0].body:
        l2.append(node)

    l3 = []
    l3.append(func_node.body[0])
    l3.append(func_node.body[0].orelse[0])
    for node in func_node.body[0].orelse[0].orelse:
        l3.append(node)

    dic[class_node] = [
        (class_node.body[0], [l0,]),
        (class_node.body[1], [l1, l2, l3])
    ]
    # TODO: only second def under test
    # only return the second half

    return dic[class_node][-1]
