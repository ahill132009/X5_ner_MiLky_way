# test_requests.py
import asyncio
import time
import aiohttp

TEST_TEXTS = [
    "сыр натура сливочный",
    "молоко ультрапастеризованное 3.2%",
    "кефир био 1%",
    "йогурт греческий с клубникой",
    "творог 5% жирности",
    "сметана деревенская 15%",
    "масло сливочное крестьянское",
    "ряженка классическая 4%",
]

async def time_single_request(session, text, idx):
    payload = {"input": text}
    start = time.perf_counter()  # ⏱️ Start timer JUST before sending
    try:
        async with session.post("http://127.0.0.1:8000/api/predict", json=payload) as resp:
            result = await resp.json()
            latency = time.perf_counter() - start  # ⏱️ Stop timer AFTER response
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

    print(f"{'#':<2} {'Text':<40} | {'Latency (s)':<12} | Entities")
    print("-" * 75)
    for idx, text, latency, resp, err in results:
        if err:
            print(f"{idx:<2} {text:<40} | {latency:<12.4f} | ❌ {err}")
        else:
            entities = resp
            if entities and isinstance(entities[0], (list, tuple)):
                ents = ", ".join(f"({e[0]}, {e[1]}, {e[2]})" for e in entities)
            else:
                ents = str(entities)
            print(f"{idx:<2} {text:<40} | {latency:<12.4f} | {ents}")

if __name__ == "__main__":
    asyncio.run(main())