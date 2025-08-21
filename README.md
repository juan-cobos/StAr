# ***StAr*** (String Array)

An experimental library to manipulate strings as arrays.  

Tired of manually splitting or using complicated regular expressions?  
Now you can transform strings as if they were arrays!

---
***StAr** stands for *"String Array"*, inspired by NumPy array indexing and the Kleene star.*

## ✂️ String slicing made easy

Just like slicing a list or an array, but with **string indexing**:

```python
# --- NumPy ---
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = a[1:] 
# b = [2, 3, 4, 5]

# --- StAr ---
import star as st

a = st.Array(["apple", "banana", "carrot"])
b = a["p":] 
# b.data = ["pple"]
```

## 📐 Multidimensional slicing

Each string is treated as a different dimension, allowing for multidimensional slicing (like arrays):

```python
a.shape()
# (5, 6, 6)

b = a["p": "le", "ba": "na"] 
# b.data = ["pp", "ba"]    
```

## 🚀 Strides and splits

Strides can be **strings** or **integers**, enabling splitting and stepping:

```python
a = st.Array(["ap,ple"])
b = a[::","] 
# b.data = ["apple"] 

a = st.Array(["apple"])
b = a["a":: 2] 
# b.data = ["ape"]
```

## 🛠️ Short-term roadmap

- [x] Implement `__getitem__` with string indexing  
- [ ] Implement `__setitem__` with string indexing  
- [ ] Allow Array indexing  
- [ ] Array operations (`+`, `*`, `**`), with integers and strings (like automata)  