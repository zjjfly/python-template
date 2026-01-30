import ast
import math

from common import assert_throw  # type: ignore

# Python中，在函数的变量如果没有global修饰，都是本地变量
gv = 1


def f1() -> int:
    # global表示gv是指的全局变量，而不是本地变量
    global gv
    gv += 1
    return gv


print(f1(), gv)


def f2() -> int:
    # 没有声明而直接访问一个变量，会认为这个变量是global变量
    return gv + 1


print(f2())


# 如果赋值语句的左边的变量名和已有的global变量一样，会shadow这个global变量
# 这种写法比较危险，会让人以为修改了global变量的值
def f3() -> int:
    gv = -1
    return gv


print(f3())


# Python中，有很多值会被认为是逻辑上False的，如None，空集合，0，0.0，0j等
# 可以重写类型的__len__方法来让这个类的对象可以直接当作bool类型进行逻辑判断
class GlassIsHalfEmpty:
    def __init__(self, mood: str):
        self.mood = mood

    def __len__(self) -> int:
        return 1 if self.mood == "pessimist" else 0


assert bool(GlassIsHalfEmpty("pessimist"))
assert not bool(GlassIsHalfEmpty("optimist"))
# 所以，不要直接用某个值是否等于True/False来判断，而是直接作为逻辑表达式使用，因为if可以识别各种类型的值

# 不要使用in来判断某个数是否在一个range中
# 因为range()返回的是一个iterable，其中存放的是在这个范围内的整数
# 所以如果要判断一个浮点数是否在这个范围中，需要使用比较操作符
assert 5 in range(10)
assert 0 <= 5.5 < 10

# 对于用户输入，最好调用strip来清空前后的空格
input("Enter your name: ").strip()

# 使用with来保证文件会被自动关闭，但如果代码全部都在with中，那么还是需要显式地调用close函数关闭
# with可以打开多个文件
with open(".gitignore") as a_file, open("pyproject.toml") as b_file:
    print(a_file.fileno())
    print(b_file.fileno())


# Python的类的字段或方法以__开头的表示是private的，无法直接访问或修改，而是需要实现setter和getter方法
# 通过这种方法，可以保证对这些字段的访问和修改是合法的
class BetterCircle:
    def __init__(self, r: float):
        self.__r: float = r
        self.__area: float = math.pi * r * r

    def get_radius(self) -> float:
        return self.__r

    def get_area(self) -> float:
        return self.__area

    def set_radius(self, r: float) -> None:
        if r < 0:  # Is it valid?
            raise ValueError("Invalid radius")
        self.__r = r
        self.__area = math.pi * r * r


my_circle = BetterCircle(10)
# 直接访问private字段会报错
assert_throw(AttributeError, lambda: my_circle.__r)  # type: ignore
# 修改private字段不会生效
my_circle.__r = -20
assert 10 == my_circle.get_radius()
# 使用setter就没问题
my_circle.set_radius(1)
assert 1 == my_circle.get_radius()


# property是一个内置类型，可用于包装private字段供外部进行访问和修改，但实际调用的是构造property的时候传入的getter和setter
class Person:
    def __init__(self, new_age: int):
        self.set_age(new_age)

    def get_age(self) -> int:
        return self.__age

    def set_age(self, new_age: int) -> None:
        if not 0 <= new_age <= 122:
            raise ValueError("Age out of range")
        self.__age = new_age

    age: property = property(get_age, set_age)


assert_throw(ValueError, lambda: Person(189))

jeanne = Person(122)
assert 122 == jeanne.age
try:
    jeanne.age += 1
except ValueError as e:
    assert e.args == ("Age out of range",)


# 但实际对property的使用把它作为decorator
class Person2:
    def __init__(self, new_age: int):
        self.age = new_age  # 这里实际调用的setter

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, new_age: int) -> None:
        if not 0 <= new_age <= 122:
            raise ValueError("Age out of range")
        self.__age = new_age


# 使用assert可以用来检查某个条件是否成立，这样可以预防程序在运行时出现不可预期的错误
# 使用-O参数运行Python程序时，assert语句会被忽略

# 不要轻易使用eval，因为eval会执行传入的字符串，可能会带来安全隐患
# 但如果真的需要把字面量字符串（字符串，数字，list，tuple，dict，set，bool，None）转换为对应的Python对象，可以使用ast.literal_eval
assert {"a": 1.1, "b": (2, 2), "c": [1, 2, 3], "d": False} == ast.literal_eval(
    '{"a": 1.1, "b": (2,2), "c": [1,2,3],"d": False}'
)

# Python中所有的变量都是引用，所以有时候会因此出现一些意想不到的错误
board = [[" "] * 3] * 3
assert board == [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
board[0][0] = "X"
assert board == [["X", " ", " "], ["X", " ", " "], ["X", " ", " "]]  # 不是想要的结果
# 这是因为使用*来初始化board时，实际上是创建了3个对同一个list对象的引用
# 正确的写法是使用列表推导式
board = [[" "] * 3 for _ in range(3)]
assert board == [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
board[0][0] = "X"
assert board == [["X", " ", " "], [" ", " ", " "], [" ", " ", " "]]

# Pythonic的编程风格推荐用try-except来包含可能会抛出异常的代码，而是包裹一大片代码
# 如果一个表达式会抛出多种异常，要对每一种错误分别进行处理
try:
    with open("somefile.txt") as infile:
        # Read the file
        data = "\n".join(infile.readlines())
except (FileNotFoundError, IsADirectoryError, PermissionError):
    # These are specific errors that you may be able to handle
    # Handle them!
    ...
except IOError:
    # These are other non-specific I/O errors
    # Give up?
    ...

# 使用startswith和endswith来判断字符串的前缀和后缀
s = "auto-movement"
if s.lower().startswith("auto"):  # starts with 'auto-'
    ...
if s.lower().endswith("ment"):  # ends with 'ment'
    ...


# is相当于Java中的==, 用于判断两个变量是否引用同一个对象
# 而==相当于Java中的equals, 用于判断两个变量的值是否相等


# type()返回的是对象的直接类型，而isinstance()会检查对象的整个继承链
# isinstance的第二个参数可以是一个类型元组，表示检查对象是否是这些类型中的某一个
def my_len(x: object) -> int:
    if isinstance(x, (str, list, tuple, map, dict)):
        return len(x)  # type: ignore
    if isinstance(x, (bool, int, float, complex)):
        return abs(x)  # type: ignore
    raise Exception("x has no length")


# split方法如果不带参数，会自动去掉字符串前后的空白字符，并以任意长度的空白字符作为分隔符
assert "Mary     had a little lamb".split() == ["Mary", "had", "a", "little", "lamb"]
# 但不要用这个方法来对自然语句进行分词，而是要使用nltk等自然语言处理库
