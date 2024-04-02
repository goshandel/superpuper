import json

import requests

from skamm import MAX_MODEL_TOKENS, FOLDER_ID, GPT_MODEL, MODEL_TEMPERATURE, TOKENS_DATA_PATH
from utils import get_iam_token

def get_system_message(janr, hero, sett, additional=None):
    prompt = (f"\nНапиши начало истории в стиле {janr} "
               f"с главным героем {hero}. "
               f"Вот начальный сеттинг: \n{sett}. \n"
               f"Начало должно быть коротким, 1-3 предложения.\n")


    return {
        "role": "system",
        "content": prompt,
    }


def count_tokens_in_dialogue(messages: list) -> int:
    iam_token = get_iam_token()

    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
        "maxTokens": MAX_MODEL_TOKENS,
        "messages": []
    }

    for row in messages:
        data["messages"].append(
            {
                "role": row["role"],
                "text": row["content"]
            }
        )

    return len(
        requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion",
            json=data,
            headers=headers
        ).json()["tokens"]
    )


def increment_tokens_by_request(messages: list[dict]):
    """
    Добавляет количество токенов потраченных на запрос и ответ
    к общей сумме в json файле
    """
    try:
        with open(TOKENS_DATA_PATH, "r") as token_file:
            tokens_count = json.load(token_file)["tokens_count"]

    except FileNotFoundError:
        tokens_count = 0

    current_tokens_used = count_tokens_in_dialogue(messages)
    tokens_count += current_tokens_used

    with open(TOKENS_DATA_PATH, "w") as token_file:
        json.dump({"tokens_count": tokens_count}, token_file)


def ask_gpt(messages):
    """Запрос к Yandex GPT"""
    iam_token = get_iam_token()

    url = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
        "completionOptions": {
            "stream": False,
            "temperature": MODEL_TEMPERATURE,
            "maxTokens": MAX_MODEL_TOKENS
        },
        "messages": []
    }

    for row in messages:
        data["messages"].append(
            {
                "role": row["role"],
                "text": row["content"]
            }
        )

    try:
        response = requests.post(url, headers=headers, json=data)

    except Exception as e:
        print("Произошла непредвиденная ошибка.", e)

    else:
        if response.status_code != 200:
            print("Ошибка при получении ответа:", response.status_code)
        else:
            result = response.json()['result']['alternatives'][0]['message']['text']
            messages.append({"role": "assistant", "content": result})
            increment_tokens_by_request(messages)
            return result


print(ask_gpt(messages))
with open(TOKENS_DATA_PATH, "r") as f:
    print("За всё время израсходовано:", json.load(f)["tokens_count"], "токенов")
