# Docker Compose — Part 2

আগের অংশে আমরা `docker-compose.yml` লিখেছি এবং Compose-এর প্রতিটা অংশ বুঝেছি।

এখন দেখি, কীভাবে এটা ব্যবহার করে আমাদের Application চালানো যায়।

---

# Step 1 — `main.py` আপডেট করি

আগে আমাদের Program শুধু একটা Message Print করত।

এবার আমরা Docker Compose থেকে আসা Environment Variable পড়বো।

`src/main.py` File-টা নিচের মতো করে Update করো।

```python
import os

redis_url = os.getenv("REDIS_URL", "না পাওয়া গেছে")

print("AI Cloud চালু হলো!")
print(f"Redis URL: {redis_url}")
print("সব Service Ready!")
```

এখানে নতুন একটা জিনিস দেখছো।

```python
os.getenv()
```

এটা Environment Variable পড়ার জন্য ব্যবহার করা হয়।

---

# `os.getenv()` কী?

ধরো Docker Compose থেকে আমরা এই Variable পাঠিয়েছি।

```yaml
environment:
  - REDIS_URL=redis://redis:6379
```

Python-এর ভিতরে

```python
os.getenv("REDIS_URL")
```

লিখলে Return করবে—

```text
redis://redis:6379
```

যদি Variable না থাকে তাহলে দ্বিতীয় Parameter Return করবে।

```python
os.getenv("REDIS_URL", "না পাওয়া গেছে")
```

তখন Output হবে—

```text
না পাওয়া গেছে
```

এভাবে Program Crash না করে Safe ভাবে Variable পড়া যায়।

---

# Step 2 — সব Container একসাথে চালাও

এখন Project Folder-এ গিয়ে Run করো।

```bash
docker compose up
```

প্রথমবার চালালে Compose কয়েকটা কাজ করবে।

১. Dockerfile থেকে App Image Build করবে।

২. Redis Image Download করবে (যদি আগে না থাকে)।

৩. দুইটা Container Start করবে।

৪. একই Network-এর মধ্যে রাখবে।

৫. তারপর Log দেখাবে।

Output কিছুটা এমন হতে পারে।

```text
redis_1  | Ready to accept connections

app_1    | AI Cloud চালু হলো!
app_1    | Redis URL: redis://redis:6379
app_1    | সব Service Ready!
```

যদি এই Output দেখতে পাও তাহলে বুঝবে সব ঠিকভাবে কাজ করছে।

---

# Background-এ Container চালানো

সব সময় Terminal Open রেখে দিতে ইচ্ছা করবে না।

তখন ব্যবহার করো—

```bash
docker compose up -d
```

এখানে

```text
-d
```

মানে Detached Mode।

অর্থাৎ Container Background-এ চলবে।

Terminal আবার ব্যবহার করতে পারবে।

---

# কোন কোন Service চলছে দেখো

```bash
docker compose ps
```

Output কিছুটা এমন হবে।

```text
NAME              STATUS

ai-cloud-app      Up
ai-cloud-redis    Up
```

এখান থেকে বুঝতে পারবে কোন Service Running আছে।

---

# নির্দিষ্ট Service-এর Log দেখো

App-এর Log দেখতে চাইলে—

```bash
docker compose logs app
```

Redis-এর Log দেখতে চাইলে—

```bash
docker compose logs redis
```

একসাথে সব Log দেখতে চাইলে—

```bash
docker compose logs
```

---

# Live Log দেখো

অনেক সময় Application Run করার সময় সাথে সাথে Log দেখতে হয়।

তখন ব্যবহার করো।

```bash
docker compose logs -f app
```

এখানে

```text
-f
```

মানে Follow।

যতক্ষণ Application নতুন Log লিখবে, Terminal-এ ততক্ষণ দেখতে থাকবে।

এটা Debug করার সময় খুব কাজে লাগে।

---

# সব Container বন্ধ করো

সব Service Stop করতে চাইলে—

```bash
docker compose down
```

এটা করলে—

* সব Container Stop হবে।
* Network Remove হবে।

কিন্তু Data Volume থেকে যাবে।

---

# সবকিছু Remove করতে চাইলে

```bash
docker compose down -v
```

এখানে

```text
-v
```

মানে Volume-ও Delete করো।

