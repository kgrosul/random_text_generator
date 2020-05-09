import pytest
from src import train
from copy import deepcopy


def test_normalize_empty():
    empty_dict = {}
    train.normalize(empty_dict)


def test_normalize_one():
    one_dict = {'a': {'b': 1}}
    another_dict = deepcopy(one_dict)
    train.normalize(one_dict)
    assert one_dict == another_dict


def test_normalize_one_more():
    one_dict = {'a': {'b': 100}}
    another_dict = {'a': {'b': 1}}
    train.normalize(one_dict)
    assert one_dict == another_dict


def test_normalize_many():
    one_dict = {'a': {'b': 1, 'c': 1, 'e': 1, 'd': 1}}
    another_dict = {'a': {'b': 0.25, 'c': 0.25, 'e': 0.25, 'd': 0.25}}
    train.normalize(one_dict)
    assert one_dict == another_dict





