import numpy as np

def make_prediction(model, input_data):
    return model.predict(np.array([input_data]))