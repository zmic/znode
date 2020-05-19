import numpy as np
import json

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
    def json_dumps(self):
        return json.dumps(self.dump())
        
    @classmethod
    def pack_arg(cls, a):
        if isinstance(a, node____):
            return a
        if isinstance(a, int):
            return cls.ŋint(a)
        if isinstance(a, float):
            return cls.ŋfloat(a)
        if isinstance(a, tuple):
            return cls.ŋtuple(a)
        else:
            raise TypeError("Can't handle type " + type(a).__name__)
        
    @property
    def r(self):
        return self[-1][0]
        
    def __mul__(self, other):
        return self.mul1(self, other)
        
    def __add__(self, other):
        return self.add1(self, other)
   
    def __sub__(self, other):
        return self.sub1(self, other)
        
    def __pow__(self, other):
        return self.pow1(self, other)
        
    def __div__(self, other):
        return self.div1(self, other)
        
    def __mod__(self, other):
        return self.mod1(self, other)
        
    def __neg__(self):
        return self.neg1(self)
        
    def __gt__(self, other):
        return self.gt1(self, other)
        
    def __lt__(self, other):
        return self.lt1(self, other) 
        
    def __ge__(self, other):
        return self.ge1(self, other)
        
    def __le__(self, other):
        return self.le1(self, other)   
    
#-------------------------------------------------------    
class node_literal__(node____):
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__,repr(self[0][0]))        
    def  __new__(cls, v):
        t = super().__new__(cls, ((v,),))
        return t
#-------------------------------------------------------    
class node__(node____):
    def  __new__(cls, *args):
        args = [cls.pack_arg(x) for x in args]
        t = super().__new__(cls, args+[list()])
        return t
    def __repr__(self):
        a = self[:-1]
        if len(a) == 1:
           return '{}({})'.format(self.__class__.__name__,repr(self[0]))        
        else:
            return self.__class__.__name__ + repr(self[:-1])        
    def eval(self):
        A = self[:-1]
        for i in A:
            if not i[-1]:
                i.eval()
        r = self.eval__(*[i[-1][0] for i in A])
        self[-1].append(r)
        return r
        

