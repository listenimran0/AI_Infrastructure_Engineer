# Month 1 - Week 1 - Day 4

# Advanced Python: Pydantic

গত লেসনে আমরা **Type Hints** শিখেছিলাম।

কিন্তু একটি বড় সমস্যা ছিল।

Type Hints শুধু Developer-কে Hint দেয়, Python নিজে Type Check করে না।

উদাহরণ—

```python
def add(a: int, b: int) -> int:
    return a + b

add("Hello ", "World")
```

এই Code কোনো Error ছাড়াই চলবে।

Production Application-এর জন্য এটি নিরাপদ নয়।

এই সমস্যার সমাধান করতে আমরা ব্যবহার করি **Pydantic**।

---

# আজকের Lesson-এ যা শিখবো

- Pydantic কী?
- BaseModel
- Data Validation
- Default Values
- Auto Type Conversion
- Custom Validation
- FastAPI-তে Pydantic
- Practice Project

---

# Pydantic কী?

Pydantic হলো একটি জনপ্রিয় Python Library যা **Data Validation** এবং **Type Enforcement** করার জন্য ব্যবহার করা হয়।

অর্থাৎ User যদি ভুল Data পাঠায়, তাহলে Pydantic সঙ্গে সঙ্গে Error দেখাবে।

প্রথমে Library Install করে নাও।

```bash
pip install pydantic
```

---

# প্রথম Pydantic Model

Pydantic-এ প্রতিটি Data Structure একটি **Model** হিসেবে তৈরি করা হয়।

```python
from pydantic import BaseModel
from typing import Optional

class InferenceRequest(BaseModel):

    prompt: str
    model_name: str

    max_tokens: int = 1000
    temperature: float = 0.7

    user_id: Optional[str] = None
```

এখানে আমরা একটি AI Request-এর জন্য একটি Model তৈরি করেছি।

---

# Model ব্যবহার করা

এখন একটি Object তৈরি করি।

```python
request = InferenceRequest(
    prompt="Hello AI",
    model_name="GPT-4",
    max_tokens=500
)

print(request.prompt)
print(request.temperature)
```

Output

```text
Hello AI

0.7
```

`temperature` আমরা দিইনি।

তাই Pydantic Default Value ব্যবহার করেছে।

---

# ভুল Data দিলে কী হবে?

এখন ইচ্ছা করে ভুল Data পাঠাই।

```python
bad_request = InferenceRequest(
    prompt="Hello",
    model_name="GPT-4",
    max_tokens="five hundred"
)
```

Output

```text
ValidationError
```

কারণ `max_tokens` অবশ্যই Integer হতে হবে।

---

# Auto Type Conversion

Pydantic-এর একটি দারুণ Feature হলো **Automatic Type Conversion**।

```python
request = InferenceRequest(
    prompt="Hello",
    model_name="GPT-4",
    max_tokens="500"
)

print(request.max_tokens)
print(type(request.max_tokens))
```

Output

```text
500

<class 'int'>
```

আমরা String পাঠিয়েছি।

কিন্তু Pydantic এটিকে Integer-এ Convert করে নিয়েছে।

যদি Convert করা সম্ভব না হয়, তখন Error দেয়।

---

# Custom Validation

আমরা চাইলে নিজের নিয়মও তৈরি করতে পারি।

```python
from pydantic import BaseModel, validator

class InferenceRequest(BaseModel):

    prompt: str
    temperature: float = 0.7

    @validator("temperature")
    def validate_temperature(cls, value):

        if not 0 <= value <= 2:
            raise ValueError(
                "Temperature অবশ্যই 0 থেকে 2 এর মধ্যে হতে হবে।"
            )

        return value
```

এখন যদি—

```python
InferenceRequest(
    prompt="Hello",
    temperature=5
)
```

Run করি,

তাহলে Output হবে—

```text
ValidationError
```

---

# আরেকটি Validation

Prompt কখনো Empty হওয়া উচিত নয়।

```python
from pydantic import BaseModel, validator

class InferenceRequest(BaseModel):

    prompt: str

    @validator("prompt")
    def validate_prompt(cls, value):

        if not value.strip():
            raise ValueError(
                "Prompt খালি হতে পারবে না।"
            )

        return value
```

এখন যদি—

```python
InferenceRequest(
    prompt="   "
)
```

Run করি,

তাহলে Validation Error আসবে।

---

# FastAPI-তে Pydantic

FastAPI-তে Pydantic সবচেয়ে বেশি ব্যবহার করা হয়।

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InferenceRequest(BaseModel):

    prompt: str
    max_tokens: int = 1000


@app.post("/inference")
async def run_inference(
    request: InferenceRequest
):

    return {
        "response": f"Processing: {request.prompt}"
    }
```

এখানে FastAPI নিজেই—

- JSON Parse করবে
- Pydantic দিয়ে Validate করবে
- ভুল Data হলে Error Response পাঠাবে

আমাদের আলাদা করে Validation লিখতে হবে না।

---

# Practice Project

নিচের Code Run করো।

```python
from pydantic import BaseModel, validator
from typing import Optional, List

class GPUJob(BaseModel):

    job_id: str
    model_name: str
    prompt: str

    priority: int = 1
    gpu_count: int = 1

    tags: List[str] = []

    user_id: Optional[str] = None

    @validator("priority")
    def priority_must_be_valid(cls, value):

        if not 1 <= value <= 5:
            raise ValueError(
                "Priority অবশ্যই 1 থেকে 5 এর মধ্যে হতে হবে!"
            )

        return value

    @validator("gpu_count")
    def gpu_count_must_be_positive(cls, value):

        if value < 1:
            raise ValueError(
                "কমপক্ষে ১টি GPU লাগবে!"
            )

        return value
```

---

# Test 1

```python
job1 = GPUJob(
    job_id="job_001",
    model_name="Llama-3",
    prompt="Hello",
    priority=3,
    gpu_count=2,
    tags=["inference", "production"]
)

print(job1)
```

---

# Test 2

```python
job2 = GPUJob(
    job_id="job_002",
    model_name="GPT-4",
    prompt="Hello",
    priority=10
)
```

---

# Test 3

```python
job3 = GPUJob(
    job_id="job_003",
    model_name="Claude",
    prompt="Hello",
    gpu_count=0
)
```

---

# আজকের Task

Run করার পরে নিচের প্রশ্নগুলোর উত্তর দেওয়ার চেষ্টা করো।

1. Test 2-এ কী Error এসেছে?

2. Test 3-এ কী Error এসেছে?

3. `Type Hints` এবং `Pydantic`-এর মধ্যে মূল পার্থক্য কী?

---

# আজকের Lesson থেকে যা শিখলে

- Pydantic কী
- BaseModel
- Data Validation
- Default Values
- Auto Type Conversion
- Custom Validator
- FastAPI-তে Pydantic-এর ব্যবহার

---

# Next Lesson

পরবর্তী Lesson-এ আমরা **Generators & Iterators** শিখবো।

এই Concept বড় Dataset, File Processing এবং AI Data Pipeline-এর ক্ষেত্রে Memory Efficient Programming-এর জন্য খুবই গুরুত্বপূর্ণ।