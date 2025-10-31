from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from imblearn.over_sampling import BorderlineSMOTE
from sklearn.impute import SimpleImputer


def create_preprocessor() -> ColumnTransformer:
    numeric_pipe = make_pipeline(
        SimpleImputer(strategy="mean"),
        StandardScaler()
    )
    categorical_pipe = make_pipeline(
        SimpleImputer(strategy="most_frequent"),
        OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    )
    preprocessor = make_column_transformer(
        (numeric_pipe, make_column_selector(dtype_include=["int64", "float64"])),
        (categorical_pipe, make_column_selector(dtype_include=["object", "string", "bool"])),
        remainder="drop"
    )
    return preprocessor

def pipeline_smote(X_preprocessed, y):
    sm = BorderlineSMOTE(random_state=42)
    X_preprocessed_smote, y_smote = sm.fit_resample(X_preprocessed, y)
    return X_preprocessed_smote, y_smote

def encode_target(y):
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    return y_encoded, le
