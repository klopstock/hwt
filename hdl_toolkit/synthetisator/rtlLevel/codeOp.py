
def If(cond, ifTrue=[], ifFalse=[]):
    # only assignments are expected there    
    for stm in ifTrue:
        stm.cond.add(cond)
    for stm in ifFalse:
        stm.cond.add(cond.opNot())
    
    ret = []
    ret.extend(ifTrue)
    ret.extend(ifFalse)
    return ret

def Switch(val, *cases):
    top = None
    for c in reversed(cases):
        if top is None:
            top = c[1]
        else:
            assert(c[0] is not None)
            top = If(val.opEq(c[0]),
                     c[1]
                     ,
                     top
                    )
        
    return top


class ReturnCalled(Exception):
    def __init__(self, val):
        self.val = val

class ReturnContainer():
    def __init__(self, val=None):
        self.val = val

    def seqEval(self):
        raise ReturnCalled(self.val.staticEval())       

def evalCond(cond):
    _cond = True
    for c in cond:
        _cond = _cond and bool(c.staticEval())
        
    return _cond


class IfContainer:
    def __init__(self, cond, ifTrue=[], ifFalse=[], elIfs=[]):
        self.cond = cond
        self.ifTrue = ifTrue
        self.elIfs = elIfs
        self.ifFalse = ifFalse
    
    def seqEval(self):
        if evalCond(self.cond):
            for s in self.ifTrue:
                s.seqEval()
        else:
            for c in self.elIfs:
                if evalCond(c[0]):
                    for s in c[1]:
                        s.seqEval()
                    return
            
            for s in self.ifFalse:
                s.seqEval()
        
    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.IfContainer(self)

class SwitchContainer():
    def __init__(self, switchOn, cases):
        self.switchOn = switchOn
        self.cases = cases
    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.SwitchContainer(self)
 
class WhileContainer():
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    
    def seqEval(self):
        
        while True:
            cond = True
            for c in self.cond:
                cond = cond and bool(c.staticEval())
            if not cond:
                break
            
            for s in self.body:
                s.seqEval()
