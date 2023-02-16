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
from typing import Callable

from .tf_tools import (
    dataset_cardinality,
    dataset_get_columns,
    dataset_image_shape,
    dataset_label_shape,
    dataset_max_pixel,
    dataset_nb_columns,
    dataset_nb_labels,
)

__all__ = ["dataset_cardinality", "dataset_get_columns", "dataset_image_shape",
           "dataset_label_shape", "dataset_max_pixel", "dataset_nb_columns",
           "dataset_nb_labels"]


def is_from(model: Callable, framework: str) -> str:
    """Check wether the model belongs to a specific framework

    Args:
        model (Callable): Neural network
        framework (str): Model framework ("torch" | "keras")

    Returns:
        bool: Wether the model belongs to specified framework or not
    """
    class_parents = list(
        map(lambda x: str(x).split("'")[1].split(".")[0],
            model.__class__.__mro__)
    )
    return framework in class_parents
