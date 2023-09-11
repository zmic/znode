import numpy as np
import ast
from types import CodeType, FunctionType

f = '''
def f(P):
    return np.add(np.multiply(P[0],3.71), np.multiply(P[1],2.71))
'''

f = '''
def foo(x,y,z):
    return np.add(x,y)
'''

#print(ast.dump(ast.parse(f), include_attributes=True))

from ast import Module, FunctionDef, arguments, arg, Return, Call, Attribute, Name, Load

f1 = FunctionDef(name='foo', args=arguments(posonlyargs=[], args=[arg(arg='x', lineno=2, col_offset=6, end_lineno=2, end_col_offset=7), arg(arg='y', lineno=2, col_offset=8, end_lineno=2, end_col_offset=9), arg(arg='z', lineno=2, col_offset=10, end_lineno=2, end_col_offset=11)], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Return(value=Call(func=Attribute(value=Name(id='np', ctx=Load(), lineno=3, col_offset=11, end_lineno=3, end_col_offset=13), attr='add', ctx=Load(), lineno=3, col_offset=11, end_lineno=3, end_col_offset=17), args=[Name(id='x', ctx=Load(), lineno=3, col_offset=18, end_lineno=3, end_col_offset=19), Name(id='y', ctx=Load(), lineno=3, col_offset=20, end_lineno=3, end_col_offset=21)], keywords=[], lineno=3, col_offset=11, end_lineno=3, end_col_offset=22), lineno=3, col_offset=4, end_lineno=3, end_col_offset=22)], decorator_list=[], lineno=2, col_offset=0, end_lineno=3, end_col_offset=22)

m = Module(body=[f1], type_ignores=[])

module_code = compile(m, "<not_a_file>", "exec")

exec(module_code)
print(foo(1,2,6))

for c in module_code.co_consts:
    if isinstance(c, CodeType):
        if c.co_name == 'foo':
            foo = FunctionType(c, {'np':np})
        
print(foo(1,2,3))
#function_code = [c for c in module_code.co_consts if isinstance(c, CodeType)][0]
#f = FunctionType(function_code, {})
from numba import jit
foo = jit(foo)
print(foo(1,2,3))
print(foo(np.ones(4),np.ones(4), 1))

