# Docker — একদম বাচ্চাদের মতো করে বুঝি

> যদি Docker শুনে ভয় লাগে, তাহলে এই লেখাটা তোমার জন্য।
> এখানে আমরা Docker এমনভাবে বুঝবো, যেন আগে কখনো Docker দেখিনি।

---

# আগে একটা সমস্যা বুঝি

ধরো, তুমি তোমার Laptop-এ একটা AI App বানালে।

সব ঠিকঠাক চলছে।

কিন্তু Server-এ Deploy করার পর...

App চলছে না।

কেন?

কারণ তোমার Laptop আর Server একরকম না।

**Laptop এ আছে**

- Python 3.11
- Redis Installed
- সব Library Installed

**Server এ আছে**

- Python 3.9
- Redis নেই
- Library নেই

এখন আবার সব Install করতে হবে।

একেকটা Server এ একেক রকম Environment।

এক কথায় Nightmare।

---

# Docker এর আইডিয়া

Docker বলে—

> "তোমার App এর সাথে App চালাতে যা যা দরকার, সব একসাথে Pack করে রাখো।"

মানে,

- Python
- Libraries
- Dependencies
- Configuration

সব একসাথে।

একটা Box এর মধ্যে।

```
তোমার App
+
Python
+
সব Library
+
সব Dependency
=
Container
```

এখন এই Box যেখানে নিয়ে যাবে...

সেখানেই একইভাবে চলবে।

---



# Real Life Example



## Docker ছাড়া

তুমি নিজের বাসায় রান্না করলে।

অন্য বাসায় নিয়ে গেলে...

- চুলা নেই
- মশলা নেই
- গ্যাস নেই

সব নতুন করে করতে হবে।

---



## Docker দিয়ে

রান্না করে একটা Tiffin Carrier-এ ভরে নিলে।

যেখানে নিয়ে যাবে...

একই খাবার পাবে।

---



# Docker এর ৩টা জিনিস মনে রাখো


| Docker     | বাস্তব উদাহরণ |
| ---------- | ------------- |
| Dockerfile | Recipe        |
| Image      | Frozen Food   |
| Container  | Ready Food    |


---



## Dockerfile

Recipe কাগজ।

এখানে লেখা থাকে—

- কোন Python লাগবে
- কোন Library লাগবে
- কীভাবে App চালাতে হবে

---



## Image

Recipe দিয়ে বানানো Ready Package।

এখনো চলছে না।

Just Stored.

---



## Container

Image Run করলে যেটা হয়।

এখন App আসলেই চলছে।

---



# আরেকটা উদাহরণ

```
Dockerfile
↓
বিরিয়ানির Recipe

Image
↓
Frozen বিরিয়ানি

Container
↓
Frozen বিরিয়ানি গরম করে খাচ্ছো
```

---



# Docker কীভাবে কাজ করে?

```
Dockerfile
      │
      ▼
docker build
      │
      ▼
Image
      │
      ▼
docker run
      │
      ▼
Container
      │
      ▼
App চলছে
```

---



# এবার Dockerfile দেখি

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
```

---



# প্রতিটা Line এর মানে



## FROM

```dockerfile
FROM python:3.11-slim
```

মানে,

"Python 3.11 দিয়ে শুরু করো।"

বাস্তব উদাহরণ:

একটা খালি বাসা ভাড়া নাও।

---



## WORKDIR

```dockerfile
WORKDIR /app
```

মানে,

Container এর ভেতরে `/app` Folder এ কাজ করবো।

বাস্তব উদাহরণ:

বাসার রান্নাঘরে যাও।

---



## COPY

```dockerfile
COPY requirements.txt .
```

মানে,

Laptop থেকে Container এর ভেতরে File Copy করো।

বাস্তব উদাহরণ:

নিজের জিনিস বাসায় নিয়ে যাও।

---



## RUN

```dockerfile
RUN pip install -r requirements.txt
```

মানে,

Container Build হওয়ার সময় এই Command চালাও।

বাস্তব উদাহরণ:

ঘরে ঢুকে Furniture সাজাও।

---



## CMD

```dockerfile
CMD ["python", "src/main.py"]
```

মানে,

Container Start হলে এই Command Run হবে।

বাস্তব উদাহরণ:

সব Ready, এখন রান্না শুরু করো।

---



# এবার একটা নতুন জিনিস শিখি

অনেকে এই Command দেখে ভয় পায়।

```bash
cat > Dockerfile << 'EOF'
```

আসলে এটা খুবই সহজ।

---



# cat কী?

`cat` এর দুইটা কাজ।

## কাজ ১

File এর Content দেখা।

```bash
cat main.py
```

Output

```text
print("Hello")
```

---



## কাজ ২

নতুন File বানানো।

```bash
cat > hello.txt
```

এখন Terminal এ যা লিখবে...

সব File এ Save হবে।

---



# `>` মানে কী?

`>` মানে

Screen এ না দেখিয়ে...

Output File এ পাঠাও।

```
Terminal
    │
    ▼