যদি Database-এর Data রাখতে চাও তাহলে `-v` ব্যবহার করবে না।

---

# একটা প্রশ্ন

App Container কীভাবে Redis Container-কে খুঁজে পেল?

আমরা তো কোথাও Redis-এর IP লিখিনি।

তবুও এটা কাজ করছে কেন?

---

# Service Discovery

Compose-এর সবচেয়ে সুন্দর Feature হলো—

সব Service Automatically একই Network-এ থাকে।

ধরো তোমার Compose File এমন।

```yaml
services:

  app:
    environment:
      - REDIS_URL=redis://redis:6379

  redis:
    image: redis:7-alpine
```

এখানে

```text
redis://redis:6379
```

এই URL-এর

```text
redis
```

অংশটা কোনো IP Address না।

এটা Service Name।

Docker Compose নিজেরাই একটা Internal DNS তৈরি করে।

তাই App যখন বলে—

> "আমি redis নামে একটা Service খুঁজছি"

Docker সঙ্গে সঙ্গে Redis Container-এর Address খুঁজে দেয়।

এজন্য IP Address মুখস্থ রাখার দরকার হয় না।

---

# আসলে ভিতরে কী হয়?

এটা অনেকটা Office-এর মতো।

ধরো একটা Office-এ তিনজন মানুষ আছে।

```
App
Redis
MongoDB
```

App যদি বলে—

> "Redis কোথায়?"

Docker উত্তর দেয়—

> "ওই যে Redis Service, আমি চিনি।"

এজন্য Service Name দিয়েই Container-গুলো একে অপরের সাথে যোগাযোগ করতে পারে।

---

# আমাদের Project এখন কেমন দেখাচ্ছে?

```
                docker compose up
                        │
                        ▼

          ┌─────────────────────────┐
          │     Docker Compose       │
          └──────────┬──────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼

     App Container        Redis Container
          │
          │  redis://redis:6379
          ▼
      Redis-এর সাথে Connect
```

এখন আর আলাদা আলাদা Command দিয়ে Container চালাতে হবে না।

Compose সবকিছু Manage করবে।

---

# আজকের Practice

## ১. `docker-compose.yml` বানাও

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:

  app:
    build: .
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

EOF
```

---

## ২. `main.py` Update করো

```bash
cat > src/main.py << 'EOF'
import os

redis_url = os.getenv("REDIS_URL", "না পাওয়া গেছে")

print("AI Cloud চালু হলো!")
print(f"Redis URL: {redis_url}")
print("Docker Compose কাজ করছে!")
EOF
```

---

## ৩. সব Service চালাও

```bash
docker compose up
```

যদি সব ঠিক থাকে তাহলে Output এমন হবে।

```text
redis_1  | Ready to accept connections

app_1    | AI Cloud চালু হলো!
app_1    | Redis URL: redis://redis:6379
app_1    | Docker Compose কাজ করছে!
```

---

# Useful Commands

| Command                      | কাজ                                   |
| ---------------------------- | ------------------------------------- |
| `docker compose up`          | সব Service একসাথে চালু করে            |
| `docker compose up -d`       | Background-এ চালায়                   |
| `docker compose ps`          | কোন Service চলছে দেখায়               |
| `docker compose logs`        | সব Service-এর Log দেখায়              |
| `docker compose logs app`    | App-এর Log দেখায়                     |
| `docker compose logs redis`  | Redis-এর Log দেখায়                   |
| `docker compose logs -f app` | Live Log Follow করে                   |
| `docker compose down`        | সব Container Stop করে                 |
| `docker compose down -v`     | Container-এর সাথে Volume-ও Remove করে |

---

# এই Chapter-এর Summary

এই Chapter শেষে তুমি শিখলে—

* Docker Compose কেন ব্যবহার করা হয়।
* এক Command দিয়ে একাধিক Container কীভাবে চালানো যায়।
* `docker compose up` কী করে।
* Background-এ Container কীভাবে চালাতে হয়।
* Log কীভাবে দেখতে হয়।
* Container কীভাবে Stop করতে হয়।
* Volume Remove করার নিয়ম।
* Docker Compose-এর Internal Network কীভাবে কাজ করে।
* কেন `redis://redis:6379` লিখলেই App Redis-কে খুঁজে পায়।

