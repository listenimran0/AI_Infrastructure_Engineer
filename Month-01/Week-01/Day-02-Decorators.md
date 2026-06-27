# Month 1 - Week 1 - Day 2

# Advanced Python: Decorators

গত লেসনে আমরা `async` এবং `await` শিখেছিলাম। আজকে আমরা Python-এর আরেকটি গুরুত্বপূর্ণ feature **Decorator** শিখবো।

FastAPI, Flask, Django, Logging, Authentication, Retry, Caching—এসব জায়গায় Decorator ব্যাপকভাবে ব্যবহার করা হয়। তাই Backend Development বা AI Infrastructure-এ কাজ করতে চাইলে এই concept ভালোভাবে বোঝা খুবই গুরুত্বপূর্ণ।

---

# Decorator কী?

সহজ ভাষায়, **Decorator হলো এমন একটি function যা অন্য একটি function-কে পরিবর্তন না করেই তার সাথে অতিরিক্ত functionality যোগ করতে পারে।**

অর্থাৎ, মূল function-এর code পরিবর্তন না করেই তার আগে বা পরে নতুন কাজ করানো যায়।

---



# একটি বাস্তব উদাহরণ

ধরো তোমার কাছে একটি সাধারণ চা আছে।

```
চা
```

এখন যদি এতে আদা যোগ করো, তাহলে সেটা হয়ে যায়—

```
আদা চা
```

আবার দুধ যোগ করলে—

```
দুধ চা
```

খেয়াল করো, মূল চা একই আছে। শুধু তার সাথে নতুন feature যোগ হয়েছে।

Decorator-ও ঠিক একইভাবে একটি function-এর সাথে নতুন functionality যোগ করে।

---



# Decorator ছাড়া সমস্যা

ধরো আমাদের একটি AI function আছে।

```python
def ai_inference(prompt):
    print(f"Processing: {prompt}")
    return "AI Response"
```

এখন আমরা চাই প্রতিবার function call হলে execution time print হোক।

একটি উপায় হলো প্রতিটি function-এর ভিতরে time measurement-এর code লিখে দেওয়া।

কিন্তু যদি project-এ ১০০টি function থাকে?

তাহলে ১০০টি function-এই একই code লিখতে হবে।

এতে code repeat হবে এবং maintain করা কঠিন হয়ে যাবে।

---



# Decorator দিয়ে সমাধান

```python
import time

def timer(func):

    def wrapper(*args, **kwargs):

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(f"{func.__name__} took {end - start:.2f} seconds")

        return result

    return wrapper
```

এখন এই decorator যেকোনো function-এর সাথে ব্যবহার করা যাবে।

```python
@timer
def ai_inference(prompt):
    time.sleep(1)
    return "AI Response"

@timer
def load_model(model_name):
    time.sleep(2)
    return f"{model_name} loaded"
```

এখন function call করলেই execution time automatically print হবে।

```python
ai_inference("Hello")
load_model("Llama-3")
```

Output

```text
ai_inference took 1.00 seconds

load_model took 2.00 seconds
```

একবার decorator লিখেই আমরা একাধিক function-এ একই functionality ব্যবহার করতে পারলাম।

---



# `@timer` আসলে কী করে?

অনেকে মনে করে `@timer` Python-এর কোনো special keyword।

আসলে তা নয়।

এই code—

```python
@timer
def ai_inference(prompt):
    ...
```

Python নিজে নিচের code-এ রূপান্তর করে।

```python
def ai_inference(prompt):
    ...

ai_inference = timer(ai_inference)
```

অর্থাৎ, `ai_inference` function-টিকে `timer()` function-এর ভিতরে পাঠানো হচ্ছে এবং `timer()` যে function return করছে, সেটিই নতুন `ai_inference` হয়ে যাচ্ছে।

---



# `wrapper()` এর ভিতরে কী হচ্ছে?

Decorator-এর আসল কাজ হয় `wrapper()` function-এর ভিতরে।

```python
def wrapper(*args, **kwargs):

    start = time.time()

    result = func(*args, **kwargs)

    print(f"Time: {time.time() - start:.2f}s")

    return result
```

এখানে ধাপে ধাপে যা হচ্ছে—

**১.**

```python
start = time.time()
```

Function শুরু হওয়ার সময়টি সংরক্ষণ করা হচ্ছে।

---

**২.**

```python
result = func(*args, **kwargs)
```

এখানে `func` হলো আসল function যেটিকে decorate করা হয়েছে।

এই লাইনে মূল function execute হয় এবং তার return value `result`-এ রাখা হয়।

---

**৩.**

```python
print(...)
```

Function শেষ হওয়ার পরে কত সময় লেগেছে তা print করা হচ্ছে।

