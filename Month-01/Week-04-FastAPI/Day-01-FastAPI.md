# Month 1 → Week 4 → Day 1

# FastAPI (Part 1)

# FastAPI কী?

FastAPI হলো Python এর একটা **Web Framework**।

সহজ ভাষায়—

FastAPI এমন একটা tool, যেটা ব্যবহার করে আমরা API বানাই।

API মানে—

একটা program অন্য একটা program-এর সাথে কথা বলার রাস্তা।

ধরো তোমার AI Cloud এ একজন user prompt পাঠালো।

```
"Explain Docker"
```

এই prompt Server পর্যন্ত কে নিয়ে যাবে?

FastAPI।

আবার AI model যখন answer তৈরি করবে—

সেই answer user-এর কাছে কে পাঠাবে?

FastAPI।

মানে FastAPI-এর কাজ হলো—

- User-এর Request নেওয়া
- Request Process করা
- Response ফেরত পাঠানো

এটা একটা চিঠি আদান-প্রদানের অফিসের মতো।

```
User/Client                FastAPI Server
     │                           │
     │──── POST /inference ─────→│
     │                           │
     │                           │── Job Queue তে দাও
     │                           │── Process করো
     │←── {"response":"..."} ────│
```

---

# কেন FastAPI?

Python এ Web Framework অনেক আছে।

সবচেয়ে জনপ্রিয় তিনটা হলো—

- Flask
- Django
- FastAPI

তাহলে আমরা FastAPI-ই কেন শিখছি?

কারণ AI Backend বানানোর জন্য এটা সবচেয়ে ভালো।

```
Flask
→ ছোট Framework
→ Async support খুব সীমিত
→ AI API এর জন্য এখন আর best choice না

Django
→ অনেক বড় Framework
→ Authentication
→ Admin Panel
→ ORM
→ অনেক extra feature

AI API এর জন্য এগুলোর বেশিরভাগই দরকার হয় না।

FastAPI
→ খুব Fast
→ Async Support Built-in
→ Automatic API Docs
→ Pydantic Built-in
→ Type Hint বুঝে কাজ করে
→ Production Ready
```

আমাদের AI Cloud-এ হাজার হাজার request একসাথে আসতে পারে।

FastAPI এগুলো efficiently handle করতে পারে।

এই কারণেই AI Startup গুলো FastAPI বেশি ব্যবহার করে।

---

# Install করি

আগের Project Folder-এ যাও।

```bash
cd ~/projects/ai-cloud
```

এখন requirements.txt update করি।

```bash
cat > requirements.txt << 'EOF'
fastapi==0.104.0
uvicorn==0.24.0
pydantic==2.0.0
redis==5.0.0
EOF
```

তারপর install করো।

```bash
pip install -r requirements.txt
```

এখন আমাদের Project-এ FastAPI install হয়ে গেছে।

---

# প্রথম FastAPI App

এখন src/main.py file বানাও।

```bash
cat > src/main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI(title="AI Cloud API")

@app.get("/")
async def root():
    return {
        "message": "AI Cloud চালু আছে!"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }
EOF
```

---

# Code টা বুঝি

প্রথম Line—

```python
from fastapi import FastAPI
```

মানে—

FastAPI library থেকে FastAPI class import করছি।

---

তারপর—

```python
app = FastAPI(title="AI Cloud API")
```

এখানে একটা FastAPI Application বানানো হলো।

এই app-এর ভেতরেই আমাদের সব API থাকবে।

---

তারপর—

```python
@app.get("/")
```

মানে—

যদি Browser থেকে

```
GET /
```

Request আসে—

তাহলে নিচের function চালাও।

---

```python
async def root():
```

এটাই Route Function।

FastAPI এই function execute করবে।

---

```python
return {
    "message": "AI Cloud চালু আছে!"
}
```

FastAPI automatically এটাকে JSON বানিয়ে Browser-এ পাঠিয়ে দেবে।

Browser-এ দেখাবে—

```json
{
    "message": "AI Cloud চালু আছে!"
}
```

---

# আরেকটা Route

```python
@app.get("/health")
async def health():
    return {
        "status": "ok"
    }
```

এখন যদি Browser-এ যাও—

```
http://localhost:8000/health
```

Response হবে—

```json
{
    "status": "ok"
}
```

Production Server-এ Health Check করার জন্য এই ধরনের Route অনেক ব্যবহার করা হয়।

---

# App চালাই

Terminal-এ লিখো—

```bash
uvicorn src.main:app --reload
```

---

# এই Command টা ভেঙে বুঝি

