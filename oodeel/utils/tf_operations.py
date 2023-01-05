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
import numpy as np
import tensorflow as tf
from tensorflow import keras

from ..types import *
from .tools import dataset_label_shape
from .tools import dataset_nb_columns
from .tools import dataset_nb_labels


def batch_tensor(
    tensors: Union[
        tf.data.Dataset, tf.Tensor, np.ndarray, Tuple[tf.Tensor], Tuple[np.ndarray]
    ],
    batch_size: int = 256,
    one_hot_encode: Optional[bool] = False,
    num_classes: Optional[int] = None,
):
    """
    Create a tensorflow dataset of tensors or series of tensors.

    Parameters
    ----------
    tensors
        Tuple of tensors or tensors to batch.
    batch_size
        Number of samples to iterate at once, if None process all at once.

    Returns
    -------
    dataset
        Tensorflow dataset batched.
    """
    if not isinstance(tensors, tf.data.Dataset):
        tensors = tf.data.Dataset.from_tensor_slices(tensors)

    if one_hot_encode:
        # check if it is one_hot_encoded
        label_shape = list(dataset_label_shape(tensors))
        if label_shape == []:
            nb_columns = dataset_nb_columns(tensors)
            assert nb_columns == 2, "No labels to one-hot-encode"
            if num_classes is None:
                num_classes = dataset_nb_labels(tensors)
            dataset = tensors.map(lambda x, y: (x, tf.one_hot(y, num_classes))).batch(
                batch_size
            )
    else:
        dataset = tensors.batch(batch_size)

    return dataset


def find_layer(model: tf.keras.Model, layer: Union[str, int]) -> tf.keras.layers.Layer:
    """
    Find a layer in a model either by his name or by his index.
    Parameters
    ----------
    model
        Model on which to search.
    layer
        Layer name or layer index
    Returns
    -------
    layer
        Layer found
    """
    if isinstance(layer, str):
        return model.get_layer(layer)
    if isinstance(layer, int):
        return model.layers[layer]
    raise ValueError(f"Could not find any layer {layer}.")


@tf.function
def gradient_single(
    model: Callable, inputs: tf.Tensor, targets: tf.Tensor
) -> tf.Tensor:
    """
    Compute gradients for a batch of samples.
    Parameters
    ----------
    model
        Model used for computing gradient.
    inputs
        Input samples to be explained.
    targets
        One-hot encoded labels or regression target (e.g {+1, -1}), one for each sample.
    Returns
    -------
    gradients
        Gradients computed, with the same shape as the inputs.
    """
    with tf.GradientTape(watch_accessed_variables=False) as tape:  # type: ignore
        tape.watch(inputs)
        score = tf.reduce_sum(tf.multiply(model(inputs), targets), axis=1)
    return tape.gradient(score, inputs)


@tf.function
def gradient(
    model: Callable, inputs: tf.Tensor, index: Union[tuple, int] = None
) -> tf.Tensor:
    """
    Compute gradients for a batch of samples.
    Parameters
    ----------
    model
        Model used for computing gradient.
    inputs
        Input samples to be explained.
    targets
        One-hot encoded labels or regression target (e.g {+1, -1}), one for each sample.
    Returns
    -------
    gradients
        Gradients computed, with the same shape as the inputs.
    """
    with tf.GradientTape(watch_accessed_variables=False) as tape:  # type: ignore
        tape.watch(inputs)
        score = model(inputs)
        score = score[:][index]
    return tape.gradient(score, inputs)


@tf.function
def gradient_full(model: Callable, inputs: tf.Tensor) -> tf.Tensor:
    """
    Compute gradients for a batch of samples.
    Parameters
    ----------
    model
        Model used for computing gradient.
    inputs
        Input samples to be explained.
    targets
        One-hot encoded labels or regression target (e.g {+1, -1}), one for each sample.
    Returns
    -------
    gradients
        Gradients computed, with the same shape as the inputs.
    """
    with tf.GradientTape(watch_accessed_variables=False) as tape:  # type: ignore
        tape.watch(inputs)
        score = model(inputs)
    return tape.gradient(score, inputs)
