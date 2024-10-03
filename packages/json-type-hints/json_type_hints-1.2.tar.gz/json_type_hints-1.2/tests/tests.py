import unittest

from test_data import (
    CLS_NAME_1,
    CLS_NAME_2,
    CLS_NAME_3,
    DUMPS_STR,
    INPUT_DICT,
    LOADS_CLS_1_ONLY,
    LOADS_DEFAULT_ONLY,
    LOADS_STR_BAD_PROP,
    TYPE_DICT_CLS1,
    TYPE_DICT_FULL,
    TYPE_DICT_PARTIAL,
)

from src.json_hints import dumps, loads


def encode_classes(obj):
    if isinstance(obj, TYPE_DICT_FULL[CLS_NAME_3]):
        return {"__type__": CLS_NAME_3}
    if type(obj) in TYPE_DICT_FULL.values():
        return {"__type__": type(obj).__name__, "__data__": obj.__dict__}
    return obj


def encode_classes_incomplete(obj):
    if isinstance(obj, TYPE_DICT_FULL[CLS_NAME_2]):
        return {"__type__": type(obj).__name__, "__data__": obj.__dict__}
    return obj


def decode_classes(obj):
    if "__type__" in obj and (_type := obj["__type__"]) in TYPE_DICT_FULL:
        return TYPE_DICT_FULL[_type](**obj.get("__data__", {}))
    return obj


def decode_class1(obj):
    if "__type__" in obj and obj["__type__"] == CLS_NAME_1:
        return TYPE_DICT_FULL[CLS_NAME_1](**obj["__data__"])
    return obj


class MyTestCase(unittest.TestCase):
    def assert_exception_msg(self, exception, expected_msg="__type__"):
        self.assertTrue(expected_msg in str(exception))

    def test_dumps(self):
        self.assertEqual(dumps(INPUT_DICT, encode_types=encode_classes), DUMPS_STR)

    def test_dumps_partially_encoded(self):
        self.assertEqual(dumps(LOADS_DEFAULT_ONLY, encode_types=encode_classes), DUMPS_STR)

    def test_dumps_no_encoder(self):
        with self.assertRaises(expected_exception=TypeError) as cm:
            dumps(INPUT_DICT)
        self.assert_exception_msg(cm.exception, CLS_NAME_2)

    def test_dumps_incomplete_encoder(self):
        with self.assertRaises(expected_exception=TypeError) as cm:
            dumps(INPUT_DICT, encode_types=encode_classes_incomplete)
        self.assert_exception_msg(cm.exception, CLS_NAME_1)

    def test_loads_no_parsers_raise(self):
        with self.assertRaises(TypeError) as cm:
            loads(DUMPS_STR)
        self.assert_exception_msg(cm.exception)

    def test_loads_no_parsers_no_raise(self):
        self.assertEqual(loads(DUMPS_STR, raise_on_unknown=False), LOADS_DEFAULT_ONLY)

    def test_loads_bad_data(self):
        with self.assertRaises(TypeError) as cm:
            loads('{"__type__":"tuple","__data__":null}')
        self.assert_exception_msg(cm.exception, "invalid '__data__'")

    def test_loads_hook(self):
        self.assertEqual(loads(DUMPS_STR, object_hook=decode_classes), INPUT_DICT)

    def test_loads_hook_cls1_raise(self):
        with self.assertRaises(TypeError) as cm:
            loads(DUMPS_STR, object_hook=decode_class1)
        self.assert_exception_msg(cm.exception)

    def test_loads_hook_cls1_no_raise(self):
        self.assertEqual(
            loads(DUMPS_STR, object_hook=decode_class1, raise_on_unknown=False), LOADS_CLS_1_ONLY
        )

    def test_loads_dict(self):
        self.assertEqual(loads(DUMPS_STR, hinted_types=TYPE_DICT_FULL), INPUT_DICT)

    def test_loads_dict_bad_data(self):
        with self.assertRaises(TypeError) as cm:
            loads(LOADS_STR_BAD_PROP, hinted_types=TYPE_DICT_FULL)
        self.assert_exception_msg(cm.exception, "invalid '__data__'")

    def test_loads_dict_cls1_raise(self):
        with self.assertRaises(TypeError) as cm:
            loads(DUMPS_STR, hinted_types=TYPE_DICT_CLS1)
        self.assert_exception_msg(cm.exception)

    def test_loads_dict_cls1_no_raise(self):
        self.assertEqual(
            loads(DUMPS_STR, hinted_types=TYPE_DICT_CLS1, raise_on_unknown=False), LOADS_CLS_1_ONLY
        )

    def test_loads_dict_and_hook(self):
        self.assertEqual(
            loads(DUMPS_STR, hinted_types=TYPE_DICT_PARTIAL, object_hook=decode_class1), INPUT_DICT
        )

    def test_dumps_and_loads(self):
        self.assertEqual(
            loads(dumps(INPUT_DICT, encode_types=encode_classes), hinted_types=TYPE_DICT_FULL),
            INPUT_DICT,
        )


if __name__ == "__main__":
    unittest.main()