---

**৪.**

```python
return result
```

সবশেষে মূল function-এর return value আবার caller-এর কাছে ফেরত পাঠানো হচ্ছে।

---



# `*args` এবং `**kwargs` কেন ব্যবহার করা হয়?

Decorator আগে থেকে জানে না ভবিষ্যতে কোন function decorate করা হবে।

কোনো function-এ একটি argument থাকতে পারে।

```python
hello(name)
```

আবার অন্য function-এ তিনটি argument থাকতে পারে।

```python
load_model(name, version, device)
```

সব ধরনের function-এর জন্য decorator কাজ করানোর জন্য `*args` এবং `**kwargs` ব্যবহার করা হয়।

---



# FastAPI-তে Decorator

FastAPI-তে আমরা পরে এই ধরনের code লিখবো।

```python
@app.get("/chat")
async def chat():
    return {"message": "Hello"}
```

এখানে `@app.get()`-ও একটি decorator।

এটি FastAPI-কে বলে দেয়—

> "`/chat` endpoint-এ GET request আসলে এই function execute করো।"

---



# আজকের Practice

১. `timer` decorator নিজে লিখে দেখো।

২. দুটি আলাদা function-এ decorator ব্যবহার করো।

- `ai_inference()`
- `load_model()`

৩. এরপর নিজে চেষ্টা করো `logger` নামে আরেকটি decorator বানাতে, যা function call হওয়ার আগে function-এর নাম print করবে।

---



# আজকের Lesson থেকে যা শিখলে

- Decorator কী
- কেন Decorator ব্যবহার করা হয়
- `@decorator` আসলে কী করে
- `wrapper()` এর কাজ
- `*args` এবং `**kwargs`
- FastAPI-তে Decorator-এর ব্যবহার

পরবর্তী অংশে আমরা শিখবো—

- `@functools.wraps()`
- Decorator with Arguments (`@retry(max_attempts=3)`)
- Multiple Decorators
- Real AI Infrastructure Examples



# Part 2: `@functools.wraps()`, Decorators with Arguments এবং Multiple Decorators

আগের অংশে আমরা সাধারণ Decorator কীভাবে কাজ করে তা শিখেছি।

এখন আমরা এমন কিছু বিষয় শিখবো যেগুলো Production Project-এ খুবই গুরুত্বপূর্ণ।

এই অংশে আমরা শিখবো—

- `@functools.wraps()` কেন ব্যবহার করা হয়
- Decorator-এ Argument কীভাবে পাঠানো হয়
- কেন কিছু Decorator-এ ২টি Layer আর কিছুতে ৩টি Layer থাকে
- Multiple Decorators

---



# `@functools.wraps()` কেন ব্যবহার করা হয়?

আগের `timer` decorator-টি একটু পরিবর্তন করি।

```python
def timer(func):

    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        return result

    return wrapper


@timer
def ai_inference(prompt):
    """Return AI Response"""
    return "Hello"
```

এখন নিচের code run করি।

```python
print(ai_inference.__name__)
print(ai_inference.__doc__)
```

Output

```text
wrapper
None
```

কিন্তু আমরা তো আশা করেছিলাম—

```text
ai_inference
Return AI Response
```

এমন হলো কেন?

---



# সমস্যাটা কোথায়?

মনে আছে আমরা বলেছিলাম—

```python
@timer
```

আসলে Python এটাকে এভাবে execute করে।

```python
ai_inference = timer(ai_inference)
```

আর `timer()` কী return করছে?

```python
return wrapper
```

অর্থাৎ এখন `ai_inference` আর আগের function নয়।

এখন এটি `wrapper` function-কে point করছে।

তাই—

```python
print(ai_inference.__name__)
```

আসল function-এর নাম না দেখিয়ে `wrapper` দেখায়।

---



# সমাধান

Python আমাদের জন্য `functools.wraps()` নামে একটি helper দিয়েছে।

```python
import functools

def timer(func):

    @functools.wraps(func)

    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        return result

    return wrapper
```

এখন আবার run করি।

```python
print(ai_inference.__name__)
print(ai_inference.__doc__)
```

Output

```text
ai_inference

Return AI Response
```

---



# `@functools.wraps()` আসলে কী করে?

এটি `wrapper`-এর মধ্যে মূল function-এর metadata copy করে।

যেমন—

- Function Name
- Docstring
- Module Name
- Annotation

ফলে বাইরে থেকে `wrapper`-কে দেখলেও মনে হবে এটি আসল function।

Production Project-এ এটি ব্যবহার করা একটি ভালো practice।

---



# Decorator-এ Argument পাঠানো

এখন পর্যন্ত আমরা এই ধরনের Decorator ব্যবহার করেছি।

```python
@timer
```

