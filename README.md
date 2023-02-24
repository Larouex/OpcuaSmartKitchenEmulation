[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;[![Python 3.0](https://img.shields.io/badge/Python-3.0-blue.svg)](https://www.python.org/)&nbsp;[![OPCUA](https://img.shields.io/badge/OPCUA-Server-orange.svg)](https://opcfoundation.org/about/opc-technologies/opc-ua/)


# Smart Kitchen Dynamic OPC-UA Emulation
Demonstrates the use of OPC-UA to Monitor the Equipment in a Smart Commercial Kitchen with Telemetry and Integration.

This project is targeted at system integrators, developers and administrators of an OPC-UA system. This project is for learning purposes and supports the OPC-UA emulation, modeling and Azure IoT concepts that will help you gain deeper knowledge of this scenario.

<b>IMPORTANT:</b> If you are pursuant of a production or commercial implementation of Industrial IoT with Azure you should start here {{{TDB}}}

## Overview
This demonstration is a reference implementation of the following...

* <b>OPC-UA Server</b> - Based on the popular FreeOPcUa project for Python.
* <b>Powerful Emulation</b> - Dynamic Configuration of OPC-UA Server, Nodes and Variables allow you to emulate topologies. In this project it is an instance of a Smart Commercial Kitchen.

## Who is Audience for this Project?
* System Integrators
* Developers
* Administrators of an OPC-UA System

## Configuration Overview
The overall goal of the emulation project is to use a series of related configuration files that support declarative definition of the telemetry from the OPCUA server. This approach makes it trivial to generate a large number of PLC emulations with fine grained control over the telemtry emiting frequency for subscribing clients.

### The Files and Relationships

<img src="./assets/config-files-relationship.png" width="750"/>


#### ring-frquency.json
The Ring Frequency file is used to define a set of telemtry frequencies that represent seconds and minutes. These definitions can then be assigned to telemetry variable that is being emulated and will publish based on the value. You can define these values and number of them anyway that meets your needs.

````json
{
  "_last-accessed": "2023-02-24 10:47:49.732424",
  "TelemetryRingsInSeconds": [
    "Frequency",
    {"Ring0": 1}, {"Ring1": 5}, {"Ring2": 10}, {"Ring3": 15}, {"Ring4": 20}, {"Ring5": 30}, {"Ring6": 40}, {"Ring7": 50}
  ],
  "TelemetryRingsInMinutes": [
    "Frequency",
    {"Ring0": 1}, {"Ring1": 5}, {"Ring2": 10}, {"Ring3": 15}, {"Ring4": 20}, {"Ring5": 30}, {"Ring6": 40}, {"Ring7": 50}
  ]
}
````

#### site-topology.json
The Site Topology file is used to link and create PLC kitchen components from the PLC definition files. The Sites node indicates a collection of sites that includes...

| Node              | Description                                                                            |
| ----------------- | -------------------------------------------------------------------------------------- |
| **SiteName**      | Free text to indicate the Resturant Name.                                              |
| **SitePrefix**    | This value is added as a prefex to enumerations indicated by the value of SiteCount.   |
| **SiteCount**     | How many iterations of this site should generated for emulation.                       |

The PlcList is defined as follows...

| Node              | Description                                                                            |
| ----------------- | -------------------------------------------------------------------------------------- |
| **PlcName**       | Free text to indicate the PLC Emulation Name. Used to indicate Hospitality Equipment   |
| **PlcCount**      | How many iterations of this site should generated for emulation.                       |
| **PlcTagPrefix**  | This value is added as a prefex to enumerations indicated by the value of PlcCount.    |


````json
{
  "_last-accessed": "2023-02-24 10:47:49.720507",
  "Sites": [
    {
      "SiteName": "Burien",
      "SitePrefix": "Burien-Shuckers-",
      "SiteCount": 130,
      "PlcList": [
        {
          "PlcName": "hvac-system",
          "PlcCount": 1,
          "PlcTagPrefix": "Shuckers-"
        },
        {
          "PlcName": "walkin-freezer",
          "PlcCount": 4,
          "PlcTagPrefix": "Shuckers-"
        },
        {
          "PlcName": "kitchen-fryer",
          "PlcCount": 16,
          "PlcTagPrefix": "Shuckers-"
        },
        {
          "PlcName": "standing-fridge",
          "PlcCount": 29,
          "PlcTagPrefix": "Shuckers-"
        },
        {
          "PlcName": "walkin-fridge",
          "PlcCount": 18,
          "PlcTagPrefix": "Shuckers-"
        },
        {
          "PlcName": "standing-freezer",
          "PlcCount": 12,
          "PlcTagPrefix": "Shuckers-"
        }
      ]
    }
  ]
}
````