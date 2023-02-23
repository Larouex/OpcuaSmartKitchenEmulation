# ==================================================================================
#   File:   ring_frequency.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Loads the file used for ring frequency definition and returns json
#
#   (author) 2023 Larouex Software
#   GNU GENERAL PUBLIC LICENSE (see LICENSE.txt for details)
# ==================================================================================
import json, os

# config and maps
namespace = 'RingFrequency'
filename = 'config/ring-frequency.json'
alerts = 'alerts.json'

class RingFrequency():

    def __init__(self, Log):
        self.logger = Log
        self.load_file()

    def load_file(self):
        with open(filename) as config_file:
            self.data = json.load(config_file)
            alerts = self.load_alerts()
            self.logger.debug(alerts["Alerts"][namespace]["Loaded"].format(self.data))

    def update_file(self, data):
        with open(filename, 'w') as config_file:
            alerts = self.load_alerts()
            self.logger.debug(alerts["Alerts"][namespace]["Updated"].format(self.data))
            config_file.write(json.dumps(data, indent=2))

    def load_alerts(self):
        with open(alerts, 'r') as alerts_file:
            return json.load(alerts_file)