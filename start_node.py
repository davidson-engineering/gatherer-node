#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""a_short_project_description"""
# ---------------------------------------------------------------------------


import logging
from logging.config import dictConfig

from mqtt_node_network.metrics_gatherer import MQTTMetricsGatherer
from mqtt_node_network.configuration import broker_config, logger_config, config
from fast_database_clients import FastInfluxDBClient

logger = logging.getLogger(__name__)

NODE_ID = config["mqtt"]["node"]["node_id"]
SUBSCRIBE_TOPIC = config["mqtt"]["node"]["subscribe_topic"]
PROMETHEUS_ENABLE = config["mqtt"]["node_network"]["enable_prometheus_server"]
PROMETHEUS_PORT = config["mqtt"]["node_network"]["prometheus_port"]
DATABASE_CONFIG = config["influxdb"]["config_filepath"]


def setup_logging(logger_config):
    from pathlib import Path

    Path.mkdir(Path("logs"), exist_ok=True)
    return dictConfig(logger_config)


def start_prometheus_server(port=8000):
    from prometheus_client import start_http_server

    start_http_server(port)


def subscribe_forever(topic="+/metric", qos=0):
    database_client = FastInfluxDBClient.from_config_file(config_file=DATABASE_CONFIG)
    database_client.start()

    client = MQTTMetricsGatherer(
        broker_config=broker_config, node_id=NODE_ID, buffer=database_client.buffer
    ).connect()
    client.subscribe(topic, qos)
    client.loop_forever()


if __name__ == "__main__":
    setup_logging(logger_config)
    if PROMETHEUS_ENABLE:
        start_prometheus_server(PROMETHEUS_PORT)
    subscribe_forever()
