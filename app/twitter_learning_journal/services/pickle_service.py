import pickle


def load_pickle_data(path: str):
    return pickle.load(open(path, 'rb'))
