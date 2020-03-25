from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase, UnitBase
from hwt.hdl.statements import HdlStatement


class HObjList(list):
    """
    Regular list with some interface/unit methods delegated on items.

    Main purpose of this class it let :class:`hwt.synthesizer.PropDeclrCollector.PropDeclrCollector`
    know that this is not an regular python array and that items should be registered as HW objects.

    :note: :class:`hwt.synthesizer.PropDeclrCollector.PropDeclrCollector` is used by
        :class:`hwt.synthesizer.interface.Interface` and :class:`hwt.synthesizer.unit.Unit`
    """

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self._name = None
        self._parent = None

    def _m(self):
        for item in self:
            item._m()
        return self

    def _getFullName(self, separator_getter=lambda x: "."):
        """get all name hierarchy separated by '.' """
        name = ""
        tmp = self
        while isinstance(tmp, (InterfaceBase, HObjList)):
            if hasattr(tmp, "_name"):
                n = tmp._name
            else:
                n = ''
            if name == '':
                name = n
            else:
                name = n + separator_getter(tmp) + name
            if hasattr(tmp, "_parent"):
                tmp = tmp._parent
            else:
                tmp = None
        return name

    def _make_association(self, *args, **kwargs):
        """
        Delegate _make_association on items

        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._make_association`
        """
        for o in self:
            o._make_association(*args, **kwargs)

    def _updateParamsFrom(self, *args, **kwargs):
        """
        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._updateParamsFrom`
        """
        for o in self:
            if isinstance(o, (InterfaceBase, UnitBase, HObjList)):
                o._updateParamsFrom(*args, **kwargs)

    def __call__(self, other):
        if not isinstance(other, list):
            raise TypeError(other)
        if len(self) != len(other):
            raise ValueError("Different number of interfaces in list",
                             len(self), len(other))

        statements = []
        for a, b in zip(self, other):
            stms = a(b)
            if isinstance(stms, HdlStatement):
                statements.append(stms)
            else:
                statements += stms

        return statements
