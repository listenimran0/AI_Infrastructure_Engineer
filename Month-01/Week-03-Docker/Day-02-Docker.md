# Docker Compose — একসাথে একাধিক Container চালানোর সহজ উপায়

আগের Chapter-এ আমরা Docker দিয়ে একটা Container বানিয়েছিলাম।

সেখানে একটা Python App ছিল, তাই একটা `docker run` দিয়েই কাজ হয়ে গিয়েছিল।

কিন্তু বাস্তবে কোনো Application শুধু একটা Container দিয়ে চলে না।

বিশেষ করে AI Application, Backend কিংবা SaaS Project-এ একাধিক Service একসাথে লাগে।

ধরো, তুমি একটা AI Cloud বানাচ্ছো।

সেখানে থাকতে পারে—

* Python/FastAPI Application
* Redis (Job Queue)
* MongoDB (Database)
* Nginx (Reverse Proxy)

এখন যদি প্রতিটা Service আলাদা আলাদা চালাও...

```bash
docker run ai-cloud:v1
```

তারপর আরেকটা Terminal খুলে...

```bash
docker run redis:7
```

আবার আরেকটা Terminal...

```bash
docker run mongo:6
```

কিছুদিন পরেই বুঝবে—

* কোন Container আগে চালাতে হবে মনে থাকে না।
* কোন Port কোনটার জন্য সেটা ভুলে যাও।
* Environment Variable আলাদা করে দিতে হয়।
* একসাথে Start বা Stop করাও ঝামেলা।

ছোট Project-এ হয়তো সমস্যা হবে না।

কিন্তু Project বড় হতে শুরু করলে এটা Manage করা কঠিন হয়ে যায়।

এখানেই Docker Compose-এর দরকার হয়।

---

# Docker Compose কী?

Docker Compose এমন একটা Tool, যেটা একাধিক Container-কে একসাথে Manage করে।

মানে, কোন Container চলবে, কোনটা আগে Start হবে, কোন Port ব্যবহার করবে, কোন Environment Variable লাগবে—সব একটা File-এর মধ্যে লিখে রাখা যায়।

তারপর শুধু একটা Command দিলেই সব Container একসাথে চালু হয়ে যায়।

```bash
docker compose up
```

এটাই Docker Compose-এর সবচেয়ে বড় সুবিধা।

---

# docker-compose.yml File

Docker Compose-এর Configuration একটা YAML File-এর মধ্যে লেখা হয়।

Project Folder-এ একটা নতুন File বানাও।

```bash
cd ~/projects/ai-cloud

cat > docker-compose.yml << 'EOF'
version: '3.8'

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
      - ./logs:/app/logs

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

EOF
```

এই File-টাই Docker Compose-এর পুরো Blueprint।

এখন একে একে প্রতিটা অংশ বুঝি।

---

# version

```yaml
version: "3.8"
```

এটা Compose File-এর Version।

আগে Version উল্লেখ করা লাগত।

বর্তমান Docker Compose-এ অনেক সময় এটা Optional হলেও, অনেক Project-এ এখনো Compatibility-এর জন্য রাখা হয়।

---

# services

সবচেয়ে গুরুত্বপূর্ণ অংশ হলো `services`।

```yaml
services:
```

এখানে লেখা হয়—

"Project-এ কোন কোন Container চলবে?"

আমাদের Project-এ দুইটা Service আছে।

```yaml
services:

  app:

  redis:
```

এখানে

* `app` হলো Python Application
* `redis` হলো Redis Server

এগুলোই Service Name।

পরে দেখবে, এই নাম দিয়েই এক Container আরেকটাকে খুঁজে পায়।

---

# build

```yaml
app:
  build: .
```

`build` মানে—

Dockerfile ব্যবহার করে Image বানাও।

এখানে Dot (`.`) মানে Current Folder।

অর্থাৎ Docker Compose বর্তমান Folder-এ Dockerfile খুঁজবে।

তারপর সেই Dockerfile ব্যবহার করে Image Build করবে।

প্রতি বার আলাদা করে

