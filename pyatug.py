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
from pyatug.exceptions import *
from pyatug.utils import *
from pyatug.DecisionMaker.DecisionMaker import _DecisionMaker
from pyatug.Parser.NodeUnderTestParser import _NodeUnderTestParser
from pyatug.Parser.TestMethodNodeParser import _TestMethodNodeParser

# Data Path
# TODO: Maybe used, depends on how many data inside path we want to store
class DataPath(object):
    '''
    Keep Track of Existing Data Paths in AST
    '''
    def __init__(self):
        pass


class AutoUnitGen(object):
    '''
    Main class
    '''
    # use file name temp to keep track file
    def __init__(self, file_name, test_file_name):
        # TODO: hard code for now
        self.file_ast = get_ast_from('NewA.py')
        self.ufile_ast = get_ast_from('NewA_test.py')
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


if __name__ == '__main__':
    a = AutoUnitGen('NewA.py', 'NewA_test.py')
