import pickle


def load_pickle_data(path: str):
    return pickle.load(open(path, 'rb'))


def write_pickle_data(_object, path: str):
    pickle.dump(_object, open(path, 'wb'))
