import concurrent.futures
import time

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def goldbach_conjecture(n):
    if n % 2 != 0 or n <= 2:
        return None
    for i in range(2, n // 2 + 1):
        if is_prime(i) and is_prime(n - i):
            return (i, n - i)
    return None

def calculate_goldbach_range(start, end, output_file):
    with open(output_file, 'a') as f:
        for num in range(start, end + 1, 2):
            result = goldbach_conjecture(num)
            if result:
                f.write(f"{num} = {result[0]} + {result[1]}\n")

def main():
    output_file = "goldbach_multithread_50million.txt"
    start_num = 2
    end_num = 50000000  # Adjust the range as needed
    num_threads = 32

    # Calculate the range for each thread
    step = (end_num - start_num + 1) // num_threads

    # Create a thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            start = start_num + i * step
            end = start + step - 1
            future = executor.submit(calculate_goldbach_range, start, end, output_file)
            futures.append(future)

        # Wait for all threads to finish
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
