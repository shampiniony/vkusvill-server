import json

import pandas as pd
import requests

csv_file = "./fruits_dump.csv"
df = pd.read_csv(csv_file)

url = "http://localhost:8000/goods/"

for _, row in df.iterrows():
    data = {
        "sku_id": str(row["sku_id"]),
        "name": str(row["name"]),
        "category": str(row["category"]),
        "amount": int(row["amount"]),
        "avg_cart": int(row["avg_cart"]),
        "dt": int(row["dt"]),
        "trigger": float(row["trigger"]),
        "shelve": str(row["shelve"]),
    }

    response = requests.post(
        url, headers={"Content-Type": "application/json"}, data=json.dumps(data)
    )

    if response.status_code == 200:
        print(f"Успешно добавлен товар: {row['name']}")
    else:
        print(
            f"Ошибка при добавлении товара: {row['name']}, код ошибки: {response.status_code}, ответ: {response.text}"
        )
