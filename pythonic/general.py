import pickle
import re
import string
import random
import itertools
import glob
import io
from typing import Any, Generator

# 使用串连的比较操作符
a = 5
if 1 < a < 10:
    print("a 在 1 和 10 之间")

# str.expandtabs方法可以智能地计算出制表符停止的位置，适用于固定宽度的文本对齐
print("column1\tcol2\tc3".expandtabs(8))

# 有时候，需要把一些中间结果保存到文件中，比如CSV，JSON，XML等格式
# 但有些对象并不容易转成字符串或二进制数组（序列化），而反序列化也同样困难
# 这时可以使用pickle模块来完成对象的序列化和反序列化
anyPythonObject: dict[str, Any] = {"key1": [1, 2, 3], "key2": ("a", "b", "c")}
with open("results.p", "wb") as pickleFile:
    pickle.dump(anyPythonObject, pickleFile)
with open("results.p", "rb") as pickleFile:
    obj = pickle.load(pickleFile)
    assert obj == anyPythonObject

# 不要在循环中使用range(len(sequence))来迭代序列，无论你是不是需要使用索引
seq = ["a", "b", "c", "d"]
for i in range(len(seq)):
    print(seq[i])
# 不需要索引可以直接迭代
for item in seq:
    print(item)
# 需要索引可以使用enumerate
for index, item in enumerate(seq):
    if index % 2 == 0:
        print(item)
# 如果要进行parallel迭代，可以使用zip
seq2 = [1, 2, 3, 4]
for item1, item2 in zip(seq, seq2):
    print(item1, item2)


# 如果不想在复合声明（class,for,if, while, try等）的body中任何代码，可以使用pass语句作为占位符
class EmptyClass:
    pass


# 有两种方式去写一段有可能报错的代码：乐观方式和悲观方式
# 悲观方式假定错误是容易发生且代价高昂的，所有会使用条件语句去检查每一个可能出错的地方
def string_to_float(s: str) -> float:
    if re.match(r"^-?\d+(\.\d+)?$", s):
        return float("nan")
    return float(s)


# 乐观方式假定错误是很少发生且代价低廉的，所以直接尝试执行代码，并在出现异常时进行处理
def string_to_float2(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        return float("nan")


# 使用哪种方式取决于三点：检查的复杂性，发生错误的后果，以及编码习惯

# Python除了list comprehensions，还有dict和set comprehensions
{c for c in "Mary had a little lamb" if c in string.ascii_letters}
s = "Mary had a little lamb"
{pos + 1: c for pos, c in enumerate(s) if c in string.ascii_letters}
# 那么使用()是什么comprehension呢？答案是generator comprehension，或者叫lazy list comprehension
gen = (c for c in s if c in string.ascii_letters)
assert isinstance(gen, Generator)


# 使用conditional expression来代替简单的if-else语句，特别是当只能使用一个表达式的情况（如在list comprehensions中）
WORDS = s.split()
print([(word.upper() if word and word[0].isupper() else word) for word in WORDS])

# Python没有switch，但可以使用if...elif..else来模拟
choice: int = random.randint(0, 99)
if choice == 0:
    print("You chose zero.")
elif choice == 1:
    print("You chose zero.")
elif choice == 99:
    print("You chose ninety-nine.")
else:
    print("You chose something else.")


# 这种写法支持任意的比较操作，而不只是等于操作
# 如果对于不同的分支调用不同的函数，可以使用一个dict
def make_computer_move(): ...


def make_human_move(): ...


def report_error(): ...


actions = {0: make_computer_move, 1: make_human_move}
actions.get(choice, report_error)()
# 这种写法在函数的参数都一致的时候是最好的，但如何它们的参数签名不一样，可以使用一个变量存放位置参数，一个变量存放关键字参数
positional = []
keyword = {}
actions.get(choice, report_error)(*positional, **keyword)

# 使用slice操作来实现string的reverse
print(s[::-1])
# 当step>0时，默认的起始index是0，当step<0时，默认的起index是-1

# sum除了对一个数字的集合求和之外，还可以连接多个数组
print(sum([(1, 2, 3), (4, 5, 6)], ()))
# 但这种操作的性能没有itertools.chain.from_iterable()好，而且它返回的是一个generator
print(itertools.chain.from_iterable([(1, 2, 3), (4, 5, 6)]))

# 实现一个Tic-Tac-Toe游戏，首先要构建一个3x3的矩阵
SIZE = 3
field = [[" "] * SIZE for _ in range(SIZE)]
field[0][0] = "x"
field[0][1] = "x"
field[0][2] = "x"
print(field)
# 下面的代码可以判断任一个row是否满足条件
win = any(row.count("x") == SIZE or row.count("o") == SIZE for row in field)
# 那如果需要验证任一个column是否满足条件呢？你需要进行矩阵的转置，这时候可以使用zip函数
transposed = zip(*field)
print(list(transposed))

# string模块中有预置的各种类型的字符串的常量
# assic码
print(string.ascii_letters)
print(string.ascii_lowercase)
print(string.ascii_uppercase)
# 数字
print(string.digits)
print(string.hexdigits)
print(string.octdigits)
# 可打印的字符串
print(string.printable)
# 标点符号
print(string.punctuation)
# 空白字符
print(string.whitespace)
# 如果要用于判断某个字符是否属于某个类型，那么最好是先把字符串集合放入set中
set_punct = set(string.punctuation)
print("".join([x for x in "Hello, world!" if x not in set_punct]))

# glob模块的glob方法可以和shell的ls命令一样列出满足某个pattern的文件
print(glob.glob("*.toml"))
# 可以使用**和参数recursive来列出所有的python源文件
print(glob.glob("**/*.py", recursive=True, include_hidden=True))

# 有些函数接收一个文件作为参数，读取其中的内容。
# 但如果现在只有字符串，可以使用io模块的StringIO来把字符串包装
with io.StringIO("Hello,\nworld!") as source:
    print(source.readlines())
# 也可以把io.StringIO作为一个输入的文件
with io.StringIO() as dest:
    dest.write("Hello,\n")
    dest.write("World!")
    # 可以使用getvalue方法获取其中的字符串
    print(dest.getvalue())


# str方法和repr方法的区别是,str返回的是对象的human readable的表示
# repr返回的是eval方法可执行来构建相同对象的代码
