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
from mqtt_node_network.configure import broker_config, logger_config, config
from sensor_library.aht import SensorAHT20

logger = logging.getLogger(__name__)

NODE_ID = config["mqtt"]["node"]["node_id"]
PUBLISH_PERIOD = config["mqtt"]["node"]["publish_period"]
PUBLISH_TOPIC = config["mqtt"]["node"]["publish_topic"]
PROMETHEUS_ENABLE = config["mqtt"]["node_network"]["enable_prometheus_server"]
PROMETHEUS_PORT = config["mqtt"]["node_network"]["prometheus_port"]


def setup_logging(logger_config):
    from pathlib import Path

    Path.mkdir(Path("logs"), exist_ok=True)
    return dictConfig(logger_config)


def start_prometheus_server(port=8000):
    from prometheus_client import start_http_server

    start_http_server(port)


def gather_data():
    node = MQTTNode(broker_config=broker_config, node_id=NODE_ID).connect()

    sensor = SensorAHT20()

    while True:
        payload = sensor.measure()
        node.publish(
            topic=f"{PUBLISH_TOPIC}/temperature", payload=payload["temperature"]
        )
        node.publish(topic=f"{PUBLISH_TOPIC}/humidity", payload=payload["humidity"])
        time.sleep(PUBLISH_PERIOD)


if __name__ == "__main__":
    setup_logging(logger_config)
    if PROMETHEUS_ENABLE:
        start_prometheus_server(PROMETHEUS_PORT)
    gather_data()
