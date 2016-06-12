from hdl_toolkit.hdlObjects.types.hdlType import HdlType 

class Enum(HdlType):
    def __init__(self, name, valueNames):
        super(Enum, self).__init__()
        self.name = name
        self._allValues = valueNames
        for n in valueNames:
            setattr(self, n, self.fromPy(n))
            
    def valAsVhdl(self, val, serializer):
        return  '%s' % str(val.val)
    
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hdl_toolkit.hdlObjects.types.enumVal import EnumVal 
            cls._valCls = EnumVal
            return cls._valCls