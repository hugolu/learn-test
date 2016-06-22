# pyparsing

這份文件不是 pyparsing 的完整說明，只為了把字串解析成數學運算式所做的練習與摸索。

除了 [Getting Started with Pyparsing](http://shop.oreilly.com/product/9780596514235.do) 這本書，pyparsing 似乎沒有完整的說明文件？！

以下透過一些練習，嘗試理解 [fourFn.py](http://pyparsing.wikispaces.com/file/view/fourFn.py) 這份解析工程數學運算式的程式碼。

## pyparsing: 從本文抽取訊息的工具

pyparsing 模組提供程式設計師使用 python 語言從結構化的文本資料抽取資訊。

這個工具比正規化表示式更強大 (python re 模組)，但又不像編譯器那樣一般化。

為了找出結構化文本中的訊息，我們必須描述結構。pyparsing 模組建立在 [Backus-Naur Form](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_Form) (BNF) 語法描述技術的基礎上。熟悉 BNF 的語法標記有助於使用 pyparsing。

pyparsing 模組運作的方式是使用遞迴減少解析器 [recursive descent parser](https://en.wikipedia.org/wiki/Recursive_descent_parser) 匹配輸入文字：我們寫出像 BNF 語法產物，然後 pyparsing 提供機制用這些產物匹配輸入文本。

The pyparsing module works best when you can describe the exact syntactic structure of the text you are analyzing. A common application of pyparsing is the analysis of log files. Log file entries generally have a predictable structure including such fields as dates, IP addresses, and such. Possible applications of the module to natural language work are not addressed here.

當你能精準描述分析的文本結構，pyparsing 模組就能發揮強大的作用。通常 pyparsing 會拿來分析 log 檔。log 檔通常有個可預測的結構，欄位包含日期、IP位置、等等。

## 建構應用程式

1. 寫出 BNF 描述要分析文本的結構
2. 視需要，安裝 pyparsing 模組
3. 在 python script 中匯入 pyparsing 模組：`import pyparsing as pp`
4. 在 python script 中寫出能匹配 BNF 的 parser
5. 準備要分析的文本
6. 如果用 p 表示 parser，用 s 表示文本，執行的程式碼就像 `p.parseString(s)`

----
## 參考

- [Pyparsing Wiki Home](http://pyparsing.wikispaces.com/)
- [pyparsing quick reference](http://infohost.nmt.edu/tcc/help/pubs/pyparsing/web/index.html)
- [Module pyparsing](https://pythonhosted.org/pyparsing/)
