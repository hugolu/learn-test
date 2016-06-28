# language: zh-TW
功能: 網頁計算機

    身為一個學生
    為了完成家庭作業
    我想要做算術運算

    場景大綱: 做簡單的運算
        假設< 我輸入<expression>
          當< 我按下等號按鈕
        那麼< 我得到的答案是<answer>

        例子:
            | expression    | answer        |
            | 3 + 2         | 5             |
            | 3 - 2         | 1             |
            | 3 * 2         | 6             |
            | 3 / 2         | 1.5           |
            | 3 +-*/ 2      | Invalid Input |
            | hello world   | Invalid Input |

    場景大綱: 滿足交換律
         當< 我先輸入<expression1>
         當< 我再輸入<expression2>
        那麼< 我得到相同的答案

        例子:
            | expression1   | expression2   |
            | 3 + 4         | 4 + 3         |
            | 2 * 5         | 5 * 2         |

    場景大綱: 滿足結合律
         當< 我先輸入<expression1>
         當< 我再輸入<expression2>
        那麼< 我得到相同的答案

        例子:
            | expression1   | expression2   |
            | (2 + 3) + 4   | 2 + (3 + 4)   |
            | 2 * (3 * 4)   | (2 * 3) * 4   |

    場景大綱: 滿足結合律
         當< 我先輸入<expression1>
         當< 我再輸入<expression2>
        那麼< 我得到相同的答案

        例子:
            | expression1   | expression2   |
            | 2 * (1 + 3)   | (2*1) + (2*3) |
            | (1 + 3) * 2   | (1*2) + (3*2) |
