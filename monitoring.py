from prometheus_client import Gauge, Counter, generate_latest, start_http_server, REGISTRY
import logging
import threading, time

from sensors import lidar, temperature
from util import AtomicBool
import yaml

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    running = AtomicBool(True)

    # unregister the default collectors. source: https://github.com/prometheus/client_python/issues/414
    for coll in list(REGISTRY._collector_to_names.keys()):
        REGISTRY.unregister(coll)
    
    lidar_distance = Gauge(name='lidar_distance', documentation='The distance (m) between the LiDAR (sensor) and the floor.')
    lidar_strength = Gauge(name='lidar_strength', documentation='The strength of the measurement taken by the LiDAR')
    pipe_temperature = Gauge(name='pipe_temperature', documentation='Temperature measured directly on the milk pipe')

    config = {}
    try: 
        with open(r"config.yaml") as file:
            config = yaml.load(file)
        logging.debug(f"Correctly imported the config: {config}")
    except Exception as e:
        logging.error(f"Could not import the configuration file ! Error message:\n{e}")
        exit(-1)
    
    threads = []
    tfluna_thread = threading.Thread(
        name="TF-Luna thread",
        target=lidar.read_tfluna,
        args= (lidar_distance, lidar_strength, config['lidar'], running))
    logging.info(f"starting the TF-Luna thread.")
    threads.append(tfluna_thread)

    temp_thread = threading.Thread(
        name="Temperature thread",
        target=temperature.read_temperature,
        args= (pipe_temperature,running))
    logging.info(f"starting the temperature reading thread.")
    threads.append(temp_thread)

    start_http_server(port=8014)

    for t in threads:
        t.start()

    while running.get():
        time.sleep(5)
        for t in threads:
            if not t.is_alive():
                logging.fatal(f"One of the threads is dead, exiting the app. thread info: {t}")
                running.set(False)
                break
    
    