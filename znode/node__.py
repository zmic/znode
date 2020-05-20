import numpy as np

def dump____(L, D, n):
    nid = id(n)
    if nid in D:
        return D[nid]
    if isinstance(n, node_literal__):
        args = [n[0][0]]
    elif isinstance(n, node__):
        args = [dump____(L, D, x) for x in n[:-1]]
    r = len(L)
    L.append([n.__class__.__name__, args])
    D[nid] = r
    return r
              
class node____(tuple):        
    def dump(self):
        L = []
        D = {}
        dump____(L, D, self)
        return L
        
    class indexer(tuple):
        def __getitem__(self, i):
            return node____.ŋindex(tuple.__getitem__(self, 0), i)       
    @property
    def index(self):
        return node____.indexer((self,))

    @classmethod
    def wrap_arg(cls, a):
        if isinstance(a, node____):
            return a
        if isinstance(a, int):
            return cls.ŋint(a)
        if isinstance(a, float):
            return cls.ŋfloat(a)
        if isinstance(a, str):
            return cls.ŋstr(a)
        if isinstance(a, tuple):
            return cls.ŋtuple(*a)
        if isinstance(a, type):
            if np.issubdtype(a, np.number):
                return cls.ŋndtype(a)
        if isinstance(a, slice):
            return cls.ŋslice(a.start, a.stop, a.step)
        if a is None:
            return cls.ŋNone(a)
        raise TypeError("Can't handle type " + type(a).__name__)
        
    @property
    def r(self):
        return self[-1][0]

    def __mul__(self, other):
        return self.ŋnp_multiply(self, other)   
        
    def __add__(self, other):
        return self.ŋnp_add(self, other)   
   
    def __sub__(self, other):
        return self.ŋnp_subtract(self, other)   
        
    def __pow__(self, other):
        return self.ŋnp_power(self, other)   
        
    def __truediv__ (self, other):
        return self.ŋnp_divide(self, other)   

    def __floordiv__ (self, other):
        return
        #return self.ŋnp_divide(self, other)   
        
    def __mod__(self, other):
        return self.ŋnp_remainder(self, other)   
        
    def __neg__(self):
        return self.ŋnp_negative(self, other)   

    def __eq__(self, other):
        return self.ŋnp_equal(self, other)   

    def __ne__(self, other):
        return self.ŋnp_not_equal(self, other)   

    def __gt__(self, other):
        return self.ŋnp_greater(self, other)   
        
    def __lt__(self, other):
        return self.ŋnp_less(self, other)   
        
    def __ge__(self, other):
        return self.ŋnp_greater_equal(self, other)   
        
    def __le__(self, other):
        return self.ŋnp_less_equal(self, other)   


    def __radd__(self, other):
        return self.ŋnp_add(self, other)   

    def __rsub__(self, other):
        return self.ŋnp_sub(self, other)   

    def __rmul__(self, other):
        return self.ŋnp_multiply(self, other)   
    
    def __rtruediv__(self, other):
        return self.ŋnp_div(self, other)           


    #def __getitem__(self, *args):
    #    raise RuntimeError()

    def yield_of_type(self, type):
        for n in yield_once(self):
            if isinstance(n, type):
                yield n

    def find_first_of_type(self, type):
        for n in self.yield_of_type(type):
            return n

#-------------------------------------------------------    
class node_literal__(node____):
    def  __new__(cls, v):
        t = super().__new__(cls, ((v,),))
        return t
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__,repr(self[0][0]))        

#-------------------------------------------------------    
class node__(node____):
    def  __new__(cls, *args):
        args = [cls.wrap_arg(x) for x in args]
        t = super().__new__(cls, args+[list()])
        return t
    def __repr__(self):
        a = self[:-1]
        if len(a) == 1:
           return '{}({})'.format(self.__class__.__name__,repr(self[0]))        
        else:
            return self.__class__.__name__ + repr(self[:-1])        
    def eval(self):
        if self[-1]:
            raise RuntimeError("Node already evaluated")
        A = self[:-1]
        for i in A:
            if not i[-1]:
                i.eval()
        r = self.eval__(*[i[-1][0] for i in A])
        self[-1].append(r)
        return r
        

#-------------------------------------------------------    
class metaclass_node_apply__(type):
    def __new__(cls, name, bases, attr):
        t = type.__new__(cls, name, bases, attr)
        name = name[1:]
        def eval__(s, o, *args):
            return getattr(o, name)(*args)
        t.eval__ = eval__
        return t

class metaclass_node_func__(type):
    def __new__(cls, name, bases, attr, **kargs):
        t = type.__new__(cls, name, bases, attr)
        func = kwargs['f']
        def eval__(s, o, *args):
            return func(*args)
        t.eval__ = eval__
        return t

#-------------------------------------------------------    
def yield_once__(S, n):
    nid = id(n)
    if not nid in S:
        yield n
        S.add(nid)
    for x in n[:-1]:
        yield from yield_once__(S, x)

def yield_once(n):
    S = set()
    yield from yield_once__(S, n)

