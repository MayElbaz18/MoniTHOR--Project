import requests
import json
import concurrent.futures
from queue import Queue
import time
from pythonBE import check_certificate 
import os

def livness_check (username):
    # Measure start time
    start_time = time.time()

    urls_queue = Queue()
    analyzed_urls_queue = Queue()

    if not os.path.exists(f'./userdata/{username}_domains.json'):
        return "Domains file is not exist"
        
    with open(f'./userdata/{username}_domains.json', 'r') as f:
        currentListOfDomains=list(json.load(f))       
     
    for d in currentListOfDomains :        
        urls_queue.put(d['domain']) 
            

    print(f"Total URLs to check: {urls_queue.qsize()}")

    # Define the URL checking function with a timeout and result storage
    def check_url():
        while not urls_queue.empty():
            url = urls_queue.get()
            certInfo= check_certificate.check_cert(url) 
            result = {'domain': url, 'status_code': 'FAILED' ,"ssl_expiration":certInfo[0],"ssl_Issuer": certInfo[1]}  # Default to FAILED
            try:
                response = requests.get(f'http://{url}', timeout=1)
                if response.status_code == 200:
                    result['status_code'] = 'OK'
            except requests.exceptions.RequestException:
                result['status_code'] = 'FAILED'
            finally:
                analyzed_urls_queue.put(result)  # Add result to analyzed queue
                urls_queue.task_done()

    # Generate report after all URLs are analyzed
    def generate_report():
        results = []
        urls_queue.join()  # Wait for all URL checks to finish

        # Collect results from analyzed queue
        while not analyzed_urls_queue.empty():
            results.append(analyzed_urls_queue.get())
            analyzed_urls_queue.task_done()

        # Write results to JSON file
        with open(f'./userdata/{username}_domains.json', 'w') as outfile:
            json.dump(results, outfile, indent=4)
        print("Report generated in report.json")

    # Run URL checks in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as liveness_threads_pool:
        # Submit URL check tasks
        futures = [liveness_threads_pool.submit(check_url) for _ in range(20)]
        # Generate report after tasks complete
        liveness_threads_pool.submit(generate_report)

    urls_queue.join()  # Ensure all URLs are processed

    # Measure end time
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"URL liveness check complete in {elapsed_time:.2f} seconds.")
    with open(f'./userdata/{username}_domains.json', 'r') as f:
        results = json.load(f)
    return results

