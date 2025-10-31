import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import ExtraTreesClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate
from ml_logic.data import clean_data

def initialize_ensemble_model() -> VotingClassifier:
    model_et = ExtraTreesClassifier(
        n_estimators=500,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features="log2",
        max_depth=50,
        bootstrap=True,
        random_state=42
    )

    model_svm = SVC(
        kernel="rbf",
        C=5,
        probability=True,
        gamma=0.1,
        random_state=42
    )

    return VotingClassifier(
        estimators=[('et', model_et), ('svm', model_svm)],
        voting='soft',
        n_jobs=-1
    )

def train_ensemble_model(
    model: VotingClassifier,
    X: np.ndarray,
    y: np.ndarray,
    cv: int = 5
) -> Tuple[VotingClassifier, dict]:
    scoring = {
        'accuracy': 'accuracy',
        'precision': 'precision_macro',
        'recall': 'recall_macro',
        'f1': 'f1_macro'
    }
    scores = cross_validate(model, X, y, cv=cv, scoring=scoring, n_jobs=-1, return_train_score=False)
    model.fit(X, y)
    return model, scores

class_names = [
    "Mitochondrial genetic inheritance disorders",
    "Multifactorial genetic inheritance disorders",
    "Single-gene inheritance diseases"
]

def predict_ensemble_model(model, X_processed_test):
    y_pred = model.predict(X_processed_test)
    y_pred_labels = np.take(class_names, y_pred.astype(int), mode='raise')
    if hasattr(X_processed_test, 'shape'):
        if len(y_pred_labels) == 1:
            return y_pred_labels[0]
        else:
            return y_pred_labels
    else:
        return y_pred_labels
