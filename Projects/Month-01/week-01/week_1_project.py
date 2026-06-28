import asyncio
import time
import functools
from pydantic import BaseModel, validator
from contextlib import asynccontextmanager
from typing import Optional, List

# ── 1. Pydantic Model ──────────────────────────────
class AIJob(BaseModel):
    job_id: str
    prompt: str
    model_name: str
    priority: int = 1
    max_tokens: int = 1000

    @validator("priority")
    def priority_valid(cls, v):
        if not 1 <= v <= 5:
            raise ValueError("Priority ১ থেকে ৫ এর মধ্যে হতে হবে!")
        return v

# ── 2. Decorator ───────────────────────────────────
def log_job(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"📝 {func.__name__} শুরু হলো")
        result = await func(*args, **kwargs)
        print(f"✅ {func.__name__} শেষ হলো")
        return result
    return wrapper

# ── 3. Context Manager ─────────────────────────────
@asynccontextmanager
async def gpu_session(gpu_id: int):
    print(f"🔌 GPU {gpu_id} allocate করলাম")
    try:
        yield gpu_id
    finally:
        print(f"🧹 GPU {gpu_id} free করলাম")

# ── 4. Generator ───────────────────────────────────
async def stream_result(job: AIJob):
    words = f"Result for {job.prompt} from {job.model_name}".split()
    for word in words:
        await asyncio.sleep(0.2)
        yield word

# ── 5. Main Logic ──────────────────────────────────
@log_job
async def process_job(job: AIJob, gpu_id: int):
    async with gpu_session(gpu_id) as gpu:
        print(f"⚙️  Processing job {job.job_id} on GPU {gpu}")
        print(f"📤 Result: ", end="", flush=True)
        async for word in stream_result(job):
            print(word, end=" ", flush=True)
        print()

async def main():
    # Job গুলো বানাও
    jobs = [
        AIJob(job_id="j001", prompt="Hello AI", model_name="Llama-3", priority=3),
        AIJob(job_id="j002", prompt="What is GPU", model_name="GPT-4", priority=5),
        AIJob(job_id="j003", prompt="Explain CUDA", model_name="Claude", priority=1),
    ]

    # Priority অনুযায়ী sort করো
    jobs.sort(key=lambda j: j.priority, reverse=True)

    print("🚀 AI Job Queue শুরু হলো\n")

    # একটা একটা করে process করো
    for i, job in enumerate(jobs):
        await process_job(job, gpu_id=i % 2)  # GPU 0 আর 1 তে ভাগ করো
        print()

    print("🎉 সব job শেষ!")

asyncio.run(main())