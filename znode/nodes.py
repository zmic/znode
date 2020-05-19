import numpy as np
import randomgen
import json

from .node__ import node____, node_literal__, node__

def in_node__(x):
    setattr(node____, x.__name__, x)
    return x

#-------------------------------------------------------    
@in_node__
class ŋint(node_literal__):
    pass

@in_node__
class ŋfloat(node_literal__):
    pass

@in_node__
class ŋstr(node_literal__):
    pass

@in_node__
class ŋtuple(node_literal__):
    def  __new__(cls, v):
        if isinstance(v, list):
            v = tuple(v)
        t = node____.__new__(cls, ((v,),))
        return t   

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

class ŋrg_MT19937(node_rg__):
    @staticmethod
    def eval__(i):
        return randomgen.Generator(randomgen.MT19937(i, mode='sequence'))

#-------------------------------------------------------    
class node_random_quantity__(node__):
    pass


#-------------------------------------------------------    
class node_apply__(node__):
    pass
    
class ŋapply_metaclass__(type):
    def __new__(cls, name, bases, attr):
        cls = type(node_apply__)
        t = cls.__new__(cls, name, node_apply__.__bases__, attr)
        name = name[1:]
        def eval__(s, o, *args):
            return getattr(o, name)(*args)
        t.eval__ = eval__
        return t
        
class ŋstandard_normal(metaclass=ŋapply_metaclass__):
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
    pass
    
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
        
class ŋnp_add(metaclass=node_numpy_metaclass__):
    pass

class ŋnp_indices(metaclass=node_numpy_metaclass__):
    pass
        
    

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

    
    