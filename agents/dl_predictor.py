import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizations import quantize_model
import numpy as np
import gc

class DeepLearningPredictor:
    def __init__(self):
        self.model = None
        self.build_model()
        
    def build_model(self):
        """Memory-efficient LSTM model"""
        model = Sequential([
            LSTM(64, return_sequences=True, input_shape=(30, 4)),
            Dropout(0.2),
            LSTM(32),
            Dropout(0.2),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(optimizer='adam', 
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
        
        # Quantize model for efficiency
        self.model = quantize_model(model, optimization='lite')
        gc.collect()
    
    def predict(self, data):
        """Make prediction with memory cleanup"""
        try:
            data = np.array(data, dtype=np.float32)
            prediction = self.model.predict(data.reshape(1, 30, 4))[0][0]
            return float(prediction)
        except Exception as e:
            print(f"Prediction error: {e}")
            return 0.5
        finally:
            tf.keras.backend.clear_session()
            gc.collect()
