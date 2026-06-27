# Month 1 - Week 1 - Day 3

# Advanced Python: Type Hints

গত দুইটি লেসনে আমরা **Async/Await** এবং **Decorators** শিখেছি। আজকে আমরা শিখবো **Type Hints**।

Production-level Python Project, FastAPI এবং AI Infrastructure-এ Type Hints খুবই গুরুত্বপূর্ণ। এটি Code আরও Readable, Maintainable এবং Developer Friendly করে তোলে।

---

# আজকের Lesson-এ যা শিখবো

- Type Hints কী?
- কেন Type Hints ব্যবহার করা হয়?
- AI Infrastructure-এ Type Hints-এর গুরুত্ব
- Basic Type Hints
- Collection Types
- Optional
- Function Type Hints
- Type Hints-এর সীমাবদ্ধতা

---

# Type Hints কী?

Python-এ সাধারণভাবে আমরা এভাবে Function লিখতে পারি।

```python
def process(data):
    return data
```

কিন্তু এখানে একটি সমস্যা আছে।

`data` কী?

- String?
- Integer?
- List?
- Dictionary?

Function দেখে বোঝার কোনো উপায় নেই।

এখন Type Hints ব্যবহার করলে—

```python
def process(data: str) -> str:
    return data
```

এখন একনজরেই বোঝা যাচ্ছে—

- `data` একটি String
- Function একটি String Return করবে

এতে Code অনেক বেশি পরিষ্কার এবং বোঝা সহজ হয়ে যায়।

---

# AI Infrastructure-এ Type Hints কেন গুরুত্বপূর্ণ?

ধরো তুমি একটি GPU Scheduler তৈরি করছো।

Type Hints ছাড়া—

```python
def schedule(job, workers, config):
    ...
```

কয়েক মাস পরে নিজেও বুঝতে কষ্ট হবে—

- `job` কী?
- `workers` কী?
- `config` কী ধরনের Data?

কিন্তু Type Hints ব্যবহার করলে—

```python
def schedule(
    job: str,
    workers: int,
    config: dict
) -> bool:
    ...
```

এখন Code দেখেই বোঝা যাচ্ছে—

- `job` → String
- `workers` → Integer
- `config` → Dictionary
- Function → Boolean Return করবে

Production Project-এ এটি Code Maintain করা অনেক সহজ করে দেয়।

---

# Basic Type Hints

## Simple Types

```python
name: str = "Imran"

age: int = 25

price: float = 9.99

is_active: bool = True
```

---

## Collection Types

Python-এর `typing` Module থেকে Collection Types ব্যবহার করা যায়।

```python
from typing import List, Dict, Optional

models: List[str] = [
    "GPT-4",
    "Claude",
    "Llama"
]

config: Dict[str, int] = {
    "max_tokens": 1000,
    "timeout": 30
}
```

---

# Optional

কিছু Variable-এর Value থাকতেও পারে, আবার `None`-ও হতে পারে।

এক্ষেত্রে `Optional` ব্যবহার করা হয়।

```python
from typing import Optional

user_id: Optional[str] = None
```

এখানে `user_id` হয় একটি String হবে, নয়তো `None` হবে।

---

# Function Type Hints

Function-এর Parameter এবং Return Type দুটোই Specify করা যায়।

```python
from typing import Optional

def load_model(
    name: str,
    version: int,
    device: Optional[str] = None
) -> bool:

    print(name)
    print(version)

    return True
```

এখানে—

- `name` → String
- `version` → Integer
- `device` → Optional String
- Function → Boolean Return করবে

---

# Type Hints-এর সবচেয়ে বড় সীমাবদ্ধতা

এখন একটি বিষয় মনে রাখা খুবই গুরুত্বপূর্ণ।

**Type Hints শুধুমাত্র Hint দেয়।**

Python এগুলো Enforce করে না।

উদাহরণ—

```python
def add(a: int, b: int) -> int:
    return a + b

print(add("Hello ", "World"))
```

Output

```text
Hello World
```

অবাক লাগলেও কোনো Error আসবে না।

কারণ Python Type Hints দেখে Code Execute বন্ধ করে না।

এটি শুধুমাত্র Developer-কে বোঝার সুবিধা দেয়।

---

# তাহলে Type Hints-এর লাভ কী?

যদিও Python Runtime-এ Type Check করে না, তবুও Type Hints অনেক জায়গায় সাহায্য করে।

- Code Read করা সহজ হয়
- IDE Auto Suggestion ভালো কাজ করে
- Team Project Maintain করা সহজ হয়
- Bug কম হয়
- Documentation হিসেবে কাজ করে

---

# কিন্তু Runtime Validation কে করবে?

ধরো User API-তে পাঠালো—

```python
{
    "max_tokens": "five hundred"
}
```

কিন্তু আমরা Integer আশা করছিলাম।

Type Hints এখানে Error দিবে না।

এই সমস্যার সমাধান করতে আমরা পরবর্তী Lesson-এ **Pydantic** ব্যবহার করবো।

Pydantic Runtime-এ Data Validate করে এবং ভুল Data হলে Error দেয়।

---

# Practice

নিচের Code Run করো।

```python
from typing import List, Optional

def load_model(
    name: str,
    version: int,
    tags: List[str],
    device: Optional[str] = None
) -> bool:

    print(f"Model Name : {name}")
    print(f"Version    : {version}")
    print(f"Tags       : {tags}")
    print(f"Device     : {device}")

    return True


load_model(
    "Llama-3",
    1,
    ["production", "gpu"]
)
```

---

# Challenge

নিজে একটি Function লেখো।

```python
create_user()
```

Requirements

- name → String
- age → Integer
- skills → List[String]
- email → Optional[String]

Function-এর Return Type হবে `bool`।

---

# আজকের Lesson থেকে যা শিখলে

- Type Hints কী
- কেন Type Hints ব্যবহার করা হয়
- Simple Types
- List
- Dict
- Optional
- Function Type Hints
- Type Hints-এর সীমাবদ্ধতা

---

# Next Lesson

পরবর্তী Lesson-এ আমরা **Pydantic** শিখবো।

সেখানে দেখবো—

- BaseModel
- Data Validation
- Auto Type Conversion
- Custom Validator
- FastAPI-তে Pydantic-এর ব্যবহার

যা Production-level AI Backend Development-এর অন্যতম গুরুত্বপূর্ণ অংশ।