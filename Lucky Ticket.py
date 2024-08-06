import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Value

def count_lucky_tickets_range(start, end, result=False):
    if result is not False:

        def get_sum(num):
            return sum(int(digit) for digit in str(num))

        count = 0
        for ticket in range(start, end + 1):
            if get_sum(ticket // 1000) == get_sum(ticket % 1000):
                count += 1
        result.value = count
    else:
        def get_sum(num):
            return sum(int(digit) for digit in str(num))

        count = 0
        for ticket in range(start, end + 1):
            if get_sum(ticket // 1000) == get_sum(ticket % 1000):
                count += 1
    return count

def main():


    M = 1
    n = 9999999
    count_threads = 8
    num_processes = 8
    start_time = time.time()


    Stream_size = n // count_threads
    ranges = [(M + i * Stream_size, M + (i + 1) * Stream_size - 1) for i in range(count_threads)]

    with ThreadPoolExecutor(max_workers=count_threads) as executor:
        results = list(executor.map(count_lucky_tickets_range, *zip(*ranges)))

    total_lucky_tickets = sum(results)
    print(f"Количество счастливых билетов в тираже {n} шт.: {total_lucky_tickets} ")

    end_time = time.time()
    print(end_time-start_time)

    start_time = time.time()

    Stream_size = n // num_processes
    ranges = [(M + i * Stream_size, M + (i + 1) * Stream_size - 1) for i in range(num_processes)]

    results = [Value('i', 0) for _ in range(num_processes)]
    processes = []

    for i, r in enumerate(ranges):
        p = Process(target=count_lucky_tickets_range, args=(r[0], r[1], results[i]))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total_lucky_tickets = sum(result.value for result in results)
    print(f"Количество счастливых билетов в тираже {n} шт.: {total_lucky_tickets}")

    end_time = time.time()
    print(end_time - start_time)

if __name__ == "__main__":
    main()