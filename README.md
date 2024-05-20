# MQTT-FTP-Bridge

MQTT-FTP-Bridge is a tool that receives MQTT messages and writes them as files to a specified FTP server.

## Installation

1. Clone this repository and install the required dependencies:
    ```bash
    git clone https://github.com/boy07132004/MQTT-FTP-Bridge.git
    cd MQTT-FTP-Bridge
    
    pip install -r requirements.txt
    ```

## Usage

1. Configure the `core/config.ini` file:

    First, copy the `core/config.template` to `core/config.ini`:
    ```bash
    cp core/config.template core/config.ini
    ```
    Then fill config settings in config.ini

2. Run the script:

    ```bash
    python main.py
    ```

    This will take the JSON messages from the specified topic and write them as files to the specified FTP folder.

## Branches

- `main` branch: Suitable for most modern environments.
- `for_winxp` branch: Provides support for Windows XP 32-bit and Python 3.4.4 environments.

    Switch to the `for_winxp` branch:
    ```bash
    git checkout for_winxp
    ```

## Configuration

- **MQTT Settings**
  - `MQTT_BROKER`: IP address of the MQTT broker
  - `MQTT_USER`: Username for the MQTT broker
  - `MQTT_PASSWD`: Password for the MQTT broker
  - `TOPIC`: MQTT topic to subscribe to

- **FTP Settings**
  - `FTP_SERVER`: IP address of the FTP server
  - `FTP_USER`: Username for the FTP server
  - `FTP_PASSWD`: Password for the FTP server
  - `FOLDER_PATH`: Directory path to upload the files to
