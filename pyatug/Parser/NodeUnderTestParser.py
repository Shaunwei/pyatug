from ..exceptions import *
from ..utils import *
from ASTNodeParser import __ASTNodeParser

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
