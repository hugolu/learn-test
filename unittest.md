# unittest 筆記

參考：[unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)

Python unittest 測試框架發想自 JUnit 並與其他單元測試的框架有類似的味道：

- 支援自動化測試
- 測試間共享 setup 與 shutdown 程式碼
- 每次測試皆是獨立，結果不會受其他測試影響

觀念名詞

| 名詞 | 解釋 |
|------|------|
| 測試夾具 (test fixture) | 包含一個或多個被執行的測試，與相關的初始與結束動作。 |
| 測試案例 (test case) | 個別單元測試，用來檢查特定輸入的反應。 |
| 測試套組 (test suite) | 由測試案例、測試套組構成，用來集合應該被一起執行的測試。 |
| 測試執行 (test runner) | 負責執行測試與回報結果。 |
