import re
import cmath
import math
import numpy as np
from collections import defaultdict, Counter
from fractions import Fraction

from common import assert_throw

# 构造单个元素的tuple，需要在元素后面加上逗号
assert isinstance((0,), tuple)
# 但最好还是不要用单个元素的tuple

# 使用raw string来加强字符串的可读性，特别是在写正则表达式的时候
regex = r"\n\\.\\n"
assert re.match(regex, "\n\\.\\n")
# 还需要注意的是，如果raw string的末尾是斜杠，它还是会被认为是转义符

# python也可以实现类似clojure的对list的解构
seq = [1, 2, 3, 4, 5]
x, y, *z = seq
print(x, y, z, sep=" | ")
# 这个带星号的变量不止可以放在末尾，也可以出现在开头或中间，但只能有一个
*a, b, c = seq
print(a, b, c, sep=" | ")
start, *rest, end = seq
print(start, rest, end, sep=" | ")

# 直接使用print打印出list或其他iterable的集合可读性不高，可以使用下面的代码
print(" ".join(str(x) for x in seq))


# 实现一个flatten函数，把嵌套的集合打平成一个简单类型的集合
def flatten(iterable) -> str:  # type: ignore
    return " ".join(
        (flatten if isinstance(x, (list, set, tuple)) else str)(x) for x in iterable
    )


letters = list("hello")
print(flatten([[letters], [letters, 1, 2, (3,)]]))

# 模块可以是一组相关的变量，函数和类的集合，但它也可以作为独立的程序执行
# 每个模块有一个预置的变量__name__，是这个模块的名称
# 但如果直接在命令行执行某个脚本，则__name__固定为main，所以可以通过把模块里的作为单独程序执行的代码放在下面的判断里
if __name__ == "main":
    ...


# Python只为一些内置数据类型提供了比较可读的字符串表示，但对于自定义类型，则需要自己实现__str__或__repr__方法
class Person:
    def __init__(self, gender: str, age: int) -> None:
        self.gender = gender
        self.age = age


person = Person("F", 51)
print(person)
# <__main__.Person object at 0x1039ae120>，这种表示方式可读性很差


# 可以重写__str__方法来改善
class Person2:
    gender: dict[str, str] = {"M": "male", "F": "female"}

    def __init__(self, gender: str, age: int) -> None:
        self._gender = gender
        self.age = age

    def __str__(self) -> str:
        g: str = Person2.gender.get(self._gender, "person")
        return f"{g} {self.age} y/o"


person1 = Person2("F", 51)
person2 = Person2("M", 17)
person3 = Person2("X", 37)
print(person1, person2, person3)
# 但如果自定义类型的对象是其他变量中的一部分，则还需要实现__repr__方法
Person2.__repr__ = Person2.__str__
team = {person1, person2, person3}
print(team)

# 如果要统计一个iterable里的元素个数，可以使用collections模块里的defaultdict
iterable = ["apple", "banana", "orange", "apple", "orange", "banana", "apple"]
counter: defaultdict[str, int] = defaultdict(int)
for item in iterable:
    counter[item] += 1
print(counter.items())

# 也可以使用collections模块里的Counter类来实现同样的功能
# 它继承了dict，并额外添加了一些有用的方法
letter_counts: Counter[str] = Counter("Mary had a little lamb")
letter_counts["l"]
# Counter不止可以对一个Iterable计数，可以通过update方法添加另一个Iterable的计数
letter_counts.update("Hello, world!")
assert letter_counts["l"] == 6
# update方法在处理大数据集的时候很有用，可以使用循环分批处理数据，然后把每一批的结果合并
# 可以使用most_common方法获取出现频率最高的N个元素
print(letter_counts.most_common(3))


# Counter是python里性能最好的计数工具，推荐优先使用它来进行计数操作
# 使用它可以很方便的实现一个判断两个单词是否是同字母异构词的函数
def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)


