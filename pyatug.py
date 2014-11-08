'''
Python Auto Unittest Generator
This is the main program for auto unittest.

Currently, need to use unittest template generator to generate
the unittests template first.

This program will read TestCase file, based on docstrings to
set testcases, with one success case and one fail case at least.

REQUIREMENTS:
specified input data types
success condition
fail condition

example:
    test_name
    Pass Condition:
        - args:
            [type value@ str]
            [params value@= random input]
        - kwargs:
            [None]
        - success: 
            [return@= value]
        - fail:
            [call_back@ called]
`-` is the field
`[]` is the requirements
`:` sperate key words and value
`:=` means equal

@author: Shaun Wei
@email: shaunweix@gmail.com

@implemented grammar:
    If, Return, Print
'''
# TODO: node matcher
# follows the process with the source node and test node
#
import re
import ast
import helpers
import unittest
import mock
from exceptions import *
import os


#####
# CONSTANTS
SUPPORTED_METHODS = {
'Add': False,
'And': False,
'Assert': False,
'Assign': False,
'Attribute': False,
'Break': False,
'Call': True,
'Compare': False,
'Continue': False,
'Del': False,
'Delete': False,
'Dict': False,
'Div': False,
'Ellipsis': False,
'Eq': False,
'Exec': False,
'Expr': False,
'Expression': False,
'For': False,
'Global': False,
'Gt': False,
'If': True,
'Import': False,
'In': False,
'Index': False,
'Interactive': False,
'Invert': False,
'Is': False,
'Lambda': False,
'List': False,
'Load': False,
'Lt': False,
'Mod': False,
'Module': False,
'Mult': False,
'Name': False,
'Not': False,
'Num': False,
'Or': False,
'Param': False,
'Pass': False,
'Pow': False,
'Print': True,
'Raise': False,
'Repr': False,
'Return': True,
'Set': False,
'Slice': False,
'Store': False,
'Str': False,
'Sub': False,
'Subscript': False,
'Suite': False,
'Tuple': False,
'While': False,
'With': False,
'Yield': False,
}
PARENTS = {
    1: 'clazz', # class under test
    2: 'tmp', # TestCase.tmp store random input
    3: 'other',
}
#
#####

##
# >>> s = args:[type value@ str]  [params value@= random input]
# >>> re.findall(RE_ARSER, s)
# [('type', 'value', '', 'str'), ('params', 'value', '=', 'random input')]
# >>> s = 'args: [return:= 123]'
# [('return', '', '=', '123')]
RE_PARSER = re.compile(r"\[(?P<type>\w+) ?(?P<key>\w+)?\@(?P<equal>\=?) (?P<value>[\w ]+)\]")

TEST_FILE_DIR = "./test"
TEST_FILE_NAME = "NewA.py"
UNIT_TEST_FILE_NAME = "NewA_test.py"

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

# Data Path
# TODO: Maybe used, depends on how many data inside path we want to store
class DataPath(object):
    '''
    Keep Track of Existing Data Paths in AST
    '''
    def __init__(self):
        pass


# Base Parser
class __ASTNodeParser(object):
    '''
    Based on AST node, parse useful informations
    methods:
        - get_paths
    '''
    def __init__(self, ast_node):
        if not isinstance(ast_node, ast.AST):
            raise WrongTypeError('Need to input a ast node instance.')
        else:
            self.ast = ast_node

class _NodeUnderTestParser(__ASTNodeParser):
    '''
    The node from ast tree, which is current under test.
    '''
    def __init__(self, ast_node):
        super(_NodeUnderTestParser, self).__init__(ast_node)
        try:
            self.func_name = ast_node.name
        except:
            raise WrongTypeError('Node:%s does not have name attr.' %ast_node)
        self.paths = get_test_data() #(func_node, paths_list,)

    def get_node_paths(self):
        return self.paths


