#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""A node to gather data from a sensor, and publish it to an MQTT broker."""
# ---------------------------------------------------------------------------

import time
import logging
from logging.config import dictConfig

from mqtt_node_network.node import MQTTNode
from mqtt_node_network.initialize import initialize
from sensor_library.aht import SensorAHT20

logger = logging.getLogger(__name__)

config = initialize(config="config/config.toml", secrets=".env", logger="config/logger.yaml")

NODE_ID = config["mqtt"]["client"]["node_id"]
PUBLISH_TOPIC = f"{NODE_ID}/environment/bedroom"
PROMETHEUS_ENABLE = config["mqtt"]["node_network"]["enable_prometheus_server"]
PROMETHEUS_PORT = config["mqtt"]["node_network"]["prometheus_port"]
BROKER_CONFIG = config["mqtt"]["broker"]
PUBLISH_PERIOD = 10


def start_prometheus_server(port=8000):
    from prometheus_client import start_http_server

    start_http_server(port)


def gather_data():

    node = MQTTNode(broker_config=BROKER_CONFIG, node_id=NODE_ID).connect()

    sensor = SensorAHT20()

    while True:
        payload = sensor.measure()
        temperature = round(payload["temperature"], 3)
        humidity = round(payload["humidity"], 3)
        node.publish(
            topic=f"{PUBLISH_TOPIC}/temperature", payload=temperature
        )
        node.publish(topic=f"{PUBLISH_TOPIC}/humidity", payload=humidity)
        time.sleep(PUBLISH_PERIOD)


if __name__ == "__main__":
    if PROMETHEUS_ENABLE:
        start_prometheus_server(PROMETHEUS_PORT)
    gather_data()
