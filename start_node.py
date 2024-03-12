#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""a_short_project_description"""
# ---------------------------------------------------------------------------


import json
import time
import random
import logging
from logging.config import dictConfig

from mqtt_node_network.node import MQTTNode
from mqtt_node_network.metrics_gatherer import MQTTMetricsGatherer
from mqtt_node_network.configuration import broker_config, logger_config, config
from fast_database_clients import FastInfluxDBClient

logger = logging.getLogger(__name__)
NODE_ID = "metrics_client_0"
PROMETHEUS_ENABLE = config["mqtt"]["node_network"]["enable_prometheus_server"]
PROMETHEUS_PORT = config["mqtt"]["node_network"]["prometheus_port"]

def setup_logging(logger_config):
    from pathlib import Path

    Path.mkdir(Path("logs"), exist_ok=True)
    return dictConfig(logger_config)


def start_prometheus_server(port=8000):
    from prometheus_client import start_http_server

    start_http_server(port)
    
def publish_forever():
    client = MQTTNode(broker_config=broker_config, node_id=NODE_ID).connect()
    
    data = random.random()
    
    while True:
        data = {
            "measurement": "measurement",
            "fields": {"data": data},
            "time": time.time(),
            "tags": {"node_id": client.node_id},
        }
        payload = json.dumps(data)
        client.publish(topic=f"{client.node_id}/metric", payload=payload)
        time.sleep(0)


def gather_forever(topic="+/metric", qos=0):
    config_file = "config/.influx_live.toml"
    database_client = FastInfluxDBClient.from_config_file(config_file=config_file)
    database_client.start()

    client = MQTTMetricsGatherer(
        broker_config=broker_config, node_id=NODE_ID, buffer=database_client.buffer
    ).connect()
    client.subscribe(topic, qos)˜
    client.loop_forever()


if __name__ == "__main__":
    setup_logging(logger_config)
    if PROMETHEUS_ENABLE:
        start_prometheus_server(PROMETHEUS_PORT)
    gather_forever()
    # publish_forever()