```bash
docker build
```

চালাতে হবে না।

Compose নিজেই Build করে নেবে।

---

# image

Redis-এর ক্ষেত্রে আমরা নিজেরা Dockerfile লিখিনি।

কারণ Redis-এর Official Image আগেই Docker Hub-এ আছে।

তাই এখানে লিখি—

```yaml
redis:
  image: redis:7-alpine
```

মানে,

Docker Hub থেকে `redis:7-alpine` Image Download করো।

যদি আগে Download করা থাকে তাহলে সেটাই ব্যবহার করবে।

না থাকলে প্রথমবার Automatically Download হবে।

---

# ports

```yaml
ports:
  - "8000:8000"
```

এখানে দুইটা সংখ্যা আছে।

```
8000 : 8000
```

প্রথমটা হলো তোমার Laptop-এর Port।

দ্বিতীয়টা হলো Container-এর Port।

মানে—

```
Laptop:8000
        │
        ▼
Container:8000
```

তুমি Browser-এ

```
http://localhost:8000
```

লিখলে সেটা Container-এর Port 8000-এ চলে যাবে।

Redis-এর ক্ষেত্রেও একই নিয়ম।

```yaml
ports:
  - "6379:6379"
```

এখানে Laptop-এর Port 6379 Container-এর Port 6379-এর সাথে যুক্ত হয়েছে।

---

# environment

Container-এর ভিতরে Environment Variable পাঠানোর জন্য `environment` ব্যবহার করা হয়।

```yaml
environment:
  - REDIS_URL=redis://redis:6379
```

এখন App-এর ভিতরে

```python
os.getenv("REDIS_URL")
```

লিখলে এই Value পাওয়া যাবে।

```
redis://redis:6379
```

এভাবে Password, API Key, Database URL, Secret Key—সব পাঠানো যায়।

বাস্তব Project-এ Environment Variable খুব বেশি ব্যবহার করা হয়।

---

# depends_on

সব Container একসাথে Start হলেও সব Service একই সময় Ready হয় না।

ধরো—

App Start হওয়ার আগেই Redis Ready থাকতে হবে।

তাহলে লিখবে—

```yaml
depends_on:
  - redis
```

মানে—

আগে Redis Container Start করো।

তারপর App Container চালাও।

এতে Startup Order Maintain হয়।

তবে একটা বিষয় মনে রাখবে।

`depends_on` শুধু Container Start হওয়ার Order ঠিক করে।

Redis পুরোপুরি Ready হয়েছে কিনা, সেটা Check করে না।

Production-এ এজন্য Health Check বা Retry Logic ব্যবহার করা হয়।

---

# volumes

অনেক সময় Container-এর ভিতরের File বাইরে Save করতে হয়।

সেটার জন্য Volume ব্যবহার করা হয়।

```yaml
volumes:
  - ./logs:/app/logs
```

এখানে দুইটা Path আছে।

```
./logs
```

এটা তোমার Laptop-এর Folder।

আর

```
/app/logs
```

এটা Container-এর Folder।

মানে Container-এর `/app/logs` Folder-এ যা লেখা হবে...

সেটা Laptop-এর `logs` Folder-এও দেখা যাবে।

এই Process-কে Volume Mapping বলা হয়।

এটা Log File, Upload File, Database Data কিংবা Cache Store করার জন্য খুবই গুরুত্বপূর্ণ।

---

# এই পর্যন্ত কী শিখলাম?

এই Chapter-এ আমরা শিখলাম—

* Docker Compose কেন দরকার
* `docker-compose.yml` কী
* `services`
* `build`
* `image`
* `ports`
* `environment`
* `depends_on`
* `volumes`

এখন আমাদের Project এমন অবস্থায় এসেছে যেখানে এক Command দিয়েই App এবং Redis একসাথে চালানো যাবে।

পরের অংশে আমরা দেখবো—

* `main.py` আপডেট করা
* `docker compose up`
* Useful Commands
* Logs দেখা
* Container Network
* কেন `redis://redis:6379` কাজ করে
* Practice Task এবং Summary
