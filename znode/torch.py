import torch

DEVICE = torch.device('cuda:0')

from znode.core.node__ import node____, node_literal__, node__, metaclass_node_apply__, def_metaclass_node_apply
from znode.core.node__ import yield_once

def in_node____(x):
    setattr(node____, x.__name__, x)
    return x


node_torch_metaclass__ = def_metaclass_node_apply(torch)


#-------------------------------------------------------    

def wrap_arch_torch(a):
    if isinstance(a, torch.dtype):
        return ŋto_dtype(a)

node____.wrap_arg_extensions.append(wrap_arch_torch)

#@in_node____
class ŋto_dtype(node__):
    def  __init__(self, v):
        if isinstance(v, torch.dtype):
            v = str(v).split('.')[1]
        node__.__init__(self, v)
    @staticmethod
    def eval__(s):
        return getattr(torch, s)
    @classmethod
    def eval_symbolic____(cls, a):
        r = 'torch.{}'.format(a)
        return r   

'''
#@in_node____
class ŋto_canvas(node__):
    @staticmethod
    def eval__(NX, NY, x0, x1, y0, y1, endpoint, dtype):
        X = torch.arange(NX,dtype=torch.float64, device=DEVICE).repeat(NY,1)
        Y = torch.arange(NY,dtype=torch.float64, device=DEVICE).unsqueeze(1).repeat(1,NX)
        fy = (y1 - y0) / (NY - 1) if endpoint else (y1 - y0) / NY
        fx = (x1 - x0) / (NX - 1) if endpoint else (x1 - x0) / NX
        X, Y = x0 + fx*X, y0 + fy*Y
        return X.type(dtype), Y.type(dtype)
'''

class ŋto_xcoords(node__):
    @staticmethod
    def eval__(NX, NY, x0, x1, endpoint, dtype):
        X = torch.arange(NX,dtype=torch.float64, device=DEVICE).repeat(NY,1)
        fx = (x1 - x0) / (NX - 1) if endpoint else (x1 - x0) / NX
        X = x0 + fx*X
        return X.type(dtype)

class ŋto_ycoords(node__):
    @staticmethod
    def eval__(NX, NY, y0, y1, endpoint, dtype):
        Y = torch.arange(NY,dtype=torch.float64, device=DEVICE).unsqueeze(1).repeat(1,NX)
        fy = (y1 - y0) / (NY - 1) if endpoint else (y1 - y0) / NY
        Y = y0 + fy*Y
        return Y.type(dtype)



