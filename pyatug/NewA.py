'''
use ast.parse
f = open('test1.py')
astree = ast.parse(''.join(f.readlines()))
'''
class ParentA(object):
    def call_back(self):
        print 'this is call back'


class NewA(ParentA):
    def __init__(self, value):
        self.value = value
        if value:
            return value
        else:
            pass

    def if_case(self, value='abc', **kwargs):
        if value:
            print 'value is', value
            return value
        elif len(value) < 5:
            print 'value is too short'
            return len(value)
        else:
            self.call_back()
