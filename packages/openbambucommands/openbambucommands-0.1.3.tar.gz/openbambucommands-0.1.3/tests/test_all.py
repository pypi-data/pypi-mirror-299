import unittest
from openbambucommands import ftp_hello_world, mqtt_hello_world


class TestOpenBambuCommands(unittest.TestCase):
    def test_ftp_hello_world(self):
        self.assertIsInstance(ftp_hello_world(), str)
        self.assertIn("Hello World from openbambucommands.ftp.hello!", ftp_hello_world())

    def test_mqtt_hello_world(self):
        self.assertIsInstance(mqtt_hello_world(), str)
        self.assertIn("Hello World from openbambucommands.mqtt.hello!", mqtt_hello_world())


if __name__ == '__main__':
    unittest.main()
