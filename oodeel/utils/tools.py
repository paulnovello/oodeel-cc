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

from oodeel.types import *


def dataset_nb_columns(dataset: tf.data.Dataset) -> int:
    try:
        return len(dataset.element_spec)
    except TypeError:
        return 1


def dataset_image_shape(dataset: tf.data.Dataset) -> Tuple[int]:
    """
    Get the shape of the images in the dataset

    Args:
        dataset:   input dataset
    Returns:
        shape of the images in the dataset
    """
    for x in dataset.take(1):
        if isinstance(x, tuple):
            shape = x[0].shape
        else:
            shape = x.shape
    return shape


def dataset_label_shape(dataset: tf.data.Dataset) -> Tuple[int]:

    for x in dataset.take(1):
        assert len(x) > 1, "No label to get the shape from"
        shape = x[1].shape
    return shape


def dataset_max_pixel(dataset: tf.data.Dataset) -> float:

    dataset = dataset_get_columns(dataset, 0)
    max_pixel = dataset.reduce(
        0.0, lambda x, y: float(tf.math.reduce_max(tf.maximum(x, y)))
    )
    return float(max_pixel)


def dataset_nb_labels(dataset: tf.data.Dataset) -> int:
    ds = dataset_get_columns(dataset, 1)
    ds = ds.unique()
    return len(list(ds.as_numpy_iterator()))


def dataset_cardinality(dataset: tf.data.Dataset) -> int:

    cardinality = dataset.reduce(0, lambda x, _: x + 1)
    return int(cardinality)


def dataset_get_columns(
    dataset: tf.data.Dataset, columns: Union[int, List[int]]
) -> tf.data.Dataset:
    """
    Construct a dataset out of the columns of the input dataset. The columns are identified by "columns". Here columns means x, y, or ood_labels

    Args:
        dataset: input dataset
        columns: columns to extract

    Returns:
        tf.data.Dataset with columns extracted from the input dataset
    """
    if isinstance(columns, int):
        columns = [columns]
    length = dataset_nb_columns(dataset)

    if length == 2:  # when image, label

        def return_columns(x, y, col):
            X = [x, y]
            return tuple([X[i] for i in col])

        dataset = dataset.map(lambda x, y: return_columns(x, y, columns))

    if length == 3:  # when image, label, ood_label or weights

        def return_columns(x, y, z, col):
            X = [x, y, z]
            return tuple([X[i] for i in col])

        dataset = dataset.map(lambda x, y, z: return_columns(x, y, z, columns))

    return dataset
