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

from ..types import Callable
from ..types import List
from ..types import TensorType
from ..types import Union
from .general_utils import is_from
from .operator import Operator


def sanitize_input(tensor_arg_func: Callable):
    def wrapper(obj, tensor, *args, **kwargs):
        if isinstance(tensor, tf.Tensor):
            pass
        elif is_from(tensor, "torch"):
            tensor = tf.convert_to_tensor(tensor.numpy())
        else:
            tensor = tf.convert_to_tensor(tensor)

        return tensor_arg_func(obj, tensor, *args, **kwargs)

    return wrapper


class TFOperator(Operator):
    """Class to handle tensorflow operations with a unified API"""

    @staticmethod
    def softmax(tensor: Union[tf.Tensor, np.ndarray]) -> tf.Tensor:
        """Softmax function"""
        return tf.keras.activations.softmax(tensor)

    @staticmethod
    def argmax(tensor: Union[tf.Tensor, np.ndarray], dim: int = None) -> tf.Tensor:
        """Argmax function"""
        return tf.argmax(tensor, axis=dim)

    @staticmethod
    def max(tensor: Union[tf.Tensor, np.ndarray], dim: int = None) -> tf.Tensor:
        """Max function"""
        return tf.reduce_max(tensor, axis=dim)

    @staticmethod
    def one_hot(tensor: Union[tf.Tensor, np.ndarray], num_classes: int) -> tf.Tensor:
        """One hot function"""
        return tf.one_hot(tensor, num_classes)

    @staticmethod
    def sign(tensor: Union[tf.Tensor, np.ndarray]) -> tf.Tensor:
        """Sign function"""
        return tf.sign(tensor)

    @staticmethod
    def CrossEntropyLoss(reduction: str = "mean"):
        """Cross Entropy Loss from logits"""

        tf_reduction = {"mean": "sum_over_batch_size", "sum": "sum"}[reduction]

        def sanitized_ce_loss(inputs, targets):
            return tf.keras.losses.SparseCategoricalCrossentropy(
                from_logits=True, reduction=tf_reduction
            )(targets, inputs)

        return sanitized_ce_loss

    @staticmethod
    def norm(tensor: Union[tf.Tensor, np.ndarray], dim: int = None) -> tf.Tensor:
        """Tensor Norm"""
        return tf.norm(tensor, axis=dim)

    @staticmethod
    @tf.function
    def matmul(tensor_1: TensorType, tensor_2: TensorType) -> TensorType:
        """Matmul operation"""
        return tf.matmul(tensor_1, tensor_2)

    @staticmethod
    def convert_to_numpy(tensor: TensorType) -> np.ndarray:
        return tensor.numpy()

    @staticmethod
    @tf.function
    def gradient(func: Callable, inputs: tf.Tensor, *args, **kwargs) -> tf.Tensor:
        """Compute gradients for a batch of samples.

        Args:
            func (Callable): Function used for computing gradient. Must be built with
                tensorflow differentiable operations only, and return a scalar.
            inputs (tf.Tensor): Input tensor wrt which the gradients are computed

        Returns:
            tf.Tensor: Gradients computed, with the same shape as the inputs.
        """
        with tf.GradientTape(watch_accessed_variables=False) as tape:
            tape.watch(inputs)
            outputs = func(inputs, *args, **kwargs)
        return tape.gradient(outputs, inputs)

    @staticmethod
    def stack(tensors: List[TensorType], dim: int = 0) -> TensorType:
        "Stack tensors along a new dimension"
        return tf.stack(tensors, dim)

    @staticmethod
    def cat(tensors: List[TensorType], dim: int = 0) -> TensorType:
        "Concatenate tensors in a given dimension"
        return tf.concat(tensors, dim)

    @staticmethod
    def mean(tensor: TensorType, dim: int = None, keepdim: bool = False) -> TensorType:
        "Mean function"
        return tf.reduce_mean(tensor, dim, keepdim)

    @staticmethod
    def flatten(tensor: TensorType) -> TensorType:
        "Flatten to 2D tensor of shape (tensor.shape[0], -1)"
        # Flatten the features to 2D (n_batch, n_features)
        return tf.reshape(tensor, shape=[tf.shape(tensor)[0], -1])

    @staticmethod
    def from_numpy(arr: np.ndarray) -> TensorType:
        "Convert a NumPy array to a tensor"
        # TODO change dtype
        return tf.constant(arr, dtype=tf.float32)

    @staticmethod
    def transpose(tensor: TensorType) -> TensorType:
        "Transpose function"
        return tf.transpose(tensor)

    @staticmethod
    def diag(tensor: TensorType) -> TensorType:
        "Diagonal function"
        return tf.linalg.diag_part(tensor)

    @staticmethod
    def reshape(tensor: TensorType, shape: List[int]) -> TensorType:
        "Reshape function"
        return tf.reshape(tensor, shape)

    @staticmethod
    def pinv(tensor: TensorType) -> TensorType:
        "Pseudo-inverse function"
        return tf.linalg.pinv(tensor)
