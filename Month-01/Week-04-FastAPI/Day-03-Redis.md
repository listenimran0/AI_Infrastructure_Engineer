# Month 1 - Week 4

# Day 3 — FastAPI + Redis

## FastAPI + Redis

### কেন Redis লাগবে?

এখন আমরা `jobs` dictionary তে data রাখছি।

```python
jobs = {}   # RAM এ আছে
```

সমস্যা কী?

- Server restart দিলে → সব jobs হারিয়ে যাবে!
- ২টা server চালালে → আলাদা আলাদা jobs দেখবে!

Redis ব্যবহার করলে—

- Server restart দিলেও data Redis এ থাকবে।
- যতগুলো server থাকুক, সবাই একই Redis থেকে data পড়বে।

---

## Redis কী?

Redis হলো একটা **In-Memory Database**।

মানে—

Data RAM এ রাখে, তাই অনেক দ্রুত কাজ করে।

```
তুমি                 Redis
 │                      │
 │── SET job_001 ─────→ │ (Save)
 │── GET job_001 ─────→ │ (Read)
 │ ←── "queued" ─────── │
```

---

## Redis এর Basic Commands

Redis CLI তে ঢুকো।

```bash
redis-cli
```

Data Save করো।

```bash
SET name "Imran"
```

Data পড়ো।

```bash
GET name
```

Output

```text
"Imran"
```

Delete করো।

```bash
DEL name
```

Expiry Time দাও।

```bash
SET job_001 "queued" EX 3600
```

মানে—

১ ঘণ্টা পরে key auto delete হয়ে যাবে।

সব key দেখো।

```bash
KEYS *
```

---

## Python থেকে Redis ব্যবহার

```python
import redis

r = redis.Redis(
    host="localhost",
    port=6379
)

r.set("job_001", "queued")

status = r.get("job_001")

print(status)
```

Output

```text
b'queued'
```

কেন `b''` আসলো?

কারণ Redis bytes return করে।

String এ convert করতে—

```python
print(status.decode())
```

Output

```text
queued
```

---

## JSON Data Save করা

```python
import json

job_data = {
    "prompt": "Hello",
    "status": "queued"
}

r.set(
    "job_001",
    json.dumps(job_data)
)
```

পড়ো—

```python
data = json.loads(
    r.get("job_001")
)

print(data["prompt"])
```

Output

```text
Hello
```

---

# এবার FastAPI + Redis একসাথে ব্যবহার করি

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import redis
import json
import uuid
import os

app = FastAPI(title="AI Cloud API")

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)

r = redis.from_url(
    REDIS_URL,
    decode_responses=True
)

# decode_responses=True
# bytes না, string return করবে


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


@app.get("/")
async def root():
    return {
        "message": "AI Cloud API চালু আছে!"
    }


@app.get("/health")
async def health():
    try:
        r.ping()

        return {
            "status": "ok",
            "redis": "connected"
        }

    except Exception:
        return {
            "status": "ok",
            "redis": "disconnected"
        }


@app.post(
    "/jobs",
    response_model=JobResponse
)
async def create_job(request: JobRequest):

    job_id = f"job_{uuid.uuid4().hex[:8]}"

    job_data = {
        "job_id": job_id,
        "prompt": request.prompt,
        "model_name": request.model_name,
        "max_tokens": request.max_tokens,
        "priority": request.priority,
        "status": "queued"
    }

    r.set(
        f"job:{job_id}",
        json.dumps(job_data)
    )

    r.zadd(
        "job_queue",
        {job_id: request.priority}
    )

    return JobResponse(
        job_id=job_id,
        status="queued",
        model_name=request.model_name
    )


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):

    data = r.get(f"job:{job_id}")

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Job পাওয়া যায়নি!"
        )

    return json.loads(data)


@app.get("/jobs")
async def list_jobs(limit: int = 10):

    job_ids = r.zrevrange(
        "job_queue",
        0,
        limit - 1
    )

    jobs = []

    for job_id in job_ids:

        data = r.get(
            f"job:{job_id}"
        )

        if data:
            jobs.append(
                json.loads(data)
            )

    return {
        "total": len(jobs),
        "jobs": jobs
    }


