from tensorflow.keras.optimizations import quantize_model

model = build_lstm_model()  # Your original model
quantized_model = quantize_model(model, optimization='lite')
