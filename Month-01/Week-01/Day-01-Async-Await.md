# Month 1 - Week 1 - Day 1

# Advanced Python: Async & Await

আজকে আমরা Python-এর সবচেয়ে গুরুত্বপূর্ণ একটি concept শিখবো — **Asynchronous Programming**।

তুমি যদি ভবিষ্যতে FastAPI, AI Backend, LLM Serving, vLLM, OpenAI API, কিংবা নিজের AI Inference Server তৈরি করতে চাও, তাহলে `async` এবং `await` অবশ্যই ভালোভাবে বুঝতে হবে।

এই chapter শেষে তুমি জানতে পারবে—

- Synchronous Programming কী
- Asynchronous Programming কী
- `async` কী
- `await` কী
- `asyncio.run()`
- `asyncio.gather()`
- বাস্তব AI Server-এ এগুলো কোথায় ব্যবহার হয়

---

# কেন Async শিখবো?

ধরো তুমি একটি AI Inference Server তৈরি করেছো।

একই সময়ে অনেক user request পাঠাচ্ছে।

```
User 1 → GPT-4
User 2 → Claude
User 3 → Llama
User 4 → DeepSeek
User 5 → Gemini
```

যদি server একবারে একজনের request process করে, তাহলে বাকিদের অপেক্ষা করতে হবে।

এভাবে server খুব ধীরে কাজ করবে।

কিন্তু production server এ হাজার হাজার request একসাথে handle করতে হয়।

এই সমস্যার সমাধান করে **Asynchronous Programming**।

এই কারণেই FastAPI, Uvicorn, Starlette, OpenAI SDK, Anthropic SDK—সবখানেই Async ব্যবহার করা হয়।

---

# Synchronous Programming

প্রথমে Normal Programming দেখি।

ধরো তুমি একটি চায়ের দোকান চালাও।

প্রথম customer আসলো।

```
চা বানাও

↓

চা দাও

↓

দ্বিতীয় customer

↓

চা বানাও

↓

চা দাও

↓

তৃতীয় customer
```

অর্থাৎ এক কাজ শেষ না হলে পরের কাজ শুরু হচ্ছে না।

যদি প্রত্যেক কাপ চা বানাতে ৩ সেকেন্ড লাগে,

তাহলে তিনজন customer-এর জন্য লাগবে—

```
3 + 3 + 3 = 9 Seconds
```

---

# Asynchronous Programming

এবার একটু ভিন্নভাবে চিন্তা করি।

প্রথম customer-এর চা চুলায় বসিয়ে দিলে সেই সময়ে তুমি বসে থাকছো না।

বরং—

```
Customer 1 এর চা চুলায়

↓

Customer 2 এর order নিলে

↓

Customer 3 এর order নিলে

↓

চা তৈরি

↓

সবাইকে serve করলে
```

এখন মোট সময় লাগলো প্রায় ৩ সেকেন্ড।

একই সময়ে অনেক কাজ এগিয়ে গেল।

এটাই Async Programming-এর মূল ধারণা।

---

# Python-এ Async Function

Python-এ asynchronous function লেখার জন্য `async` keyword ব্যবহার করা হয়।

```python
async def make_tea():
    print("Making Tea...")
```

একটি `async` function call করলেই সাথে সাথে execute হয় না।

এটি একটি **Coroutine Object** return করে।

---

# Await কী?

যখন কোনো asynchronous কাজ শেষ হওয়ার জন্য অপেক্ষা করতে হবে, তখন `await` ব্যবহার করি।

```python
await asyncio.sleep(3)
```

এখানে Python পুরো program বন্ধ করে বসে থাকে না।

বরং অন্য async task execute করতে পারে।

এটাই Async-এর সবচেয়ে বড় সুবিধা।

---

# প্রথম Example

