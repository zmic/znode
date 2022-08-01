import numpy as np

from znode.core.node__ import node____, node_literal__, node__, metaclass_node_apply__

def in_node____(x):
    setattr(node____, x.__name__, x)
    return x

#-------------------------------------------------------    
@in_node____
class ŋNone(node_literal__):
    pass

@in_node____
class ŋbool(node_literal__):
    pass

@in_node____
class ŋint(node_literal__):
    pass

@in_node____
class ŋfloat(node_literal__):
    pass

@in_node____
class ŋcomplex(node_literal__):
    pass

@in_node____
class ŋstr(node_literal__):
    pass

def tuples2lists__(t):
    return [tuples2lists__(x) if isinstance(x, (list, tuple)) else x for x in t]

# this class is only used for ŋp_array constructor
class ŋlist_literal(node_literal__):
    def  __new__(cls, items):
        # items can be single number since np.array constructor allows this
        if isinstance(items, (list, tuple)):
            items = tuples2lists__(items)
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

@in_node____
class ŋkwarg(node__):
    @staticmethod
    def eval__(k, v):        
        return node__.kwargx(k, v)
    @classmethod
    def eval_symbolic____(cls, k, v):
        r = '{}={}'.format(k, v)
        return r   

#-------------------------------------------------------  
  
@in_node____
class ŋadd(node__):
    @staticmethod
    def eval__(x, y):
        return x + y
    
@in_node____
class ŋmul(node__):
    @staticmethod
    def eval__(x, y):
        return x * y
            
@in_node____
class ŋsub(node__):
    @staticmethod
    def eval__(x, y):
        return x - y
    
@in_node____
class ŋdiv(node__):
    @staticmethod
    def eval__(x, y):
        return x / y
            
#-------------------------------------------------------    
class node_rg__(node__):
    pass

class ŋp_RandomState(node_rg__):
    @staticmethod
    def eval__(i):
        return np.random.RandomState(i)

class ŋrg_MT19937(node_rg__):
    @staticmethod
    def eval__(i, j = None):
        rng = np.random.Generator( np.random.MT19937(i))
        return rng
#-------------------------------------------------------    
class node_random_quantity__(node__):
    pass

