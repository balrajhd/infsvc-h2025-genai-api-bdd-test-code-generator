# API Test Case Generator

This project is a web application designed to generate API test cases based on input specifications such as HTTP method, endpoint, request body, and schema. It integrates with AWS Bedrock to generate the necessary test files and provides a downloadable zip of the test case files. The generated test case files are tailored for a specific framework and language and are ready to run immediately, reducing manual effort and streamlining the API test automation process.
Note: End goal being 0 manual efforts, the current code is still a WIP.

[demo video](https://infoservicesllc-my.sharepoint.com/:v:/g/personal/balrajhd_infoservices_com/ERgQsRAL6dFGif1voDOSTsgBM-4pCb8vYELnLpW5hYQdlQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=sXlWBt)

## Features

- **Generate API Test Cases**: Based on the provided API details (HTTP method, endpoint, body, etc.), the application generates test cases that are modular, reusable, and follow best practices for API test automation.
- **Framework and Language Support**: Supports customization of the generated test cases based on the test framework and programming language.
- **Downloadable Test Files**: The generated test cases are provided as a downloadable zip file containing feature files and step-definition files.
- **AWS Integration**: Uses AWS Bedrock service for test case generation.

## Requirements

- Python 3.x
- Flask
- Boto3 (for AWS SDK)
- AWS credentials (Access Key, Secret Key, and Region)
- `.env` file containing the AWS credentials
- Python Libraries:
  - `Flask`
  - `boto3`
  - `dotenv`
  - `zipfile`
  - `re`
  - `json`

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/balrajhd/infsvc-h2025-genai-api-bdd-test-code-generator.git
    cd infsvc-h2025-genai-api-bdd-test-code-generator
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up AWS credentials**:
    Create a `.env` file at the root of the project and add your AWS credentials:
    ```dotenv
    AWS_ACCESS_KEY_ID=your-access-key-id
    AWS_SECRET_ACCESS_KEY=your-secret-access-key
    AWS_REGION=your-region
    ```

4. **Run the Flask app**:
    ```bash
    python app.py
    ```

    The app will be running at `http://127.0.0.1:5000/`.

## Usage

1. **Go to the web interface** at `http://127.0.0.1:5000/`.

2. **Fill in the form**:
   - Select the **framework** (e.g., Cucumber, Playwright, etc.)
   - Select the **language** (e.g., JavaScript, TypeScript, Python, etc.)
   - Provide the **HTTP Method** (e.g., GET, POST, PUT, DELETE)
   - Provide the **API endpoint** (e.g., `/api/v1/user`)
   - Enter the **request body** (if applicable)
   - Provide the **schema** (optional, can be left empty)

3. **Click "Generate Test Cases"** to generate the test cases.

4. Once the generation is complete, a **download link** will be provided.

5. **Download the test cases** as a `.zip` file containing:
   - Feature files
   - Step definition files (with all necessary imports and functions)

## Folder Structure

- `output/`: Contains generated files, including test cases and zip archives.
- `.env`: Stores AWS credentials.
- `app.py`: Main Flask application with API routes and logic for generating test cases.
- `utils.py`: Helper class for file management and zip creation.

## Code Explanation

### **Bedrock Class**
This class interacts with the AWS Bedrock runtime to generate the test cases. It:
- Formats the input prompt.
- Sends the request to the AWS Bedrock model.
- Processes the response to extract generated test cases.

### **Utils Class**
This class provides utility functions for:
- Finding file names based on input text.
- Clearing old test case files in the `output` folder.
- Writing the generated test case content into appropriate files.
- Creating a zip file of the generated test case files.

### **Flask Routes**
- **`/`**: Displays the main form to input API details.
- **`/generate_test_cases`**: Handles the generation of test cases when a POST request is made with API details.
- **`/download/<filename>`**: Allows the user to download the generated test case zip file.

## Error Handling

If something goes wrong while generating the test cases, the application will return an error message:
```json
{
    "error": "Failed to generate test cases"
}
```