# Month 1 - Week 1 - Day 5

# Advanced Python: Generators & Iterators

গত লেসনে আমরা **Pydantic** শিখেছিলাম। আজকে আমরা শিখবো **Generators** এবং **Iterators**।

এই Topic টি প্রথমে সাধারণ Python Concept মনে হলেও, AI Infrastructure, Data Pipeline এবং LLM Streaming-এর ক্ষেত্রে এটি অত্যন্ত গুরুত্বপূর্ণ।

---

# আজকের Lesson-এ যা শিখবো

- Iterator কী?
- Generator কী?
- `yield` কীভাবে কাজ করে?
- `yield` vs `return`
- Real-world AI Streaming
- Async Generator
- Practice

---

# Generators কেন দরকার?

তুমি যখন ChatGPT বা Claude ব্যবহার করো, লক্ষ্য করলে দেখবে Response একসাথে আসে না।

এভাবে আসে—

```text
Hello...

How...

Can...

I...

Help...

You...
```

অর্থাৎ Response **Word by Word** Stream হয়।

এই ধরনের Streaming Feature তৈরি করতে Generator ব্যবহার করা হয়।

---

# Iterator কী?

Iterator-এর কাজ হলো **একটি একটি করে Item Return করা।**

উদাহরণ—

```python
numbers = [1, 2, 3, 4, 5]

for number in numbers:
    print(number)
```

এখানে `numbers` একটি **Iterable**।

`for` Loop প্রতিবার List থেকে একটি করে Value নিয়ে কাজ করছে।

Output

```text
1
2
3
4
5
```

---

# List-এর সমস্যা

ধরো আমাদের ১০ মিলিয়ন সংখ্যা নিয়ে কাজ করতে হবে।

```python
numbers = list(range(10_000_000))
```

এখানে কী হচ্ছে?

Python শুরুতেই ১০ মিলিয়ন সংখ্যা RAM-এ Load করে ফেলছে।

যদি Data আরও বড় হয়, তাহলে অনেক Memory ব্যবহার হবে।

---

# Generator কী?

Generator সব Data একসাথে Memory-তে রাখে না।

যখন দরকার হয়, তখন একটি করে Value তৈরি করে।

List

```python
numbers = [x * 2 for x in range(10_000_000)]
```

Generator

```python
numbers = (x * 2 for x in range(10_000_000))
```

খেয়াল করো—

শুধু `[]` এর জায়গায় `()` ব্যবহার করেছি।

কিন্তু Memory Usage সম্পূর্ণ পরিবর্তন হয়ে গেছে।

Generator একবারে একটি করে Value তৈরি করে।

---

# `yield` কী?

`yield` হলো Generator Function-এর সবচেয়ে গুরুত্বপূর্ণ Keyword।

Normal Function

```python
def get_tokens(text):

    tokens = text.split()

    return tokens
```

এখানে Function একবারেই সব Token Return করে।

Output

```text
["Hello", "How", "Are", "You"]
```

---

Generator Function

```python
def get_tokens(text):

    tokens = text.split()

    for token in tokens:

        yield token
```

এখানে Function সব Token একসাথে Return করছে না।

একটি করে Token Return করছে।

---

# `yield` কীভাবে কাজ করে?

ধরো নিচের Code Run করলাম।

```python
def get_tokens(text):

    tokens = text.split()

    for token in tokens:

        print(f"Yield করছি: {token}")

        yield token

        print("আবার এখান থেকে শুরু হলো")


generator = get_tokens("Hello How Are You")

print(next(generator))

print(next(generator))
```

Output

```text
Yield করছি: Hello

Hello

আবার এখান থেকে শুরু হলো

Yield করছি: How

How
```

প্রথম `next()` Call-এ Function `yield` পর্যন্ত Execute হয় এবং সেখানেই Pause হয়ে যায়।

পরের `next()` Call-এ Function আবার ঠিক সেই জায়গা থেকেই Execute শুরু করে।

---

# `yield` vs `return`

এটি Generator-এর সবচেয়ে গুরুত্বপূর্ণ Concept।

### `return`

```python
def hello():

    return "Hello"

    print("Never Execute")
```

`return` Execute হওয়ার সাথে সাথে Function পুরোপুরি শেষ হয়ে যায়।

---

### `yield`

```python
def hello():

    yield "Hello"

    print("Again Started")
```

`yield` Function শেষ করে না।

এটি শুধু একটি Value Return করে এবং Function-কে Pause করে রাখে।

পরবর্তীতে `next()` Call করলে Function আবার একই জায়গা থেকে শুরু হয়।

---

# Real-world AI Streaming

ধরো একটি AI Model Word by Word Response পাঠাচ্ছে।

```python
import time

def stream_ai_response(prompt: str):

    words = f"This is the AI response for {prompt}".split()

    for word in words:

        time.sleep(0.3)

        yield word
```

