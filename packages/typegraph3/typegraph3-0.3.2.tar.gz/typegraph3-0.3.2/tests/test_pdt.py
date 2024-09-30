from __future__ import annotations

import unittest
import asyncio
from typing import TypeVar, Generic, Callable, Sequence
from typing_extensions import TypedDict
from typegraph.converter.base import PdtConverter, Converter

K = TypeVar("K")
V = TypeVar("V")


class PdtConverterTests(unittest.TestCase):
    def setUp(self):
        self.converter = PdtConverter()

    def test_register_converter(self):
        @self.converter.register_converter(int, str)
        def int_to_str(value: int) -> str:
            return str(value)

        self.assertEqual(int_to_str(10), "10")

    def test_async_register_converter(self):
        @self.converter.async_register_converter(str, int)
        async def str_to_int(value: str) -> int:
            return int(value)

        async def test_async_conversion():
            result = await str_to_int("10")
            self.assertEqual(result, 10)

        asyncio.run(test_async_conversion())

    def test_can_convert(self):
        class Test(int): ...

        self.converter.register_converter(int, str)(str)
        self.converter.register_converter(str, int)(int)

        self.assertTrue(self.converter.can_convert(int, int))

        self.assertTrue(self.converter.can_convert(int, str))
        self.assertTrue(self.converter.can_convert(str, int))

        self.assertFalse(self.converter.can_convert(int, Test))
        self.assertFalse(self.converter.can_convert(Test, int))

        self.assertFalse(self.converter.can_convert(Test, str))

        self.assertFalse(self.converter.can_convert(str, float | int))
        self.assertFalse(self.converter.can_convert(int, float))

    def test_get_converter(self):
        self.converter.register_converter(int, str)(str)
        self.converter.register_converter(str, int)(int)

        result = list(self.converter.get_converter(int, str))
        self.assertEqual(result[0][0], [int, str])
        self.assertEqual(result[0][1](10), "10")

        result = list(self.converter.get_converter(str, int))
        self.assertEqual(result[0][0], [str, int])
        self.assertEqual(result[0][1]("10"), 10)

        # Test Self -> Self
        result = list(self.converter.get_converter(int, int))
        self.assertEqual(result[0][0], [int, int])
        self.assertEqual(result[0][1](10), 10)

    def test_convert(self):
        class Test(int): ...

        self.converter.register_converter(int, str)(str)
        self.converter.register_converter(str, int)(int)

        result = self.converter.convert(10, str)
        self.assertEqual(result, "10")

        result = self.converter.convert("10", int)
        self.assertEqual(result, 10)

        # Test Self -> Self
        result = self.converter.convert(10, int)
        self.assertEqual(result, 10)

        # Test Union Type
        result = self.converter.convert(10, list | str)
        self.assertEqual(result, "10")

        # Test Subclass
        result = self.converter.convert(Test(10), str)
        self.assertEqual(result, "10")

        # Test Structural
        result = self.converter.convert([10], list[str])
        self.assertEqual(result, ["10"])

        # Test Nest Structural
        result = self.converter.convert([[10, "10"]], list[list[Callable | str]])
        self.assertEqual(result, [["10", "10"]])

        # Test Dict Structural
        result = self.converter.convert({"1": 1}, dict[int, str])
        self.assertEqual(result, {1: "1"})

        # Test Nest Dict Structural
        result = self.converter.convert(
            [[{"1": 1}]], list[list[dict[int, Callable | str]]]
        )
        self.assertEqual(result, [[{1: "1"}]])

    def test_combined_converters(self):
        t = PdtConverter()
        c = Converter()
        c1 = Converter()

        def convert_A_T(x):
            return x

        c.register_converter(int, str)(str)
        c1.register_converter(int, str)(convert_A_T)

        t.add_converter(c)
        t.add_converter(c1)

        result = t.convert((1, 2, 3), Sequence[str])
        self.assertEqual(result, (1, 2, 3))

        result = t.convert(10, str)
        self.assertEqual(result, 10)

        result = t.convert(10, str)
        self.assertEqual(result, 10)

    def test_async_combined_converters(self):
        t = PdtConverter()
        c = Converter()
        c1 = Converter()

        c.register_converter(int, str)(str)

        t.add_converter(c)

        async def test_async_conversion():
            result = await t.async_convert((1, 2, 3), Sequence[str])
            self.assertEqual(result, ("1", "2", "3"))

            result = await t.async_convert(10, str)
            self.assertEqual(result, "10")

        asyncio.run(test_async_conversion())

    def test_async_get_converter(self):
        class Test(int): ...

        async def async_str2int(value: str) -> int:
            return int(value)

        self.converter.register_converter(int, str)(str)

        self.converter.async_register_converter(str, int)(async_str2int)

        async def test_async_get_converter():
            # result = list(self.converter.async_get_converter(int, str))
            async for path, converter in self.converter.async_get_converter(int, str):
                self.assertEqual(path, [int, str])
                self.assertEqual(await converter("10"), "10")
                break

            async for path, converter in self.converter.async_get_converter(str, int):
                self.assertEqual(path, [str, int])
                self.assertEqual(await converter("10"), 10)
                break

            # Test Self -> Self
            async for path, converter in self.converter.async_get_converter(int, int):
                self.assertEqual(path, [int, int])
                self.assertEqual(await converter(10), 10)
                break

        asyncio.run(test_async_get_converter())

    def test_async_convert(self):
        class Test(int): ...

        async def async_str2int(value: str) -> int:
            return int(value)

        self.converter.register_converter(int, str)(str)

        self.converter.async_register_converter(str, int)(async_str2int)

        async def test_async_conversion():
            result = await self.converter.async_convert("10", int)
            self.assertEqual(result, 10)

            result = await self.converter.async_convert(10, str)
            self.assertEqual(result, "10")

            # Test Self -> Self
            result = await self.converter.async_convert(10, int)
            self.assertEqual(result, 10)

            # Test Union Type
            result = await self.converter.async_convert(10, list | str)
            self.assertEqual(result, "10")

            # Test Subclass
            result = await self.converter.async_convert(Test(10), str)
            self.assertEqual(result, "10")

            # Test Structural
            result = await self.converter.async_convert([10], list[str])
            self.assertEqual(result, ["10"])

            # Test Nest Structural
            result = await self.converter.async_convert(
                [[10, "10"]], list[list[list | str]]
            )
            self.assertEqual(result, [["10", "10"]])

            # Test Dict Structural
            result = await self.converter.async_convert({"1": 1}, dict[int, str])
            self.assertEqual(result, {1: "1"})

            # Test Nest Dict Structural
            result = await self.converter.async_convert(
                [[{"1": 1}]], list[list[dict[int, Callable | str]]]
            )
            self.assertEqual(result, [[{1: "1"}]])

        asyncio.run(test_async_conversion())

    def test_auto_convert(self):
        t = self.converter

        class Test:
            def __init__(self, t):
                self.t = t

        class Test2(int): ...

        @t.register_converter(str, int)
        def str_to_int(input_value):
            return int(input_value)

        @t.register_converter(int, str)
        def int_to_str(input_value):
            return str(input_value)

        @t.register_converter(int, float)
        def int_to_float(input_value):
            return float(input_value)

        @t.register_converter(float, str)
        def float_to_str(input_value):
            return str(input_value)

        @t.register_converter(float, Test)
        @t.register_converter(int, Test)
        @t.register_converter(str, Test)
        def str_int_float_to_Test(input_value):
            return Test(input_value)

        @t.register_converter(Test, float)
        def Test_to_float(input_value):
            return float(input_value.t)

        @t.register_converter(str, float)
        def str_to_float(input_value):
            return float(input_value)

        @self.converter.async_register_converter(dict[K, V], dict[V, K])
        async def reverse_dict(d: dict[K, V]) -> dict[V, K]:
            return {v: k for k, v in d.items()}

        @self.converter.auto_convert(localns=locals())
        def test_float_to_str(x: Test):
            return x.t

        @self.converter.auto_convert()
        def test_switch(x: str):
            return x

        @self.converter.auto_convert()
        def add_one(x: int) -> int:
            return x + 1

        @self.converter.auto_convert()
        def test_union(x: list | float):
            return x

        @self.converter.auto_convert()
        def test_structural(x: list[str]):
            return x

        @self.converter.auto_convert()
        def test_next_structural(x: list[dict[str, int]]):
            return x

        result = test_float_to_str("10")
        self.assertEqual(result, "10")

        result = test_switch(Test("10.0"))
        self.assertEqual(result, "10.0")

        result = add_one(10)
        self.assertEqual(result, 11)

        result = test_union(10)
        self.assertEqual(result, 10)

        result = test_switch(10)
        self.assertEqual(result, "10")

        result = test_switch(Test2(10))
        self.assertEqual(result, "10")

        result = test_structural([1, 2, 3])
        self.assertEqual(result, ["1", "2", "3"])

        result = test_next_structural([{1: "1"}, {2: "2"}, {3: "3"}])
        self.assertEqual(result, [{"1": 1}, {"2": 2}, {"3": 3}])

    def test_auto_convert_protocol(self):
        from typing import Protocol, TypedDict
        from dataclasses import dataclass

        t = self.converter

        class Person(Protocol):
            name: str
            phone: str
            address: str

            def get_name(self) -> str: ...

        class PersonDict(TypedDict):
            name: str
            phone: str
            address: str

        class A:
            name: str
            phone: str
            address: str

            def __init__(self, name: str, phone: str, address: str):
                self.name = name
                self.phone = phone
                self.address = address

            def get_name(self) -> str:
                return self.name

        @dataclass
        class B:
            name: str
            phone: str
            address: str

        @t.register_converter(dict, PersonDict)
        def convert_dict_to_persondict(data: dict):
            return PersonDict(
                name=data["name"], phone=data["phone"], address=data["address"]
            )

        @t.register_converter(Person, str)
        def convert_person_to_str(data: Person):
            return f"{data.name} {data.phone} {data.address}"

        @t.register_converter(dict, A)
        def convert_dict_to_a(data: dict):
            return A(data["name"], data["phone"], data["address"])

        @t.register_converter(dict, B)
        def convert_dict_to_b(data: dict):
            return B(data["name"], data["phone"], data["address"])

        @t.auto_convert()
        def test(a: str):
            return a

        @t.auto_convert()
        def tests(a: list[str]):
            return a

        d = {"name": "John", "phone": "123", "address": "123"}

        result = test(d)
        self.assertEqual(result, "John 123 123")

        result = tests([d])
        self.assertEqual(result, ["John 123 123"])

    def test_auto_convert_generic(self):
        t = self.converter

        class A: ...

        class B(Generic[K, V]): ...

        @t.register_converter(list[dict[str, int]], A)
        def convert_list_dict_to_a(data: list[dict[str, int]]):
            return A()

        @t.register_generic_converter(dict[K, V], dict[V, K])  # type: ignore
        def convert_dict(data: dict[K, V]):
            return {v: k for k, v in data.items()}

        @t.register_generic_converter(dict[V, K], B[V, K])  # type: ignore
        def convert_dict_to_b(data: dict[V, K]):
            return B[V, K]()

        @t.auto_convert(localns=locals())
        def test_generic(a: "B[str, int]"):
            return a

        result = test_generic({1: "1", 2: "2"})
        self.assertIsInstance(result, B)

        result = test_generic({"1": 1, "2": 2})
        self.assertIsInstance(result, B)

    def test_async_auto_convert(self):
        t = self.converter

        class Test:
            def __init__(self, t):
                self.t = t

        class Test2(int): ...

        @t.register_converter(str, int)
        def str_to_int(input_value):
            return int(input_value)

        @t.register_converter(int, str)
        def int_to_str(input_value):
            return str(input_value)

        @t.register_converter(int, float)
        def int_to_float(input_value):
            return float(input_value)

        @t.register_converter(float, str)
        def float_to_str(input_value):
            return str(input_value)

        @t.register_converter(float, Test)
        @t.register_converter(int, Test)
        @t.register_converter(str, Test)
        def str_int_float_to_Test(input_value):
            return Test(input_value)

        @t.register_converter(Test, float)
        def Test_to_float(input_value):
            return float(input_value.t)

        @t.register_converter(str, float)
        def str_to_float(input_value):
            return float(input_value)

        @t.async_auto_convert(localns=locals())
        async def test_float_to_str(x: Test):
            return x.t

        @t.async_auto_convert()
        async def test_switch(x: str):
            return x

        @t.async_auto_convert()
        async def add_one(x: int) -> int:
            return x + 1

        @t.async_auto_convert()
        async def test_union(x: list | float):
            return x

        @t.async_auto_convert()
        async def test_structural(x: list[str]):
            return x

        @t.async_auto_convert()
        async def test_next_structural(x: list[dict[str, int]]):
            return x

        async def test_async_conversion():
            result = await test_float_to_str("10")
            self.assertEqual(result, "10")

            result = await test_switch(Test("10.0"))
            self.assertEqual(result, "10.0")

            result = await add_one(10)
            self.assertEqual(result, 11)

            result = await test_union(10)
            self.assertEqual(result, 10)

            result = await test_switch(10)
            self.assertEqual(result, "10")

            result = await test_switch(Test2(10))
            self.assertEqual(result, "10")

            result = await test_structural([1, 2, 3])
            self.assertEqual(result, ["1", "2", "3"])

            result = await test_next_structural([{1: "1"}, {2: "2"}, {3: "3"}])
            self.assertEqual(result, [{"1": 1}, {"2": 2}, {"3": 3}])

        asyncio.run(test_async_conversion())

    def test_async_auto_convert_protocol(self):
        from typing import Protocol, TypedDict
        from dataclasses import dataclass

        t = self.converter

        class Person(Protocol):
            name: str
            phone: str
            address: str

            def get_name(self) -> str: ...

        class PersonDict(TypedDict):
            name: str
            phone: str
            address: str

        class A:
            name: str
            phone: str
            address: str

            def __init__(self, name: str, phone: str, address: str):
                self.name = name
                self.phone = phone
                self.address = address

            def get_name(self) -> str:
                return self.name

        @dataclass
        class B:
            name: str
            phone: str
            address: str

        @t.register_converter(dict, PersonDict)
        def convert_dict_to_persondict(data: dict):
            return PersonDict(
                name=data["name"], phone=data["phone"], address=data["address"]
            )

        @t.register_converter(Person, str)
        def convert_person_to_str(data: Person):
            return f"{data.name} {data.phone} {data.address}"

        @t.register_converter(dict, A)
        def convert_dict_to_a(data: dict):
            return A(data["name"], data["phone"], data["address"])

        @t.register_converter(dict, B)
        def convert_dict_to_b(data: dict):
            return B(data["name"], data["phone"], data["address"])

        @t.auto_convert()
        async def test(a: str):
            return a

        @t.auto_convert()
        async def tests(a: list[str]):
            return a

        async def test_async_conversion_protocol():
            d = {"name": "John", "phone": "123", "address": "123"}

            result = await test(d)
            self.assertEqual(result, "John 123 123")

            result = await tests([d])
            self.assertEqual(result, ["John 123 123"])

        asyncio.run(test_async_conversion_protocol())

    def test_async_auto_convert_generic(self):
        t = self.converter

        class A: ...

        class B(Generic[K, V]): ...

        @t.register_converter(list[dict[str, int]], A)
        def convert_list_dict_to_a(data: list[dict[str, int]]):
            return A()

        @t.register_generic_converter(dict[K, V], dict[V, K])  # type: ignore
        def convert_dict(data: dict[K, V]):
            return {v: k for k, v in data.items()}

        @t.register_generic_converter(dict[V, K], B[V, K])  # type: ignore
        def convert_dict_to_b(data: dict[V, K]):
            return B[V, K]()

        @t.auto_convert(localns=locals())
        async def test_generic(a: "B[str, int]"):
            return a

        async def test_async_auto_convert_generic():
            result = await test_generic({1: "1", 2: "2"})
            self.assertIsInstance(result, B)

            result = await test_generic({"1": 1, "2": 2})
            self.assertIsInstance(result, B)

        asyncio.run(test_async_auto_convert_generic())

    def test_obj_subclass_outside_converter(self):
        class Test(TypedDict):
            name: str
            age: int

        obj = {"name": "John", "age": 20, "extra": "extra"}
        self.assertEqual(self.converter.convert(obj, Test), obj)


if __name__ == "__main__":
    unittest.main()
