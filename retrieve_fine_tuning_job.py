import openai
import sys

if len(sys.argv) != 3:
    print("Usage: python script_name.py <OPENAI_API_KEY> <JOB_ID>")
    exit()

openai.api_key = sys.argv[1]
job_id = sys.argv[2]

try:
    response = openai.FineTuningJob.retrieve(job_id)
    print(response)
except Exception as e:
    print(f"Error retrieving the fine-tuning job status: {e}")
