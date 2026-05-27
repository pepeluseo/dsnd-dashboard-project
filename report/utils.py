from pathlib import Path
import pickle


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "assets" / "model.pkl"


def load_model():
    """
    Load and return the trained machine learning model.

    Returns
    -------
    object
        Deserialized machine learning model from assets/model.pkl.
    """
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

    return model