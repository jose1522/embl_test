import fakeredis
from unittest import TestCase
from util.caching import Cache


class TestCache(TestCase):

    def setUp(self) -> None:
        self.conn = fakeredis.FakeStrictRedis()
        self.cache = Cache(self.conn)

    def tearDown(self) -> None:
        self.conn.close()

    def test_exists(self):
        test = "test"
        self.cache.exists(test)

    def test_keep(self):
        expected = {"hello": "world"}
        self.cache.keep("test", expected)
        result = self.cache.exists("test")
        self.assertEqual(expected, result)

    def test_flush(self):
        test = {"hello": "world"}
        self.cache.keep("test", test)
        self.cache.flush()
        result = self.cache.exists("test")
        self.assertIs(result, None)