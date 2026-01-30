from common import assert_throw
from typing import Any, Generator
import random

# 函数最好是返回一致的类型，无论其输入如何变化
# 如果是悲观主义者，那你要定义一个表示失败的特殊值，而且必须和正常返回值类型一致
assert 0 == "abc".find("a")
assert -1 == "abc".find("d")
# 如果是乐观主义者，那就直接让它在输入不符合预期时抛出异常
assert "abc".index("a") == 0
assert_throw(ValueError, lambda: "abc".index("d"))


# 对于一些通用的函数，不要在里面打印出其返回结果或做其他类似的操作，而是让调用者决定如何处理返回值
# 如果实在需要打印（比如调试时），那就加一个可选参数来控制是否打印
def add1(x: int, debug: bool = False) -> int:
    if debug:
        print(x + 1)
    return x + 1


# 返回多个值的函数实际上是返回一个元组
def aFuncThatReturnsValues():
    return 1, 2, 3, 4


assert isinstance(aFuncThatReturnsValues(), tuple)


# 函数的位置参数如果有默认值，最好把这些参数放在最后，因为第一次出现默认值的参数后面的参数都必须有默认值
def addWithCarry(a: int, b: int, carry: int = 0):
    s = a + b + carry
    return s % 2, s // 2


# 在位置参数之后，可以加可选的位置参数*args和关键字参数**kwargs，它们都最多只能出现一次
def add_all(a: int, *args: list[int]) -> int:
    return a + sum(args)  # type: ignore


# 对于关键字参数，需要考虑当调用者没有传入该参数时的默认行为，一般是会提供一个默认值
def addWithCarry_kw(a: int, b: int, **kwargs: Any) -> tuple[int, int]:
    carry: int = kwargs.get("carry", 0)
    s: int = a + b + carry
    return s % 2, s // 2


# Python比较偏好把函数的链式调用写在一行里，而不是定义多个中间变量
text = "Hello, World!"
print(len(text.strip().lower().split()))


# generator可以惰性地一个个的产生对象
def fortune_teller(attempts: int = 2):
    for _ in range(attempts):
        yield bool(random.randint(0, 1))
    return "Do not call me again!"


oracle = fortune_teller(2)
# next函数可以返回generator的下一个值
assert next(oracle) in (True, False)
assert next(oracle) in (True, False)
# 当generator没有更多值可产出时，next会抛出StopIteration异常
assert_throw(StopIteration, lambda: next(oracle))
# 但如果你提供一个默认值参数给next，则不会抛出异常，而是返回该默认值
assert next(oracle, True)
# 可以使用list函数一次取出generator的所有值
oracle = fortune_teller(2)
print(list(oracle))


# generator可以实现一个无穷的序列
def bottomless_mug() -> Generator[str, None, None]:
    count = 1
    while True:  # No return
        yield f"Coffee #{count}"
        count += 1


for coffee in bottomless_mug():
    print(coffee)
    if "3" in coffee:
        break

# lambda适合用在一个statement中应用很多次的场景
print(list(map(len, "Mary had a little lamb".split())))
# 但对于Python来说，lambda实际上不是必须的，上面的代码就可以使用列表推导式来实现，而且性能更好
