import numpy as np
import randomgen
import json

from .node__ import node____, node_literal__, node__, metaclass_node_apply__

def in_node____(x):
    setattr(node____, x.__name__, x)
    return x

#-------------------------------------------------------    
@in_node____
class ŋNone(node_literal__):
    pass

@in_node____
class ŋint(node_literal__):
    pass

@in_node____
class ŋfloat(node_literal__):
    pass

@in_node____
class ŋstr(node_literal__):
    pass

class ŋtuple_literal(node_literal__):
    def  __new__(cls, items):
        if isinstance(items, list):
            items = tuple(items)
        t = node_literal__.__new__(cls, items)
        return t  

#-------------------------------------------------------  
@in_node____
class ŋtuple(node__):
    @staticmethod
    def eval__(*args):
        return args

@in_node____
class ŋindex(node__):
    @staticmethod
    def eval__(a, i):        
        return a[i]

#-------------------------------------------------------  
  
class ŋadd(node__):
    @staticmethod
    def eval__(x, y):
        return x + y
    
class ŋmul(node__):
    @staticmethod
    def eval__(x, y):
        return x * y
            
#-------------------------------------------------------    
class node_rg__(node__):
    pass

class ŋnp_RandomState(node_rg__):
    @staticmethod
    def eval__(i):
        return np.random.RandomState(i)

class ŋrg_MT19937(node_rg__):
    @staticmethod
    def eval__(i):
        return randomgen.Generator(randomgen.MT19937(i, mode='sequence'))

#-------------------------------------------------------    
class node_random_quantity__(node__):
    pass

class ŋstandard_normal(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass
        
class ŋintegers(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

class ŋrandint(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

class ŋrandom(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

class ŋrandn(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

#-------------------------------------------------------  

@in_node____
class ŋndtype(node__):
    def  __new__(cls, v):
        if isinstance(v, type):
            v = v.__name__
        t = node__.__new__(cls, v)
        return t   
    @staticmethod
    def eval__(s):
        return getattr(np, s)


class node_numpy__(node__):
    class slice__(tuple):
        def __getitem__(self, i):
            return ŋnp_slice(tuple.__getitem__(self, 0), i)       
    @property
    def slice(self):
        return node_numpy__.slice__((self,))

    class slicer_inplace_operation__(tuple):
        def __getitem__(self, i):
            operation, n = self
            #n = tuple.__getitem__(self, 1)
            return operation( n, ŋnp_slice(n, i[:-1]), i[-1])
    @property
    def slice_assign(self):
        return node_numpy__.slicer_inplace_operation__((ŋnp_inplace_assign, self))
    @property
    def slice_multiply(self):
        return node_numpy__.slicer_inplace_operation__((ŋnp_inplace_multiply, self))
    @property
    def slice_add(self):
        return node_numpy__.slicer_inplace_operation__((ŋnp_inplace_add, self))
    
    def astype(self, ndtype):
        return ŋnp_astype(self, ndtype)



class ŋnp_array(node_numpy__):
    @classmethod
    def ŋtuple(cls, *args):
        return ŋtuple_literal(args)
    @staticmethod
    def eval__(*args):        
        return np.array(*args)

class ŋnp_slice(node_numpy__):
    @staticmethod
    def eval__(a, i):        
        return a[i]

class node_numpy_metaclass__(type):
    def __new__(cls, name, bases, attr):
        cls = type(node_numpy__)
        t = cls.__new__(cls, name, (node_numpy__,), attr)
        name = name[4:]
        f = getattr(np, name)
        def eval__(s, *args):
            return f(*args)
        t.eval__ = eval__
        return t
        
class ŋnp_inplace_assign(node_numpy__):
    @staticmethod
    def eval__(a, b, i):  
        b[...] = i
        return a

class ŋnp_inplace_multiply(node_numpy__):
    @staticmethod
    def eval__(a, b, i):  
        b[...] *= i
        return a

class ŋnp_inplace_add(node_numpy__):
    @staticmethod
    def eval__(a, b, i):  
        b[...] += i
        return a

class ŋnp_astype(node_numpy__):
    @staticmethod
    def eval__(a, dtype):  
        return a.astype(dtype)

@in_node____
class ŋnp_add(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋnp_subtract(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋnp_multiply(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋnp_divide(metaclass=node_numpy_metaclass__):
    pass

class ŋnp_indices(metaclass=node_numpy_metaclass__):
    pass
        
class ŋnp_transpose(metaclass=node_numpy_metaclass__):
    pass
    
class ŋnp_concatenate(metaclass=node_numpy_metaclass__):
    pass

class ŋnp_reshape(metaclass=node_numpy_metaclass__):
    pass

class ŋnp_copy(metaclass=node_numpy_metaclass__):
    pass

class ŋnp_ascontiguousarray(metaclass=node_numpy_metaclass__):
    pass

#-------------------------------------------------------    
def node_wrap_function(baseclass, func, in_node____ = False):
    name = 'ŋ' + func.__name__
    t = type.__new__(type, name, (baseclass,), {})
    def eval__(s, *args):
        return func(*args)
    t.eval__ = eval__
    globals()[name] = t
    if in_node____:
        setattr(node____, t.__name__, t)

node_wrap_function(node__, slice, in_node____ = True)

#-------------------------------------------------------    
def json_loads(json_string):
    data = json.loads(json_string)
    L = []
    G = globals()
    for type, args in data:
        t = G[type]
        if issubclass(t, node__):
            args = [L[x] for x in args]
        elif issubclass(t, node_literal__):
            pass
        else:
            raise TypeError()
        L.append(t(*args))  
    return L[-1]

#-------------------------------------------------------    
__all__ = ["json_loads"]
for x, y in list(globals().items()):
    if isinstance(y, type):
        if y.__name__[0] == 'ŋ':
            __all__.append(x)
