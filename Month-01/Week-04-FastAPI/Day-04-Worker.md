# Month 1 - Week 4

# Day 4 — Background Tasks + Worker

## আগে সমস্যাটা বোঝো

এখন আমাদের API কী করছে?

```
Client
   │
   │ POST /jobs
   ▼
FastAPI
   │
   ▼
Redis এ Save
   │
   ▼
Response দিয়ে দিলো
```

কিন্তু একটা সমস্যা আছে।

Job শুধু Redis এ Queue তে বসে আছে।

কেউ সেই Job Process করছে না।

---

## Real System এ কী হওয়া উচিত?

```
Client
   │
   │ POST /jobs
   ▼
FastAPI
   │
   ▼
Redis Queue
   │
   ▼
Worker
   │
   ▼
Job Process
   │
   ▼
Status Update
```

অর্থাৎ—

- Client Request দিলো।
- FastAPI Job Queue তে রেখে দিলো।
- Worker পরে সেই Job তুলে Process করলো।
- তারপর Status Update করলো।

```
queued
   │
   ▼
processing
   │
   ▼
done
```

---

# FastAPI Background Tasks

FastAPI এর built-in **BackgroundTasks** আছে।

এটা কী করে?

Response পাঠিয়ে দেয় আগে।

তারপর Background এ Function চালায়।

```python
from fastapi import BackgroundTasks

@app.post("/jobs")
async def create_job(
    request: JobRequest,
    background_tasks: BackgroundTasks
):

    job_id = f"job_{uuid.uuid4().hex[:8]}"

    r.set(
        f"job:{job_id}",
        json.dumps({...})
    )

    background_tasks.add_task(
        process_job,
        job_id
    )

    return {
        "job_id": job_id,
        "status": "queued"
    }
```

---

## `background_tasks.add_task()` কী করে?

```python
background_tasks.add_task(
    process_job,
    job_id
)
```

মানে—

```
Response পাঠাও
        │
        ▼
process_job(job_id)
```

Client অপেক্ষা করবে না।

Response সাথে সাথেই পেয়ে যাবে।

Background এ Processing চলতে থাকবে।

---

# Worker Function বানাও

`src/worker.py`

```python
import redis
import json
import os
import asyncio

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)

r = redis.from_url(
    REDIS_URL,
    decode_responses=True
)


async def process_job(job_id: str):

    print(f"Processing শুরু: {job_id}")

    data = json.loads(
        r.get(f"job:{job_id}")
    )

    data["status"] = "processing"

    r.set(
        f"job:{job_id}",
        json.dumps(data)
    )

    await simulate_ai_inference(data)

    data["status"] = "done"

    data["result"] = (
        f"AI response for: {data['prompt']}"
    )

    r.set(
        f"job:{job_id}",
        json.dumps(data)
    )

    r.zrem(
        "job_queue",
        job_id
    )

    print(f"Done: {job_id}")


async def simulate_ai_inference(data: dict):

    delays = {
        "llama-3": 2,
        "gpt-4": 3,
        "claude": 1.5
    }

    delay = delays.get(
        data["model_name"],
        2
    )

    print(
        f"{data['model_name']} processing ({delay}s)..."
    )

    await asyncio.sleep(delay)
```

---

## Worker কী করছে?

### Step 1

Redis থেকে Job পড়ছে।

```python
data = json.loads(
    r.get(f"job:{job_id}")
)
```

---

### Step 2

Status Update করছে।

```python
data["status"] = "processing"
```

---

### Step 3

AI কাজ করছে এমন অভিনয় করছে।

```python
await simulate_ai_inference(data)
```

এখন শুধু `sleep()` হচ্ছে।

পরে এখানে LLM Call হবে।

---

### Step 4

Processing শেষ।

```python
data["status"] = "done"
```

Result Add করছে।

```python
data["result"] = (
    f"AI response for: {data['prompt']}"
)
```

---

### Step 5

