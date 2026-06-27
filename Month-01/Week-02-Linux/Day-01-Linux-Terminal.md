# Month 1 - Week 2 - Day 1

# Linux Essentials: Linux Basics & Terminal

Week 1-এ আমরা Advanced Python শেষ করেছি। এবার শুরু হচ্ছে **Linux**।

AI Infrastructure, Cloud Computing, Docker, Kubernetes, GPU Server—সবকিছুই Linux-এর উপর চলে। তাই একজন AI Infrastructure Engineer-এর Linux Terminal-এ দক্ষ হওয়া বাধ্যতামূলক।

---

# আজকের Lesson-এ যা শিখবো

- কেন Linux শিখতে হবে
- Linux File System
- Basic Terminal Commands
- File & Folder Management
- File Editing
- Linux Permissions
- Process Management
- Pipe (`|`)
- Practice Project

---

# কেন Linux শিখতে হবে?

তুমি ভবিষ্যতে যেসব জিনিস নিয়ে কাজ করবে—

- AI Compute Cloud
- GPU Server
- Docker Container
- Kubernetes Cluster
- Cloud VM (AWS, GCP, Azure)

এসব প্রায় সবই Linux-এ চলে।

তাই Terminal ব্যবহার করতে স্বাচ্ছন্দ্য হওয়া খুবই গুরুত্বপূর্ণ।

---

# Terminal খুলে নাও

Mac ব্যবহার করলে—

```bash
Terminal
```

Windows ব্যবহার করলে—

```text
WSL2 (Ubuntu)
```

Linux ব্যবহার করলে—

```bash
Terminal
```

---

# Linux File System

Windows-এ যেমন—

```text
C:\Users\Imran\Documents
```

Linux-এ সবকিছুর শুরু হয় Root (`/`) থেকে।

```text
/

├── home/
│   └── imran/
│       ├── projects/
│       └── documents/
│
├── etc/
│
├── var/
│
└── usr/
```

Directory-এর কাজ—

| Folder | কাজ |
|---------|------|
| `/` | Root Directory |
| `/home` | User Files |
| `/etc` | System Configuration |
| `/var` | Logs & Temporary Files |
| `/usr` | Installed Programs |

---

# বর্তমান Location দেখো

```bash
pwd
```

Output

```text
/home/imran
```

`pwd` এর অর্থ **Print Working Directory**।

---

# Folder-এর ভিতরে কী আছে দেখো

```bash
ls
```

Hidden File এবং বিস্তারিত তথ্য দেখতে—

```bash
ls -la
```

Output

```text
drwxr-xr-x projects
-rw-r--r-- README.md
```

---

# Folder Change করো

```bash
cd projects
```

এক ধাপ পিছনে যেতে—

```bash
cd ..
```

Home Directory-তে যেতে—

```bash
cd ~
```

Root Directory-তে যেতে—

```bash
cd /
```

---

# নতুন Folder তৈরি করো

```bash
mkdir ai-project
```

Nested Folder একসাথে তৈরি করতে—

```bash
mkdir -p src/api/routes
```

---

# নতুন File তৈরি করো

```bash
touch main.py
```

Hidden File

```bash
touch .env
```

---

# File দেখো

পুরো File দেখো—

```bash
cat README.md
```

প্রথম ৫ লাইন—

```bash
head -n 5 README.md
```

শেষ ৫ লাইন—

```bash
tail -n 5 README.md
```

Live Log Monitor করতে—

```bash
tail -f logs.txt
```

Production Server-এ এটি খুবই গুরুত্বপূর্ণ Command।

---

# Copy, Move & Delete

Copy

```bash
cp config.py config_backup.py
```

Move অথবা Rename

```bash
mv config.py src/config.py
```

Delete File

```bash
rm config.py
```

Delete Folder

```bash
rm -rf folder_name
```

> **সতর্কতা:** `rm -rf` ব্যবহার করার সময় খুব সাবধান। এটি Recover করা কঠিন।

---

# Terminal থেকেই File-এ লিখো

নতুন File তৈরি করে লিখো—

```bash
echo "Hello World" > file.txt
```

আরও Line যোগ করতে—

```bash
echo "Second Line" >> file.txt
```

---

# nano Editor

```bash
nano config.py
```

Useful Shortcut

```text
Ctrl + O  → Save

Ctrl + X  → Exit
```

---

# Linux Permission

Linux-এ প্রতিটি File ও Folder-এর Permission থাকে।

দেখতে—

```bash
ls -la
```

Output

```text
-rwxr-xr-- main.py
```

এটি ভাগ করলে—

```text
-   rwx   r-x   r--

│    │     │     │
│    │     │     └── Others
│    │     └──────── Group
│    └────────────── Owner
└────────────────── File Type
```

---

## File Type

```text
- = File

d = Directory
```

---

## Permission

```text
r = Read

w = Write

x = Execute
```

---

## Owner, Group, Others

ধরো—

```text
-rwxr-xr--
```

এর মানে—

Owner

```text
rwx
```

- Read
- Write
- Execute

Group

```text
r-x
```

- Read
- Execute

Others

```text
r--
```

- শুধুমাত্র Read

---

