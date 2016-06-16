# language: zh-TW

功能: 用戶帳號
    為了買賣商品
    身為買家或賣家
    我想要有一個電子商務網站帳號

    場景: 用正確的帳號跟密碼登入
        假設< 帳號django與密碼django123已註冊
          當< 我用django與密碼django123登入
        那麼< 我得到登入結果：成功

    場景: 用不正確的帳號跟密碼登入
        假設< 帳號django與密碼django123已註冊
          當< 我用django與密碼abcdef123登入
        那麼< 我得到登入結果：失敗

    場景大綱: 帳號與密碼必須大於5個字元
        當< 嘗試用帳號<username>與密碼<password>註冊
        那麼< 我得到註冊結果：<result>

        例子: 一些帳號與密碼
            | username  | password  | result            |
            | abc       | 123456    | 無效的帳號或密碼  |
            | abcedf    | 123       | 無效的帳號或密碼  |
            | abc       | 123       | 無效的帳號或密碼  |
            | abcdef    | 123456    | 帳號建立          |
