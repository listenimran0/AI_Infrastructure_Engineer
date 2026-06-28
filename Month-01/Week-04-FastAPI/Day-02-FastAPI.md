# Month 1 → Week 4 → Day 2

# FastAPI (Part 2)

# Request Body

এখন পর্যন্ত আমরা URL থেকে Data নিয়েছি।

কিন্তু AI Cloud-এ User Prompt পাঠাবে কীভাবে?

ধরো User এই Data পাঠালো—

```json
{
  "prompt": "Explain Docker",
  "model_name": "llama-3",
  "priority": 3
}
```

এই JSON Data-কে FastAPI-এর ভিতরে Receive করার জন্য আমরা **Request Body** ব্যবহার করি।

আর Request Body Handle করার জন্য FastAPI ব্যবহার করে **Pydantic**।

---

# Pydantic কী?

Pydantic হলো Python-এর একটা Data Validation Library।

এর কাজ হলো—

- User যে JSON পাঠিয়েছে সেটা পড়া
- JSON-কে Python Object বানানো
- Data Validate করা
- ভুল হলে Automatically Error দেওয়া

মানে—

```
JSON
      │
      ▼
Pydantic
      │
      ▼
Python Object
```

---

# Request Model

```python
from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI(title="AI Cloud API")


class InferenceRequest(BaseModel):
    prompt: str
    model_name: str = "llama-3"
    max_tokens: int = 1000
    priority: int = 1

    @field_validator("priority")
    @classmethod
    def priority_valid(cls, value):
        if not 1 <= value <= 5:
            raise ValueError("Priority ১ থেকে ৫ এর মধ্যে হতে হবে!")
        return value
```

---

# Code টা ভেঙে বুঝি

```python
class InferenceRequest(BaseModel):
```

মানে—

User যে JSON পাঠাবে—

সেটার Structure এই Class-এর মতো হবে।

---

```python
prompt: str
```

User অবশ্যই একটা Prompt পাঠাবে।

যেমন—

```json
{
  "prompt": "Explain Docker"
}
```

---

```python
model_name: str = "llama-3"
```

যদি User Model Name না পাঠায়—

তাহলে Default হিসেবে

```
llama-3
```

ব্যবহার হবে।

---

```python
max_tokens: int = 1000
```

Default Value হবে—

```
1000
```

---

```python
priority: int = 1
```

Default Priority হবে—

```
1
```

---

# field_validator কী?

Pydantic v2 থেকে

```
@validator
```

Deprecated।

এখন ব্যবহার করা হয়—

```python
@field_validator()
```

---

আমরা লিখেছি—

```python
@field_validator("priority")
```

মানে—

Priority Field Validate করো।

---

```python
@classmethod
def priority_valid(cls, value):
```

এখানে

```
value
```

হলো User যে Value পাঠিয়েছে।

---

যদি Value হয়—

```
3
```

তাহলে

```
value = 3
```

---

তারপর—

```python
if not 1 <= value <= 5:
```

মানে—

Priority যদি

১–৫

এর মধ্যে না থাকে—

---

তাহলে—

```python
raise ValueError(...)
```

Error দাও।

---

না হলে—

```python
return value
```

মানে—

ঠিক আছে।

এই Value ব্যবহার করো।

---

# Response Model

Request যেমন একটা Structure Follow করে,

Response-এরও একটা Structure থাকতে পারে।

```python
class InferenceResponse(BaseModel):
    job_id: str
    status: str
    message: str
```

এখন Server সবসময় এই Format-এ Response পাঠাবে।

---

# POST Route

```python
@app.post(
    "/inference",
    response_model=InferenceResponse
)
async def run_inference(
    request: InferenceRequest
):

    return InferenceResponse(
        job_id="job_001",
        status="queued",
        message=f"{request.model_name} এ Job দেওয়া হয়েছে!"
    )
```

---

# এখানে কী হচ্ছে?

```python
@app.post("/inference")
```

মানে—

যখন

```
POST /inference
```

Request আসবে—

তখন এই Function চলবে।

---

```python
request: InferenceRequest
```

FastAPI Automatically—

- JSON Receive করবে
- Pydantic দিয়ে Validate করবে
- Python Object বানাবে

তোমাকে Manual Parsing করতে হবে না।

---

যদি User পাঠায়—

```json
{
  "prompt": "Explain Docker",
  "model_name": "llama-3",
  "priority": 3
}
```

