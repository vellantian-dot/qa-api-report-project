QA API Homework

========================
作業一：API資料整理與格式化
========================

執行：
python main.py

功能：
1. API資料抓取
2. 欄位中文化
3. Excel輸出
4. 勝率計算
5. 勝率超過5%警示
6. Google Sheet自動上傳


========================
作業二：Allure測試報表
========================

執行測試：
python -m pytest --alluredir=allure-results

產生報表：
allure generate allure-results -o allure-report --clean

開啟報表：
allure open allure-report


測試項目：
1. API回傳驗證
2. 原始Excel產生驗證
3. 勝率Excel產生驗證
4. Warning Log產生驗證
5. 中文欄位轉換驗證

測試結果：
5 Passed
0 Failed