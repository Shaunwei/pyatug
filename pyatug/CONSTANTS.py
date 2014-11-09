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