এখানে কোনো Argument নেই।

কিন্তু যদি আমরা চাই—

```python
@retry(max_attempts=3)
```

তাহলে?

এখন Decorator-এর ভিতরে `3` পাঠাতে হবে।

এজন্য আরেকটি Layer দরকার।

---



# Decorator without Argument

```python
@timer
def hello():
    ...
```

Structure

```python
def timer(func):

    def wrapper():

        ...

    return wrapper
```

এখানে মাত্র দুইটি Layer আছে।

```
timer()

↓

wrapper()
```

---



# Decorator with Argument

এবার দেখি।

```python
@retry(max_attempts=3)
```

Structure

```python
def retry(max_attempts):

    def decorator(func):

        def wrapper(*args, **kwargs):

            ...

        return wrapper

    return decorator
```

এখানে তিনটি Layer।

```
retry()

↓

decorator()

↓

wrapper()
```

---



# কেন ৩টি Layer লাগলো?

কারণ Python প্রথমে Argument collect করে।

```python
retry(max_attempts=3)
```

এরপর Function পাঠায়।

```python
decorator(call_ai_api)
```

তারপর Wrapper return হয়।

পুরো Process

```
retry(3)

↓

decorator

↓

call_ai_api

↓

wrapper

↓

call_ai_api = wrapper
```

---



# Retry Decorator

```python
import functools
import random
import time

def retry(max_attempts=3):

    def decorator(func):

        @functools.wraps(func)

        def wrapper(*args, **kwargs):

            for attempt in range(1, max_attempts + 1):

                try:

                    return func(*args, **kwargs)

                except Exception as e:

                    print(f"Attempt {attempt} Failed")

                    if attempt == max_attempts:

                        raise

                    time.sleep(1)

        return wrapper

    return decorator
```

ব্যবহার

```python
@retry(max_attempts=3)
def call_ai_api(prompt):

    if random.random() < 0.7:

        raise Exception("Timeout")

    return "Success"
```

---



# Code Execution Flow

যখন আমরা লিখি—

```python
call_ai_api("Hello")
```

তখন ভিতরে যা হয়—

```
wrapper()

↓

Attempt 1

↓

Function Fail

↓

Sleep

↓

Attempt 2

↓

Function Fail

↓

Sleep

↓

Attempt 3

↓

Success

↓

Return Result
```

যদি তিনবারই Fail করে—

```
raise Exception
```

---



# Multiple Decorators

একটি Function-এর উপর একাধিক Decorator ব্যবহার করা যায়।

```python
@logger
@timer
def ai_inference():

    ...
```

Python এটাকে এভাবে execute করে।

```python
ai_inference = logger(

                    timer(

                        ai_inference

                    )

               )
```

অর্থাৎ—

প্রথমে

```
timer()
```

Apply হবে।

তারপর

```
logger()
```

Apply হবে।

---



# বাস্তব উদাহরণ

Production Backend-এ একটি API-এর উপর একসাথে অনেক Decorator থাকতে পারে।

```python
@authenticate
@rate_limit
@cache
@timer
def inference():

    ...
```

প্রতিটি Decorator আলাদা কাজ করছে।

- Authentication
- Rate Limiting
- Caching
- Logging
- Execution Time

কিন্তু মূল Function-এর Code একদম পরিষ্কার থাকছে।

---



# AI Infrastructure-এ Decorator কোথায় ব্যবহার হয়?

তুমি যখন AI Backend বা AI Infrastructure নিয়ে কাজ করবে, তখন Decorator বিভিন্ন জায়গায় দেখবে।

উদাহরণ—

- Logging
- Retry Mechanism
- Authentication
- Authorization
- Rate Limiting
- Caching
- Monitoring
- API Routing (FastAPI)
- Performance Measurement

তাই Decorator শুধু Python Interview-এর Topic নয়, এটি Production Development-এর একটি গুরুত্বপূর্ণ অংশ।

---



# Practice

১. `timer` Decorator লিখো।

২. `logger` Decorator লিখো।

৩. `retry` Decorator লিখো।

৪. একই Function-এর উপর তিনটি Decorator একসাথে ব্যবহার করো।

---



# Challenge

একটি Function লিখো—

```python
process_ai_request()
```

এর উপর নিচের তিনটি Decorator ব্যবহার করো।

```python
@logger

@timer

@retry(max_attempts=3)
```

Run করে দেখো কোন Decorator আগে execute হচ্ছে এবং কেন।

---



# আজকের Lesson থেকে যা শিখলে

- `@functools.wraps()`
- Function Metadata
- Decorator with Arguments
- ২ Layer vs ৩ Layer Decorator
- Multiple Decorators
- Retry Decorator
- Production Use Cases

