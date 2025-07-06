# In main.py
import gc

def clean_memory():
    gc.collect()
    if psutil.virtual_memory().percent > 80:
        logger.warning("High memory usage - clearing cache")
        tf.keras.backend.clear_session()
