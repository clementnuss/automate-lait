import logging, time
import tfluna
from prometheus_client import Gauge

def read_tfluna(lidar_distance: Gauge, lidar_strength: Gauge, config: map):

    ref_height_tag = "reference_height"
    ref_height = 0
    
    if not ref_height_tag in config:
        logging.warn("Reference height for the LiDAR not set, logging the raw measurement")
    else:
        ref_height = float(config[ref_height_tag])

    logging.info(f"Reference height is {ref_height} [cm]")
    try:
        with tfluna.TfLuna() as tfl:
            tfl.set_samp_rate(5)
            logging.info("correctly opened the tfluna driver")
            while True:
                distance,strength,_ = tfl.read_tfluna_data()
                lidar_distance.set(ref_height-100*distance)
                lidar_strength.set(strength)
                time.sleep(1)
    except:
        logging.error("TF-Luna error (probably timeout), exiting")
