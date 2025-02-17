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
import tempfile

import numpy as np
import pytest
import torch
import torchvision

from oodeel.datasets import OODDataset
from tests.tests_torch import generate_data
from tests.tests_torch import generate_data_torch


def test_instanciate_from_torchvision():
    with tempfile.TemporaryDirectory() as tmpdirname:
        dataset = OODDataset(
            dataset_id="MNIST",
            backend="torch",
            load_kwargs=dict(root=tmpdirname, train=False, download=True),
        )

        assert len(dataset.data) == 10000
        assert dataset.len_item == 2


@pytest.mark.parametrize(
    "expected_output", [[100, 2, 2]], ids=["Instanciate from torch data"]
)
def test_instanciate_ood_dataset(expected_output):
    """Test the instanciation of OODDataset."""

    dataset_id = generate_data_torch(x_shape=(3, 32, 32), num_labels=10, samples=100)

    dataset = OODDataset(dataset_id=dataset_id, backend="torch")

    item_len = len(dataset.data[0])

    assert len(dataset.data) == expected_output[0]
    assert dataset.len_item == expected_output[1]
    assert item_len == expected_output[2]


@pytest.mark.parametrize(
    "ds2_from_numpy, expected_output",
    [
        (True, [200, 2, 3, 0.5]),
        (False, [200, 2, 3, 0.5]),
    ],
    ids=[
        "[torch] Concatenate two OODDatasets",
        "[torch] Concatenate a OODDataset and a numpy dataset",
    ],
)
def test_add_ood_data(ds2_from_numpy, expected_output):
    """Test the concatenation of OODDataset."""

    x_shape = (3, 32, 32)

    dataset1 = OODDataset(
        dataset_id=generate_data_torch(x_shape=x_shape, num_labels=10, samples=100),
        backend="torch",
    )

    if ds2_from_numpy:
        dataset2 = generate_data(x_shape=(38, 38, 3), num_labels=10, samples=100)
    else:
        dataset2 = OODDataset(
            dataset_id=generate_data_torch(x_shape=x_shape, num_labels=10, samples=100),
            backend="torch",
        )

    dataset = dataset1.add_out_data(dataset2, shape=(23, 23))
    ood_labels = dataset.get_ood_labels()
    item_len = len(dataset.data[0])
    assert len(dataset.data) == expected_output[0]
    assert dataset.len_item == expected_output[1]
    assert item_len == expected_output[2]
    assert np.mean(ood_labels) == expected_output[3]


@pytest.mark.parametrize(
    "in_labels, out_labels, one_hot, expected_output",
    [
        ([1, 2], None, False, [100, 67, 33, 2, 1]),
        (None, [1, 2], True, [100, 33, 67, 1, 2]),
        ([1], [2], False, [100, 33, 34, 1, 1]),
    ],
    ids=[
        "[torch] Assign OOD labels by class with ID labels",
        "[torch] Assign OOD labels by class with OOD labels",
        "[torch] Assign OOD labels by class with ID and OOD labels",
    ],
)
def test_assign_ood_labels_by_class(in_labels, out_labels, one_hot, expected_output):
    """Test the assign_ood_labels_by_class method."""

    # generate data
    x_shape = (3, 32, 32)
    images, labels = generate_data(
        x_shape=x_shape,
        num_labels=3,
        samples=100,
        one_hot=one_hot,
    )

    if not one_hot:
        for i in range(100):
            if i < 33:
                labels[i] = 0
            if i >= 33 and i < 66:
                labels[i] = 1
            if i >= 66:
                labels[i] = 2
    else:
        for i in range(100):
            if i < 33:
                labels[i] = np.array([1, 0, 0])
            if i >= 33 and i < 66:
                labels[i] = np.array([0, 1, 0])
            if i >= 66:
                labels[i] = np.array([0, 0, 1])

    dataset = OODDataset(dataset_id=(images, labels), backend="torch")

    in_dataset, out_dataset = dataset.assign_ood_labels_by_class(
        in_labels=in_labels,
        out_labels=out_labels,
    )

    len_ds = len(dataset)
    len_inds = len(in_dataset)
    len_outds = len(out_dataset)

    classes = dataset._data_handler.get_feature_from_ds(dataset.data, "label")
    classes = np.unique(classes, axis=0)

    classes_in = dataset._data_handler.get_feature_from_ds(in_dataset.data, "label")
    classes_in = np.unique(classes_in, axis=0)

    classes_out = dataset._data_handler.get_feature_from_ds(out_dataset.data, "label")
    classes_out = np.unique(classes_out, axis=0)

    assert len_ds == expected_output[0]
    assert len_inds == expected_output[1]
    assert len_outds == expected_output[2]
    assert len(classes_in) == expected_output[3]
    assert len(classes_out) == expected_output[4]


@pytest.mark.parametrize(
    "shuffle, with_labels, with_ood_labels, expected_output",
    [
        (False, True, True, [3, (32, 10)]),
        (False, False, True, [2, (32,)]),
        (True, True, True, [3, (32, 10)]),
        (True, True, False, [2, (32, 10)]),
    ],
    ids=[
        "[torch] Prepare OODDataset for scoring with labels and ood labels",
        "[torch] Prepare OODDataset for scoring with only ood labels",
        "[torch] Prepare OODDataset for training (with shuffle and augment_fn) with "
        "labels and ood labels",
        "[torch] Prepare OODDataset for training (with shuffle and augment_fn) "
        "with only labels",
    ],
)
def test_prepare(shuffle, with_labels, with_ood_labels, expected_output):
    """Test the prepare method."""

    num_labels = 10
    batch_size = 32
    samples = 100

    x_shape = (3, 32, 32)

    dataset = OODDataset(
        dataset_id=generate_data_torch(
            x_shape=x_shape,
            num_labels=num_labels,
            samples=samples,
            one_hot=True,
        ),
        backend="torch",
    )

    def preprocess_fn(inputs):
        x = inputs[0] / 255
        return tuple([x] + list(inputs[1:]))

    def augment_fn_(inputs):
        x = torchvision.transforms.RandomHorizontalFlip()(inputs[0])
        return tuple([x] + list(inputs[1:]))

    augment_fn = augment_fn_ if shuffle else None

    dataset2 = OODDataset(
        dataset_id=generate_data_torch(
            x_shape=x_shape,
            num_labels=num_labels,
            samples=samples,
            one_hot=True,
        ),
        backend="torch",
    )

    dataset = dataset.add_out_data(dataset2)

    ds = dataset.prepare(
        batch_size=batch_size,
        preprocess_fn=preprocess_fn,
        with_labels=with_labels,
        with_ood_labels=with_ood_labels,
        shuffle=shuffle,
        augment_fn=augment_fn,
    )

    batch1 = next(iter(ds))
    batch2 = next(iter(ds))

    assert len(batch1) == expected_output[0]
    if shuffle:
        assert torch.sum(batch1[0] - batch2[0]) != 0
    assert batch1[1].shape == torch.Size(expected_output[1])
    if with_ood_labels and with_labels:
        assert batch1[2].shape == torch.Size([32])
    assert batch1[0].shape == torch.Size([batch_size, 3, 32, 32])
    assert torch.max(batch1[0]) <= 1
    assert torch.min(batch1[0]) >= 0
