

from logging.config import dictConfig
import logging
import os
from dotenv import load_dotenv
import Adafruit_DHT

from data_node_network.data_gatherer import GathererNodeTCP
from data_node_network.sensor import Sensor, SensorNode

load_dotenv()
HOSTNAME = os.getenv('HOSTNAME')
PORT = int(os.getenv('PORT'))
    

def setup_logging(filepath="config/logger.yaml"):
    import yaml
    from pathlib import Path

    if Path(filepath).exists():
        with open(filepath, "r") as stream:
            config = yaml.load(stream, Loader=yaml.FullLoader)
    else:
        raise FileNotFoundError
    logger = dictConfig(config)
    return logger

logger = setup_logging()

class SensorDHT11(Sensor):
    def __init__(self, pin, name:str = "DHT11"):
        self.name = name
        self.sensor = Adafruit_DHT.DHT11
        self.pin = pin
        
    def read(self):
        humidity, temperature = Adafruit_DHT.read(self.sensor, self.pin)
        if humidity is not None and temperature is not None:
            logging.info("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        else:
            logging.error("Sensor failure. Check wiring.")
            return None
        return dict(humidity=humidity, temperature=temperature)
        

def main():
    dht11 = SensorDHT11(pin=18)
    # Create and start the server
    node_server = SensorNode(host=HOSTNAME, port=PORT, sensors=[dht11])
    print(node_server.gather_data())
    # node_server.start()

if __name__ == "__main__":
    
    main()
