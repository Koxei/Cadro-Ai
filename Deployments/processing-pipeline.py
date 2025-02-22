import asyncio
import threading
import random
import time
from queue import Queue

# Simulated blockchain transaction event generator
async def blockchain_event_stream(event_queue: asyncio.Queue):
    while True:
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulating real-time event arrival
        transaction = {"tx_id": random.randint(1000, 9999), "amount": random.uniform(0.1, 5)}
        print(f"New transaction received: {transaction}")
        await event_queue.put(transaction)

# Worker function to process transaction batches
def transaction_worker(worker_id, input_queue: Queue, batch_size: int):
    while True:
        batch = []
        for _ in range(batch_size):
            transaction = input_queue.get()
            if transaction is None:
                return  # Graceful shutdown
            batch.append(transaction)
        print(f"Worker {worker_id} processing batch: {batch}")
        time.sleep(random.uniform(0.5, 1.5))  # Simulated processing time

# Async event dispatcher to distribute events to workers
async def event_dispatcher(event_queue: asyncio.Queue, processing_queue: Queue, num_workers: int, batch_size: int):
    threads = []
    for i in range(num_workers):
        thread = threading.Thread(target=transaction_worker, args=(i, processing_queue, batch_size), daemon=True)
        thread.start()
        threads.append(thread)
    
    while True:
        transaction = await event_queue.get()
        processing_queue.put(transaction)

# Main event loop
async def main():
    event_queue = asyncio.Queue()
    processing_queue = Queue()
    num_workers = 4  # Number of parallel workers
    batch_size = 5  # Transactions per batch
    
    asyncio.create_task(blockchain_event_stream(event_queue))
    await event_dispatcher(event_queue, processing_queue, num_workers, batch_size)

if __name__ == "__main__":
    asyncio.run(main())
