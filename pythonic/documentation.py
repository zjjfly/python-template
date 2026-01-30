import __hello__  # This will print "Hello world!" when the module is imported
import enum
import this  # This will print "The Zen of Python" when the module is imported

# 在Python REPL中，可以使用函数copyright()来查看版权信息，credits()来查看贡献者信息，license()来查看许可证信息。

# Python可以使用\来把一行代码拆分成多行，以提高代码的可读性。例如：
n = 1 + 2 + 3 + 4 + 5 + 6
s = "Hello, World!"
ss = s.lower().strip().split()
# 如果有未关闭的(, [, {，Python会自动将代码行连接在一起，无需使用反斜杠。例如：
int_list = [1, 2, 3, 4, 5, 6]
# 还可以在字符串中使用\换行
print(
    "Hello, \
       World!"
)

# Python的docstring用于为模块、类和函数提供文档说明。docstring一般使用三重引号括起来，但也可以使用双引号或单引号。
# 它可以通过访问模块、类和函数的__doc__属性来查看。
print(len.__doc__)
# 还可以使用help()函数来查看docstring
# help(len)

# docstring应该只用于解释模块、类和函数的目的以及如何使用它们，而不应该包含实现细节。
# 实现细节应该使用注释来说明。注释使用#符号开头，直到行尾结束。

# 不要使用magic value，而应该使用常量来代替。如：
PI = 3.14159
# 即使值相同，如果含义不同，也要声明为不同的常量
N_COLUMNS = 3
N_ROWS = 3


# 另一种避免magic value的方法是使用枚举（enum）来表示一组相关的常量。例如：
class TrafficLightState(enum.Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3
    OFF = 4


# 如果不关心枚举的值，可以使用auto()函数自动分配值
class TrafficLightState2(enum.Enum):
    RED = enum.auto()
    YELLOW = enum.auto()
    GREEN = enum.auto()
    OFF = enum.auto()
