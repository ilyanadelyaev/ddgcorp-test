import django.test

import ddgcorp.tools.enum


class TestEnum(ddgcorp.tools.enum.Enum):
    var_1 = 0
    var_2 = 1
    choices = (
        (var_1, 'var 1'),
        (var_2, 'var 2'),
    )


class EnumTests(django.test.TestCase):
    def test__call(self):
        assert TestEnum(TestEnum.var_1) == 'var 1'
        assert TestEnum(TestEnum.var_2) == 'var 2'

    def test__iter(self):
        data = [e for e in TestEnum]
        assert data == [TestEnum.var_1, TestEnum.var_2]
