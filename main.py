from configparser import ConfigParser
from core import config
from core import zm_ftp_lib
import json
import logging
import paho.mqtt.client as mqtt

CONFIG = config.load_config("core/config.ini")
FTP = zm_ftp_lib.ZM_FTP(CONFIG)

MQTT_BROKER = CONFIG["MQTT"]["MQTT_BROKER"]
MQTT_USER = CONFIG["MQTT"]["MQTT_USER"]
MQTT_PASSWD = CONFIG["MQTT"]["MQTT_PASSWD"]
MQTT_TOPIC = CONFIG["MQTT"]["TOPIC"]


def check_recipe_format(recipe):
    return True


def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    logging.info(msg.topic+" "+str(msg.payload))

    # parse message
    try:
        recipe = json.loads(msg)
        if check_recipe_format(recipe) is False:
            raise ValueError("Recipe check failed")

        FTP.write_recipe(msg)

    except Exception as e:
        logging.warning(f"Recipe load error {e}")
        return


if __name__ == "__main__":
    # logging init

    # mqtt init
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.username_pw_set(MQTT_USER, MQTT_PASSWD)
    mqttc.connect(MQTT_BROKER, 1883, 60)

    mqttc.loop_forever()
    FTP.quit()
