from NewA import NewA
import unittest
from mock import MagicMock
from helpers import test_fail_with_docs
from helpers import get_random_string

class NewATestCase(unittest.TestCase):

    def setUp(self):
        self.tmp = MagicMock()
        self.clazz = NewA(10)

    @test_fail_with_docs
    def test_if_case(self):
        '''test_if_case
        Pass Condition:
            - args:
                [type value@ str]
                [params value@= random input]
            - success: 
                [return@= value]
            - fail:
                [call_back@ called]
        '''
        # setup inputs

        # call test method
        #self.clazz.if_case()
        # check outputs

        pass

    @test_fail_with_docs
    def test_if_case_success(self):
        '''test_if_case_success
        Pass Condition:
            - args:
                [type value@ str]
                [params value@= random input]
            - success: 
                [return@= value]
        '''
        self.tmp.value = get_random_string()

        return_value = self.clazz.if_case(self.tmp.value)

        self.assertEqual(self.tmp.value, return_value)
