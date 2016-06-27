#file: features/calc.feature

Feature: Web calculator

    As a student
    In order to finish my homework
    I want to do arithmatical operations

    Scenario Outline: do simple operations
        Given I enter <expression>
         When I press "=" button
         Then I get the answer <answer>

        Examples:
            | expression    | answer        |
            | 3 + 2         | 5             |
            | 3 - 2         | 1             |
            | 3 * 2         | 6             |
            | 3 / 2         | 1.5           |
            | 3 +-*/ 2      | Invalid Input |
            | hello world   | Invalid Input |

    Scenario Outline: satisfy commutative property
         When I enter <expression1> first
          And I enter <expression2> again
         Then I get the same answer

        Examples:
            | expression1   | expression2   |
            | 3 + 4         | 4 + 3         |
            | 2 * 5         | 5 * 2         |

    Scenario Outline: satisfy associative property
         When I enter <expression1> first
          And I enter <expression2> again
         Then I get the same answer

        Examples:
            | expression1   | expression2   |
            | (2 + 3) + 4   | 2 + (3 + 4)   |
            | 2 * (3 * 4)   | (2 * 3) * 4   |

    Scenario Outline: satisfy distributive property
         When I enter <expression1> first
          And I enter <expression2> again
         Then I get the same answer

        Examples:
            | expression1   | expression2   |
            | 2 * (1 + 3)   | (2*1) + (2*3) |
