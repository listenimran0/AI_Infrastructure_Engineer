# Month 1 - Week 2 - Day 2

# Git Basics: Version Control Fundamentals

গত Lesson-এ আমরা Linux Terminal এবং Basic Commands শিখেছি। আজকে আমরা শিখবো **Git**।

Git হলো পৃথিবীর সবচেয়ে জনপ্রিয় **Version Control System (VCS)**। একজন Software Engineer, AI Engineer বা AI Infrastructure Engineer হিসেবে Git জানা বাধ্যতামূলক।

---

# আজকের Lesson-এ যা শিখবো

- Git কী?
- কেন Git শিখতে হবে
- Git Workflow
- Working Directory, Staging Area ও Repository
- Basic Git Commands
- `.gitignore`
- Git Branch
- GitHub-এ Push
- Practice

---

# Git কেন শিখতে হবে?

ধরো আজকে তুমি একটি Project-এ একা কাজ করছো।

কিন্তু ৬ মাস পরে—

- তোমার Team-এ আরও ৫ জন Developer যোগ দিলো।
- অথবা ভুল করে Project-এর গুরুত্বপূর্ণ Code Delete করে ফেললে।

তখন কী করবে?

Git তোমার Code-এর **Time Machine** হিসেবে কাজ করে।

```text
আজ Code লিখলে
        │
        ▼
Commit করলে
        │
        ▼
Git History-তে Save হয়ে গেল
        │
        ▼
যেকোনো সময় আগের Version-এ ফিরে যেতে পারবে
```

---

# Git-এর ৩টি ধাপ

Git-এ Code সরাসরি Save হয় না।

প্রথমে তিনটি Stage অতিক্রম করে।

```text
Working Directory
        │
    git add
        ▼
Staging Area
        │
 git commit
        ▼
Repository
```

---

## Working Directory

এখানে তুমি Code লিখছো।

যেকোনো নতুন File বা পরিবর্তন প্রথমে এখানে থাকে।

---

## Staging Area

যে File-গুলো Commit করতে চাও, সেগুলো এখানে রাখো।

```bash
git add main.py
```

---

## Repository

Commit করার পরে File Permanent History-তে Save হয়ে যায়।

```bash
git commit -m "Add AI job queue"
```

---

# Real Life Example

```text
Working Directory
↓

খাতায় লিখছো

↓

Staging Area

জেরক্স করার জন্য প্রস্তুত

↓

Repository

জেরক্স হয়ে স্থায়ীভাবে সংরক্ষণ হয়েছে
```

---

# Git প্রথমবার Setup

নিজের Name এবং Email Configure করো।

```bash
git config --global user.name "Imran"

git config --global user.email "imran@email.com"
```

একবার করলেই যথেষ্ট।

---

# নতুন Project-এ Git শুরু করো

Project Folder-এ যাও।

```bash
cd ~/projects/ai-cloud
```

তারপর—

```bash
git init
```

এখন Git এই Folder Track করা শুরু করবে।

---

# Project Status দেখো

```bash
git status
```

এই Command দেখায়—

- কোন File নতুন
- কোন File Modify হয়েছে
- কোন File Commit হয়নি

এটি Git-এর সবচেয়ে বেশি ব্যবহৃত Command।

---

# File Add করো

একটি File Add

```bash
git add main.py
```

একটি Folder Add

```bash
git add src/
```

সব File Add

```bash
git add .
```

---

# Commit করো

```bash
git commit -m "Add AI job queue"
```

`-m` এর পরে Commit Message লিখতে হয়।

ভালো Commit Message ভবিষ্যতে History বুঝতে অনেক সাহায্য করে।

---

# Commit History দেখো

সব Commit

```bash
git log
```

সংক্ষেপে

```bash
git log --oneline
```

উদাহরণ

```text
2d4ac31 Initial commit

7acb928 Add GPU Scheduler

af91d92 Update README
```

---

# `.gitignore`

সব File GitHub-এ Push করা উচিত নয়।

এর জন্য `.gitignore` ব্যবহার করা হয়।

```text
.env

__pycache__/

*.pyc

node_modules/

logs/
```

---

# কেন `.env` Ignore করবো?

`.env` File-এ সাধারণত থাকে—

- API Key
- Database Password
- Secret Token

যদি ভুল করে GitHub-এ Push করে দাও—

তাহলে অন্য কেউ Secret Key ব্যবহার করতে পারবে।

তাই Production Project-এ `.env` সবসময় `.gitignore`-এ রাখা উচিত।

---

# Git Branch

Branch হলো একই Project-এর আলাদা Working Area।

```text
main

├── feature/gpu-scheduler

├── feature/streaming

└── feature/authentication
```

`main`

Production Ready Code থাকে।

নতুন Feature সবসময় নতুন Branch-এ তৈরি করা হয়।

---

# বর্তমান Branch দেখো

```bash
git branch
```

---

# নতুন Branch তৈরি করো

```bash
git checkout -b feature/gpu
```

এটি—

- নতুন Branch তৈরি করবে
- সেই Branch-এ Switch করবে

---

# Main Branch-এ ফিরে যাও

```bash
git checkout main
```

---

# Branch Merge

Feature শেষ হলে—

```bash
git merge feature/gpu
```

Feature Branch-এর Code Main Branch-এ Merge হয়ে যাবে।

---

# GitHub-এ Push

প্রথমে Remote Repository যোগ করো।

```bash
git remote add origin https://github.com/username/ai-cloud.git
```

তারপর Push করো।

```bash
git push -u origin main
```

এরপর থেকে শুধু—

```bash
git push
```

লিখলেই হবে।

---

# Practice

Project Folder-এ যাও।

```bash
cd ~/projects/ai-cloud
```

Git Initialize করো।

```bash
git init
```

---

`.gitignore` তৈরি করো।

```bash
echo ".env" > .gitignore

echo "__pycache__/" >> .gitignore

echo "*.pyc" >> .gitignore

echo "logs/" >> .gitignore
```

---

README.md Update করো।

```bash
echo "# AI Cloud" > README.md

echo "Decentralized AI Inference Cloud" >> README.md
```

---

`src/main.py` তৈরি করো।

```bash
echo "# Main entry point" > src/main.py

echo "print('AI Cloud starting...')" >> src/main.py
```

---

Git Status দেখো।

```bash
git status
```

সব File Add করো।

```bash
git add .
```

প্রথম Commit করো।

```bash
git commit -m "Initial commit: AI Cloud project structure"
```

History দেখো।

```bash
git log --oneline
```

---

# আজকের Task

নিজে Terminal-এ নিচের কাজগুলো করো।

1. Git Initialize করো।
2. `.gitignore` তৈরি করো।
3. `README.md` Update করো।
4. `src/main.py` তৈরি করো।
5. `git status` Run করো।
6. `git add .` Run করো।
7. প্রথম Commit করো।
8. `git log --oneline` দিয়ে History দেখো।

---

# আজকের Lesson থেকে যা শিখলে

- Git
- Version Control
- Working Directory
- Staging Area
- Repository
- `git init`
- `git status`
- `git add`
- `git commit`
- `git log`
- `.gitignore`
- Git Branch
- `git checkout`
- `git merge`
- `git push`

---

# Next Lesson

পরবর্তী Lesson-এ আমরা **Git Branching & GitHub Collaboration** শিখবো। সেখানে Branch Workflow, Merge Conflict, Pull Request এবং Team Collaboration নিয়ে কাজ করবো।