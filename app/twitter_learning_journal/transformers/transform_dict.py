def transform_dict_into_keys_sorted_by_value(input_dict, *, reverse=False):
    return sorted(input_dict, key=input_dict.get, reverse=reverse)
