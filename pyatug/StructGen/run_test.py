from StructGen import PathGen
from ..utils import *

if __name__ == '__main__':
    '''
    Running at top level
    python -m pyautg.StructGen.run_test
    '''
    s = get_ast_from('NewA.py')
    p = PathGen(s)

    print p.get_paths()
