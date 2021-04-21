from prometheus_client import Gauge, Counter, generate_latest, start_http_server, REGISTRY
import logging
import threading, time

from sensors import lidar, temperature

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # unregister the default collectors. source: https://github.com/prometheus/client_python/issues/414
    for coll in list(REGISTRY._collector_to_names.keys()):
        REGISTRY.unregister(coll)
    
    lidar_distance = Gauge(name='lidar_distance', documentation='The distance (m) between the LiDAR (sensor) and the floor.')
    lidar_strength = Gauge(name='lidar_strength', documentation='The strength of the measurement taken by the LiDAR')
    pipe_temperature = Gauge(name='pipe_temperature', documentation='Temperature measured directly on the milk pipe')

    tfluna_thread = threading.Thread(
        target=lidar.read_tfluna,
        args= (lidar_distance, lidar_strength))
    logging.info(f"starting the TF-Luna thread.")
    tfluna_thread.start()

    temp_thread = threading.Thread(
        target=temperature.read_temperature,
        args= (pipe_temperature,))
    logging.info(f"starting the temperature reading thread.")
    temp_thread.start()

    start_http_server(port=8014)