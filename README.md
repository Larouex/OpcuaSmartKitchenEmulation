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
| **SiteName**      | Free text to indicate the Restaurant Name.                                             |
| **SitePrefix**    | This value is added as a prefex to enumerations indicated by the value of SiteCount.   |
| **SiteCount**     | How many iterations of this site should generated for emulation.                       |

The PlcList is defined as follows...

| Node              | Description                                                                            |
| ----------------- | -------------------------------------------------------------------------------------- |
| **PlcName**       | Free text to indicate the PLC Emulation Name. Used to indicate Hospitality Equipment.  |
| **PlcCount**      | How many iterations of this site should generated for emulation.                       |
| **PlcTagPrefix**  | This value is added as a prefex to enumerations indicated by the value of PlcCount.    |

The PlcName is also used to indicate the pattern of the file name of the PLC file. For example **hvac-system** indicates that there is a file named **hvac-system.json** in the /config folder.

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
#### hvac-system.json
This file is just one of the files used in the emulation for creating instances of the PLC device and telemetry variables.

| Node                      | Description                                                                    |
| ------------------------- | ------------------------------------------------------------------------------ |
| **Name**                  | Free text to indicate the PLC/Device Name.                                     |
| **InterfacelId**          | The DTDL Interface ID.                                                         |
| **InterfaceInstanceName** | DTDL IoTHub Interface Name.                                                    |

The **Variables** collection list define the telemetry value that is emulated by the OPCUA server and provide a subscriable value for clients to track...

| Node                      | Description                                                                    |
| ------------------------- | ------------------------------------------------------------------------------ |
| **DisplayName**           | Free text to describe the Variable/Telemetry Name.                             |
| **TelemetryName**         | Free text to indicate the Variable/Telememetry Name.                           |
| **DataType**              | Data type for processing the variable value emitted.                           |
| **Frequency**             | This value points to the frequency indicated in the **ring-frquency.json**     |
| **OnlyOnValueChange**     | Boolean that indicated to the OPCUA server if the value emitted gets a publish.|
| **_comment**              | Ignored, used for in file reading clarity.                                     |
| **RangeValues**           | N+1 values you can use to generate variable values.                            |

