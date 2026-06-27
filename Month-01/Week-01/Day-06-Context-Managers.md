# Month 1 - Week 1 - Day 6

# Advanced Python: Context Managers

গত লেসনে আমরা **Generators & Iterators** শিখেছিলাম। আজকে আমরা শিখবো **Context Managers**।

এটি Python-এর একটি গুরুত্বপূর্ণ Feature যা File Handling, Database Connection, Network Connection, GPU Resource Management এবং AI Infrastructure-এ নিয়মিত ব্যবহার করা হয়।

---

# আজকের Lesson-এ যা শিখবো

- Context Manager কী?
- `with` Statement
- `__enter__()` এবং `__exit__()`
- নিজের Context Manager তৈরি করা
- `contextlib.contextmanager`
- Async Context Manager
- Practice

---

# Context Manager কেন দরকার?

AI Infrastructure-এ প্রায়ই নিচের কাজগুলো করতে হয়—

- File Open করা
- Database Connect করা
- GPU Memory Allocate করা
- API Connection তৈরি করা

কাজ শেষ হলে আবার Resource Release করাও সমান গুরুত্বপূর্ণ।

---

# সমস্যা কোথায়?

ধরো আমরা একটি File Open করলাম।

```python
file = open("model_config.json", "r")

data = file.read()

file.close()
```

সবকিছু ঠিক থাকলে সমস্যা নেই।

কিন্তু যদি `file.read()` করার সময় কোনো Error আসে?

```python
file = open("model_config.json", "r")

data = file.read()

raise Exception("Something went wrong!")

file.close()
```

এখানে `file.close()` কখনো Execute হবে না।

ফলে File Open অবস্থায় থেকে যাবে।

একই সমস্যা Database Connection, GPU Memory এবং Network Connection-এর ক্ষেত্রেও হতে পারে।

---

# Solution — `with` Statement

Python আমাদের জন্য `with` Statement দিয়েছে।

```python
with open("model_config.json", "r") as file:

    data = file.read()
```

`with` Block শেষ হওয়ার সাথে সাথে File Automatically Close হয়ে যাবে।

Error আসলেও Cleanup হবে।

এ কারণেই Production Code-এ File Open করার সময় সবসময় `with` ব্যবহার করা হয়।

---

# Context Manager কী?

Context Manager এমন একটি Object যা দুটি গুরুত্বপূর্ণ Method Implement করে।

- `__enter__()`
- `__exit__()`

`with` Block শুরু হলে `__enter__()` Call হয়।

`with` Block শেষ হলে `__exit__()` Call হয়।

Error আসলেও `__exit__()` অবশ্যই Execute হয়।

---

# নিজের Context Manager তৈরি করা

```python
class GPUMemory:

    def __init__(self, gpu_id: int, memory_gb: int):

        self.gpu_id = gpu_id
        self.memory_gb = memory_gb

    def __enter__(self):

        print(
            f"GPU {self.gpu_id} তে {self.memory_gb}GB Memory Allocate করা হলো"
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        print(
            f"GPU {self.gpu_id} Memory Free করা হলো"
        )

        return False
```

---

# ব্যবহার

```python
with GPUMemory(
    gpu_id=0,
    memory_gb=24
) as gpu:

    print(
        f"Inference চলছে GPU {gpu.gpu_id} তে..."
    )
```

Output

```text
GPU 0 তে 24GB Memory Allocate করা হলো

Inference চলছে GPU 0 তে...

GPU 0 Memory Free করা হলো
```

---

# Error আসলেও Cleanup হবে

```python
with GPUMemory(
    gpu_id=0,
    memory_gb=24
) as gpu:

    print("Inference শুরু...")

    raise Exception("Model Crash!")

    print("এই Line Execute হবে না")
```

Output

```text
GPU 0 তে 24GB Memory Allocate করা হলো

Inference শুরু...

GPU 0 Memory Free করা হলো

Exception: Model Crash!
```

খেয়াল করো—

Error হওয়ার পরেও `__exit__()` Execute হয়েছে।

---

# `contextlib` দিয়ে Context Manager

সবসময় Class লিখতে হবে এমন নয়।

`contextlib` Module ব্যবহার করে আরও সহজভাবে Context Manager তৈরি করা যায়।