class _TestMethodNodeParser(__ASTNodeParser):
    '''
    Based on unittest template, parse useful information from docstrings
    init with ast node
    methods:
        - get_sucess_condition
        - get_fail_condition
    '''
    def __init__(self, ast_node):
        super(_TestMethodNodeParser, self).__init__(ast_node)
        self.docs = None
        self.func_name = None
        self.condition_dict = {
            'args': [],
            'kwargs': [],
            'success': [],
            'fail': []
        }
        self._parse_node_docs()

    def _parse_node_docs(self):
        try:
            self.docs = ast.get_docstring(self.ast)
            if not self.docs:
                return

            _parse_list = self.docs.splitlines()
            # method name is the first element
            # name = _parse_list[0]

            # key value pairs start from the third element
            self.func_name = _parse_list[0]

            self.condition_dict = get_docs_key_value_pairs(_parse_list[2:])

        except Exception, e:
            print e
            raise AutoUnitGeneratorBaseException('Error Parse Docs.')

    def get_test_condition_dict(self):
        return self.condition_dict

    def get_sucess_condition(self):
        return self.condition_dict['success']

    def get_fail_condition(self):
        return self.condition_dict['fail']


class __DecisionEngine(object):
    '''
    '''
    # TODO: need to add supported methods in the class?
    def __init__(self):
        self.__supported_methods = SUPPORTED_METHODS

    def decide_if(self):
        # TODO: put them into a decision folder
        pass

    def decide_return(self):
        pass

    def decide_print(self):
        pass

class __FuncScopeItem(object):
    '''Store local variables in scope'''
    def __init__(self, node_id, ctx=None, params=None, _type=None, parent=None):
        self.id = node_id
        self.ctx = ctx
        self.params = params
        self.type = _type
        # track whose attrs
        # three types: clazz, tmp, other
        # Use to setup inputs in test case
        self.parent = parent


class _DecisionMaker(__DecisionEngine):
    '''
    Based on docstrings, generate correct code blocks in test file.
    '''
    # condtion_dict =
    #    {'args': [('type', 'value', '', 'str'),
    #      ('params', 'value', '=', 'random input')],
    #       'fail': [('true', '', '', 'call_back called')],
    #       'success': [('return', '', '=', 'value')]}
    # TODO: need to add supported methods in the class?
    def __init__(self, condition_dict, node_paths):
        super(_DecisionMaker, self).__init__()
        self._mock_funcs = get_supported_funcs_map_dict(mock.MagicMock)
        self._unit_funcs = get_supported_funcs_map_dict(unittest.TestCase)
        self._condition_dict = condition_dict
        self._func_node, self._node_paths = node_paths
        self._func_scope = {} # {id: _ast.Node} # store local variables
        self.code_block = {
            # item, helper method
            'input_block': [],
            'call_block': [],
            # assertEqual, first value, flag
            'output_block': [],}


        self._prepare()

    def _prepare(self):
        '''Prepare paths and decision engine'''
