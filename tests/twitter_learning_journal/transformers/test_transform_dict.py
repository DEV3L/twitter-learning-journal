from pytest import mark

from app.twitter_learning_journal.transformers.transform_dict import transform_dict_into_keys_sorted_by_value


@mark.parametrize('input_dict, expected_key_list, reverse',
                  [  # input_dict, expected_key_list, reverse
                      ({'a': 1, 'b': 2}, ['a', 'b'], False),
                      ({'a': 2, 'b': 1}, ['b', 'a'], False),
                      ({'a': 1, 'b': 2}, ['b', 'a'], True),
                      ({'a': 2, 'b': 1}, ['a', 'b'], True),
                  ])
def test_transform_dict_into_keys_sorted_by_value(input_dict, expected_key_list, reverse):
    assert expected_key_list == transform_dict_into_keys_sorted_by_value(input_dict, reverse=reverse)
