import logging, time
from prometheus_client import Gauge

from w1thermsensor import W1ThermSensor, Unit, SensorNotReadyError

def read_temperature(pipe_temperature: Gauge, running):
    sensor = W1ThermSensor()
    if not sensor.exists():
        logging.error("Could not open the temperature sensor (W1 sensor not found)."
            "exiting in a minute")
        time.sleep(6)
        raise Exception("W1 sensor not found")
    
    logging.info("Correctly opened the temperature sensor")
    while running.get():
        try:
            temperature_in_celsius = sensor.get_temperature()
            pipe_temperature.set(temperature_in_celsius)
            time.sleep(5)
        except SensorNotReadyError:
            logging.info("sensor not ready")
            pass