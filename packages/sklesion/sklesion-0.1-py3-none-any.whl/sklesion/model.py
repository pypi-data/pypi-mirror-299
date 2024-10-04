import tensorflow as tf
import pickle
import os
import importlib
import pandas as pd


# Python class for the skin cancer classifier
class SkinLesionClassifier:
    # ---> Construct instance
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Path to the file with Keras model
        self.model_path = os.path.join(current_dir, "model.keras")
        # Path to file with model properties' dictionary
        self.model_props_path = os.path.join(current_dir, "model_props.pkl")
        # Path to file with ProbToLabel Keras layer (for getting labels from predicted
        # probabilities)
        self.prob_to_label_path = os.path.join(current_dir, "prob_to_label.py")
        # The model itself
        self.model = self.load_model()
        # Model properties dictionary
        self.model_props = self.load_model_props()
        # ProbToLabel layer
        self.prob_to_label = self.load_prob_to_label()

    # ---> Load model from file
    def load_model(self):
        if os.path.exists(self.model_path):
            return tf.keras.models.load_model(self.model_path)
        else:
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

    # ---> Load model properties dictionary from file
    def load_model_props(self):
        if os.path.exists(self.model_props_path):
            with open(self.model_props_path, "rb") as f:
                return pickle.load(f)
        else:
            raise FileNotFoundError(
                f"Model properties' file not found: {self.model_props_path}"
            )

    # Load ProbToLabel Keras layer from file (for getting labels from predicted
    # probabilities)
    def load_prob_to_label(self):
        if os.path.exists(self.prob_to_label_path):
            spec = importlib.util.spec_from_file_location(
                "prob_to_label.py", self.prob_to_label_path
            )
            file = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(file)
            ProbToLabel = file.ProbToLabel
            return ProbToLabel(self.model_props["i_cl_map"])
        else:
            raise FileNotFoundError(
                f"ProbToLabel file not found: {self.prob_to_label_path}"
            )

    # ---> Pre-process features
    def preprocess(self, image: tf.Tensor, meta: pd.DataFrame) -> tf.data.Dataset:

        # Re-scale image image
        image = tf.image.resize(image, self.model_props["img_shape"])

        # Handle the possibility of age missing its value
        meta["age_missing"] = meta["age"].isnull().astype(int)
        meta["age"].fillna(self.model_props["age_mean"], inplace=True)

        # One-hot encode nominal meta features (sex and location)
        meta["sex"] = meta["sex"].map(
            {key: value for (key, value) in self.model_props["oh_map"]["sex"].items()}
        )
        meta["location"] = meta["location"].map(
            {key: value for (key, value) in self.model_props["oh_map"]["loc"].items()}
        )

        # Normalize numeral meta feature age
        meta["age"] = meta["age"] / self.model_props["age_max"]

        # Combine the different meta features to define an overall feature vector
        meta = (
            meta["sex"]
            + meta["location"]
            + meta["age"].apply(lambda x: [x])
            + meta["age_missing"].apply(lambda x: [x])
        )

        # Define TensorFlow Dataset from image and metadata
        x = tf.data.Dataset.zip(
            (
                (
                    tf.data.Dataset.from_tensor_slices(image),
                    tf.data.Dataset.from_tensor_slices(meta.to_list()),
                ),
            )
        ).batch(1)

        return x

    # ---> Predict diagnoses probabilities
    def predict_P(self, x):
        x_pre = self.preprocess(x)
        P = self.model.predict(x_pre)
        return P

    # ---> Predict diagnosis
    def predict(self, x):
        P = self.predict_P(x)
        y = self.prob_to_label(P).numpy().astype(str).tolist()[0]

        return y

    # ---> Get a detailed dicription of the diagnosis classes
    @staticmethod
    def cl_det():
        cl_det = {
            "bkl": {
                "type": "benign",
                "desc": "benign keratosis-like lesion - solar lentigo, seborrheic keratosis or a lichen-planus like keratosis",
            },
            "df": {
                "type": "benign",
                "desc": "dermatofibroma - very common",
            },
            "nv": {
                "type": "benign",
                "desc": "melanocytic nevus - the medical term for a mole, which is very common",
            },
            "vasc": {
                "type": "benign",
                "desc": "vascular lesion - angioma, angiokeratoma, pyogenic granuloma or hemorrhage",
            },
            "akiec": {
                "type": "malign",
                "desc": 'actinic keratosis or intraepithelial carcinoma - also called "Bowen\'s disease", an early form of skin cancer',
            },
            "bcc": {
                "type": "malign",
                "desc": "basal cell carcinoma - a type of skin cancer",
            },
            "mel": {
                "type": "malign",
                "desc": "melanoma - a type of skin cancer",
            },
        }
        return cl_det
