from copy import deepcopy
import os
import inspect

from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.synthetisator.rtlLevel.context import Context
from vhdl_toolkit.synthetisator.rtlLevel.unit import VHDLUnit
from vhdl_toolkit.synthetisator.interfaceLevel.interfaces.all import allInterfaces
from vhdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from vhdl_toolkit.synthetisator.interfaceLevel.buildable import Buildable
from vhdl_toolkit.architecture import Component
from vhdl_toolkit.synthetisator.param import Param

from python_toolkit.arrayQuery import single


class Unit(Buildable):
    """
    Class members:
    origin  - origin vhdl file
    @attention: Current implementation does not control if connections are connected to right interface objects
                this mean you can connect it to class interface definitions for example 
    """
    def __init__(self, intfClasses=allInterfaces):
        self.__class__._intfClasses = intfClasses
        self.__class__._builded()
        copyDict = {}
        
        for pName in  ["_entity", "_sigLvlUnit", "_params", "_interfaces", "_subUnits"]:
            v = getattr(self.__class__, pName, None)
            setattr(self, pName, deepcopy(v, copyDict)) 
            
        
        for intfName, interface in self._interfaces.items():
            interface._name = intfName
            interface._parent = self
            setattr(self, intfName, interface)
        
        for uName, unit in self._subUnits.items():
            unit._name = uName
            unit._parent = self
            setattr(self, uName, unit)
         
    @classmethod
    def _build(cls):
        cls._interfaces = {}
        cls._subUnits = {}
        cls._params = {}
        for propName, prop in vars(cls).items():
            if isinstance(prop, Interface):
                cls._interfaces[propName] = prop
            elif issubclass(prop.__class__, Unit):
                cls._subUnits[propName] = prop
            elif issubclass(prop.__class__, Param):
                cls._params[propName] = prop
                prop.name = propName    
        cls._clsBuildFor = cls
    def _cleanAsSubunit(self):
        for _, i in self._interfaces.items():
            i._rmSignals()
                    
    def _signalsForMyEntity(self, context, prefix):
        for suPortName, suPort in self._interfaces.items():  # generate for all ports of subunit signals in this context
            suPort._signalsForInterface(context, prefix + Interface.NAME_SEPARATOR + suPortName)
    #        suPort._connectToItsEntityPort()
    
    def _connectMyInterfaceToMyEntity(self, interface):
            if interface._subInterfaces:
                for _, subIntf in interface._subInterfaces.items():
                    self._connectMyInterfaceToMyEntity(subIntf)  
            else:
                portItem = single(self._entity.port, lambda x : x._interface == interface)
                interface._originSigLvlUnit = self._sigLvlUnit
                interface._originEntityPort = portItem
    
    def _synthesise(self, name=None):
        """
        synthesize all subunits, make connections between them, build entity and component for this unit
        """
        if not name:
            name = self.__class__.__name__
        self._name = name
        # construct globals (generics for entity)
        globalNames = {}
        for k, v in self._params.items():
            globalNames[k.lower()] = v 
        cntx = Context(name, globalNames=globalNames)
        externInterf = [] 
        # prepare subunits
        for subUnitName, subUnit in self._subUnits.items():
            yield from subUnit._synthesise(subUnitName)
            subUnit._signalsForMyEntity(cntx, "sig_" + subUnitName)
        
        # prepare connections     
        for connectionName, connection in self._interfaces.items():
            signals = connection._signalsForInterface(cntx, connectionName)
            if connection._isExtern:
                externInterf.extend(signals)
        
        for _, interface in self._interfaces.items():
            interface._propagateSrc()
        for subUnitName, subUnit in self._subUnits.items():
            for _, suIntf in subUnit._interfaces.items():
                suIntf._propagateConnection()

        # propagate connections on interfaces in this unit
        for _, connection in self._interfaces.items():
            connection._propagateConnection()
        
        if not externInterf:
            raise  Exception("Can not find any external interface for unit " + name \
                              + "- there is no such a thing as unit without interfaces")

        # synthetize signal level context
        s = cntx.synthetize(externInterf)
        self._entity = s[1]

        self._architecture = s[2]
            
        self._sigLvlUnit = VHDLUnit(self._entity)
        # connect results of synthetized context to interfaces of this unit
        for _, intf in self._interfaces.items():
            if intf._isExtern:
                self._connectMyInterfaceToMyEntity(intf)
        yield from s
            
        self._component = Component(self._entity)
        self._cleanAsSubunit() 
        for _ , intf in self._interfaces.items(): 
            # reverse because other components looks at this one from outside
            intf._reverseDirection()

class BlackBox(Unit):
    pass      

class UnitWithSource(Unit):
    @classmethod
    def _build(cls):
        assert(cls._origin)
        def setIntfAsExtern(intf):
            intf._isExtern = True
            for _, subIntf in intf._subInterfaces.items():
                setIntfAsExtern(subIntf)
        cls._interfaces = {}
        cls._subUnits = {}
        cls._params = {}
        baseDir = os.path.dirname(inspect.getfile(cls))
        cls._origin = os.path.join(baseDir, cls._origin)

        cls._entity = entityFromFile(cls._origin)
        for g in cls._entity.generics:
            g.defaultVal = Param(g.defaultVal)
            setattr(cls, g.name, g.defaultVal)
        cls._sigLvlUnit = VHDLUnit(cls._entity)

        for intfCls in cls._intfClasses:
            for intfName, interface in intfCls._tryToExtract(cls._sigLvlUnit):
                if hasattr(cls, intfName):
                    raise  Exception("Already has " + intfName)
                cls._interfaces[intfName] = interface
                setattr(cls, intfName, interface)
                setIntfAsExtern(interface)
        for p in cls._entity.port:
            assert(hasattr(p, '_interface') and p._interface)  # every port should have interface (Ap_none at least)        
        cls._clsBuildFor = cls
    
    def _synthesise(self, name=None):
        assert(self._entity)
        with open(self._origin) as f:
            return ['--%s' % (self._origin)]  # [f.read()]
            