```bash
uvicorn
```

মানে—

FastAPI Server চালাও।

---

```bash
src.main
```

মানে—

```
src/main.py
```

এই file।

---

```bash
app
```

মানে—

এই file-এর ভিতরের

```python
app = FastAPI(...)
```

এই variable।

---

```bash
--reload
```

মানে—

Code Change করলে Server Automatically Restart হবে।

তোমাকে বারবার বন্ধ করে আবার চালাতে হবে না।

Development-এর সময় সবসময় এটা ব্যবহার করা হয়।

---

Server চালু হলে দেখবে—

```text
INFO: Uvicorn running on http://127.0.0.1:8000
```

Browser-এ যাও—

```
http://localhost:8000
```

Output—

```json
{
    "message": "AI Cloud চালু আছে!"
}
```

---

# FastAPI এর Magic

Browser-এ যাও—

```
http://localhost:8000/docs
```

FastAPI Automatically একটা Documentation বানিয়ে দেয়।

এখানে—

- সব Route দেখা যাবে
- API Test করা যাবে
- Request পাঠানো যাবে
- Response দেখা যাবে

কোনো আলাদা Documentation লিখতে হবে না।

এটাই FastAPI-এর সবচেয়ে বড় সুবিধাগুলোর একটি।

---

# Route কী?

Route মানে—

User কোন URL-এ গেলে কোন Function চলবে—

সেই Mapping।

উদাহরণ—

```python
@app.get("/health")
async def health():
    return {
        "status": "ok"
    }
```

মানে—

```
GET /health
```

↓

FastAPI

↓

```python
health()
```

↓

```json
{
    "status":"ok"
}
```

---

# HTTP Methods

সব Request একরকম হয় না।

কিছু Data পড়ে।

কিছু Data তৈরি করে।

কিছু Update করে।

কিছু Delete করে।

FastAPI এগুলোর জন্য আলাদা Method দেয়।

```python
@app.get("/jobs")
```

Data পড়ো।

---

```python
@app.post("/jobs")
```

নতুন Data তৈরি করো।

---

```python
@app.put("/jobs/1")
```

আগের Data Update করো।

---

```python
@app.delete("/jobs/1")
```

Data Delete করো।

---

# Path Parameter

কখনো URL-এর ভেতর Variable পাঠাতে হয়।

যেমন—

```
/jobs/job_001
```

এখানে

```
job_001
```

প্রতিবার বদলাবে।

এজন্য Path Parameter ব্যবহার করি।

```python
@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    return {
        "job_id": job_id,
        "status": "processing"
    }
```

---

যদি Request আসে—

```
GET /jobs/job_001
```

তাহলে Response—

```json
{
    "job_id": "job_001",
    "status": "processing"
}
```

---

আবার যদি Request আসে—

```
GET /jobs/job_002
```

তাহলে Response—

```json
{
    "job_id": "job_002",
    "status": "processing"
}
```

FastAPI Automatically URL থেকে Variable নিয়ে আসে।

---

# Query Parameter

সব Data URL-এর Path-এ থাকে না।

কখনো Filter পাঠানো হয়।

যেমন—

```
/jobs?limit=5
```

এখানে

```
limit
```

একটা Query Parameter।

Code—

```python
@app.get("/jobs")
async def list_jobs(
    limit: int = 10,
    status: str = "all"
):
    return {
        "limit": limit,
        "status": status,
        "jobs": []
    }
```

---

Default Request—

```
GET /jobs
```

Response—

```json
{
    "limit": 10,
    "status": "all",
    "jobs": []
}
```

---

যদি Request হয়—

```
GET /jobs?limit=5
```

Response—

```json
{
    "limit": 5,
    "status": "all",
    "jobs": []
}
```

---

যদি Request হয়—

```
GET /jobs?status=done
```

Response—

```json
{
    "limit": 10,
    "status": "done",
    "jobs": []
}
```

---

যদি Request হয়—

```
GET /jobs?limit=5&status=done
```

Response—

```json
{
    "limit": 5,
    "status": "done",
    "jobs": []
}
```

---

# আজ Part 1 এ যা শিখলে

- FastAPI কী
- কেন FastAPI ব্যবহার করি
- FastAPI Install
- প্রথম FastAPI App
- Uvicorn দিয়ে Server চালানো
- Automatic Documentation
- Route
- HTTP Methods
- Path Parameter
- Query Parameter

পরের Part-এ আমরা শিখবো—

- Request Body
- BaseModel
- field_validator (Pydantic v2)
- Response Model
- Error Handling
- Mini AI Job API