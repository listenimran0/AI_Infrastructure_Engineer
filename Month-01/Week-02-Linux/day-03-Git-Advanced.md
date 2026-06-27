# Month 1 - Week 2 - Day 3

# Git Advanced: Branching, Merge & Git Workflow

গত Lesson-এ আমরা Git-এর Basic Concepts শিখেছি। আজকে আমরা শিখবো **Git Branching, Merge, Merge Conflict এবং Real Project Workflow**।

Production Project-এ একজন Developer কখনো সরাসরি `main` Branch-এ কাজ করে না। নতুন Feature, Bug Fix বা Experiment—সবকিছু আলাদা Branch-এ করা হয়।

---

# আজকের Lesson-এ যা শিখবো

- Branch কী এবং কেন দরকার
- Branch Workflow
- Merge
- Merge Conflict
- GitHub Push
- Real Project Git Workflow
- Advanced Git Commands
- Practice

---

# Branch কেন দরকার?

ধরো `main` Branch-এ তোমার Production Code আছে।

এখন তুমি নতুন GPU Scheduler Feature বানাতে চাও।

যদি সরাসরি `main` Branch-এ কাজ করো, তাহলে ভুল হলে পুরো Project নষ্ট হতে পারে।

তাই নতুন Feature সবসময় আলাদা Branch-এ তৈরি করা হয়।

```text
main ───────────────────────────────► (Production)

        │

        └──────── feature/gpu-scheduler

                    │

                এখানে কাজ করো

                    │

                Merge করে Main-এ আনো
```

---

# Branch তৈরি করো

বর্তমান Branch দেখো।

```bash
git branch
```

Output

```text
* main
```

`*` চিহ্নটি বোঝায় বর্তমানে কোন Branch-এ আছো।

---

নতুন Branch তৈরি করো।

```bash
git checkout -b feature/gpu-scheduler
```

এটি একই সাথে—

- নতুন Branch তৈরি করবে
- সেই Branch-এ Switch করবে

---

আবার Branch দেখো।

```bash
git branch
```

Output

```text
* feature/gpu-scheduler

  main
```

---

# Branch-এ কাজ করো

নতুন File তৈরি করো।

```bash
echo "# GPU Scheduler" > src/scheduler.py

echo "print('Scheduler running')" >> src/scheduler.py
```

Commit করো।

```bash
git add .

git commit -m "Add GPU scheduler"
```

---

# Main Branch-এ ফিরে যাও

```bash
git checkout main
```

এখন File List দেখো।

```bash
ls src
```

Output

```text
main.py
```

খেয়াল করো—

`scheduler.py` নেই।

কারণ এটি Feature Branch-এ আছে।

---

# Merge কী?

Feature-এর কাজ শেষ হলে সেটিকে Main Branch-এ নিয়ে আসাকে Merge বলে।

Main Branch-এ থাকো।

```bash
git checkout main
```

তারপর—

```bash
git merge feature/gpu-scheduler
```

এখন আবার দেখো—

```bash
ls src
```

Output

```text
main.py

scheduler.py
```

Feature Branch-এর Code Main Branch-এ চলে এসেছে।

---

# Merge Conflict কী?

Merge Conflict হয় যখন—

দুটি Branch একই File-এর একই জায়গা পরিবর্তন করে।

Git তখন বুঝতে পারে না কোন Code রাখবে।

তখন Manual Decision নিতে হয়।

---

# Conflict তৈরি করো

Main Branch-এ থাকো।

```bash
git checkout main
```

`main.py` Update করো।

```python
def process():
    return "main version"
```

Commit করো।

```bash
git add .

git commit -m "Main: add process function"
```

---

নতুন Branch তৈরি করো।

```bash
git checkout -b feature/update
```

একই Function পরিবর্তন করো।

```python
def process():
    return "feature version"
```

Commit করো।

```bash
git add .

git commit -m "Feature: update process function"
```

---

আবার Main Branch-এ ফিরে যাও।

```bash
git checkout main
```

এবার Merge করো।

```bash
git merge feature/update
```

Output

```text
CONFLICT (content): Merge conflict in src/main.py

Automatic merge failed.
```

---

# Conflict File দেখতে কেমন?

```python
<<<<<<< HEAD

def process():
    return "main version"

=======

def process():
    return "feature version"

>>>>>>> feature/update
```

এখানে—

```text
<<<<<<< HEAD
```

বর্তমান Branch-এর Code

```text
=======
```

দুই Version-এর Separator

```text
>>>>>>> feature/update
```

Feature Branch-এর Code

---

# Conflict কীভাবে Resolve করবো?

Git তোমার জন্য Decision নেবে না।

তোমাকেই File Edit করতে হবে।

Option 1

শুধু Main Version রাখো।