class ŋstandard_normal(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

class ŋnormal(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

class ŋintegers(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

class ŋrandint(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

class ŋrandom(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

class ŋrandn(node_random_quantity__, metaclass=metaclass_node_apply__):
    pass

class ŋnormal_int(node_random_quantity__):
    @staticmethod
    def eval__(rng, loc=0.0, scale=1.0, size=None):
        return np.round(rng.normal(loc, scale, size)).astype(int)



#-------------------------------------------------------  

@in_node____
class ŋp_ndtype(node__):
    def  __new__(cls, v):
        if isinstance(v, type):
            v = v.__name__
        t = node__.__new__(cls, v)
        return t   
    @staticmethod
    def eval__(s):
        return getattr(np, s)
    @classmethod
    def eval_symbolic____(cls, a):
        r = 'np.{}'.format(a)
        return r   

class node_numpy__(node__):
    class slice__(tuple):
        def __getitem__(self, i):
            return ŋp_slice(tuple.__getitem__(self, 0), i)       
    @property
    def slice(self):
        return node_numpy__.slice__((self,))

    class slicer_inplace_operation__(tuple):
        def __getitem__(self, i):
            operation, n = self
            #n = tuple.__getitem__(self, 1)
            return operation( n, ŋp_slice(n, i[:-1]), i[-1])
    @property
    def slice_assign(self):
        return node_numpy__.slicer_inplace_operation__((ŋp_inplace_assign, self))
    @property
    def slice_multiply(self):
        return node_numpy__.slicer_inplace_operation__((ŋp_inplace_multiply, self))
    @property
    def slice_add(self):
        return node_numpy__.slicer_inplace_operation__((ŋp_inplace_add, self))
    




class ŋp_array(node_numpy__):
    @classmethod
    def ŋtuple(cls, *args):
        return ŋlist_literal(args)
    @staticmethod
    def eval__(*args):        
        return np.array(*args)

class ŋp_slice(node_numpy__):
    @staticmethod
    def eval__(a, i):        
        return a[i]
    def eval_symbolic____(cls, o, *args, **kwargs):
        args = cls.eval_symbolic_packargs(args, kwargs)
        r = '{}[{}]'.format(o, args)
        return r   

class node_numpy_metaclass__(type):
    def __new__(cls, name, bases, attr):
        cls = type(node_numpy__)
        t = cls.__new__(cls, name, (node_numpy__,), attr)
        name = name[3:]
        f = getattr(np, name)
        def eval__(s, *args, **kwargs):
            return f(*args, **kwargs)
        t.eval__ = eval__
        if not 'eval_symbolic____' in attr:
            def eval_symbolic____(cls, *args, **kwargs):
                args = cls.eval_symbolic_packargs(args, kwargs)
                r = 'np.{}({})'.format(name, args)
                return r                    
            t.eval_symbolic____ = eval_symbolic____
        return t        
        
class ŋp_inplace_assign(node_numpy__):
    @staticmethod
    def eval__(a, b, i):  
        b[...] = i
        return a

class ŋp_inplace_multiply(node_numpy__):
    @staticmethod
    def eval__(a, b, i):  
        b[...] *= i
        return a

class ŋp_inplace_add(node_numpy__):
    @staticmethod
    def eval__(a, b, i):  
        b[...] += i
        return a

@in_node____
class ŋp_astype(node_numpy__):
    @staticmethod
    def eval__(a, dtype):  
        return a.astype(dtype)
    @classmethod
    def eval_symbolic____(cls, o, *args, **kwargs):
        args = cls.eval_symbolic_packargs(args, kwargs)
        r = '{}.astype({})'.format(o, args)
        return r           
#------------------------------------------------------------

@in_node____
class ŋp_add(metaclass=node_numpy_metaclass__):
    @classmethod
    def eval_symbolic____(cls, a, b):
        r = '({} + {})'.format(a, b)
        return r           

@in_node____
class ŋp_subtract(metaclass=node_numpy_metaclass__):
    @classmethod
    def eval_symbolic____(cls, a, b):
        r = '({} - {})'.format(a, b)
        return r    
@in_node____
class ŋp_multiply(metaclass=node_numpy_metaclass__):
    @classmethod
    def eval_symbolic____(cls, a, b):
        r = '({} * {})'.format(a, b)
        return r     

@in_node____
class ŋp_divide(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_mod(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_remainder(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_negative(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_square(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_sqrt(metaclass=node_numpy_metaclass__):
    pass

#------------------------------------------------------------
    
@in_node____
class ŋp_equal(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_not_equal(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_greater(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_less(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_greater_equal(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_less_equal(metaclass=node_numpy_metaclass__):
    pass

#------------------------------------------------------------

@in_node____
class ŋp_sin(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_cos(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_tan(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_arcsin(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_arccos(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_arctan(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_sinh(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_cosh(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_tanh(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_arcsinh(metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_arccosh(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_arctanh(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_exp(metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_log(metaclass=node_numpy_metaclass__):
    pass
    
#------------------------------------------------------------

class ŋp_fmod(metaclass=node_numpy_metaclass__):
    pass

class ŋp_abs(metaclass=node_numpy_metaclass__):
    pass

class ŋp_real(metaclass=node_numpy_metaclass__):
    pass

class ŋp_imag(metaclass=node_numpy_metaclass__):
    pass

class ŋp_angle(metaclass=node_numpy_metaclass__):
    pass

class ŋp_floor(metaclass=node_numpy_metaclass__):
    pass

class ŋp_ceil(metaclass=node_numpy_metaclass__):
    pass

class ŋp_max(metaclass=node_numpy_metaclass__):
    pass

class ŋp_min(metaclass=node_numpy_metaclass__):
    pass

class ŋp_maximum(metaclass=node_numpy_metaclass__):
    pass

class ŋp_minimum(metaclass=node_numpy_metaclass__):
    pass

class ŋp_isnan(metaclass=node_numpy_metaclass__):
    pass

class ŋp_indices(metaclass=node_numpy_metaclass__):
    pass

class ŋp_repeat(metaclass=node_numpy_metaclass__):
    pass

class ŋp_digitize(metaclass=node_numpy_metaclass__):
    pass

class ŋp_take(metaclass=node_numpy_metaclass__):
    pass

class ŋp_copy(metaclass=node_numpy_metaclass__):
    pass

class ŋp_where(metaclass=node_numpy_metaclass__):
    pass
                
class ŋp_transpose(metaclass=node_numpy_metaclass__):
    pass
    
class ŋp_concatenate(metaclass=node_numpy_metaclass__):
    pass

class ŋp_dstack(metaclass=node_numpy_metaclass__):
    pass

class ŋp_reshape(metaclass=node_numpy_metaclass__):
    pass

class ŋp_ascontiguousarray(metaclass=node_numpy_metaclass__):
    pass

class ŋp_zeros(metaclass=node_numpy_metaclass__):
    pass

class ŋp_ones(metaclass=node_numpy_metaclass__):
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
ŋf_load = node____.load
__all__ = []
for x, y in list(globals().items()):
    if isinstance(y, type):
        if y.__name__[0] == 'ŋ':
            __all__.append(x)

