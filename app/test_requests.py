# test_requests.py
import asyncio
import time
import aiohttp
import numpy as np
import pandas as pd

submission_file_path = "/home/mikhail/Documents/Хакатоны/X5_ner_MiLky_way/data/submission.csv"
df = pd.read_csv(submission_file_path, sep=";")
TEST_TEXTS = df["sample"].tolist()

async def time_single_request(session, text, idx):
    payload = {"input": text}
    
    # ⏱️ Start timer JUST before THIS request's HTTP call
    start = time.perf_counter()

    # HOST = "158.160.184.207"
    HOST = "127.0.0.1"
    PORT = 8000
    
    try:
        async with session.post(f"http://{HOST}:{PORT}/api/predict", json=payload) as resp:
            result = await resp.json()
            latency = time.perf_counter() - start  # ⏱️ Stop after response received
            return idx, text, latency, result, None
    except Exception as e:
        latency = time.perf_counter() - start
        return idx, text, latency, None, str(e)

async def main():
    async with aiohttp.ClientSession() as session:
        # Launch all requests CONCURRENTLY
        tasks = [time_single_request(session, text, i) for i, text in enumerate(TEST_TEXTS)]
        results = await asyncio.gather(*tasks)
    
    # Sort by original order
    results.sort(key=lambda x: x[0])
    
    print(f"{'#':<4} {'Text':<40} | {'Latency (s)':<12} | Entities")
    print("-" * 100)
    
    latencies = []
    for idx, text, latency, resp, err in results:
        latencies.append(latency)
        if err:
            print(f"{idx:<4} {text:<40} | {latency:<12.4f} | ❌ {err}")
        else:
            entities = resp
            # print(entities)
            if entities and isinstance(entities[0], (list, tuple)):
                ents = ", ".join(f"({e[0]}, {e[1]}, {e[2]})" for e in entities[:3])  # Show first 3
                if len(entities) > 3:
                    ents += f" ... (+{len(entities)-3} more)"
            else:
                ents = str(entities)
            print(f"{idx:<4} {text:<40} | {latency:<12.4f} | {ents}")
    
    latencies_arr = np.array(latencies)
    print(f"\n📊 Latency Statistics:")
    print(f"   Mean:   {latencies_arr.mean():.4f} s")
    print(f"   Median: {np.median(latencies_arr):.4f} s")
    print(f"   P95:    {np.percentile(latencies_arr, 95):.4f} s")
    print(f"   Min:    {latencies_arr.min():.4f} s")
    print(f"   Max:    {latencies_arr.max():.4f} s")

if __name__ == "__main__":
    asyncio.run(main())