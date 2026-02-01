import unittest
from datetime import datetime, timedelta

from spypointapi import Camera


class CameraTest(unittest.TestCase):

    def test_is_online_when_last_status_is_within_24_hours(self):
        camera = Camera(id="id", name="name", model="model",
                        modem_firmware="modem_firmware", camera_firmware="camera_firmware",
                        last_update_time=datetime.now().astimezone() - timedelta(hours=23, minutes=59, seconds=59),
                        signal=100, temperature=20, battery=200, memory=100)

        self.assertEqual(camera.is_online, True)

    def test_is_offline_when_last_status_is_past_24_hours(self):
        camera = Camera(id="id", name="name", model="model",
                        modem_firmware="modem_firmware", camera_firmware="camera_firmware",
                        last_update_time=datetime.now().astimezone() - timedelta(hours=24, minutes=0, seconds=1),
                        signal=100, temperature=20, battery=200, memory=100)

        self.assertEqual(camera.is_online, False)

    def test_is_offline_when_no_last_status(self):
        camera = Camera(id="id", name="name", model="model",
                        modem_firmware="modem_firmware", camera_firmware="camera_firmware",
                        last_update_time=None,
                        signal=100, temperature=20, battery=200, memory=100)

        self.assertEqual(camera.is_online, False)