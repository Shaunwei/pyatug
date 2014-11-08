'''
Various function helper used only by unittests
'''

import re
import string
import random
from nose.tools import nottest
from functools import wraps
from mock import MagicMock


##############################################################################
# Random String
# https://docs.python.org/2/library/string.html
##############################################################################


def get_random_string(
        length=5,
        letters=False,
        digits=False,
        punctuation=False,
        printable=False):
    """
    Generate a string which containing letters and digits and punctuation
    letters: `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`
    digits: `0123456789`
    punctuation: `!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~`
    printable: `0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLM\
    NOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c`
    """
    result = ''
    if letters:
        string_list = string.letters
    elif digits:
        string_list = string.digits
    elif punctuation:
        string_list = string.punctuation + string.letters
    elif printable:
        string_list = string.printable
    else:
        string_list = string.letters + string.digits
    for x in xrange(length):
        result += random.choice(string_list)

    return result


def get_random_string_list(length=5, string_length=None, **kwargs):
    '''Generate sting list'''
    result_list = []
    for x in xrange(length):
        string_length = string_length if string_length else \
            int(random.choice(string.digits))
        result_list.append(get_random_string(string_length, **kwargs))

    return result_list


class SafeDict(dict):
    '''Make sure dict behave error free
        - Overwrite x[y]
        - Overwrite del x[y]
    '''
    def __getitem__(self, item):
        return self.get(item, None)

    def __delitem__(self, item):
        if self.get(item):
            super(SafeDict, self).__delitem__(item)
        else:
            pass

    def copy(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result


def get_random_dict(length=5, item=None, safe=False):
    '''Generate random dictionary
        - Side Effect: if use safe=True, type value would be helper.SafeDict
    '''
    key_vals = zip(
        get_random_string_list(length), get_random_string_list(length))
    result_dict = dict(key_vals) if not safe else SafeDict(key_vals)
    if item:
        result_dict.update(item)

    return result_dict


##############################################################################
# Random Error
# Based on StandardErrors listed in:
# https://docs.python.org/2/library/exceptions.html
##############################################################################


def get_random_standard_error(exclude_list=[]):
    """
    Warning: This function will only return Error class, which is not instance.
    StandardError:
         +-- BufferError
         +-- ArithmeticError
         +-- AssertionError
         +-- AttributeError
         +-- EnvironmentError
         +-- EOFError
         +-- ImportError
         +-- LookupError
         +-- MemoryError
         +-- NameError
         +-- ReferenceError
         +-- RuntimeError
         +-- SyntaxError
         +-- SystemError
         +-- TypeError
         +-- ValueError
    """
    error_list = [
        BufferError,
        ArithmeticError,
        AssertionError,
        AttributeError,
        EnvironmentError,
        EOFError,
        ImportError,
        LookupError,
        MemoryError,
        NameError,
        ReferenceError,
        RuntimeError,
        SyntaxError,
        SystemError,
        TypeError,
        ValueError]
    for error in exclude_list:
        idx = error_list.index(error)
        if idx >= 0:
            error_list.pop(idx)
    return random.choice(error_list)

##############################################################################
# JSON helper
##############################################################################


def check_output_dict(output_dict, required_keys=[], exclude_keys=[]):
    '''Checks output dictionary has required_keys
            and Not have any exclude_keys
            return
                True: if all required_keys exists and exclude_keys not exsit
            else:
                return False
    '''
    success = True
    tmp_value = get_random_string()

    def _extract(dict_in, dict_out, tmp_value):
        '''Flatten dictionary
        '''
        for key, value in dict_in.iteritems():
            if isinstance(value, dict):
                dict_out[key] = tmp_value
                _extract(value, dict_out, tmp_value)
            else:
                dict_out[key] = value
        return dict_out

    out = {}
    if not isinstance(output_dict, dict):
        success = False
        print 'Input is not a dict, please recheck input.'
        print 'Input type is ', type(output_dict)
        return success

    result = _extract(output_dict, out, tmp_value)
    print 'Extract Dictionary is ', result
    print 'Required Keys are', required_keys
    print 'Excluded Keys are', exclude_keys

    for key in required_keys:
        if result.get(key, None) is None:
            print 'Error: key[%s] is not in result.' % key
            success = False
    for key in exclude_keys:
        if result.get(key, None) is not None:
            print 'Error: key[%s] is in result.' % key
            success = False
    return success


##############################################################################
# Other helpers
##############################################################################


@nottest
def test_fail_with_docs(func):
    '''Show test method docstring, when test fail
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        print func.__doc__
        return func(*args, **kwargs)
    return wrapper


def get_selected_values_dict_from_sql(sql):
    '''extract `SELECT` column names from sql string
        return dict
            - {`column_name`: True} pairs
    '''
    column_name_dict = {}
    sql = sql.upper()
    select_list = sql.split('FROM')[0].replace(
        'SELECT', '').replace('\n', '').split(',')
    for select_val in select_list:
        if ' as ' in select_val:
            old_column_name, column_name = select_val.split(' as ')
        elif 'max(' in select_val:
            column_name_matches = \
                re.search(r'max\((?P<column_name>\w+)\)', select_val)
            column_name = column_name_matches.groupdict().get('column_name')
        else:
            column_name = select_val
        column_name = column_name.replace(' ', '').lower()
        column_name_dict[column_name] = True
    return column_name_dict


##############################################################################
# API Constants
##############################################################################


MODULE_DBOP = MagicMock()
MODULE_CX_ORACLE = MagicMock()
MODULE_CX_ORACLE.DatabaseError = get_random_standard_error()
