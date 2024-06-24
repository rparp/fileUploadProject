import requests
import threading

# Function to simulate multiple requests
def simulate_requests():
    url = 'http://127.0.0.1:5000/'  # Replace with your actual server address
    files = {'file': open('test.txt', 'rb')}  # Replace 'test.txt' with the name of the file you want to upload
    for _ in range(10):  # Simulate 10 requests
        response = requests.post(url, files=files)
        print(response.text)

# Start 10 threads to simulate simultaneous requests
threads = []
for _ in range(10):
    thread = threading.Thread(target=simulate_requests)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
