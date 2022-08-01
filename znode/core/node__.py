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
              

node_dict___ = {}        
class metaclass_node(type):
    def __new__(cls, name, bases, attr, **kwargs):
        t = super().__new__(cls, name, bases, attr)
        if name[0] == 'ŋ':
            if name in node_dict___:
                raise TypeError("Node type '{}' already exists".format(name))
            node_dict___[name] = t
        return t

class node____(tuple, metaclass = metaclass_node):
    def dump(self):
        L = []
        D = {}
        dump____(L, D, self)
        return L
        
    @staticmethod
    def load(data):
        L = []
        for type, args in data:
            t = node_dict___[type]
            if issubclass(t, node__):
                args = [L[x] for x in args]
            elif issubclass(t, node_literal__):
                pass
            else:
                raise TypeError()
            L.append(t(*args))  
        return L[-1]

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
        if isinstance(a, complex):
            return cls.ŋcomplex(a)
        if isinstance(a, str):
            return cls.ŋstr(a)
        if isinstance(a, tuple):
            return cls.ŋtuple(*a)
        if isinstance(a, type):
            if np.issubdtype(a, np.number):
                return cls.ŋp_ndtype(a)
        if isinstance(a, slice):
            return cls.ŋslice(a.start, a.stop, a.step)
        if a is None:
            return cls.ŋNone(a)
        raise TypeError("Can't handle type " + type(a).__name__)
        
    @property
    def r(self):
        return self[-1][0]

    def __mul__(self, other):
        return self.ŋp_multiply(self, other)   
        
    def __add__(self, other):
        return self.ŋp_add(self, other)   
   
    def __sub__(self, other):
        return self.ŋp_subtract(self, other)   
        
    def __pow__(self, other):
        return self.ŋp_power(self, other)   
        
    def __truediv__ (self, other):
        return self.ŋp_divide(self, other)   

    def __floordiv__ (self, other):
        return
        #return self.ŋp_divide(self, other)   
        
    def __mod__(self, other):
        return self.ŋp_mod(self, other)   
        
    def __neg__(self):
        return self.ŋp_negative(self, other)   

    def __eq__(self, other):
        return self.ŋp_equal(self, other)   

    def __ne__(self, other):
        return self.ŋp_not_equal(self, other)   

    def __gt__(self, other):
        return self.ŋp_greater(self, other)   
        
    def __lt__(self, other):
        return self.ŋp_less(self, other)   
        
    def __ge__(self, other):
        return self.ŋp_greater_equal(self, other)   
        
    def __le__(self, other):
        return self.ŋp_less_equal(self, other)   


    def __radd__(self, other):
        return self.ŋp_add(other, self)   

    def __rsub__(self, other):
        return self.ŋp_subtract(other, self)   

    def __rmul__(self, other):
        return self.ŋp_multiply(other, self)   
    
    def __rtruediv__(self, other):
        return self.ŋp_divide(other, self)           


    #def __getitem__(self, *args):
    #    raise RuntimeError()

    def yield_of_type(self, type):
        for n in yield_once(self):
            if isinstance(n, type):
                yield n

    def find_first_of_type(self, type):
        for n in self.yield_of_type(type):
            return n

load = node____.load
#-------------------------------------------------------    
class node_literal__(node____):
    def  __new__(cls, v):
        t = super().__new__(cls, ((v,),))
        return t
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__,repr(self[0][0]))        
    def reset(self):
        pass
