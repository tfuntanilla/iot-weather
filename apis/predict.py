"""Services for making the weather prediction"""

import pickle

import numpy as np
import pandas as pd
import tensorflow as tf


def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=400):
    """Input function for the DNNRegressor predictor"""
    return tf.estimator.inputs.pandas_input_fn(x=X,
                                               y=y,
                                               num_epochs=num_epochs,
                                               shuffle=shuffle,
                                               batch_size=batch_size)


def predict(model, data):
    """Loads prediction models and returns the prediction result"""
    X = pd.DataFrame(data, index=[0])
    print(X.info())

    if model == 'linear':
        regressor = pickle.load(open('./models/linear_regression_model.sav', 'rb'))
        prediction = regressor.predict(X)
        print("Prediction: {}".format(str(prediction[0])))
        return str(prediction[0])
    elif model == 'dnn':
        feature_cols = [tf.feature_column.numeric_column(col) for col in X.columns]
        regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                              hidden_units=[50, 50],
                                              model_dir='dnn_regression_model')
        predictions = regressor.predict(input_fn=wx_input_fn(X, num_epochs=1, shuffle=False))
        prediction = np.array([p['predictions'][0] for p in predictions])
        print("Prediction: {}".format(str(prediction[0])))
        return str(prediction[0])
    else:
        print("Invalid model.")
    return "Invalid model."
