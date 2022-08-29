import tensorflow as tf
from .base import OODModel
import numpy as np
import faiss

class DKNN(OODModel):
    """
    "Out-of-Distribution Detection with Deep Nearest Neighbors"
    https://arxiv.org/abs/2204.06507
    Simplified version adapted to convnet as built in ./models/train/train_mnist.py

    Parameters
    ----------
    model : tf.keras model 
        keras models saved as pb files e.g. with model.save()
    """
    def __init__(self, model, nearest=1, output_layers=[-2], output_activations=["base"],
                 flatten=True, threshold=None):
        """
        Initializes the feature extractor 
        """
        super().__init__(model, output_layers, output_activations, threshold, flatten)
        self.index = None
        self.nearest = nearest

    def fit(self, fit_dataset):
        """
        Constructs the index from ID data "fit_dataset", which will be used for
        nearest neighbor search.

        Parameters
        ----------
        fit_dataset : np.array
            input dataset (ID) to construct the index with.
        """
        self.id_projected = self.feature_extractor(fit_dataset)
        self.index = faiss.IndexFlatL2(self.id_projected[0].shape[1])
        self.index.add(self.id_projected[0])

    def score(self, inputs):
        """
        Computes an OOD score for input samples "inputs" based on 
        the distance to nearest neighbors in the feature space of self.model

        Parameters
        ----------
        inputs : np.array
            input samples to score

        Returns
        -------
        np.array
            scores
        """
        inp_proj = self.feature_extractor(inputs)
        scores, _ = self.index.search(inp_proj[0], self.nearest)
        return scores[:,0]

        
