#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""A node to gather data from a sensor, and publish it to an MQTT broker."""
# ---------------------------------------------------------------------------


import json
import time
import random
import logging
from logging.config import dictConfig

from mqtt_node_network.node import MQTTNode
from mqtt_node_network.config import broker_config, logger_config, config
from sensor_library.dht import SensorDHT11

logger = logging.getLogger(__name__)

NODE_ID = "metrics_client_0"
PUBLISH_PERIOD = config["mqtt"]["node"]["publish_period"]
MEASUREMENT = config["mqtt"]["node"]["measurement_id"]
PUBLISH_ROOT_TOPIC = config["mqtt"]["node"]["publish_root_topic"]
PUBLISH_TOPIC = f"{NODE_ID}/{PUBLISH_ROOT_TOPIC}/{MEASUREMENT}"
PROMETHEUS_ENABLE = config["mqtt"]["node_network"]["enable_prometheus_server"]
PROMETHEUS_PORT = config["mqtt"]["node_network"]["prometheus_port"]
SENSOR_PIN = 18


def setup_logging(logger_config):
    from pathlib import Path

    Path.mkdir(Path("logs"), exist_ok=True)
    return dictConfig(logger_config)


def start_prometheus_server(port=8000):
    from prometheus_client import start_http_server

    start_http_server(port)


def gather_data():
    node = MQTTNode(broker_config=broker_config, node_id=NODE_ID).connect()

    sensor = SensorDHT11(pin=SENSOR_PIN)

    while True:
        data = {
            "measurement": MEASUREMENT,
            "fields": sensor.read(),
            "time": time.time(),
            "tags": {"node_id": node.node_id},
        }
        payload = json.dumps(data)
        node.publish(topic=PUBLISH_TOPIC, payload=payload)
        time.sleep(PUBLISH_PERIOD)


if __name__ == "__main__":
    setup_logging(logger_config)
    if PROMETHEUS_ENABLE:
        start_prometheus_server(PROMETHEUS_PORT)
    gather_data()
