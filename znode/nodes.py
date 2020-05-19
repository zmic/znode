import numpy as np
import randomgen
import json

from .node__ import node____, node_literal__, node__, metaclass_node_apply__

def in_node__(x):
    setattr(node____, x.__name__, x)
    return x

#-------------------------------------------------------    
@in_node__
class ŋNone(node_literal__):
    pass

@in_node__
class ŋint(node_literal__):
    pass

@in_node__
class ŋfloat(node_literal__):
    pass

@in_node__
class ŋstr(node_literal__):
    pass

class ŋtuple_literal(node_literal__):
    def  __new__(cls, items):
        if isinstance(items, list):
            items = tuple(items)
        t = node_literal__.__new__(cls, items)
        return t  

#-------------------------------------------------------  
@in_node__
class ŋtuple(node__):
    @staticmethod
    def eval__(*args):
        return args
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

#-------------------------------------------------------  

@in_node__
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
    class slicer(tuple):
        def __getitem__(self, i):
            return ŋnp_array_slice(tuple.__getitem__(self, 0), i)       
        def __setitem__(self, i, v):
            return ŋnp_assign(ŋnp_array_slice(tuple.__getitem__(self, 0), i), v)
    @property
    def slice(self):
        return node_numpy__.slicer((self,))
        
class ŋnp_array(node_numpy__):
    @classmethod
    def ŋtuple(cls, *args):
        return ŋtuple_literal(args)
    @staticmethod
    def eval__(*args):        
        return np.array(*args)

class ŋnp_array_slice(node_numpy__):
    @staticmethod
    def eval__(a, i):        
        return a[i]

class node_numpy_metaclass__(type):
    def __new__(cls, name, bases, attr):
        cls = type(node_numpy__)
        t = cls.__new__(cls, name, node_numpy__.__bases__, attr)
        name = name[4:]
        f = getattr(np, name)
        def eval__(s, *args):
            return f(*args)
        t.eval__ = eval__
        return t
        
class ŋnp_assign(node_numpy__):
    @staticmethod
    def eval__(a, i):        
        a[...] = i
        return a

@in_node__
class ŋnp_add(metaclass=node_numpy_metaclass__):
    pass

@in_node__
class ŋnp_subtract(metaclass=node_numpy_metaclass__):
    pass

@in_node__
class ŋnp_multiply(metaclass=node_numpy_metaclass__):
    pass

@in_node__
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



#-------------------------------------------------------    
def node_wrap_function(baseclass, func):
    name = 'ŋ' + func.__name__
    t = type.__new__(type, name, (baseclass,), {})
    def eval__(s, o, *args):
        return func(*args)
    t.eval__ = eval__
    globals()[name] = t

node_wrap_function(node__, slice)

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
print(__all__)