```python
def process():
    return "main version"
```

---

Option 2

শুধু Feature Version রাখো।

```python
def process():
    return "feature version"
```

---

Option 3 (সবচেয়ে Common)

দুই Version মিলিয়ে নতুন Code লিখো।

```python
def process():

    main_result = "main version"

    feature_result = "feature version"

    return f"{main_result} | {feature_result}"
```

---

তারপর—

```bash
git add src/main.py

git commit -m "Resolve merge conflict"
```

এতেই Conflict শেষ।

---

# GitHub-এ Push

Remote যোগ করো।

```bash
git remote add origin https://github.com/username/ai-cloud.git
```

তারপর—

```bash
git push -u origin main
```

---

# Real Project Workflow

Production Project-এ সাধারণত Workflow এমন হয়।

```bash
git pull origin main

git checkout -b feature/redis-queue

# Code লিখো

git add .

git commit -m "Add Redis job queue"

git commit -m "Add priority sorting"

git commit -m "Add retry logic"

git checkout main

git merge feature/redis-queue

git push origin main
```

---

# Advanced Git Commands

## ১. একটি File-এর Commit History দেখো

```bash
git log --oneline src/main.py
```

এটি শুধু `src/main.py`-এর History দেখায়।

Output

```text
91bc212 Resolve merge conflict

8ac71fd Update process function

54de111 Initial commit
```

Bug Tracking-এর সময় এটি খুবই উপকারী।

---

## ২. Commit করার আগে কী পরিবর্তন হয়েছে দেখো

```bash
git diff
```

Output

```diff
-print("Old Code")

+print("New Code")
```

এখানে—

`-` মানে Remove হয়েছে।

`+` মানে নতুন যোগ হয়েছে।

Staging-এর পরে দেখতে চাইলে—

```bash
git diff --staged
```

---

## ৩. Last Commit Undo করো (Code রেখে)

```bash
git reset --soft HEAD~1
```

এতে—

- শেষ Commit Delete হবে।
- কিন্তু Code থাকবে।
- আবার নতুন Commit করা যাবে।

এটি সবচেয়ে বেশি ব্যবহার হয় ভুল Commit Message ঠিক করার সময়।

---

## ৪. একটি File আগের Version-এ ফিরিয়ে আনো

```bash
git checkout HEAD~1 src/main.py
```

ধরো—

`main.py` নষ্ট করে ফেলেছো।

এই Command File-টিকে ১ Commit আগের অবস্থায় ফিরিয়ে আনবে।

```text
HEAD~1

↓

এক Commit আগে

HEAD~2

↓

দুই Commit আগে
```

---

## ৫. Git Stash

অনেক সময় Feature শেষ হয়নি।

Commit করতে চাও না।

কিন্তু জরুরি Bug Fix করতে হবে।

তখন—

```bash
git stash
```

তোমার অসম্পূর্ণ কাজ Temporary Save হয়ে যাবে।

Working Directory আবার Clean হয়ে যাবে।

---

Bug Fix শেষ হলে—

```bash
git stash pop
```

Stash করা সব পরিবর্তন আবার ফিরে আসবে।

---

# Practice

নতুন Branch তৈরি করো।

```bash
git checkout -b feature/streaming
```

Streaming Module তৈরি করো।

```bash
echo "# Streaming module" > src/streaming.py

echo "print('Streaming started')" >> src/streaming.py
```

Commit করো।

```bash
git add .

git commit -m "Add streaming module"
```

Main Branch-এ ফিরে Merge করো।

```bash
git checkout main

git merge feature/streaming
```

History দেখো।

```bash
git log --oneline
```

---

# আজকের Task

নিজে নিচের কাজগুলো করো।

1. `feature/streaming` নামে নতুন Branch তৈরি করো।
2. `streaming.py` File তৈরি করো।
3. নতুন Commit করো।
4. Main Branch-এ Merge করো।
5. `git log --oneline` দেখো।
6. ইচ্ছা করে একটি Merge Conflict তৈরি করে Manual Resolve করার চেষ্টা করো।
7. `git diff` দিয়ে পরিবর্তন দেখো।
8. `git stash` এবং `git stash pop` Practice করো।

---

# আজকের Lesson থেকে যা শিখলে

- Git Branch
- Branch Workflow
- Merge
- Merge Conflict
- Conflict Resolution
- GitHub Push
- `git diff`
- `git log`
- `git reset --soft`
- `git checkout HEAD~1`
- `git stash`
- `git stash pop`

---

# Next Lesson

পরবর্তী Lesson-এ আমরা **Docker Basics** শুরু করবো। সেখানে Container, Image, Dockerfile এবং Docker Workflow নিয়ে হাতে-কলমে কাজ করবো।