import { Given, When, Then } from '@cucumber/cucumber';
import { APIRequestContext, expect, request } from '@playwright/test';

let apiEndpoint = 'https://reqres.in/api/users';
let apiContext: APIRequestContext;

Given('the API endpoint is {string}', async (endpoint) => {
  apiEndpoint = endpoint;
  apiContext = await request.newContext();
});

When('I send a GET request to the API', async () => {
  const response = await apiContext.get('https://reqres.in/api/users');
  return response;
});

Then('the response status code should be {int}', async (statusCode) => {
  const response = await apiContext.get(apiEndpoint);
  expect(response.status()).toBe(parseInt(statusCode));
});

Then('the response body should contain a list of users', async () => {
  const response = await apiContext.get(apiEndpoint);
  const responseBody = await response.json();
  expect(responseBody).toBeInstanceOf(Object);
  expect(responseBody).toHaveProperty('page');
  expect(responseBody).toHaveProperty('per_page');
  expect(responseBody).toHaveProperty('total');
  expect(responseBody).toHaveProperty('total_pages');
  expect(responseBody).toHaveProperty('data');
  expect(responseBody.data).toBeInstanceOf(Array);
});