তাহলে Function-এর ভিতরে লিখতে পারবে—

```python
request.prompt

request.model_name

request.priority
```

---

Response হবে—

```json
{
  "job_id": "job_001",
  "status": "queued",
  "message": "llama-3 এ Job দেওয়া হয়েছে!"
}
```

---

# ভুল Data পাঠালে কী হবে?

যদি User পাঠায়—

```json
{
  "prompt": "Hello",
  "priority": 10
}
```

তাহলে

```
field_validator()
```

Run হবে।

Priority Invalid।

FastAPI Automatically Error Return করবে।

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "priority"
      ],
      "msg": "Priority ১ থেকে ৫ এর মধ্যে হতে হবে!"
    }
  ]
}
```

Validation-এর জন্য আলাদা Code লিখতে হয় না।

---

# Error Handling

সব Error Validation Error না।

ধরো User একটা Job দেখতে চাইলো।

কিন্তু সেই Job Database-এ নেই।

তখন কী করবে?

---

```python
from fastapi import HTTPException
```

---

```python
@app.get("/jobs/{job_id}")
async def get_job(job_id: str):

    if job_id not in [
        "job_001",
        "job_002"
    ]:

        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} পাওয়া যায়নি!"
        )

    return {
        "job_id": job_id,
        "status": "processing"
    }
```

---

যদি Request হয়—

```
GET /jobs/job_001
```

Response—

```json
{
  "job_id": "job_001",
  "status": "processing"
}
```

---

যদি Request হয়—

```
GET /jobs/job_999
```

Response—

```json
{
  "detail": "Job job_999 পাওয়া যায়নি!"
}
```

Status Code হবে—

```
404 Not Found
```

---

# আজকের Mini Project

এবার একটা ছোট AI Job API বানাও।

```bash
cat > src/main.py << 'EOF'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import uuid

app = FastAPI(title="AI Cloud API")

jobs = {}


class JobRequest(BaseModel):
    prompt: str
    model_name: str = "llama-3"
    max_tokens: int = 1000
    priority: int = 1

    @field_validator("priority")
    @classmethod
    def priority_valid(cls, value):
        if not 1 <= value <= 5:
            raise ValueError("Priority ১ থেকে ৫ এর মধ্যে হতে হবে!")
        return value


class JobResponse(BaseModel):
    job_id: str
    status: str
    model_name: str


@app.get("/")
async def root():
    return {
        "message": "AI Cloud API চালু আছে!"
    }


@app.post("/jobs", response_model=JobResponse)
async def create_job(request: JobRequest):

    job_id = f"job_{uuid.uuid4().hex[:8]}"

    jobs[job_id] = {
        "prompt": request.prompt,
        "model_name": request.model_name,
        "status": "queued",
        "priority": request.priority
    }

    return JobResponse(
        job_id=job_id,
        status="queued",
        model_name=request.model_name
    )


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job পাওয়া যায়নি!"
        )

    return {
        "job_id": job_id,
        **jobs[job_id]
    }


@app.get("/jobs")
async def list_jobs(limit: int = 10):

    job_list = list(jobs.items())[:limit]

    return {
        "total": len(jobs),
        "jobs": job_list
    }
EOF
```

---

# App চালাও

```bash
uvicorn src.main:app --reload
```

---

# Browser-এ যাও

```
http://localhost:8000/docs
```

এখান থেকে সব API Test করতে পারবে।

---

# নতুন Job Create করো

`POST /jobs`

Body—

```json
{
  "prompt": "Hello AI",
  "model_name": "llama-3",
  "priority": 3
}
```

Response—

```json
{
  "job_id": "job_a3f9d4c2",
  "status": "queued",
  "model_name": "llama-3"
}
```

---

# Job Fetch করো

```
GET /jobs/{job_id}
```

উদাহরণ—

```
GET /jobs/job_a3f9d4c2
```

---

# সব Job দেখো

```
GET /jobs
```

---

# আজ যা শিখলে

- Request Body
- Pydantic
- BaseModel
- field_validator
- Response Model
- POST Route
- Automatic Validation
- HTTPException
- In-memory Job Storage
- Simple AI Job API

---

# Homework

আজকের Task—

- FastAPI App চালাও
- `/docs` Open করো
- একটা নতুন Job Create করো
- Job ID Copy করো
- সেই Job Fetch করো
- `/jobs` দিয়ে সব Job দেখো

