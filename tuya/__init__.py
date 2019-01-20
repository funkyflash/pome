import pytuya

class TuyaDevice:
    def __init__(self, device_id, ip_address, local_key):
        self.thing = pytuya.OutletDevice(device_id, ip_address, local_key)

    def off(self):
        self.thing.set_status(False)

    def on(self):
        self.thing.set_status(True)

    def state(self):
        return self.thing.status()['dps']['1']