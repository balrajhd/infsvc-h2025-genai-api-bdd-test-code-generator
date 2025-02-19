Feature: Get Users
  As a user
  I want to retrieve a list of users
  So that I can use the API

  Scenario: Get Users
    Given the API endpoint is "https://reqres.in/api/users"
    When I send a GET request to the API
    Then the response status code should be 200
    And the response body should contain a list of users
