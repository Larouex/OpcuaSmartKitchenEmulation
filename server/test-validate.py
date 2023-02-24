#/usr/bin/env python3.8
# ==================================================================================
#   File:   test-vaidate.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Test to validate the correct files and configuration is ready
#
#   (author) 2023 Larouex Software
#   GNU GENERAL PUBLIC LICENSE (see LICENSE.txt for details)
# ==================================================================================
import  getopt, sys, time, string, threading, asyncio, os
import logging as Log
from datetime import datetime

# our classes
from classes.file_handlers.site_topology import SiteTopology
from classes.file_handlers.ring_frequency import RingFrequency
from classes.file_handlers.plc_item import PlcItem

# Workers
config_data = None
logger_namespace = "[TEST-VALIDATE]"

# -------------------------------------------------------------------------------
#   Function:   load_site_topology
#   Usage:      Loads the configuration from file
# -------------------------------------------------------------------------------
def load_site_topology():

  site_topology = SiteTopology(Log)
  return site_topology.data

# -------------------------------------------------------------------------------
#   Function:   update_site_topology
#   Usage:      Loads the configuration from file
# -------------------------------------------------------------------------------
def update_site_topology(config_data):

  site_topology = SiteTopology(Log)
  update_datetime = datetime.now()
  config_data["_last-accessed"] = str(update_datetime)
  site_topology.update_file(config_data)
  return

# -------------------------------------------------------------------------------
#   Function:   load_ring_frequency
#   Usage:      Loads the configuration from file
# -------------------------------------------------------------------------------
def load_ring_frequency():

  ring_frequency = RingFrequency(Log)
  return ring_frequency.data

# -------------------------------------------------------------------------------
#   Function:   update_site_topology
#   Usage:      Loads the configuration from file
# -------------------------------------------------------------------------------
def update_ring_frequency(config_data):

  ring_frequency = RingFrequency(Log)
  update_datetime = datetime.now()
  config_data["_last-accessed"] = str(update_datetime)
  ring_frequency.update_file(config_data)
  return

# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

  # parameters
  whatif = False

  # execution state from args
  short_options = "hvdw"
  long_options = ["help", "verbose", "debug", "whatif"]
  full_cmd_arguments = sys.argv
  argument_list = full_cmd_arguments[1:]
  try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
  except getopt.error as err:
    print (str(err))

  for current_argument, current_value in arguments:

    if current_argument in ("-h", "--help"):
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("HELP for test-validate.py")
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("")
      print("  BASIC PARAMETERS...")
      print("")
      print("  -h or --help - Print out this Help Information")
      print("  -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging")
      print("  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging")
      print("  -w or --whatif - Combine with Verbose it will Output the Configuration")
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      return
      
    if current_argument in ("-v", "--verbose"):
      Log.basicConfig(format="%(levelname)s: %(message)s", level = Log.INFO)
      Log.info("Verbose Logging Mode...")
    else:
      Log.basicConfig(format="%(levelname)s: %(message)s")

    if current_argument in ("-d", "--debug"):
      Log.basicConfig(format="%(levelname)s: %(message)s", level = Log.DEBUG)
      Log.info("Debug Logging Mode...")
    else:
      Log.basicConfig(format="%(levelname)s: %(message)s")

    if current_argument in ("-w", "--whatif"):
      whatif = True
      Log.info("WhatIf Mode...")

  # validate the site topology
  Log.info(logger_namespace + " Loading %s" % "Site Topology File (site-topology.json)")
  config_data = load_site_topology()
  Log.info(logger_namespace + " Updating %s" % "Site Topology File (site-topology.json)")
  update_site_topology(config_data)

  # validate the ring frquency
  Log.info(logger_namespace + " Loading %s" % "Ring Frequency File (ring-frequency.json)")
  config_data = load_ring_frequency()
  Log.info(logger_namespace + " Updating %s" % "Ring Frequency  File (ring-frequency.json)")
  update_ring_frequency(config_data)

  # now load the plc/assets referenced in the site topology file...
  plc_item_data_count_all = 0
  Log.info(logger_namespace + " Loading %s" % "Site Topology File (site-topology.json)")
  config_data = load_site_topology()
  Log.info(logger_namespace + " Enumerating Sites and PLC's")
  for site in config_data["Sites"]:
    site_name = site["SiteName"]
    site_prefix = site["SitePrefix"]
    site_count = site["SiteCount"]
    Log.info(logger_namespace + " Site Name: %s Site Prefix: %s Site Count: %i" % (site_name, site_prefix, site_count))
    for x in range(0, site_count):
      for plc_list in site["PlcList"]:
        plc_name = plc_list["PlcName"]
        plc_count = plc_list["PlcCount"] 
        plc_prefix = plc_list["PlcTagPrefix"] 
        plc_filename = "config/" + plc_name + ".json"
        Log.info(logger_namespace + " PLC File Name: %s PLC Count: %i Plc Tag Prefix: %s" % (plc_name, plc_count, plc_prefix))
        Log.info(logger_namespace + " Loading %s" % "PLC Defintiion File (" + plc_filename + ")")
        plc_item = PlcItem(Log, plc_filename, plc_name)
        plc_item_data =  plc_item.data
        Log.info(logger_namespace + " PLC Name: %s" % plc_item_data["Name"])
        plc_item_data_count = len(plc_item_data["Variables"])
        Log.info(logger_namespace + " PLC Variable Count: %s" % plc_item_data_count)
        plc_item_data_count_all += (plc_item_data_count * plc_count)
        Log.info(logger_namespace + " PLC All Variable Count: %s" % plc_item_data_count_all)
      




if __name__ == "__main__":
  asyncio.run(main(sys.argv[1:]))