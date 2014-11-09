from ..exceptions import *
from ..utils import *
from ASTNodeParser import __ASTNodeParser



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
