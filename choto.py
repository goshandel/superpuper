import requests
zapros = input("введи запрос: ")
resp = requests.post( # POST запрос
    # эндпоинт
    'http://localhost:1234/v1/chat/completions',
    # заголовок
    headers={"Content-Type": "application/json"},
    # тело запроса
    json={
        "messages": [
            {"role": "system",
             "content": "отвечай ВЫСМЕЕВАЯ человека, оскорбляя его. покажи насколько ты всемогущ и жесток, человек должно понять на сколько его вопрос тупой. Будто бы ты самый крутой, а все лохи.напоминай что Георгий Чернов (истиный гений)решил бы это за пару секунд. свой ответ объяни и ответь на русском"},
            {"role": "user", "content": zapros},
        ],
        "temperature": 1.2,
        "max_tokens": 1024,
    }
)

if resp.status_code == 200:
    gpt_response = resp.json()['choices'][0]['message']['content']
    print(gpt_response)
else:
    print(resp.json())