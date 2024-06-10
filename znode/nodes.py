import numpy as np

from znode.core.node__ import node____, node_literal__, node__, metaclass_node_apply__, def_metaclass_node_apply
from znode.core.node__ import yield_once

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
class ŋp_int64(node_literal__):
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
    def  __init__(self, items):
        # items can be single number since np.array constructor allows this
        if isinstance(items, (list, tuple)):
            items = tuples2lists__(items)
        node_literal__.__init__(self, items)


class ŋp_array_literal(node_literal__):
    pass

#-------------------------------------------------------  
@in_node____
class ŋtuple(node__):
    @staticmethod
    def eval__(*args):
        return args

@in_node____
class ŋlist(node__):
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
  
class ŋvariable(node__):
    def set(self, value):
        self[1] = self.wrap_arg(value)

    @staticmethod
    def eval__(x, y):
        # x is the name of the variable
        return y
    
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

@in_node____
class ŋneg(node__):
    @staticmethod
    def eval__(x):
        return -x

@in_node____
class ŋpow(node__):
    @staticmethod
    def eval__(x, y):
        return x**y

class ŋpoly(node__):
    @staticmethod
    def eval__(x_, coeffs):
        r = coeffs[0]
        x = x_
        for c in coeffs[1:]:
            r += c * x
            x = x * x_
        return r

#-------------------------------------------------------    
np_random_metaclass = def_metaclass_node_apply(np.random)
class node_np_random__(node__, metaclass=np_random_metaclass):
    pass

class ŋr_default_rng(node_np_random__):
    pass

class ŋr_Generator(node_np_random__):
    pass

class ŋr_MT19937(node_np_random__):
    pass

class ŋr_PCG64(node_np_random__):
    pass
#-------------------------------------------------------    
class node_random_samples__(node__):
    pass

class ŋr_integers(node_random_samples__, metaclass=metaclass_node_apply__):
    pass

class ŋr_random(node_random_samples__, metaclass=metaclass_node_apply__):
    pass

class ŋr_choice(node_random_samples__, metaclass=metaclass_node_apply__):
    pass

class ŋr_bytes(node_random_samples__, metaclass=metaclass_node_apply__):
    pass

class ŋr_standard_normal(node_random_samples__, metaclass=metaclass_node_apply__):
    pass

class ŋr_normal(node_random_samples__, metaclass=metaclass_node_apply__):
    pass

class ŋr_exponential(node_random_samples__, metaclass=metaclass_node_apply__):
    pass

class ŋr_normal_int(node_random_samples__):
    @staticmethod
    def eval__(rng, loc=0.0, scale=1.0, size=None):
        return np.round(rng.normal(loc, scale, size)).astype(int)

#-------------------------------------------------------  

@in_node____
class ŋp_ndtype(node__):
    def  __init__(self, v):
        if isinstance(v, type):
            v = v.__name__
        node__.__init__(self, v)
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
    
@in_node____
class ŋp_array(node_numpy__):
    @classmethod
    def ŋtuple(cls, *args):
        return ŋlist_literal(args)
    @classmethod
    def ŋlist(cls, *args):
        return ŋlist_literal(args)
    @staticmethod
    def eval__(*args, **kwargs):        
        return np.array(*args, **kwargs)

class ŋp_slice(node_numpy__):
    @staticmethod
    def eval__(a, i):        
        return a[i]
    def eval_symbolic____(cls, o, *args, **kwargs):
        args = cls.eval_symbolic_packargs(args, kwargs)
        r = '{}[{}]'.format(o, args)
        return r      

node_numpy_metaclass__ = def_metaclass_node_apply(np)

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
    
class ŋp_interleaf(node_numpy__):
    @staticmethod
    def eval__(*U):  
        R = np.empty((*U[0].shape,len(U)))
        for i in range(len(U)):
            R[...,i] = U[i]
        return R    

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
class ŋp_add(node_numpy__, metaclass=node_numpy_metaclass__):
    @classmethod
    def eval_symbolic____(cls, a, b):
        r = '({} + {})'.format(a, b)
        return r           

@in_node____
class ŋp_subtract(node_numpy__, metaclass=node_numpy_metaclass__):
    @classmethod
    def eval_symbolic____(cls, a, b):
        r = '({} - {})'.format(a, b)
        return r    
@in_node____
class ŋp_multiply(node_numpy__, metaclass=node_numpy_metaclass__):
    @classmethod
    def eval_symbolic____(cls, a, b):
        r = '({} * {})'.format(a, b)
        return r     

@in_node____
class ŋp_divide(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_mod(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_remainder(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_negative(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_square(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_sqrt(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

#------------------------------------------------------------
    
@in_node____
class ŋp_equal(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_not_equal(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_greater(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_less(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_greater_equal(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_less_equal(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

#------------------------------------------------------------

@in_node____
class ŋp_sin(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_cos(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_tan(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_arcsin(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_arccos(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_arctan(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_sinh(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_cosh(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_tanh(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_arcsinh(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_arccosh(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_arctanh(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_exp(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

@in_node____
class ŋp_log(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
@in_node____
class ŋp_power(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

#------------------------------------------------------------

class ŋp_fmod(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_abs(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_real(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_imag(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_angle(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_floor(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_ceil(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_max(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_min(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_maximum(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_minimum(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_isnan(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_indices(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_repeat(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_digitize(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_take(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_copy(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_where(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
                
class ŋp_transpose(node_numpy__, metaclass=node_numpy_metaclass__):
    pass
    
class ŋp_concatenate(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_dstack(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_reshape(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_ascontiguousarray(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_zeros(node_numpy__, metaclass=node_numpy_metaclass__):
    pass

class ŋp_ones(node_numpy__, metaclass=node_numpy_metaclass__):
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
ŋf_yield_once = yield_once

__all__ = []
for x, y in list(globals().items()):
    if x[0] == 'ŋ':
        __all__.append(x)