# int()函数其实可以传两个参数，第一个是要转换的字符串，bytes或bytearray，第二个是进制(0~36)
assert int("10", 2) == 2
assert int("10", 8) == 8
assert int("ff", 16) == 255
# 当传0时，表示的是C-style的数字表示法，可以识别前缀0b, 0o, 0x
assert int("0b10", 0) == 2
assert int("0o10", 0) == 8
assert int("0x10", 0) == 16
# 但把数字转换为字符串只支持二进制，八进制，十进制和十六进制
n = 1234
print(f"{n:b} {n:o} {n:d} {n:x} {n:X}")

# Python是天然支持复数的，复数的虚数部分使用{实数}j/J结尾
assert isinstance(3 + 4j, complex)
assert 1j * 1j == -1
# Python所有的数学函数都支持复数
print((1 + 1j) ** (1 + 1j))
# 如果要使用sin或log这样的函数，可以使用cmath模块
print(cmath.sin(1 + 1j))
print(cmath.log(1 + 1j))
# 但cmath里没有hypot和gamma，但作为补偿，它提供了一些特殊的函数，比如phase函数
print(cmath.phase(1 + 1j))
# 它还提供了rect和polar函数，可以进行极坐标和直角坐标的转换
z = cmath.rect(1, cmath.pi / 4)
print(z)
print(cmath.polar(z))

# Python也支持有理函数，但需要使用fractions模块
print(Fraction(22, 7))
# 使用pi的近似值计算半径为3/4的圆形的面积
print(Fraction(22, 7) * Fraction(3, 4) ** 2)
# 如果Fraction构造函数只传了一个参数，这个参数表示这个数的分子，分母默认为1

# Python中的无穷大可以使用float('inf')或float('-inf')表示
pos_inf = float("inf")
neg_inf = float("-inf")
print(pos_inf, neg_inf)
# 也可以使用math模块里的math.inf
print(math.inf, -math.inf)
# 还可以使用numpy模块里的numpy.inf，它们都是等价的
assert np.inf == float("inf") == math.inf
# Python支持的对无穷数的操作：
# 1.可以使用1/3e-324来得到正无穷大
# 2.可以用它来除，结果是0或一个负0
# 3.可以乘以一个数，结果还是无穷大，除非乘以0，结果是0
# 4.可以减去一个数，结果还是无穷大。一个有限的数减去无穷大，等于无穷小
assert (1 - math.inf) == -math.inf

# 无限大乘以0，无限大减去无限大，无限大除以无限大，得到的都是nan
# Python中有三种nan，分别是float('nan'), math.nan和numpy.nan，但它们是不相等的
# 一样的nan本身也不相等
assert float("nan") != math.nan != np.nan
assert float("nan") != float("nan")
# nan的作用是，可以表示一个本应该有数值但由于某种原因没有值的情况
# math中有isfinite,isinfinite和isnan等用于判断是否是特异值的函数
assert math.isnan(float("nan"))
# 在Python中，使用标准库是无法用0去除以某个数的
assert_throw(ZeroDivisionError, lambda: 1 / 0)

# tuple拥有的方法list几乎都有，但tuple是不可变的，所以对list的那些修改操作tuple都不支持
print(set(dir(list)) - set(dir(tuple)))
# {'clear', '__setitem__', '__iadd__', 'reverse', 'copy', 'pop', 'remove', 'extend', 'append', '__reversed__', '__delitem__', '__imul__', 'insert', 'sort'}
# tuple是Python中为数不多的不可变数据类型之一，所以可以用来存放一组相关的常量
some_constants = (math.pi, math.e, 1, 0)
# tuple字面量可以省略括号
other_constants = math.pi, math.e, 1, 0
# tuple也没有底层机制来进行缩小和扩展操作，所以它的性能相对于list是更高的，特别是当元素数量比较少的时候
# 所以，在能用tuple的地方尽量用tuple来代替list

# Python中没有tree数据结构，但dict可以很方便地用来表示树，而且它的搜索的时间复杂度是O(1)，可以打败所有的树结构
