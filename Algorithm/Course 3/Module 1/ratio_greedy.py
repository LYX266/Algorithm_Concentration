import requests

class Job:
    def __init__(self, weight, length):
        self.weight = weight
        self.length = length

def compute_ratio(job):
    # Compute the ratio (weight / length) for sorting
    return job.weight / job.length

def compute_weighted_completion_time(jobs):
    # Sort jobs by (weight / length) in descending order
    jobs.sort(key=compute_ratio, reverse=True)

    total_weighted_completion_time = 0
    current_time = 0

    # Calculate the weighted completion time for each job
    for job in jobs:
        current_time += job.length
        total_weighted_completion_time += job.weight * current_time

    return total_weighted_completion_time

def main():
    # URL of the input data file
    url = "https://d3c33hcgiwev3.cloudfront.net/_642c2ce8f3abe387bdff636d708cdb26_jobs.txt?Expires=1730592000&Signature=c3aOwXrS3rQiM3K771~LTtpEv~~3IyWIhVg01jjuHaIKwC9QKaCTkUen6C4ca219rJQbM2IyUNemK6Yn0e9T~zNIB~R6RppOK7JTjRiETChCDY9GkA-W7RRVReUaf4XafZAlG6iQGMcfFZGRL-Uf3kuWZJN55zfmtirBpXfKtVM_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
    
    # Download the file from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for any errors in the download

    # Read lines from the downloaded file
    lines = response.text.strip().split('\n')
    
    # First line contains the number of jobs
    number_of_jobs = int(lines[0].strip())
    
    # Parse each job's weight and length
    jobs = []
    for line in lines[1:]:
        weight, length = map(int, line.strip().split())
        jobs.append(Job(weight, length))
    
    # Calculate the result
    result = compute_weighted_completion_time(jobs)
    print(result)

if __name__ == "__main__":
    main()
