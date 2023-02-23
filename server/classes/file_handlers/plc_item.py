# ==================================================================================
#   File:   plc_item.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Loads the file used for plc item definition and returns json
#
#   (author) 2023 Larouex Software
#   GNU GENERAL PUBLIC LICENSE (see LICENSE.txt for details)
# ==================================================================================
import json, os

# config and maps
alerts = 'alerts.json'

class PlcItem():

    def __init__(self, Log, FileName, NameSpace):
        self.logger = Log
        self.filename = FileName
        self.namespace = NameSpace
        self.load_file()

    def load_file(self):
        with open(self.filename) as config_file:
            self.data = json.load(config_file)
            alerts = self.load_alerts()
            self.logger.debug(alerts["Alerts"][self.namespace]["Loaded"].format(self.data))

    def update_file(self, data):
        with open(self.filename, 'w') as configs_file:
            alerts = self.load_alerts()
            self.logger.debug(alerts["Alerts"][self.namespace]["Updated"].format(self.data))
            configs_file.write(json.dumps(data, indent=2))

    def load_alerts(self):
        with open(alerts, 'r') as alerts_file:
            return json.load(alerts_file)