এখন Output দেখো।

```python
print("AI: ", end="", flush=True)

for word in stream_ai_response("Hello"):

    print(word, end=" ", flush=True)

print()
```

Output

```text
AI: This is the AI response for Hello
```

Word গুলো একসাথে আসে না।

একটি একটি করে আসে।

এভাবেই ChatGPT-এর মতো Streaming তৈরি করা যায়।

---

# `end=""` কেন ব্যবহার করা হয়?

Normal `print()` প্রতিবার নতুন Line-এ যায়।

```python
print("Hello")

print("World")
```

Output

```text
Hello

World
```

কিন্তু Streaming-এর সময় আমরা চাই একই Line-এ Word আসুক।

```python
print(word, end=" ")
```

এখানে `end=" "` দেওয়ার কারণে নতুন Line না গিয়ে একটি Space যোগ হয়।

---

# `flush=True` কেন ব্যবহার করা হয়?

Python সাধারণত Output Buffer-এ জমা রাখে।

তারপর একসাথে Screen-এ দেখায়।

Streaming-এর সময় আমরা চাই প্রতিটি Word সঙ্গে সঙ্গে Screen-এ দেখা যাক।

তাই—

```python
print(word, end=" ", flush=True)
```

`flush=True` Buffer Empty করে Output সাথে সাথে Screen-এ পাঠিয়ে দেয়।

এ কারণেই ChatGPT-এর মতো Streaming Effect পাওয়া যায়।

---

# শেষে `print()` কেন?

Loop-এর ভিতরে আমরা লিখেছি—

```python
print(word, end=" ")
```

তাই Loop শেষ হলেও Cursor একই Line-এ থাকে।

```text
AI: Hello World |
```

যদি এরপর আবার কিছু Print করি—

```python
print("Done")
```

Output হবে—

```text
AI: Hello World Done
```

এটি সুন্দর দেখায় না।

তাই শেষে শুধু—

```python
print()
```

লিখি।

এটি শুধু একটি নতুন Line তৈরি করে।

---

# Async Generator

Production AI Application-এ সাধারণ Generator-এর পাশাপাশি Async Generator-ও ব্যবহার করা হয়।

```python
import asyncio

async def stream_ai_response(prompt: str):

    words = f"AI response for {prompt}".split()

    for word in words:

        await asyncio.sleep(0.3)

        yield word
```

এখন এটি ব্যবহার করতে হবে—

```python
async def main():

    print("AI: ", end="", flush=True)

    async for word in stream_ai_response("Hello"):

        print(word, end=" ", flush=True)

    print()

asyncio.run(main())
```

খেয়াল করো—

এখানে `for` নয়, `async for` ব্যবহার করা হয়েছে।

কারণ এটি একটি **Async Generator**।

---

# Practice

নিচের Code Run করো।

```python
import asyncio
import time

def gpu_job_queue(jobs: list):

    for job in jobs:

        print(f"Queue থেকে নিলাম: {job}")

        yield job


async def stream_inference(prompt: str):

    response = f"Processing your prompt about {prompt} complete".split()

    for word in response:

        await asyncio.sleep(0.2)

        yield word


async def main():

    jobs = [
        "job_001",
        "job_002",
        "job_003",
        "job_004"
    ]

    print("=== GPU Job Queue ===")

    queue = gpu_job_queue(jobs)

    for job in queue:

        print(f"Processing: {job}")

        time.sleep(0.5)

    print("\n=== AI Streaming ===")

    print("AI: ", end="", flush=True)

    async for word in stream_inference("machine learning"):

        print(word, end=" ", flush=True)

    print("\nDone!")

asyncio.run(main())
```

---

# আজকের Task

Code Run করার পরে নিচের প্রশ্নগুলোর উত্তর দেওয়ার চেষ্টা করো।

1. `yield` এবং `return`-এর মধ্যে মূল পার্থক্য কী?

2. Generator কেন List-এর তুলনায় কম Memory ব্যবহার করে?

3. `flush=True` কেন ব্যবহার করা হয়?

4. `end=" "` ব্যবহার না করলে কী হবে?

5. Async Generator ব্যবহার করার সময় `for` এর পরিবর্তে `async for` কেন ব্যবহার করতে হয়?

---

# আজকের Lesson থেকে যা শিখলে

- Iterator
- Iterable
- Generator
- `yield`
- `yield` vs `return`
- Generator Expression
- AI Streaming
- Async Generator
- `end=""`
- `flush=True`
- `async for`

---

# Next Lesson

পরবর্তী Lesson-এ আমরা **Context Managers (`with` Statement)** শিখবো।

এটি File Handling, Database Connection, API Connection এবং Resource Management-এর জন্য Production Python-এর অন্যতম গুরুত্বপূর্ণ Concept।