#        self._prepare_scope()
        pass

    def _prepare_scope(self):
        '''Store args and kwargs'''
        for arg in self._func_node.args.args:
            ctx = getattr(arg, 'ctx', None)
            self._func_scope[arg.id] = __FuncScopeItem(arg.id, ctx)

        if self._func_node.kwargs:
            # TODO: process later
            pass

        if self._func_node.defaults:
            # TODO: maybe store later
            pass

    def get_supported_tool_funcs(self):
        return self._mock_funcs

    def get_supported_unittest_funcs(self):
        return self._unit_funcs

    def _decide_input(self, node_path):
        '''
        Given input args and kwargs, generate setup code.
        - Execute before process inside method.
        - No local variables yet.
        '''
        # TODO: only do str and random for now
        if 'args' in self._condition_dict:
            args = self._condition_dict['args']
        try:
            for t_p, value, equal, req in args:
                self._func_scope[value].parent = PARENTS.get(2)
                if t_p == 'type':
                    self._func_scope[value].type = req
                elif t_p == 'params' and equal:
                    self._func_scope[value].params = req
                else:
                    raise AUGSyntaxError('Syntax Error for test docstrings. %s' %args)
        except Exception, e:
            if 'Syntax' in e:
                raise AUGSyntaxError(e)
            else:
                raise AutoUnitGeneratorBaseException('No input name is %s' %value)

        for item in self._func_scope:
            # TODO: implement other input types
            if item.type == 'str':
                if 'random' in item.params:
                    # TODO: self. + item.parent + . + item.value + get_ + random_string + ()
                    self.code_block['input_block'].append((item, 'random_string',))
                else:
                    pass
            else:
                pass


    def _decide_path(self, node_path):
        '''Given all paths, keep track which path visited'''
        # # trick: if the next element is the child
        # # then, if is true

        # if node_path[1] in node_path[0].body:
        flag = None
        if self.is_success_path(node_path):
            self._generate_success_path()
            flag = 'success'
        elif self.is_fail_path(node_path):
            self._generate_fail_path()
            flag = 'fail'
        else:
            pass
        return flag

    def is_success_path(self, node_path):
        # TODO: maybe you could just set one success test assertion?
        # do the first for now
        success_flag = self._condition_dict['success'][0][0]
        if node_path[-1].__class__.__name__.lower() == success_flag:
            return True
        else:
            return False

    def is_fail_path(self, node_path):
        # TODO: need to think about how to process call
        # Maybe use scope?
        pass

    def _generate_success_path(self):
        success_reqs = self._condition_dict['success']
        # TODO: do only return for now
        for return_flag, _, equal, req in success_reqs:
            if return_flag == 'return':
                if equal:
                    func_item = self._func_scope.get(req)
                    self.__write_output_block('equal', first_arg=func_item, return_flag=True)

    def __write_output_block(self, assert_method, **kwargs):
        '''Given output requirements, generate assertion code'''
        first_arg = kwargs.pop('first_arg')
        return_flag = kwargs.pop('return_flag', None)
        try:
            assertion = self._unit_funcs[assert_method]
        except:
            raise AutoUnitGeneratorBaseException('%s method not supported in unittest.' %assert_method)

        if return_flag:
            self.code_block['output_block'].append((assertion, first_arg, return_flag))

    def run(self):
        for node_path in self._node_paths:
            self._decide_input(node_path)
            # success or fail or None
            path_flag = self._decide_path(node_path)
            if path_flag:
                self._make_path(node_path, path_flag)

    def _make_path(self, node_path, path_flag):
        '''
        Make current path valid
        '''
        pass



class AutoUnitGen(object):
    '''
    Main class
    '''
    # use file name temp to keep track file
    def __init__(self, file_name, test_file_name):
        test_file_ast = os.path.join(TEST_FILE_DIR, TEST_FILE_NAME)
        test_ufile_ast = os.path.join(TEST_FILE_DIR,UNIT_TEST_FILE_NAME)
        self.file_ast = get_ast_from(test_file_ast)
        self.ufile_ast = get_ast_from(test_ufile_ast)
        # TODO: add magic writer for now
#        self.test_writer = open(test_file_name, 'w')
        self.prepare()

    def run(self):
        pass

    def prepare(self):
        # TODO: add magic track, hard code for now
        # Maybe a tracker class?
        self.cur_node = self.file_ast.body[-1].body[-1]
        self.ucur_node = self.ufile_ast.body[-1].body[-1]
        # get ready to make decisions
        self.cnp = _NodeUnderTestParser(self.cur_node)
        self.ucnp = _TestMethodNodeParser(self.ucur_node)
        self._prepare_decition_maker()

    def _prepare_decition_maker(self):
        test_conditions = self.ucnp.get_test_condition_dict()
        node_paths = self.cnp.get_node_paths()
        self.dec_maker = _DecisionMaker(test_conditions, node_paths)


    def finish(self):
        self.test_writer.close()

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
    lis = []

    test_file_ast = os.path.join(TEST_FILE_DIR, TEST_FILE_NAME)
    astree = get_ast_from(test_file_ast)
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



if __name__ == '__main__':
    a = AutoUnitGen('NewA.py', 'NewA_test.py')
#EndOfFile




