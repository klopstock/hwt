
class Param():
    def __init__(self, initval):
        self.val = initval
        self.parent = None
        self._expr = None
        a = 1
        for propName in dir(initval):
            prop = getattr(initval, propName)
            if isinstance(prop, a.__abs__.__class__):
                def wrap(*args, **kwargs):
                    return getattr(self.val, propName)(*args, **kwargs)
                setattr(self, propName, wrap)
    def get(self):
        if self.parent:
            v = self.parent.get()
        else:
            v = self.val
        if self._expr:
            return self._expr(v)
        else:
            return v
  
    def inherit(self, param):
        self.parent = param
    
    def set(self, val):
        self.val = val
        
    def expr(self, fn):
        p = Param(self.val)
        p.inherit(self)
        p._expr = fn
        return p
    def toVhdlStr(self):
        v = self
        while v.parent:
            v = v.parent
        if hasattr(v, "name"):
            return v.name
        else:
            return v.get()
    def __str__(self):
        if hasattr(self, "name"):
            return self.name.upper()
        if not self.parent:
            return str(self.get())
        else:
            if self._expr:
                return str(self.get())
                #raise NotImplementedError()
            return str(self.parent)

    def __repr__(self):
        return "<%s, val=%s>" % (self.__class__.__name__, self.get()) 
        

def getParamVhdl(p):
    if isinstance(p, Param):
        return p.toVhdlStr()
    else:
        return p
    
def getParam(p):
    if isinstance(p, Param):
        return p.get()
    else:
        return p
    
    
def inheritAllParams(cls):
    '''foreach _subInterfaces, _interfaces and _subUnits  inherit parameters'''
    cls._builded()
    def inherit(subelements):
        for _, intf in subelements.items():
            for paramName, param in cls._params.items():
                if hasattr(intf, paramName):
                    p = getattr(intf, paramName)
                    p.inherit(param)
    for n in ['_subInterfaces', '_interfaces', '_subUnits']:
        if hasattr(cls, n):
            inherit(getattr(cls, n))
        
    return cls