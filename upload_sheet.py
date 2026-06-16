import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open("QA API Homework").sheet1

# 讀取Excel
df = pd.read_excel("game_win_rate.xlsx")

# 將 NaN 轉成空字串
df = df.fillna("")

# 若沒有警示欄位則建立
if "警示" not in df.columns:
    df["警示"] = ""

# 超過5%標示警示
for index, row in df.iterrows():
    if float(row["勝率"]) > 5:
        df.at[index, "警示"] = "⚠️超過5%"

# 清空 Google Sheet
sheet.clear()

# 上傳資料
sheet.update(
    [df.columns.tolist()] +
    df.values.tolist()
)

print("Google Sheet 上傳成功")