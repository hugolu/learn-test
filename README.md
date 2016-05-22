# 學習測試

![](http://continuousdelivery.com/images/test-quadrant.png)
(圖片來自：http://continuousdelivery.com/foundations/test-automation/)

## 業務導向且支持開發過程的測試

### 驗收測試
- 確保用戶故事的驗收條件得到滿足

## 技術導向且支持開發過程的測試

### 單元測試
- 單元測試單獨測試一段特定的程式碼
- 常常倚賴測試替身 (test double) 模擬系統其他部分

### 組件測試

### 部署測試

## 業務導向且評價專案的測試

### 展示
- 每次迭代結束時，敏捷開發團隊向用戶展示其開發完成的新功能

### 探索性測試
- 創造學習的過程，不只是發現缺陷
- 創建新的自動化測試，用來覆蓋新的需求

### 易用性測試
- 驗證用戶能否容易使用軟體完成工作
- 情境調查：觀察使用者操作過程，收集量化數據，如使用者多久時間完成任務、按了多少次錯誤的按鈕、試用者自評滿意度
- Beta測試：網站同時運行多個版本，收集、統計、分析新功能的使用情形，讓功能適者生存不斷演進

## 技術導向且評價專案的測試

### 非功能性測試
- 除了功能之外的系統品質測試，如容量、可用性、安全性
- 客戶不關心非功能需求，但當他們意識這方面的問題，事情往往一發不可收拾
  - 容量：網站因為容量問題，停止提供服務
  - 安全性：用戶個資外洩、信用卡被盜刷

## 參考資料
- [Continuous Testing](http://continuousdelivery.com/foundations/test-automation/)
- [Behavior-Driven Development in Python](http://code.tutsplus.com/tutorials/behavior-driven-development-in-python--net-26547)
- [behave](http://pythonhosted.org/behave/) is behaviour-driven development, Python style.
- [Lettuce](http://lettuce.it/) is a Behavior-Driven Development tool written by Gabriel Falcão G. de Moura.
- [unittest](https://docs.python.org/3/library/unittest.html) — Unit testing framework
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) — mock object library
- [Doubles](http://doubles.readthedocs.io/) is a Python package that provides test doubles for use in automated tests.