#-------------------------------------------------------    
class node__(node____):
    symbolic_name = None
    symbolic_standalone = None
    symbolic_standalone_arguments = None
    class kwargx(tuple):
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
            return self.__class__.__name__ + repr(a) 
    def eval_debug(self):
        self.debug_info = []
        return self.eval_debug_(0, self.debug_info)
    def eval_debug_(self, depth, debug_info):
        if self[-1]:
            raise RuntimeError("Node already evaluated")
        A = self[:-1]
        for i in A:
            if not i[-1]:
                i.eval_debug_(depth + 1, debug_info)
        debug_info.append((depth,str(self)[:120]))
        args = [i[-1][0] for i in A if not isinstance(i[-1][0], node__.kwargx)]
        kwargs = {i[-1][0][0]:i[-1][0][1] for i in A if isinstance(i[-1][0], node__.kwargx)}
        r = self.eval__(*args, **kwargs)
        self[-1].append(r)
        return r                   
    def eval(self):
        if self[-1]:
            raise RuntimeError("Node already evaluated")
        A = self[:-1]
        for i in A:
            if not i[-1]:
                i.eval()
        args = [i[-1][0] for i in A if not isinstance(i[-1][0], node__.kwargx)]
        kwargs = {i[-1][0][0]:i[-1][0][1] for i in A if isinstance(i[-1][0], node__.kwargx)}
        r = self.eval__(*args, **kwargs)
        self[-1].append(r)
        return r
    @staticmethod
    def eval_symbolic_packargs(args, kwargs):
        args = ', '.join([str(a) for a in args])
        kwargs = ', '.join([ '%s=%s'%(k,v) for k, v in kwargs.items()])
        if args and kwargs:
            args += ', '
        return args + kwargs
    @classmethod
    def eval_symbolic____(cls, *args, **kwargs):
        args = cls.eval_symbolic_packargs(args, kwargs)
        symbolic_name = cls.symbolic_name or cls.__name__
        r = '{}({})'.format(symbolic_name, args)
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
            if self.symbolic_standalone_arguments != None:
                for i in A:
                    i.symbolic_standalone = self.symbolic_standalone_arguments                    
            for i in A:
                usage_count[id(i)] += 1
        elif round == 1:
            if not self[-1]:
                args = [i[-1][0] for i in A]
                r = self.eval_symbolic____(*args, **{})
                if (self.symbolic_standalone==1) or (usage_count[id(self)] != 1) or (len(r) > 60 and self.symbolic_standalone!=0):
                    x_count = usage_count['x_count']            
                    usage_count['x_count'] += 1
                    variable = 'r{}'.format(x_count)
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
    def astype(self, ndtype):
        return self.ŋp_astype(self, ndtype)
    def reset(self):
        for x in self[:-1]:
            x.reset()
        self[-1].clear()
           

#-------------------------------------------------------    

class metaclass_node_apply__(metaclass_node):
    def __new__(cls, name, bases, attr):
        t = super().__new__(cls, name, bases, attr)
        name = s_[1] if len(s_ := name.split('_', 1)) > 1 else name[1:]
        def eval__(s, o, *args, **kwargs):
            return getattr(o, name)(*args, **kwargs)
        t.eval__ = eval__ 
        def eval_symbolic____(cls, o, *args, **kwargs):
            args = cls.eval_symbolic_packargs(args, kwargs)
            r = '{}.{}({})'.format(o, name, args)
            return r                    
        t.eval_symbolic____ = eval_symbolic____
        return t


def def_metaclass_node_apply(container, container_name=None):
    container_name = container_name or str(container)
    class metaclass_node_apply__(metaclass_node):
        def __new__(cls, name, bases, attr):
            t = super().__new__(cls, name, bases, attr)
            if name[-2:] != '__':
                name = name.split('_', 1)[1]
                f = getattr(container, name)
                def eval__(s, *args, **kwargs):
                    return f(*args, **kwargs)
                t.eval__ = eval__ 
                if not 'eval_symbolic____' in attr:
                    def eval_symbolic____(cls, *args, **kwargs):
                        args = cls.eval_symbolic_packargs(args, kwargs)
                        r = '{}.{}({})'.format(container_name, name, args)
                        return r                    
                t.eval_symbolic____ = eval_symbolic____
            return t
    return metaclass_node_apply__
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

