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
from ..types import Any


avail_lib = []
try:
    import tensorflow as tf

    avail_lib.append("tensorflow")
except ImportError:
    pass

try:
    import torch

    avail_lib.append("torch")
except ImportError:
    pass


if len(avail_lib) == 2:
    from .tf_operator import TFOperator
    from .torch_operator import TorchOperator
elif "tensorflow" in avail_lib:
    from .tf_operator import TFOperator
elif "torch" in avail_lib:
    from .torch_operator import TorchOperator


def is_from(model_or_tensor: Any, framework: str) -> str:
    """Check wether a model or tensor belongs to a specific framework

    Args:
        model_or_tensor (Any): Neural network or Tensor
        framework (str):  Model or tensor framework ("torch" | "keras" | "tensorflow")

    Returns:
        bool: Wether the model belongs to specified framework or not
    """
    keywords_list = []
    class_parents = list(model_or_tensor.__class__.__mro__)
    for class_id in class_parents:
        class_list = str(class_id).split("'")[1].split(".")
        for keyword in class_list:
            keywords_list.append(keyword)
    return framework in keywords_list
