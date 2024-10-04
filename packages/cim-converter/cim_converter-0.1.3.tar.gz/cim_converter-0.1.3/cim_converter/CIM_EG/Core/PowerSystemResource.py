from cim_converter.CIM_EG.Core.IdentifiedObject import IdentifiedObject


class PowerSystemResource(IdentifiedObject):

    def __init__(self,
                 *args,
                 Location=None,
                 Measurements=None,
                 **kw_args):
        """Initialises a new 'PowerSystemResource' instance.

        @param Location: 
        """

        self._Location = None
        self.Location = Location

        self._Measurements = []
        self.Measurements = [] if Measurements is None else Measurements

        super(PowerSystemResource, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ['Location', 'Measurements']
    _many_refs = ['Measurements']


    def getLocation(self):
        """Location of this power system resource.
        """
        return self._Location

    def setLocation(self, value):
        if self._Location is not None:
            filtered = [
                x for x in self.Location.PowerSystemResources if x != self
            ]
            self._Location._PowerSystemResources = filtered

        self._Location = value
        if self._Location is not None:
            if self not in self._Location._PowerSystemResources:
                self._Location._PowerSystemResources.append(self)

    Location = property(getLocation, setLocation)

    def getMeasurements(self):
        """The Measurements that are included in the naming hierarchy where the PSR is the containing object
        """
        return self._Measurements

    def setMeasurements(self, value):
        for x in self._Measurements:
            x.PowerSystemResource = None
        for y in value:
            y._PowerSystemResource = self
        self._Measurements = value

    Measurements = property(getMeasurements, setMeasurements)

    def addMeasurements(self, *Measurements):
        for obj in Measurements:
            obj.PowerSystemResource = self

    def removeMeasurements(self, *Measurements):
        for obj in Measurements:
            obj.PowerSystemResource = None