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

                    case int(), None, int(): # [int:: int]
                        # TODO: implement this
                        ...
                    case str(), None, str(): # [str:: str]
                        # TODO: implement this
                        ...

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

    def __setitem__(self, key, value, axis=0):

        match key:

            case int():
                self.data[key] = value

            case str():
                self.data[axis].replace(key, value)

            case slice():

                match key.start, key.stop, key.step:

                    case int(), None, None:  # [int:]
                        self.data[:key] += str(value)

                    case str(), None, None:  # [str:]
                        # Match index string and append value at the end
                        m = re.search(re.escape(key.start) + r"(.*)", self.data[0])
                        self.data[axis] = self.data[0][:m.start] + value

                    case None, int(), None:  # [: int:]
                        self.data[:key] = str(value)

                    case None, str(), None:  # [: str:]
                        # Match stop index and store value + the end of data
                        m = re.search(r"(.*?)" + re.escape(key.stop), self.data[axis])
                        self.data[0] = value + self.data[0][m.stop:]

                    case None, None, int():  # [::int]
                        out = ""
                        for i in range(len(self.data[axis])):
                            out += self.data[axis][i] if i % key.step else value
                        self.data[axis] = out

                    case None, None, str():  # [::str]
                        # TODO: check if this pattern matching works, otherwise try with re.split()
                        pattern = f"(?!{re.escape(key.step)})"
                        self.data[axis] = re.sub(pattern + ".", value, self.data[axis])

                    case int(), int(), None:  # [int: int:]
                        self.data[axis] = self.data[axis][:key.start] + value + self.data[axis][key.stop]

                    case str(), str(), None:  # [str: str:]
                        pattern = re.escape(key.start) + r"(.*?)" + re.escape(key.stop)
                        m = re.search(pattern, self.data[axis])
                        # TODO: decide what should be assigned in case of non-match string
                        self.data[axis] = self.data[axis][:m.start()] + value + key.stop if m else ""

                    case int(), int(), int():  # [int: int: int]
                        out = self.data[axis][:key.start]
                        for i in range(key.start, key.stop):
                            out += self.data[axis][i] if i % key.step else value
                        self.data[axis] = out

                    case str(), str(), int():  # [str: str: int]
                        out = self.data[axis][:key.start]
                        pattern = re.escape(key.start) + r"(.*?)" + re.escape(key.stop)
                        m = re.search(pattern, self.data[axis])
                        if m:
                            for i in range(m.start(), m.stop()):
                                out += self.data[axis][i] if i % key.step else value
                            self.data[axis] = out
                        else:
                            self.data[axis] = ""

                    case str(), str(), str():  # [str: str: str]
                        pattern = re.escape(key.start) + r"(.*?)" + re.escape(key.stop)
                        m = re.search(pattern, self.data[axis])
                        if m:
                            out = self.data[axis][: m.start()]
                            out += (key.start + m.group(1)).replace(key.step, value) + key.stop
                            self.data[axis] = out
                        else:
                            self.data[axis] = ""
