# Demo of BDD/TDD/CI on Django

## 前言

本來想用網站帳號註冊與登入來示範 TDD/BDD，但是
- 帳號檢查的邏輯太簡單，很難示範 TDD
- Behave-django 做得太好了，Model 根本不需要 mock

要找出一個範例會複雜到需要拆成 features, steps, interfaces, implementation of [SUT](http://xunitpatterns.com/SUT.html), 還有要切割依賴的 [DOC](http://xunitpatterns.com/DOC.html)，同時又必須簡單到範例可以塞進一張投影片。幾經考量，轉而想使用解析字串的計算機(類似工程用計算機)做範例。

計算機須滿足幾個規則
- [四則運算規則](https://zh.wikipedia.org/wiki/%E5%9B%9B%E5%88%99%E8%BF%90%E7%AE%97): 先乘除、後加減
- [交換律](https://zh.wikipedia.org/wiki/%E4%BA%A4%E6%8F%9B%E5%BE%8B): "3 + 4 = 4 + 3",  "2 × 5 = 5 × 2"
- [結合律](https://zh.wikipedia.org/wiki/%E7%BB%93%E5%90%88%E5%BE%8B): "(5+2)+1 = 5 + (2+1) = 8"
- [分配律](https://zh.wikipedia.org/wiki/%E5%88%86%E9%85%8D%E5%BE%8B): "2 ⋅ (1 + 3) = (2 ⋅ 1) + (2 ⋅ 3)"
