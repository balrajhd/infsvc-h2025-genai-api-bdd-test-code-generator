import json
import boto3
from flask import Flask, render_template, request, jsonify, send_file
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import re
import zipfile
from io import BytesIO

# Load AWS credentials and region from environment
load_dotenv()

app = Flask(__name__)

if not os.path.exists('output'):
    os.makedirs('output')


# Bedrock client class
class Bedrock:
    def __init__(self, region, access_key, secret_key):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.native_request = {
            "prompt": "",
            "max_gen_len": 2048,
            "temperature": 0.5,
        }

    def generate_testcases(self, prompt: str):
        formatted_prompt = self.format_prompt(prompt)
        self.native_request["prompt"] = formatted_prompt
        model_id = "meta.llama3-8b-instruct-v1:0"

        try:
            # Invoke the model with the request.
            response = self.client.invoke_model(
                modelId=model_id, body=json.dumps(self.native_request)
            )
            model_response = self.process_response(response)
            return model_response
        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            return None

    def format_prompt(self, prompt: str) -> str:
        return f"""
        <|start_header_id|>user<|end_header_id|>
        {prompt}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

    def process_response(self, response) -> dict:
        response_body = response["body"].read()
        return json.loads(response_body)


class Utils:
    def __init__(self):
        pass

    def find_file_name(self, input_text: str):
        if any(ext in input_text for ext in ['.feature', '.ts', '.py', '.js', '.robot', '.json']):
            match = re.search(r'\b[\w]+\.(feature|steps\.ts|request\.ts|ts)\b', input_text)
            if match:
                print(match.group(0))
                return match.group(0)
        return None

    def clear_output_folder(self):
        for file in os.listdir("output"):
            os.remove(f"output/{file}")

    def generate_files(self, content):
        self.clear_output_folder()
        lines = content.split("\n")
        file = None
        write = False
        for line in lines:
            new_file = self.find_file_name(line)
            if new_file:
                file = new_file
                continue

            if line.startswith("```"):
                write = not write
                continue

            if write and file:
                with open(f"output/{file}", "a") as f:
                    f.write(line + '\n')

    def zip_output_folder(self):
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for foldername, subfolders, filenames in os.walk('output'):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zf.write(file_path, os.path.relpath(file_path, 'output'))
        memory_file.seek(0)
        return memory_file


# Initialize the Bedrock client with AWS credentials
bedrock_client = Bedrock(
    region=os.getenv("AWS_REGION"),
    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_test_cases", methods=["POST"])
def generate_test_cases():
    data = request.json

    # Extract form data
    framework = data.get("framework")
    language = data.get("language")
    http_method = data.get("httpMethod")
    endpoint = data.get("endpoint")
    request_body = data.get("requestBody", "")
    schema = data.get("schema", "")

    prompt = f"""
    Generate test cases for the following API:
    Method: {http_method}
    Endpoint: {endpoint}
    Request Body: {request_body}
    Schema: {schema}
    Framework: {framework}
    Langugaue: {language}
    Ensure the generated code is modular, reusable, and maintains best practices for API test automation.
    Also provide the file names along with the code.
    Provide only a single feature and step definition file.
    step-definition files should only contain import statements from `@cucumber/cucumber` and `@playwright/test` libraries.
    Only import expect, request from `@playwright/test` library.
    Also implement all the necessary functions in the step-definition file.
    Both the files should be ready to run without any modifications.
    """
    model_response = bedrock_client.generate_testcases(prompt)

    # Check if we got a response
    if (model_response):
        generated_test_cases = model_response.get("generation", "No generation available")
        utils = Utils()
        utils.generate_files(generated_test_cases)

        # Create zip file
        zip_file = utils.zip_output_folder()

        # Save the zip file to the output folder
        zip_file_path = 'output/generated_test_cases.zip'
        with open(zip_file_path, 'wb') as f:
            f.write(zip_file.getbuffer())

        return jsonify({"generatedTestCases": generated_test_cases, "download_link": f"/download/{os.path.basename(zip_file_path)}"})
    else:
        return jsonify({"error": "Failed to generate test cases"}), 500


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(f'output/{filename}', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