File
```

---



# তাহলে `<<` কী?

`<<`

মানে,

আমি এখন অনেকগুলো Line লিখবো।

একটা Special Word না আসা পর্যন্ত লিখতে থাকো।

---



# EOF কী?

EOF মানে

**End Of File**

এটা কোনো Magic Keyword না।

শুধু একটা Marker।

---

এইভাবে লিখতে পারো।

```bash
cat > hello.txt << 'EOF'

Hello
World

EOF
```

File এর ভেতরে থাকবে

```text
Hello
World
```

---



# EOF এর বদলে অন্য Word?

হ্যাঁ।

সবই কাজ করবে।

```bash
cat > hello.txt << 'END'

Hello

END
```

অথবা

```bash
cat > hello.txt << 'DONE'

Hello

DONE
```

Convention হিসেবে সবাই `EOF` ব্যবহার করে।

---



# পুরো Command টা ভেঙে বুঝি

```bash
cat > Dockerfile << 'EOF'
```

```
cat
│
File এ লিখবে

>

Screen এ না দেখিয়ে File এ পাঠাবে

Dockerfile

যে File এ লিখবে

<<

Multiple Line আসবে

EOF

EOF দেখা পর্যন্ত লিখে যাও
```

তারপর

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

সব Line Dockerfile এ Save হবে।

শেষে

```text
EOF
```

দেখলেই Save Complete।

---



# একই কাজ Nano দিয়েও করা যায়

```bash
nano Dockerfile
```

তারপর নিজের হাতে লিখবে।

---



# অথবা VS Code দিয়ে

```
Dockerfile

Open

Paste

Save
```

---



# এবার Build করি

```bash
docker build -t ai-cloud:v1 .
```

---



# ভেঙে বুঝি



## docker build

মানে

Image বানাও।

---



## -t

মানে

Tag দাও।

অর্থাৎ নাম দাও।

---



## ai-cloud:v1

```text
ai-cloud
```

Image এর নাম।

```text
v1
```

Version।

পরে

```bash
docker build -t ai-cloud:v2 .
```

করতে পারবে।

---



# শেষে Dot (.)

অনেকে এটাতেই Confused হয়।

```bash
docker build -t ai-cloud:v1 .
```

এই

```text
.
```

মানে

Current Folder।

অর্থাৎ

"এই Folder এ Dockerfile খুঁজে বের করো।"

---

যদি অন্য Folder এ থাকে

```bash
docker build -t ai-cloud:v1 /home/imran/project
```

তাহলে ওই Folder ব্যবহার করবে।

---



# পুরো Flow



## Step 1

Dockerfile বানাও

```bash
cat > Dockerfile << 'EOF'

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]

EOF
```

---



## Step 2

ঠিকমতো হয়েছে কিনা দেখো।

```bash
cat Dockerfile
```

---



## Step 3

Image Build করো।

```bash
docker build -t ai-cloud:v1 .
```

---



## Step 4

সব Image দেখো।

```bash
docker images
```

Output

```text
REPOSITORY     TAG

ai-cloud       v1
```

---



## Step 5

Container Run করো।

```bash
docker run ai-cloud:v1
```

Output

```text
AI Cloud চালু হলো!

Python Ready

Docker Container এর ভেতর থেকে বলছি!
```

---



# Summary


| Command         | কাজ                    |
| --------------- | ---------------------- |
| `cat > file`    | File এ লেখা            |
| `cat file`      | File দেখা              |
| `<< EOF`        | Multi-line Input শুরু  |
| `EOF`           | Multi-line Input শেষ   |
| `docker build`  | Image বানানো           |
| `docker run`    | Container চালানো       |
| `docker ps`     | Running Container দেখা |
| `docker stop`   | Container বন্ধ         |
| `docker images` | সব Image দেখা          |


---



# মনে রাখো

Docker শিখতে গেলে শুধু এই তিনটা জিনিস মাথায় রাখো।

```text
Dockerfile
↓
Recipe

Image
↓
Frozen Food

Container
↓
Ready Food
```

এগুলো বুঝে গেলে Docker-এর ৭০% Concept Clear।