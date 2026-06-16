import requests
import pandas as pd
import logging
import os

from config import WINLOSE_URL
from config import WARNING_RATE

# =========================
# Log設定
# =========================

logging.basicConfig(
    filename="logs/warning.log",
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8"
)

# =========================
# API抓取資料
# =========================

response = requests.get(WINLOSE_URL)

print("狀態碼：", response.status_code)

if response.status_code != 200:
    raise Exception("API取得失敗")

data = response.json()

df = pd.DataFrame(data["rows"])

print("資料筆數：", len(df))

# =========================
# 欄位中文化
# =========================

column_mapping = {
    "account": "會員帳號",
    "gameName": "遊戲名稱",
    "betId": "注單編號",
    "betValue": "投注金額",
    "profit": "盈利",
    "currency": "幣別",
    "gameEndTime": "結束時間",
    "roomType": "房間類型",
    "revenue": "營收",
    "score": "分數"
}

df.rename(
    columns=column_mapping,
    inplace=True
)

# =========================
# 數值欄位轉換
# =========================

numeric_columns = [
    "盈利",
    "投注金額",
    "營收",
    "分數"
]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# =========================
# 原始報表輸出
# =========================

df.to_excel(
    "winlose_report.xlsx",
    index=False
)

print("winlose_report.xlsx 產生完成")

# =========================
# 勝率計算
# =========================

result = []

for game_name, game_df in df.groupby("遊戲名稱"):

    total_count = len(game_df)

    win_count = len(
        game_df[
            game_df["盈利"] > 0
        ]
    )

    win_rate = (
        win_count / total_count
    ) * 100

    result.append({
        "遊戲名稱": game_name,
        "總局數": total_count,
        "贏局數": win_count,
        "勝率": round(win_rate, 2),
        "警示": "⚠️超過5%" if win_rate > WARNING_RATE else ""
    })

result_df = pd.DataFrame(result)

# =========================
# 勝率報表輸出
# =========================

result_df.to_excel(
    "game_win_rate.xlsx",
    index=False
)

print("game_win_rate.xlsx 產生完成")

# =========================
# 警示檢查
# =========================

for _, row in result_df.iterrows():

    try:

        win_rate = float(row["勝率"])

        if win_rate > WARNING_RATE:

            warning_msg = (
                f"WARNING 遊戲:{row['遊戲名稱']} "
                f"勝率:{win_rate}%"
            )

            print(warning_msg)

            logging.warning(
                warning_msg
            )

    except Exception as e:

        print(
            f"警示檢查失敗:{e}"
        )

# =========================
# Google Sheet上傳
# =========================

print("開始上傳 Google Sheet...")

os.system(
    "python upload_sheet.py"
)

print("全部流程完成")