```python
from contextlib import contextmanager

@contextmanager
def gpu_memory(
    gpu_id: int,
    memory_gb: int
):

    print(
        f"GPU {gpu_id} তে {memory_gb}GB Allocate করা হলো"
    )

    try:

        yield gpu_id

    finally:

        print(
            f"GPU {gpu_id} Memory Free করা হলো"
        )
```

---

# ব্যবহার

```python
with gpu_memory(
    gpu_id=1,
    memory_gb=48
) as gpu:

    print(
        f"Inference চলছে GPU {gpu} তে..."
    )
```

এখানে—

- `yield` এর আগে Setup
- `yield` এর পরে Cleanup

---

# `finally` কেন ব্যবহার করা হয়?

```python
try:

    yield

finally:

    cleanup()
```

`finally` Block-এর বিশেষ বৈশিষ্ট্য হলো—

Error আসুক বা না আসুক, এটি সবসময় Execute হয়।

তাই Resource Cleanup করার জন্য এটি সবচেয়ে নিরাপদ জায়গা।

---

# Async Context Manager

Production AI Application-এ অনেক Resource Async হয়।

যেমন—

- Database Connection
- Redis
- HTTP Client
- API Connection

এক্ষেত্রে Async Context Manager ব্যবহার করা হয়।

```python
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def db_connection(host: str):

    print(f"{host} এ Connect করছি...")

    await asyncio.sleep(0.5)

    print("Connected!")

    try:

        yield {
            "host": host,
            "status": "connected"
        }

    finally:

        await asyncio.sleep(0.2)

        print("Disconnected!")
```

---

# ব্যবহার

```python
async def main():

    async with db_connection(
        "mongodb://localhost"
    ) as conn:

        print(conn)

        await asyncio.sleep(0.3)

asyncio.run(main())
```

এখানে `with` এর পরিবর্তে `async with` ব্যবহার করা হয়েছে।

কারণ এটি একটি Async Context Manager।

---

# Practice

নিচের Code Run করো।

```python
from contextlib import contextmanager
import time

@contextmanager
def inference_session(
    model_name: str,
    gpu_id: int
):

    print(
        f"\nSession শুরু: {model_name} on GPU {gpu_id}"
    )

    start_time = time.time()

    session = {
        "model": model_name,
        "gpu": gpu_id,
        "requests": 0
    }

    try:

        yield session

    finally:

        duration = time.time() - start_time

        print("\nSession Summary")

        print(f"Model: {session['model']}")

        print(f"Requests: {session['requests']}")

        print(f"Duration: {duration:.2f}s")

        print("Session Cleanup Complete\n")
```

---

# Test 1

```python
with inference_session(
    "Llama-3",
    gpu_id=0
) as session:

    for _ in range(3):

        time.sleep(0.3)

        session["requests"] += 1

        print(
            f"Request {session['requests']} Processed"
        )
```

---

# Test 2

```python
try:

    with inference_session(
        "GPT-4",
        gpu_id=1
    ) as session:

        session["requests"] += 1

        print("Request 1 Processed")

        raise Exception("GPU Out Of Memory!")

        session["requests"] += 1

except Exception as e:

    print(e)
```

---

# আজকের Task

Code Run করার পরে নিচের প্রশ্নগুলোর উত্তর দেওয়ার চেষ্টা করো।

1. `with` Statement ব্যবহার করলে কী সুবিধা পাওয়া যায়?

2. `__enter__()` এবং `__exit__()` কখন Execute হয়?

3. `finally` কেন ব্যবহার করা হয়?

4. `contextmanager` ব্যবহার করলে Class লেখার প্রয়োজন কেন কমে যায়?

5. `with` এবং `async with`-এর মধ্যে পার্থক্য কী?

---

# আজকের Lesson থেকে যা শিখলে

- Context Manager
- `with` Statement
- `__enter__()`
- `__exit__()`
- Resource Cleanup
- `contextlib`
- `@contextmanager`
- `finally`
- Async Context Manager
- `async with`

---

# Next Lesson

Week 1 সম্পন্ন।

পরবর্তী Lesson থেকে আমরা **Week 2: Linux Essentials** শুরু করবো।

Linux হলো AI Infrastructure, Cloud Computing এবং Production Server-এর ভিত্তি। তাই পরবর্তী সপ্তাহে আমরা Linux-এর গুরুত্বপূর্ণ Concept এবং Command নিয়ে কাজ করবো।