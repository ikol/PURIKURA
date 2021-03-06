from pyrikura.plugin import Plugin
from pyrikura.broker import Broker
import piggyphoto
import time



class CTetherBroker(Broker):
    def __init__(self, name='capture.jpg', test=False):
        super(CTetherBroker, self).__init__()
        self._name = name
        self._test = test
        self.reset()

    def process(self, msg, sender=None):
        try:
            if not self._test:
                self.camera.capture_image(self._name)
        except piggyphoto.libgphoto2error:
            self.reset()
            self.camera.capture_image(self._name)

        self.publish([self._name])

    def reset(self):
        if not self._test:
            self.camera = piggyphoto.camera()
            self.camera.leave_locked()
            time.sleep(.5)

class CTether(Plugin):
    _decendant = CTetherBroker