Redis Update করছে।

```python
r.set(
    f"job:{job_id}",
    json.dumps(data)
)
```

---

### Step 6

Queue থেকে Remove করছে।

```python
r.zrem(
    "job_queue",
    job_id
)
```

---

# main.py Update

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, field_validator
import redis
import json
import uuid
import os

from src.worker import process_job

app = FastAPI(title="AI Cloud API")

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)

r = redis.from_url(
    REDIS_URL,
    decode_responses=True
)


class JobRequest(BaseModel):
    prompt: str
    model_name: str = "llama-3"
    max_tokens: int = 1000
    priority: int = 1

    @field_validator("priority")
    @classmethod
    def priority_valid(cls, value):
        if not 1 <= value <= 5:
            raise ValueError(
                "Priority ১ থেকে ৫ এর মধ্যে হতে হবে!"
            )
        return value


class JobResponse(BaseModel):
    job_id: str
    status: str
    model_name: str
    message: str


@app.post(
    "/jobs",
    response_model=JobResponse
)
async def create_job(
    request: JobRequest,
    background_tasks: BackgroundTasks
):

    job_id = f"job_{uuid.uuid4().hex[:8]}"

    job_data = {
        "job_id": job_id,
        "prompt": request.prompt,
        "model_name": request.model_name,
        "max_tokens": request.max_tokens,
        "priority": request.priority,
        "status": "queued",
        "result": None
    }

    r.set(
        f"job:{job_id}",
        json.dumps(job_data)
    )

    r.zadd(
        "job_queue",
        {job_id: request.priority}
    )

    background_tasks.add_task(
        process_job,
        job_id
    )

    return JobResponse(
        job_id=job_id,
        status="queued",
        model_name=request.model_name,
        message="Job queue তে গেছে, processing শুরু হবে!"
    )


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):

    data = r.get(
        f"job:{job_id}"
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Job পাওয়া যায়নি!"
        )

    return json.loads(data)
```

---

# Run করো

```bash
docker compose up --build
```

---

# Test Flow

## Step 1

```
POST /jobs
```

```json
{
  "prompt": "Hello AI",
  "model_name": "llama-3",
  "priority": 3
}
```

Response

```json
{
  "job_id": "job_a1b2",
  "status": "queued",
  "model_name": "llama-3",
  "message": "Job queue তে গেছে, processing শুরু হবে!"
}
```

---

## Step 2

সাথে সাথেই Status দেখো।

```
GET /jobs/job_a1b2
```

Expected Output

```json
{
  "job_id": "job_a1b2",
  "status": "processing"
}
```

---

## Step 3

২–৩ সেকেন্ড পরে আবার দেখো।

```
GET /jobs/job_a1b2
```

Expected Output

```json
{
  "job_id": "job_a1b2",
  "status": "done",
  "result": "AI response for: Hello AI"
}
```

---

## Terminal Output

```text
Processing শুরু: job_a1b2
llama-3 processing (2s)...
Done: job_a1b2
```

---

# আজকে কী শিখলে?

| জিনিস | কাজ |
|--------|-----|
| `BackgroundTasks` | Response পাঠানোর পরে Background এ কাজ চালায় |
| `add_task()` | Background Function Run করে |
| `Worker` | Queue থেকে Job Process করে |
| `processing` | Job চলছে |
| `done` | Job শেষ |
| `result` | AI এর Response Store করে |

---

## আজকের Flow

```
Client
    │
POST /jobs
    │
    ▼
Redis Queue
    │
    ▼
Background Task
    │
    ▼
Worker
    │
    ▼
processing
    │
    ▼
done
    │
    ▼
Result Redis এ Save
```

এখন `/docs` থেকে একটি Job Create করো, তারপর সাথে সাথে `GET /jobs/{job_id}` কল করে Status দেখো। ২–৩ সেকেন্ড পরে আবার Call করলে Status `done` এবং `result` দেখতে পাবে।