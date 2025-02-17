# -*- coding: utf-8 -*-
# Copyright IRT Antoine de Saint Exupéry et Université Paul Sabatier Toulouse III - All
# rights reserved. DEEL is a research program operated by IVADO, IRT Saint Exupéry,
# CRIAQ and ANITI - https://www.deel.ai/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from oodeel.models.training_funs_tf import train_keras_app
from tests.tests_tensorflow import generate_data_tf


def test_convnet_classifier():
    input_shape = (32, 32, 3)
    num_labels = 10
    samples = 100

    train_config = {
        "model_name": "toy_convnet",
        "batch_size": 5,
        "epochs": 3,
        "input_shape": input_shape,
        "num_classes": num_labels,
    }

    data = generate_data_tf(
        x_shape=input_shape, num_labels=num_labels, samples=samples, one_hot=False
    )

    train_keras_app(data, **train_config)


def test_train_keras_app_imagenet():
    input_shape = (224, 224, 3)
    num_labels = 1000
    samples = 100

    train_config = {
        "batch_size": 5,
        "epochs": 3,
        "input_shape": input_shape,
        "num_classes": num_labels,
    }

    data = generate_data_tf(
        x_shape=input_shape, num_labels=num_labels, samples=samples, one_hot=False
    )

    train_keras_app(
        data, model_name="MobileNet", imagenet_pretrained=True, **train_config
    )


def test_train_keras_app():
    input_shape = (56, 56, 3)
    num_labels = 123
    samples = 100

    train_config = {
        "batch_size": 5,
        "epochs": 3,
        "input_shape": input_shape,
        "num_classes": num_labels,
    }

    data = generate_data_tf(
        x_shape=input_shape, num_labels=num_labels, samples=samples, one_hot=False
    )

    validation_data = generate_data_tf(
        x_shape=input_shape, num_labels=num_labels, samples=samples, one_hot=False
    )

    train_keras_app(
        data,
        model_name="MobileNet",
        imagenet_pretrained=False,
        validation_data=validation_data,
        **train_config
    )
