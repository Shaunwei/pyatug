import ast
import gen_struct

f = open("NewA.py")

s = ast.parse(f.read())
s = ast.fix_missing_locations(s)

# print codegen.to_source(s)
# print get_children(get_children(s)[0])[0].s

b = ast.parse('import tornado')

p = gen_struct.print_code()

print p.print_node(s)
# print p.visit_If(s)
# for b in p.print_node(s):
#     print {b: p.print_node(s).get(b)}
# print "b", b._attributes
