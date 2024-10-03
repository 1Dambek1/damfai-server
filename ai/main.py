import json
import requests
import time

all_time = 0

for i in range(10):
    time_started = time.time()

    app = requests.post("http://localhost:4200/v1/chat/completions", 
                        data={"model": "microsoft/Phi-3-mini-4k-instruct-gguf/Phi-3-mini-4k-instruct-q4.gguf",
                            "messages": json.dumps([{"role": "user", "content": "Say hello"}]), 
                            "temperature": 0.7,
                            "max_tokens": -1,
                            "stream": False})
    print(json.loads(app.text)["choices"][0]["message"]["content"])


    print(time.time()-time_started)

    all_time += time.time()-time_started
print(all_time/10)