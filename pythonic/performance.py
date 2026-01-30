import gc
import hashlib
import pickle
import timeit
import traceback
from pathlib import Path

# 使用timeit模块来测量代码性能
# timeit函数的第一个参数是要测试的代码的字符串
# 第二个参数是setup代码的字符串，在执行测试代码之前运行
# 下面是测试几种计算数的平方的方法的性能
print(timeit.timeit("a ** 2", "a = 10.0"))
print(timeit.timeit("a ** a", "a = 10.0"))
print(timeit.timeit("math.pow(a, 2)", "import math; a = 10.0"))

# 尽量避免函数调用，如果使用内联代码不是很影响可读性和可维护性的话
# 如果确实有影响，那么使用timeit看一下两种实现的性能，如果无函数的解决方案明显性能好很多，那么还是使用它

# 尽量少调用print函数，因为print函数是IO操作，开销比较大
for _ in range(1000):
    print("a", end="")
print()
# 应该先把要打印的内容都准备好，然后一次性调用print函数
a = 1000 * "a"
print(a)

# Python使用in来查找元素是否在集合中，但不同集合的查找的效率是不一样的
# list是查找是最慢的，因为在最坏的情况下，需要遍历整个列表
print(timeit.timeit("1001 in haystack", "haystack = list(range(1000))"))
# 4.825605541991536
# tuple也一样糟糕，因为它和list的底层结构类似
print(timeit.timeit("1001 in haystack", "haystack = tuple(range(1000))"))
# 4.159789249999449
# dict和set的查找效率要高得多，因为它们使用哈希函数来定位元素
print(
    timeit.timeit(
        "1001 in haystack", "haystack=dict(enumerate(range(1000)))", number=100000000
    )
)
# 1.260945707996143
print(
    timeit.timeit("1001 in haystack", "haystack = set(range(1000))", number=100_000_000)
)
# 1.2079626249906141

# 一种常用的提高性能的方式是缓存。除了使用常用的如Redis这样的缓存数据库或基于内存的缓存，还可以把要缓存的数据存入一个文件中。
# 要产生这样的文件，首先要给给它一个统一且唯一的命名
source = "https://lj-dev.livejournal.com/653177.html"
hash = hashlib.sha256(source.encode())
filename = hash.hexdigest()
print(filename)
# 接着把要缓存的数据使用pickle序列化写入文件
cache_dir = Path("cache")
if not cache_dir.exists():
    cache_dir.mkdir()
cache = cache_dir / f"{filename}.p"
try:
    with open(cache, "rb") as infile:
        # Has been pickled before! Simply unpickle
        object = pickle.load(infile)
except FileNotFoundError:
    # Download and pickle
    object = {a: 1}
    cache.touch()
    with open(cache, "wb") as outfile:
        pickle.dump(object, outfile)
except Exception as e:
    traceback.print_exception(e)
    print("Things happen...")


# 当要运行一个有很多步骤且有些步骤非常耗时的任务，某个步骤的失败会导致整个任务失败。
# 为了能实现重试的时候跳过之前已经完成的步骤，可以把关键步骤的结果存入文件
checkpoints_dir = Path("checkpoints")
if not checkpoints_dir.exists():
    checkpoints_dir.mkdir()


def checkpoint(filename):  # type: ignore
    checkpoint_file = checkpoints_dir / f"{filename}.p"

    def checkpoint(func):  # type: ignore
        def wrapper(*args, **kwargs):  # type: ignore
            try:
                with open(checkpoint_file, "rb") as infile:
                    result = pickle.load(infile)
            except FileNotFoundError:
                result = func(*args, **kwargs)  # type: ignore
                with open(checkpoint_file, "wb") as outfile:
                    pickle.dump(result, outfile)

        return wrapper  # type: ignore

    return checkpoint  # type: ignore


@checkpoint("foo")
def foo(s: str):
    s.upper()


foo("xyz")

# Python中有两个排序相关的函数：list.sort()和sorted()
# 前者是直接在原有的list中进行排序，适用于需要对存放了很多元素的list的场景
# 后者会返回一个新的排好序的集合，不会改变原始的集合，适用于元素数量不多或需要保留原始的集合的顺序的场景

# Python有垃圾收集器，它使用的垃圾回收算法是引用计数。
# 使用del可以把某个变量标记为已删除，这样垃圾收集器在运行时会回收它
bigdata = [1, 2, 3]
del bigdata
# 但del不会马上让它被回收，如果想要达到这个效果，需要手动调用垃圾收集器
gc.collect()
# 但collect方法比较耗时，所以只在真正需要的时候调用它

# Python一个特性是支持无限的整数，即变量可以赋予很大或很小的整数
big_int = 10**100
big_int2 = big_int + 1
print(big_int2)
# 但这不是没有代价的，这种整数的操作的性能不高，相比于浮点数运算
# 因为整数运算需要的精确的结果，而浮点数只要近似的结果
print(timeit.timeit("10**100 * 10**100"))
# 0.9552337079658173
print(timeit.timeit("10.**100 * 10.**100"))
# 0.014541708980686963

# Python提供了很多很棒的内置数据类型，但也不能满足所有的需求，有时候需要使用多种数据结构来完成任务
# 对一个list进行去重并保持原来的顺序
data = [7, 2, 3, 4, 7, 7, 7]
dups: set[int] = set()
result: list[int] = []
for d in data:
    if d not in dups:
        dups.add(d)
        result.append(d)
print(result)

# 不要传给str()一个字符串，这样会影响性能
