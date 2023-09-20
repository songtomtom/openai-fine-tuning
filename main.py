import openai
import time
import sys

if len(sys.argv) < 2:
    print("Usage: python script_name.py <OPENAI_API_KEY> [MODEL_NAME]")
    exit()

openai.api_key = sys.argv[1]
model_name = sys.argv[2] if len(sys.argv) > 2 else "gpt-3.5-turbo-0613"

# 파일 업로드
try:
    file = openai.File.create(
        file=open("mydata2.jsonl", "rb"),
        purpose='fine-tune'
    )
    print(f'file = {file}')
except Exception as e:
    print(f"Error uploading file: {e}")
    exit()

file_id = file["id"]

# 파일 상태가 "processed"가 될 때까지 기다림
while True:
    try:
        retrieved_file = openai.File.retrieve(file_id)
        status = retrieved_file["status"]
        print(f'File status: {status}')

        if status == "processed":
            break
        elif status == "error":
            print("Error processing the file.")
            exit()
        time.sleep(10)
    except Exception as e:
        print(f"Error checking file status: {e}")
        exit()

# 미세 조정 작업 시작
try:
    response = openai.FineTuningJob.create(training_file=file_id, model=model_name)
    print(f'response = {response}')
except Exception as e:
    print(f"Error starting fine-tuning job: {e}")
    exit()

job_id = response["id"]

# job 상태가 "succeeded"가 될 때까지 기다림
while True:
    try:
        response = openai.FineTuningJob.retrieve(job_id)
        status = response["status"]
        print(f'Job status: {status}')

        if status == "succeeded":
            print("Job succeeded!")
            break
        elif status == "failed":
            print("Error: Job failed.")
            exit()
        elif status == "cancelled":
            print("Job was cancelled.")
            exit()
        elif status in ["queued", "running"]:
            pass  # Job is still in progress, just wait and check again.
        else:
            print(f"Unknown status: {status}. Exiting.")
            exit()
        time.sleep(10)
    except Exception as e:
        print(f"Error checking job status: {e}")
        exit()