@app.delete("/jobs/{job_id}")
async def delete_job(job_id: str):

    deleted = r.delete(
        f"job:{job_id}"
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Job পাওয়া যায়নি!"
        )

    r.zrem(
        "job_queue",
        job_id
    )

    return {
        "message": f"{job_id} মুছে গেছে"
    }
```

---

## কোডটা কী করছে?

### Redis Connection

```python
r = redis.from_url(
    REDIS_URL,
    decode_responses=True
)
```

এখান থেকে Redis এর সাথে connection হচ্ছে।

`decode_responses=True` দেওয়ায় bytes এর বদলে string পাওয়া যাবে।

---

### Job Save

```python
r.set(
    f"job:{job_id}",
    json.dumps(job_data)
)
```

Job Redis এ save হচ্ছে।

---

### Priority Queue

```python
r.zadd(
    "job_queue",
    {job_id: request.priority}
)
```

`zadd()` মানে Sorted Set এ data রাখা।

Priority যত বেশি হবে,
তত আগে আসবে।

---

### Job Read

```python
data = r.get(
    f"job:{job_id}"
)
```

Redis থেকে Job পড়ছে।

---

### Queue অনুযায়ী List

```python
r.zrevrange(
    "job_queue",
    0,
    limit - 1
)
```

Highest Priority Job আগে আসবে।

---

### Delete

```python
r.delete(...)
```

Redis থেকে Job মুছে ফেলছে।

```python
r.zrem(...)
```

Queue থেকেও remove করছে।

---

# Docker Compose Update

`docker-compose.yml`

```yaml
version: "3.8"

services:

  app:
    build: .

    ports:
      - "8000:8000"

    environment:
      - REDIS_URL=redis://redis:6379

    depends_on:
      - redis

    volumes:
      - .:/app

    command: uvicorn src.main:app --host 0.0.0.0 --reload

  redis:
    image: redis:7-alpine

    ports:
      - "6379:6379"
```

---

## Run করো

```bash
docker compose up --build
```

---

# Test করো

## 1. Health Check

```
GET /health
```

Expected Output

```json
{
  "status": "ok",
  "redis": "connected"
}
```

---

## 2. প্রথম Job Create করো

```
POST /jobs
```

```json
{
  "prompt": "Hello AI",
  "model_name": "llama-3",
  "priority": 5
}
```

Expected Output

```json
{
  "job_id": "job_a1b2c3d4",
  "status": "queued",
  "model_name": "llama-3"
}
```

---

## 3. আরেকটা Job Create করো

```json
{
  "prompt": "What is GPU?",
  "model_name": "gpt-4",
  "priority": 1
}
```

Expected Output

```json
{
  "job_id": "job_x8y7z6w5",
  "status": "queued",
  "model_name": "gpt-4"
}
```

---

## 4. সব Job দেখো

```
GET /jobs
```

Expected Output

```json
{
  "total": 2,
  "jobs": [
    {
      "job_id": "job_a1b2c3d4",
      "priority": 5,
      "status": "queued"
    },
    {
      "job_id": "job_x8y7z6w5",
      "priority": 1,
      "status": "queued"
    }
  ]
}
```

খেয়াল করো—

Priority **5** এর Job আগে এসেছে।

---

## 5. নির্দিষ্ট Job দেখো

```
GET /jobs/job_a1b2c3d4
```

Expected Output

```json
{
  "job_id": "job_a1b2c3d4",
  "prompt": "Hello AI",
  "model_name": "llama-3",
  "priority": 5,
  "status": "queued"
}
```

---

## 6. Job Delete করো

```
DELETE /jobs/job_a1b2c3d4
```

Expected Output

```json
{
  "message": "job_a1b2c3d4 মুছে গেছে"
}
```

---

# আজকে কী শিখলে?

| Command | কাজ |
|----------|-----|
| `r.set()` | Redis এ Save |
| `r.get()` | Redis থেকে Read |
| `r.delete()` | Redis থেকে Delete |
| `r.ping()` | Redis চলছে কিনা Check |
| `r.zadd()` | Priority Queue তে Add |
| `r.zrevrange()` | Priority অনুযায়ী Read |
| `docker compose up --build` | App + Redis একসাথে চালানো |

---

এখন `/docs` থেকে সব API একবার Test করো।

সব Output যদি উপরের মতো আসে, তাহলে FastAPI এবং Redis integration ঠিকভাবে কাজ করছে।