import dill as pickle

from typing import Callable


def load_model(model_path: str) -> Callable:
    filehandler = open(model_path, "rb")
    model_object = pickle.load(filehandler)
    filehandler.close()
    return model_object


def save_model(full_path: str, model_object: Callable):
    filehandler = open(full_path, "wb")
    pickle.dump(model_object, filehandler)
    filehandler.close()
