Feature: User account
    In order to buy or sell commodities
    As a buyer or seller
    I want to have a account in the web site

    Scenario: Login as correct username and password
        Given an username "django" with the password "django123" is registered
         When I login as "django" and give the password "django123"
         Then I get the login result: "successful"

    Scenario: Login as incorrect username and password
        Given an username "django" with the password "django123" is registered
         When I login as "django" and give the password "abcdef123"
         Then I get the login result: "failed"

    Scenario Outline: username and password must be large than 5 characters
         When try to register a name <username> with a password <password>
         Then I get the register result: <result>

        Examples: some usernames and passwords
            | username  | password  | result                            |
            | abc       | 123456    | "username or password too short"  |
            | abcedf    | 123       | "username or password too short"  |
            | abc       | 123       | "username or password too short"  |
            | abcdef    | 123456    | "the account is created"          |
