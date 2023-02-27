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
import torch

from oodeel.utils.torch_operator import TorchOperator
from tests.tools_torch import generate_data
from tests.tools_torch import Net


def test_gradient_model():
    """Test gradient model."""
    input_shape = (3, 32, 32)
    num_labels = 10
    samples = 100

    x, y = generate_data(
        x_shape=input_shape, num_labels=num_labels, samples=samples, one_hot=True
    )

    x = torch.Tensor(x)
    y = torch.Tensor(y)
    model = Net()

    torch_operator = TorchOperator()
    gradients = torch_operator.gradient_model(model, x, y)

    assert tuple(gradients.shape) == (samples, 3, 32, 32)


def test_gradient():
    """Test gradient."""
    input_shape = (3, 32, 32)

    def diff_fun(x):
        return x.sum()

    x = torch.ones(input_shape)
    torch_operator = TorchOperator()
    gradients = torch_operator.gradient(diff_fun, x)[0]

    assert tuple(gradients.shape) == input_shape
    assert torch.all(gradients == torch.ones(input_shape))