# chmod কী?

Permission পরিবর্তন করতে ব্যবহার করা হয়।

```bash
chmod +x script.py
```

এতে File Execute করা যাবে।

---

# Numeric Permission

Linux-এ Permission Number দিয়েও লেখা যায়।

| Permission | Number |
|------------|--------|
| r | 4 |
| w | 2 |
| x | 1 |

---

উদাহরণ

```text
rwx = 7

r-x = 5

r-- = 4
```

তাই—

```bash
chmod 755 script.py
```

মানে—

```text
Owner  → rwx

Group  → r-x

Others → r-x
```

---

## Common Permissions

| Permission | ব্যবহার |
|------------|----------|
| 755 | Script / Program |
| 644 | সাধারণ File |
| 600 | Secret File (.env) |
| 400 | Read Only |
| 777 | কখনো ব্যবহার না করাই ভালো |

---

## AI Project-এ Real Example

Python Script

```bash
chmod 755 main.py
```

Environment Variable

```bash
chmod 600 .env
```

Config File

```bash
chmod 644 settings.py
```

---

# Process কী?

যখন তুমি একটি Program চালাও, Linux সেটিকে একটি **Process** হিসেবে Run করে।

প্রতিটি Process-এর একটি আলাদা **PID (Process ID)** থাকে।

সব Process দেখতে—

```bash
ps aux
```

Output

```text
USER     PID   COMMAND

imran   1234   python main.py

root     999   nginx
```

---

# Process Search

সব Process না দেখে শুধু Python Process দেখতে—

```bash
ps aux | grep python
```

এখানে—

`ps aux`

সব Process-এর List দেয়।

তারপর Pipe (`|`) ব্যবহার করে সেই Output `grep`-এ পাঠানো হয়।

`grep python`

শুধু যেসব Line-এ `python` আছে সেগুলো দেখায়।

---

# Pipe (`|`) কী?

Pipe-এর কাজ হলো—

একটি Command-এর Output অন্য Command-এর Input হিসেবে পাঠানো।

Syntax

```bash
command1 | command2
```

---

## Example 1

```bash
ps aux | grep python
```

Step-by-Step

```text
ps aux
        │
        ▼
সব Process-এর List
        │
        ▼
Pipe (|)
        │
        ▼
grep python
        │
        ▼
শুধু Python Process দেখাও
```

---

## Example 2

```bash
cat logs.txt | grep ERROR
```

এখানে—

`cat logs.txt`

পুরো Log File পড়ে।

তারপর—

```bash
grep ERROR
```

শুধু যেসব Line-এ `ERROR` আছে সেগুলো দেখায়।

উদাহরণ

```text
[ERROR] GPU Out Of Memory

[ERROR] Model Timeout
```

---

## আরও একটি Example

ERROR কয়টি আছে Count করো—

```bash
cat logs.txt | grep ERROR | wc -l
```

এখানে—

```text
cat
 ↓

grep ERROR
 ↓

wc -l
```

অর্থাৎ—

Log পড়ো → ERROR Filter করো → মোট কত Line আছে Count করো।

---

# Process বন্ধ করা

Normal ভাবে বন্ধ করতে—

```bash
kill 1234
```

Force করে বন্ধ করতে—

```bash
kill -9 1234
```

`kill`

Process-কে বলে সুন্দরভাবে বন্ধ হতে।

`kill -9`

Linux সরাসরি Process বন্ধ করে দেয়।

---

# Practice Project

আজকে Terminal ব্যবহার করে নিচের Project Structure তৈরি করো।

```bash
mkdir -p ~/projects/ai-cloud

cd ~/projects/ai-cloud

mkdir -p src logs config

touch src/main.py

touch src/queue.py

touch config/settings.py

touch .env

touch README.md
```

---

README.md-তে লিখো—

```bash
echo "# AI Cloud Project" > README.md

echo "Decentralized AI Inference Cloud" >> README.md
```

---

সবশেষে Check করো—

```bash
ls -la

ls -la src

cat README.md
```

---

# আজকের Task

Terminal-এ নিচের কাজগুলো নিজে করো।

1. `ai-cloud` নামে Project Folder তৈরি করো।
2. Project Structure তৈরি করো।
3. `README.md`-তে Content যোগ করো।
4. `ls -la` দিয়ে Structure দেখো।
5. `chmod 600 .env` Run করে Permission পরিবর্তন করো।
6. `ps aux | grep python` Run করে Python Process দেখো।
7. একটি `logs.txt` File তৈরি করে `grep ERROR` ব্যবহার করে শুধু Error Line বের করো।

---

# আজকের Lesson থেকে যা শিখলে

- Linux Terminal
- File System
- `pwd`
- `ls`
- `cd`
- `mkdir`
- `touch`
- `cat`
- `head`
- `tail`
- `echo`
- `nano`
- Linux Permission
- `chmod`
- Process
- `ps`
- `kill`
- Pipe (`|`)
- `grep`

---

# Next Lesson

পরবর্তী Lesson-এ আমরা **Git & GitHub Basics** শিখবো।

সেখানে Version Control, Repository, Commit, Branch এবং GitHub Workflow নিয়ে কাজ করবো।