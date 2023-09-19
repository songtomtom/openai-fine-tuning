import json

# 변환된 데이터를 저장할 리스트
transformed_data = []

with open("example_prepared.jsonl", "r") as f:
    for line in f:
        data = json.loads(line.strip())
        prompt = data["prompt"]
        completion = data["completion"]

        transformed_entry = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that analyzes sentences based on grammar elements."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": completion}
            ]
        }

        transformed_data.append(transformed_entry)

# 변환된 데이터를 새 파일에 저장
with open("example_chat_prepared.jsonl", "w") as f:
    for entry in transformed_data:
        f.write(json.dumps(entry) + "\n")
