import tensorflow as tf
from .base import OODModel
import numpy as np
from ..types import *

class MLS(OODModel):
    """
    Maximum Logit Scores method for OOD detection.
    "Open-Set Recognition: a Good Closed-Set Classifier is All You Need?"
    https://arxiv.org/abs/2110.06207

    Parameters
    ----------
    model : tf.keras model 
        keras models saved as pb files e.g. with model.save()
    """
    def __init__(
        self, 
        output_activation: str = "linear", 
        batch_size: int = 256,
        threshold: Optional[float] = None
    ):
        """
        Initializes the feature extractor 
        """
        super().__init__(output_activation=output_activation, 
                         batch_size=batch_size,
                         threshold=threshold)

    def _score_tensor(
        self, 
        inputs: Union[tf.data.Dataset, tf.Tensor, np.ndarray]
    ) -> np.ndarray:
        """
        Computes an OOD score for input samples "inputs" based on 
        maximum logits value.

        Parameters
        ----------
        inputs : np.array
            input samples to score

        Returns
        -------
        np.array
            scores
        """
        assert self.feature_extractor is not None, "Call .fit() before .score()"

        pred = self.feature_extractor(inputs)[0]
        scores = np.max(pred, axis=1)
        self.scores = -scores
        return self.scores

        