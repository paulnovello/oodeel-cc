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
from abc import ABC
from abc import abstractmethod

import numpy as np

from ..types import Callable
from ..types import List
from ..types import TensorType


class Operator(ABC):
    """Class to handle tensorflow and torch operations with a unified API"""

    @abstractmethod
    def softmax(tensor: TensorType) -> TensorType:
        """Softmax function"""
        raise NotImplementedError()

    @abstractmethod
    def argmax(tensor: TensorType, dim: int = None) -> TensorType:
        """Argmax function"""
        raise NotImplementedError()

    @abstractmethod
    def max(tensor: TensorType, dim: int = None) -> TensorType:
        """Max function"""
        raise NotImplementedError()

    @abstractmethod
    def one_hot(tensor: TensorType, num_classes: int) -> TensorType:
        """One hot function"""
        raise NotImplementedError()

    @abstractmethod
    def sign(tensor: TensorType) -> TensorType:
        """Sign function"""
        raise NotImplementedError()

    @abstractmethod
    def CrossEntropyLoss(reduction: str = "mean"):
        """Cross Entropy Loss from logits"""
        raise NotImplementedError()

    @abstractmethod
    def norm(tensor: TensorType, dim: int = None) -> TensorType:
        """Norm function"""
        raise NotImplementedError()

    @abstractmethod
    def matmul(tensor_1: TensorType, tensor_2: TensorType) -> TensorType:
        """Matmul operation"""
        raise NotImplementedError()

    @abstractmethod
    def convert_to_numpy(tensor: TensorType) -> np.ndarray:
        "Convert a tensor to a NumPy array"
        raise NotImplementedError()

    @abstractmethod
    def gradient(func: Callable, inputs: TensorType) -> TensorType:
        """Compute gradients for a batch of samples.

        Args:
            func (Callable): Function used for computing gradient. Must be built with
                differentiable operations only, and return a scalar.
            inputs (Any): Input tensor wrt which the gradients are computed

        Returns:
            Gradients computed, with the same shape as the inputs.
        """
        raise NotImplementedError()

    @abstractmethod
    def stack(tensors: List[TensorType], dim: int = 0) -> TensorType:
        "Stack tensors along a new dimension"
        raise NotImplementedError()

    @abstractmethod
    def cat(tensors: List[TensorType], dim: int = 0) -> TensorType:
        "Concatenate tensors in a given dimension"
        raise NotImplementedError()

    @abstractmethod
    def mean(tensor: TensorType, dim: int = None, keepdim: bool = False) -> TensorType:
        "Mean function"
        raise NotImplementedError()

    @abstractmethod
    def flatten(tensor: TensorType) -> TensorType:
        "Flatten to 2D tensor (batch_size, -1)"
        # Flatten the features to 2D (n_batch, n_features)
        raise NotImplementedError()

    @abstractmethod
    def from_numpy(arr: np.ndarray) -> TensorType:
        "Convert a NumPy array to a tensor"
        # TODO change dtype
        raise NotImplementedError()

    @abstractmethod
    def transpose(tensor: TensorType) -> TensorType:
        "Transpose function"
        raise NotImplementedError()

    @abstractmethod
    def diag(tensor: TensorType) -> TensorType:
        "Diagonal function: return the diagonal of a 2D tensor"
        raise NotImplementedError()

    @abstractmethod
    def reshape(tensor: TensorType, shape: List[int]) -> TensorType:
        "Reshape function"
        raise NotImplementedError()

    @abstractmethod
    def pinv(tensor: TensorType) -> TensorType:
        "Pseudo-inverse function"
        raise NotImplementedError()