```python
import asyncio

async def make_tea(customer):
    print(f"{customer} এর চা বানানো শুরু")

    await asyncio.sleep(3)

    print(f"{customer} এর চা রেডি")

async def main():

    await asyncio.gather(
        make_tea("Imran"),
        make_tea("Rahim"),
        make_tea("Karim"),
    )

asyncio.run(main())
```

---

# Code ব্যাখ্যা

প্রথমে আমরা একটি asynchronous function তৈরি করেছি।

```python
async def make_tea(customer):
```

এরপর

```python
await asyncio.sleep(3)
```

এখানে আমরা ৩ সেকেন্ডের একটি asynchronous delay দিয়েছি।

এই delay চলাকালীন Python অন্য async task execute করতে পারে।

এরপর

```python
asyncio.gather(...)
```

একাধিক async function একই সাথে চালিয়েছে।

সবশেষে

```python
asyncio.run(main())
```

সম্পূর্ণ program-এর event loop শুরু করেছে।

---

# Output

```
Imran এর চা বানানো শুরু

Rahim এর চা বানানো শুরু

Karim এর চা বানানো শুরু

...

Imran এর চা রেডি

Rahim এর চা রেডি

Karim এর চা রেডি
```

খেয়াল করো, তিনজনের কাজ একই সাথে শুরু হয়েছে।

---

# এবার AI Example

বাস্তবে AI Server-এ ঠিক এমনটাই হয়।

```python
import asyncio

async def fetch_ai_response(model, delay):

    print(f"{model} processing...")

    await asyncio.sleep(delay)

    print(f"{model} finished")

    return model

async def main():

    results = await asyncio.gather(

        fetch_ai_response("GPT-4",2),

        fetch_ai_response("Claude",1),

        fetch_ai_response("Llama",3),

    )

    print(results)

asyncio.run(main())
```

---

# কেন Claude আগে শেষ হলো?

অনেকেই এখানে confused হয়।

তিনটি model একই সময়ে শুরু হয়েছে।

কিন্তু Claude-এর delay মাত্র ১ second।

তাই সেটি সবার আগে শেষ হয়েছে।

Async মানে সবাই একই সময়ে finish করবে এমন নয়।

Async মানে সবাই একই সময়ে কাজ শুরু করতে পারবে।

---

# মনে রাখার বিষয়

১. `await` শুধুমাত্র `async` function-এর ভিতরে ব্যবহার করা যায়।

২. Program শুরু করতে `asyncio.run()` ব্যবহার করা হয়।

৩. একাধিক task একসাথে চালাতে `asyncio.gather()` ব্যবহার করা হয়।

৪. `time.sleep()` কখনো async code-এর মধ্যে ব্যবহার করা উচিত নয়।

এর পরিবর্তে ব্যবহার করো—

```python
await asyncio.sleep()
```

---

# কোথায় Async ব্যবহার হবে?

এই roadmap-এর পরবর্তী অংশে আমরা Async ব্যবহার করবো—

- FastAPI
- AI APIs
- Database Query
- Redis
- Docker Services
- OpenAI SDK
- Anthropic SDK
- vLLM
- AI Inference Server

তাই এই concept যত ভালো বুঝবে, পরের chapter গুলো তত সহজ লাগবে।

---

# Practice

আজকের কাজ খুব সহজ।

নিচের AI Inference Program টি নিজে লিখে run করো।

এরপর নিজে উত্তর দেওয়ার চেষ্টা করো—

১. Program run হতে কত সময় লাগলো?

২. যদি Async ব্যবহার না করতে, তাহলে কত সময় লাগতো?

৩. Claude কেন GPT-4-এর আগে শেষ হলো?

৪. আরও দুটি model (Gemini এবং DeepSeek) যোগ করো।

---

# আজকের Lesson থেকে যা শিখলে

- Synchronous Programming
- Asynchronous Programming
- async
- await
- asyncio.run()
- asyncio.gather()

পরের Lesson-এ আমরা শিখবো **Decorators**, যেটি না জানলে FastAPI-এর routing system পুরোপুরি বোঝা সম্ভব নয়।