import numpy as np
import randomgen

from .node__ import node____, node_literal__, node__, metaclass_node_apply__
from .nodes import node_numpy__

#-------------------------------------------------------    

class ŋcanvas(node_numpy__):
    @staticmethod
    def eval__(X, Y, x0, x1, y0, y1, endpoint, dtype):
        I = np.indices((Y,X)).astype(np.float64)
        fy = (y1 - y0) / (Y - 1) if endpoint else (y1 - y0) / Y
        fx = (x1 - x0) / (X - 1) if endpoint else (x1 - x0) / X
        I[0], I[1] = x0 + fx*I[1], y0 + fy*I[0]
        return I.astype(dtype)

class ŋccanvas(node_numpy__):
    @staticmethod
    def eval__(X, Y, x0, x1, y0, y1, endpoint, dtype):
        I = np.indices((Y,X)).astype(dtype)
        fy = (y1 - y0) / (Y - 1) if endpoint else (y1 - y0) / Y
        fx = (x1 - x0) / (X - 1) if endpoint else (x1 - x0) / X
        return (x0 + fx*I[1]) + 1j*(y0 + fy*I[0])

class ŋrotatexy(node_numpy__):
    @staticmethod
    def eval__(X, Y, a):
        return X*np.cos(a)+Y*np.sin(a), -X*np.sin(a)+Y*np.cos(a)

