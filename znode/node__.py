import numpy as np
from collections import defaultdict

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
        if isinstance(a, bool):
            return cls.ŋbool(a)
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
        return self.ŋnp_add(other, self)   

    def __rsub__(self, other):
        return self.ŋnp_subtract(other, self)   

    def __rmul__(self, other):
        return self.ŋnp_multiply(other, self)   
    
    def __rtruediv__(self, other):
        return self.ŋnp_divide(other, self)           


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
    class kwarg(tuple):
        def  __new__(cls, k, v):
            t = super().__new__(cls, (k, v))
            return t        
    def  __new__(cls, *args, **kwargs):
        args = [cls.wrap_arg(x) for x in args]
        args += [cls.ŋkwarg(x, cls.wrap_arg(y)) for x, y in kwargs.items()]
        t = super().__new__(cls, args+[list()])
        return t
    def __repr__(self):
        a = self[:-1]
        if len(a) == 1:
           return '{}({})'.format(self.__class__.__name__,repr(self[0]))        
        else:
            return self.__class__.__name__ + repr(self[:-1])        
    def eval(self, debug=0):
        if self[-1]:
            raise RuntimeError("Node already evaluated")
        if debug:
            debug += 2
        A = self[:-1]
        for i in A:
            if not i[-1]:
                i.eval(debug)
        if debug:
            debug -= 2
            print(' '*debug, str(self)[:120])
        args = [i[-1][0] for i in A if not isinstance(i[-1][0], node__.kwarg)]
        kwargs = {i[-1][0][0]:i[-1][0][1] for i in A if isinstance(i[-1][0], node__.kwarg)}
        r = self.eval__(*args, **kwargs)
        self[-1].append(r)
        return r
    def eval_symbolic____(self, args, kwargs):
        args = ', '.join([str(a) for a in args])
        kwargs = ', '.join([ '%s=%s'%(k,v) for k, v in kwargs.items()])
        if args and kwargs:
            args += ', '
        r = '{}({}{})'.format(self.__class__.__name__, args, kwargs)
        return r            
    def eval_symbolic__(self, usage_count, round, debug, already_visited):
        if debug:
            debug += 2
        A = self[:-1]
        for i in A:
            if not isinstance(i, node_literal__):
                if not id(i) in already_visited:
                    already_visited.add(id(i))
                    s = i.eval_symbolic__(usage_count, round, debug, already_visited)
        if debug:
            debug -= 2
        if round == 0:
            for i in A:
                usage_count[id(i)] += 1
        elif round == 1:
            if not self[-1]:
                args = [i[-1][0] for i in A if not isinstance(i[-1][0], node__.kwarg)]
                kwargs = {i[-1][0][0]:i[-1][0][1] for i in A if isinstance(i[-1][0], node__.kwarg)}
                r = self.eval_symbolic____(args, kwargs)
                if usage_count[id(self)] > 1 or len(r) > 40:
                    x_count = usage_count['x_count']            
                    usage_count['x_count'] += 1
                    variable = 'x{}'.format(x_count)
                    usage_count['L'] += ['{} = {}'.format(variable, r)]
                    r = variable
                self[-1].append(r)            
                #print(' '*debug, str(self)[:120])
    def eval_symbolic(self, debug=0):
        lines = []
        usage_count = defaultdict(int)
        usage_count['L'] = lines
        self.eval_symbolic__(usage_count, 0, debug, set())
        self.eval_symbolic__(usage_count, 1, debug, set())
        return lines

        

#-------------------------------------------------------    
class metaclass_node_apply__(type):
    def __new__(cls, name, bases, attr):
        t = type.__new__(cls, name, bases, attr)
        name = name[1:]
        def eval__(s, o, *args, **kwargs):
            return getattr(o, name)(*args, **kwargs)
        t.eval__ = eval__
        return t

class metaclass_node_func__(type):
    def __new__(cls, name, bases, attr, **kargs):
        t = type.__new__(cls, name, bases, attr)
        func = kwargs['f']
        def eval__(s, o, *args, **kwargs):
            return func(*args, **kwargs)
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

