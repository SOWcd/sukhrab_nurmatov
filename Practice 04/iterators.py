# Example 1: Basic iterator with iter() and next()
my_list = [1, 2, 3, 4, 5]
my_iter = iter(my_list)

print(next(my_iter))
print(next(my_iter))
print(next(my_iter))

# Example 2: Loop through iterator
my_tuple = ("apple", "banana", "cherry")
my_iter = iter(my_tuple)

for item in my_iter:
    print(item)

# Example 3: String iterator
my_string = "Python"
my_iter = iter(my_string)

for char in my_iter:
    print(char)


# Example 4: Create custom iterator class
class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= 5:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration


myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
    print(x)


# Example 5: Fibonacci iterator
class Fibonacci:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.max_count:
            result = self.a
            self.a, self.b = self.b, self.a + self.b
            self.count += 1
            return result
        else:
            raise StopIteration


fib = Fibonacci(10)
for num in fib:
    print(num, end=" ")
print()


# Example 6: Range-like iterator
class MyRange:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.end:
            num = self.current
            self.current += 1
            return num
        raise StopIteration


for i in MyRange(1, 6):
    print(i)


# Example 7: Reverse iterator
class ReverseIterator:
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index > 0:
            self.index -= 1
            return self.data[self.index]
        raise StopIteration


rev = ReverseIterator([1, 2, 3, 4, 5])
for item in rev:
    print(item)