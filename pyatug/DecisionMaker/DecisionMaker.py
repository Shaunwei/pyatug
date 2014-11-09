import unittest
import mock
from DecisionEngine import __DecisionEngine
from ..utils import *


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