````json
{
  "_last-accessed": "2023-02-23 11:56:09.167898",
  "Name": "HVAC",
  "InterfacelId": "urn:larouexsmartkitchen:HVACInterface:1",
  "InterfaceInstanceName": "HVACInterface",
  "Variables": [
    {
      "DisplayName": "HVAC Airflow Temperature",
      "TelemetryName": "hvac_airflow_temperature",
      "DataType": "float",
      "Frequency": "TelemetryRingsInMinutes.Ring0",
      "OnlyOnValueChange": false,
      "_comment": "Measured in Fahrenheit and Reported by Minute.",
      "RangeValues": [72.45, 73.23, 73.9, 71.54, 72.28, 73.23]
    },
    {
      "DisplayName": "HVAC Airflow CFM",
      "TelemetryName": "hvac_cfm_airflow",
      "DataType": "integer",
      "Frequency": "TelemetryRingsInMinutes.Ring0",
      "OnlyOnValueChange": false,
      "_comment": "Measured in Cubic Feet per Minute(CPM) and Reported by Minute.",
      "RangeValues": [127, 121, 131, 130, 129]
    },
    {
      "DisplayName": "HVAC Main Motor RPM",
      "TelemetryName": "hvac_rpm_main_motor",
      "DataType": "integer",
      "Frequency": "TelemetryRingsInMinutes.Ring0",
      "OnlyOnValueChange": false,
      "_comment": "Measured in Revolutions by Minute(RPM) and Reported by Minute.",
      "RangeValues": [
        18000, 18500, 18200, 19000, 19200, 18000, 18500, 18200, 19000, 19200
      ]
    },
    {
      "DisplayName": "HVAC Mass Flow Rate",
      "TelemetryName": "hvac_mass_flow_rate",
      "DataType": "float",
      "Frequency": "TelemetryRingsInMinutes.Ring8",
      "OnlyOnValueChange": false,
      "_comment": "Measured in Kilograms by Hourly Mass Flow Rate.",
      "RangeValues": [3, 1, 3.2, 3.1, 4.13, 4.15, 4.12, 4.01, 5.3, 5.12]
    },
    {
      "DisplayName": "HVAC Volume Flow Rate",
      "TelemetryName": "hvac_volume_flow_rate",
      "DataType": "float",
      "Frequency": "TelemetryRingsInMinutes.Ring8",
      "OnlyOnValueChange": false,
      "_comment": "Measured in Litres by Hourly Volume Rate",
      "RangeValues": [
        1102.21, 1115.33, 1215.32, 1323.56, 1398.87, 1102.12, 1278.98, 1245.32,
        1100.45, 1189.11
      ]
    },
    {
      "DisplayName": "HVAC Power Inout to Drive",
      "TelemetryName": "hvac_power_input_to_drive",
      "DataType": "float",
      "Frequency": "TelemetryRingsInMinutes.Ring8",
      "OnlyOnValueChange": false,
      "_comment": "Measured in Kilowatts by Hourly Rate",
      "RangeValues": [
        1102, 1115, 1215, 1323, 1398, 1102, 1278, 1245, 1100, 1189
      ]
    },
    {
      "DisplayName": "HVAC Developed Pressure",
      "TelemetryName": "hvac_developed_pressure",
      "DataType": "float",
      "Frequency": "TelemetryRingsInMinutes.Ring8",
      "OnlyOnValueChange": false,
      "_comment": "Desired Developed Pressure of the System Measured kiloPascal units of Pressure by Hourly Rate.",
      "RangeValues": [
        101.325, 101.333, 101.121, 101.432, 101.65, 102.112, 102, 544, 101.547,
        101.54
      ]
    },
    {
      "DisplayName": "HVAC Static Pressure",
      "TelemetryName": "hvac_static_pressure",
      "DataType": "float",
      "Frequency": "TelemetryRingsInMinutes.Ring8",
      "OnlyOnValueChange": false,
      "_comment": "Actual Static Pressure of the System Measured kiloPascal units of Pressure by Hourly Rate.",
      "RangeValues": [
        101.325, 101.333, 101.121, 101.432, 101.65, 102.112, 102, 544, 101.547,
        101.54
      ]
    }
  ]
}
````
In this repository project, we have the following PC files...

* kitchen-fryer
* standing-freezer
* walkin-freezer
* walkin-fridge
* kitchen-fryer
* hvac-system

## Test and Validate the Configuration
The file **test-validate.py** is a Python app that tests the configuration files.

````bash
cd server
python .\test-validate.py -v
````
Running this file will result in demonstrating that we can generate 50310 variables for emmitting telemetry...
````bash
...
INFO: [TEST-VALIDATE] PLC Name: KitchenFryer
INFO: [TEST-VALIDATE] PLC Variable Count: 3
INFO: [TEST-VALIDATE] PLC All Variable Count: 50015
INFO: [TEST-VALIDATE] PLC File Name: standing-fridge PLC Count: 29 Plc Tag Prefix: Shuckers-
INFO: [TEST-VALIDATE] Loading PLC Defintiion File (config/standing-fridge.json)
INFO: [TEST-VALIDATE] PLC Name: StandingFridge
INFO: [TEST-VALIDATE] PLC Variable Count: 5
INFO: [TEST-VALIDATE] PLC All Variable Count: 50160
INFO: [TEST-VALIDATE] PLC File Name: walkin-fridge PLC Count: 18 Plc Tag Prefix: Shuckers-
INFO: [TEST-VALIDATE] Loading PLC Defintiion File (config/walkin-fridge.json)
INFO: [TEST-VALIDATE] PLC Name: WalkinFridge
INFO: [TEST-VALIDATE] PLC Variable Count: 5
INFO: [TEST-VALIDATE] PLC All Variable Count: 50250
INFO: [TEST-VALIDATE] PLC File Name: standing-freezer PLC Count: 12 Plc Tag Prefix: Shuckers-
INFO: [TEST-VALIDATE] Loading PLC Defintiion File (config/standing-freezer.json)
INFO: [TEST-VALIDATE] PLC Name: StandingFreezer
INFO: [TEST-VALIDATE] PLC Variable Count: 5
INFO: [TEST-VALIDATE] PLC All Variable Count: 50310
````
