import pickle

def load_model(path):
    with open(path, "rb") as file:
        return pickle.load(file)
