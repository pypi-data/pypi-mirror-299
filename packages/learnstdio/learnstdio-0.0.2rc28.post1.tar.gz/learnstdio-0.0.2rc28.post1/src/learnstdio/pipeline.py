#   ---------------------------------------------------------------------------------
#   Copyright (c) Learnstdio. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is Pipeline module."""


from __future__ import annotations
import json
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression

def read_parameters(path: str) -> dict:
    """This is to read parameters from a file."""
    if not path:
        raise ValueError('Path not provided')
    if not path.endswith('.json'):
        raise ValueError('File format not supported')
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def load_model(model: dict) -> LoadableModel:
    """This is to load a model from parameters."""
    if not model:
        raise ValueError('Model parameters not found')
    # Create a model object
    new_model_instance = None
    if 'K-Nearest Neighbors' in model['name']:
        new_model_instance = LoadableKNN(model)
    elif 'Multivariate Linear Regression' in model['name']:
        new_model_instance = LoadableMultivariableLinearRegression(model)
    elif 'Decision Tree Classifier' in model['name']:
        new_model_instance = LoadableDecisionTreeClassifier(model)
    elif 'Decision Tree Regression' in model['name']:
        new_model_instance = LoadableDecisionTreeRegression(model)
    elif 'Logistic Regression' in model['name']:
        new_model_instance = LoadableLogisticRegression(model)
    elif 'Gaussian Naive Bayes' in model['name']:
        new_model_instance = LoadableGaussianNaiveBayes(model)
    elif 'Multinomial Naive Bayes' in model['name']:
        new_model_instance = LoadableMultinomialNaiveBayes(model)
    elif 'Random Forest Classifier' in model['name']:
        new_model_instance = LoadableRandomForestClassifier(model)
    elif 'Random Forest Regression' in model['name']:
        new_model_instance = LoadableRandomForestRegression(model)
    else:
        raise ValueError('Model not supported')
    #
    return new_model_instance

def load_pipeline(path: str) -> LoadableModel:
    """This is to load a pipeline from a file."""
    # Read file
    data = read_parameters(path)
    # Read model information
    model = data['model']
    if not model:
        raise ValueError('Model not found')
    # Read model parameters information
    new_model = load_model(model)
    #
    return new_model

class LoadableModel:
    """Loadable model from parameters."""

    def __init__(self):
        """Initialize the model."""
        self.model = None

    def predict(self, *args):
        """Predict the output from the model."""
        # Convert args to a 2D array
        input_features = np.array(args).reshape(1, -1)
        # Make prediction
        if not self.model:
            raise ValueError('Model was not loaded')
        prediction = self.model.predict(input_features)
        # Return the first (and only) prediction
        return prediction.item() if prediction.size == 1 else prediction

class LoadableKNN(LoadableModel):
    """Loadable KNN model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        self.model = KNeighborsClassifier(
            n_neighbors=parameters['k'],
        )
        self.model.fit(
            parameters['X'],
            parameters['y'],
        )


class LoadableMultivariableLinearRegression(LoadableModel):
    """Loadable Linear Regression model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        self.model = LinearRegression()
        self.model.coef_ = np.array(parameters['weights'][:-1]).reshape(1, -1)
        self.model.intercept_ = np.array(parameters['weights'][-1])

class LoadableDecisionTreeClassifier(LoadableModel):
    """Loadable Decision Tree Classifier model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        raise NotImplementedError('Decision Tree Classifier coming soon!')

class LoadableDecisionTreeRegression(LoadableModel):
    """Loadable Decision Tree Regression model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        raise NotImplementedError('Decision Tree Regression coming soon!')

class LoadableLogisticRegression(LoadableModel):
    """Loadable Logistic Regression model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        raise NotImplementedError('Logistic Regression coming soon!')

class LoadableGaussianNaiveBayes(LoadableModel):
    """Loadable Gaussian Naive Bayes model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        raise NotImplementedError('Gaussian Naive Bayes coming soon!')

class LoadableMultinomialNaiveBayes(LoadableModel):
    """Loadable Multinomial Naive Bayes model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        raise NotImplementedError('Multinomial Naive Bayes coming soon!')

class LoadableRandomForestClassifier(LoadableModel):
    """Loadable Random Forest Classifier model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        raise NotImplementedError('Random Forest Classifier coming soon!')

class LoadableRandomForestRegression(LoadableModel):
    """Loadable Random Forest Regression model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        raise NotImplementedError('Random Forest Regression coming soon!')
