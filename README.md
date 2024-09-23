# Generative AI AWS Application - Blog Generator
A Machine Learning application implemented and deployed on the AWS cloud, leveraging its AWS Bedrock tool to utilize the Llama 3 8B Instruct LLM.

## Application Diagram

<img src="assets/function_diagram.png" alt="Function_Diagram" width="400" />

1. Lambda Function: Triggered when a POST request is received with the blog's subject embedded in the body of the request.
   * Boto Layer: Added to the Function containing the latest version of Python's Boto3 library
2. API Gateway: Linked to the Lambda function to trigger it when an API request is received. Configured to listen to POST requests.
3. AWS Bedrock: Invoked by the Lambda function to access a Foundation Model (Llama 3 8B Instruct) using the Boto3 client. Receives requests with a prompt for the use case and returns a response.
4. S3 Bucket: Stores the final generated output - the blog content as a txt file.


### Lambda Function Permissions

<img src="assets/iam_policies.png" alt="Permissions" width="600" />

The IAM Role assigned to the Lambda Function requires all permissions (admin privileges) to invoke the Bedrock Client, or the application fails.


### API Gateway

<img src="assets/api_gateway.png" alt="Gateway Stage" width="600" />

A stage named dev is created and deployed to activate the URL that invokes the Gateway application when sending the POST request.


### Cloudwatch Logs

<img src="assets/cloudwatch_logs.png" alt="Cloudwatch Logs" width="600" />

AWS Cloudwatch logs all the relevant data when the event triggers the Lambda function and is a useful tool to debug any errors.

### S3 Storage

<img src="assets/s3.png" alt="S3 Output Storage" width="600" />

As indicated in the Cloudwatch logs, the generated blog content is stored in the S3 bucket as a txt file.

### POSTMAN API Call

<img src="assets/postman.png" alt="Postman" width="600" />

The Postman client is used to make an API POST request call and trigger the Lambda Function
