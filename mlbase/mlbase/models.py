import pickle
import os
from abc import ABC, abstractmethod, abstractproperty
from typing import List
from typing import Dict, Literal, Union
import numpy as np
from sklearn.ensemble import RandomForestRegressor


class Model(ABC):
    def __init__(
        self,
        mode: Literal['regression'],
        params: Dict[str, Union[str, int, float]]
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
        self.model_name = "Random_Forest"
        super().__init__(**model_kwargs)

    @property
    def model(self):
        if not hasattr(self, "_model"):
            if self.mode == "regression":
                self._model = RandomForestRegressor(**self.params)
            else:
                raise ValueError(f"Unsupported mode: {self.mode}")
        return self._model

    def fit(self, X: np.array, y: np.array):
        self.model.fit(X, y)

    def predict(self, X) -> np.array:
        return self.model.predict(X)


class EnsembleModel:
    def __init__(
        self,
        models: List[Model],
        all_same: bool = True,
        model_name: str = None
    ):
        self.all_same = all_same
        self.models = self._check_models(models)
        self.model_name = model_name or self.models[0].model_name + "_Ensemble"

    def _check_models(self, models: List[Model]):
        for model in models:

            if self.all_same and not isinstance(model, Model):
                raise TypeError(
                    "All models have to be of type Model if all_same is True"
                )
        return models

    def predict(self, X: np.ndarray):
        return np.mean(
            np.column_stack(
                [model.predict(X) for model in self.models]
            ),
            axis=1
        )
    def save_model(self, path):
        path = os.path.join(path, f'{self.model_name}.pkl')
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'wb') as file:
            pickle.dump(self, file)

        self.model_path = path

        return path

