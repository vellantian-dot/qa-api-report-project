import requests
import pandas as pd
import os

from config import WINLOSE_URL


def test_api_response():
    response = requests.get(WINLOSE_URL)
    assert response.status_code == 200


def test_excel_exists():
    assert os.path.exists("winlose_report.xlsx")


def test_win_rate_excel_exists():
    assert os.path.exists("game_win_rate.xlsx")


def test_warning_log_exists():
    assert os.path.exists("logs/warning.log")


def test_chinese_column():
    df = pd.read_excel("winlose_report.xlsx")

    assert "會員帳號" in df.columns
    assert "遊戲名稱" in df.columns