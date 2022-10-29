from abc import ABC, abstractmethod, abstractproperty
from typing import Dict, Literal, Union
import numpy as np
from sklearn.ensemble import RandomForestRegressor


class Model(ABC):
    def __init__(
        self,
        mode: Literal['regression'],
        params: Dict[str: Union[str, int, float]]
    ):
        self.mode = mode
        self.params = params

    @abstractmethod
    def fit(self, X: np.array, y: np.array):
        pass

    @abstractproperty
    def model(self):
        pass

    def predict(self, X: np.array) -> np.array:
        pass


class RandomForest(Model):
    def __init__(self, **model_kwargs):
        super().__init__(**model_kwargs)

    @property
    def model(self):
        if not hasattr(self, "_model"):
            if self.mode == "regression":
                self._model = RandomForestRegressor(**self.params)
            else:
                raise ValueError(f"Unsupported mode: {self.mode}")

    def fit(self, X: np.array, y: np.array):
        self._model.fit(X, y)

    def predict(self, X) -> np.array:
        return self._model.predict(X)


