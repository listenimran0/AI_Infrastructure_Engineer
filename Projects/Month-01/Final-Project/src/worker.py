import json
import asyncio
from src.redis_client import r


async def simulate_llm(
    message: str,
    history: str,
    model_name: str
):
    delays = {"llama-3": 1.5, "gpt-4": 2, "claude": 1}
    await asyncio.sleep(delays.get(model_name, 2))
    
    if "hello" in message.lower():
        return f"Hello! আমি {model_name}। কীভাবে help করতে পারি?"
    elif "gpu" in message.lower():
        return f"GPU হলো Graphics Processing Unit। AI training এ অনেক কাজে লাগে!"
    elif "ai" in message.lower():
        return f"AI মানে Artificial Intelligence। আমি নিজেও একটা AI!"
    else:
        return f"{model_name} বলছে: '{message}' — interesting প্রশ্ন!"
    
    
    
async def process_chat_job(job_id: str):
    
    print("Chat job started...")
    
    raw = r.get(f"job:{job_id}")
    
    if not raw:
        print("Job is not available with given job_id")
        return
    
    data = json.loads(raw)
    
    data["status"] = "processing"
    
    r.set(f"job:{job_id}", json.dumps(data))
    
    session_id = data["session_id"]
    history_raw = r.get(f"session:{session_id}")
    history = json.loads(history_raw) if history_raw else []
    
    print(f"🤖 {data['model_name']} thinking...")
    
    response = await simulate_llm(
        message= data["message"],
        history= history,
        model_name= data["model_name"]
    )
    
    history.append({"role": "user", "content": data["message"]})
    history.append({"role": "assistant", "content": response})
    
    r.set(f"session:{session_id}", json.dumps(history))
    
    data["status"] = "Done"
    data["result"] = response
    data["history"] = history
    
    r.set(f"job:{job_id}", json.dumps(data))
    
    print(f"✅ Chat job done: {job_id}")
    print(f"💬 Response: {response}")
    

    

    