import re

class Array:

    def __init__(self, data):
        assert isinstance(data, list) or isinstance(data, tuple) , "Input string must be List or Tuple"
        # TODO: allow also ints
        self.data = data # Here I have the list of words

    def shape(self):
        return tuple(len(word) for word in self.data)

    def size(self):
        size = 1
        for word in self.data:
            size *= len(word) if len(word) != 0 else 1
        return tuple(len(word) for word in self.data)

    def ndims(self):
        return len(self.data)

    @staticmethod
    def empty(shape):
        # TODO: decide how to init empty Arrays
        if isinstance(shape, int):
            return Array(["" for _ in range(shape)])
        return Array([["" for _ in range(dim)] for dim in shape])

    def square(self):
        max_length = max(map(len, self.data))
        for i, word in enumerate(self.data):
            while len(word) < max_length:
                self.data[i] += " "
        return self

    def __repr__(self):
        print(f"[Array Object], data = {self.data}")

    def __str__(self):
        return f"{self.data}"

    def __getitem__(self, items, axis=0):

        match items:

            case int(): # [int]
                return Array([self.data[items]]) # Returns the elements in that dim.

            case str(): # [str]
                return Array([items if items in self.data[axis] else ""]) # Returns  all the elements except with the axised str removed

            case slice():
                match items.start, items.stop, items.step:

                    case int(), None, None: # [int:]
                        return Array([self.data[axis][items.start:]])

                    case str(), None, None: # [str:]
                        m = re.search(re.escape(items.start) + r"(.*)", self.data[axis])
                        return Array([items.start + m.group(1)]) if m else Array([])

                    case None, int(), None: # [: int:]
                        return Array([self.data[axis][:items.stop]])

                    case None, str(), None: # [: str:]
                        m = re.search(r"(.*?)" + re.escape(items.stop), self.data[axis])
                        return Array([m.group(1)]) if m else Array([])
                    
                    case None, None, int(): # [::int]
                        return Array([self.data[axis][::items.step]])

                    case None, None, str(): # [::str]
                        # TODO: decide whether to return [] or [""]
                        return Array(["".join(self.data[axis].split(items.step))])

                    case int(), int(), None: # [int: int:]
                        return Array([self.data[axis][items.start: items.stop]])

                    case str(), str(), None: # [str: str:]
                        pattern = re.escape(items.start) + r"(.*?)" + re.escape(items.stop)
                        m = re.search(pattern, self.data[axis])
                        return Array([items.start + m.group(1)]) if m else Array([])

                    case int(), int(), int(): # [int: int: int]
                        return Array([self.data[axis][items.start: items.stop: items.step]])

                    case str(), str(), int():  # [str: str: int]
                        pattern = re.escape(items.start) + r"(.*?)" + re.escape(items.stop)
                        m = re.search(pattern, self.data[axis])
                        return Array([items.start + m.group(1)[::items.step]]) if m else Array([])

                    case str(), str(), str():  # [str: str: str]
                        # TODO: decide how str step should work!
                        pattern = re.escape(items.start) + r"(.*?)" + re.escape(items.stop)
                        m = re.search(pattern, self.data[axis])
                        substring = items.start + m.group(1)
                        res = ["".join(substring.split(items.step))]
                        return Array(res) if m else Array([])

            case Array():
                # TODO: allow indexing by Array object
                return NotImplementedError

            case tuple():
                out = []
                # For each item in the tuple, match it recursively with the above patterns, and return it as a Array
                for k, item in enumerate(items):
                    substring_list = self.__getitem__(item, axis=k).data
                    out.extend(substring_list)
                return Array(out)

            case _:
                return SyntaxError

    def __setitem__(self, x: str):
        ...

