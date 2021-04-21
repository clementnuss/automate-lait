import logging, time
import tfluna
from prometheus_client import Gauge

def read_tfluna(lidar_distance: Gauge, lidar_strength: Gauge):
    try:
        with tfluna.TfLuna() as tfl:
            tfl.set_samp_rate(5)
            logging.info("correctly opened the tfluna driver")
            while True:
                distance,strength,_ = tfl.read_tfluna_data()
                lidar_distance.set(109-100*distance)
                lidar_strength.set(strength)
                time.sleep(1)
    except:
        logging.error("TF-Luna error (probably timeout), exiting")
