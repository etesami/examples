from __future__ import print_function
import sys
import tensorflow as tf
import numpy as np
import yaml
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from data.read_data import read_data
import os


def train(model,data,settings):
    print("-- RUNNING TRAINING --", flush=True)

    (x_train, y_train) = read_data(data, trainset=True)

    model.fit(x_train, y_train, batch_size=settings['batch_size'], epochs=settings['epochs'], verbose=1)

    print("-- TRAINING COMPLETED --", flush=True)
    return model

if __name__ == '__main__':

    with open('settings.yaml', 'r') as fh:
        try:
            settings = dict(yaml.safe_load(fh))
        except yaml.YAMLError as e:
            raise(e)

    from fedn.utils.kerashelper import KerasHelper
    helper = KerasHelper()
    weights = helper.load_model(sys.argv[1])

    from models.mnist_model import create_seed_model
    model = create_seed_model()
    model.set_weights(weights)

    model = train(model,'../data/mnist.npz',settings)
    helper.save_model(model.get_weights(),sys.argv[2])
