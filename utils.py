import json
import time

import requests

from skamm import IAM_TOKEN_ENDPOINT, IAM_TOKEN_PATH


def create_new_iam_token():
    """
    Получает новый IAM-TOKEN и дату истечения его срока годности и
    записывает полученные данные в json
    """
    headers = {"Metadata-Flavor": "Google"}

    try:
        response = requests.get(IAM_TOKEN_ENDPOINT, headers=headers)

    except Exception as e:
        print("Не удалось выполнить запрос:", e)
        print("Токен не получен")

    else:
        if response.status_code == 200:
            token_data = {
                "access_token": response.json().get("access_token"),
                "expires_at": response.json().get("expires_in") + time.time()
            }

            with open(IAM_TOKEN_PATH, "w") as token_file:
                json.dump(token_data, token_file)

        else:
            print("Ошибка при получении ответа:", response.status_code)
            print("Токен не получен")


def get_iam_token() -> str:
    """
    Получает действующий IAM-TOKEN и возвращает его
    """
    try:
        with open(IAM_TOKEN_PATH, "r") as token_file:
            token_data = json.load(token_file)

        expires_at = token_data.get("expires_at")

        if expires_at <= time.time():
            create_new_iam_token()

    except FileNotFoundError:
        create_new_iam_token()

    with open(IAM_TOKEN_PATH, "r") as token_file:
        token_data = json.load(token_file)

    return token_data.get("access_token")