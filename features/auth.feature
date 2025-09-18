Feature: ReqRes authentication

  @auth
  Scenario Outline: Login attempts return expected result
    Given I have login payload with "<email>" and "<password>"
    When I POST to /login
    Then response status should be <status>
    And response should contain "<field>"

    Examples:
      | email                  | password     | status | field  |
      | eve.holt@reqres.in     | cityslicka   | 200    | token  |
      | peter@klaven           | test         | 400    | error  |