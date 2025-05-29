# mcp-lambda

This project contains a serverless application that processes natural language prompts using an AI agent with the Model Completion Protocol (MCP). The application is built with AWS Lambda and can be deployed using the SAM CLI.

## Project Overview

The Lambda function:
- Receives a natural language prompt as input
- Uses the MCP (Model Completion Protocol) client to connect to a documentation server
- Creates an agent with tools from the MCP server using the strands library
- Processes the prompt with the agent and returns the result

## Project Structure

- `hello_world/` - Code for the Lambda function that processes prompts
  - `app.py` - Main Lambda handler that integrates with MCP and strands
  - `requirements.txt` - Dependencies including strands-agents and aws-documentation-mcp-server
- `events/` - Sample events for testing the Lambda function
- `tests/` - Unit and integration tests
- `template.yaml` - SAM template defining AWS resources including Lambda and API Gateway

## Dependencies

The application relies on:
- Python 3.12 runtime
- strands-agents library
- awslabs.aws-documentation-mcp-server
- Amazon Bedrock for AI capabilities (via AmazonBedrockFullAccess policy)

## Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda.

To use the SAM CLI, you need the following tools:

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3.12 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Using the Lambda Function

The Lambda function expects an event with a `prompt` field containing the natural language prompt to process. When invoked through API Gateway, the prompt should be included in the request body.

### Testing Locally

Build your application with the `sam build --use-container` command:

```bash
sam build --use-container
```

Test the function locally by invoking it with a test event:

```bash
sam local invoke HelloWorldFunction --event events/event.json
```

The sample event in `events/event.json` contains a simple "hello world" prompt. You can modify this file to test different prompts.

### Using the API Endpoint

After deployment, you can send requests to the API Gateway endpoint:

```bash
curl -X GET https://your-api-id.execute-api.your-region.amazonaws.com/Prod/hello/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "your prompt here"}'
```

Replace `your-api-id` and `your-region` with the actual values from your deployment output.

## Testing

Tests are defined in the `tests` folder in this project. Use pip to install the test dependencies and run tests.

```bash
pip install -r tests/requirements.txt
# unit test
python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
AWS_SAM_STACK_NAME="mcp-lambda" python -m pytest tests/integration -v
```

## Monitoring and Troubleshooting

### Logs

To view logs from your deployed Lambda function, use the SAM CLI:

```bash
sam logs -n HelloWorldFunction --stack-name "mcp-lambda" --tail
```

This command will display logs in real-time, which is useful for debugging issues with the MCP client, strands agent, or Bedrock integration.

### Common Issues

1. **Bedrock Access**: Ensure your AWS account has access to Amazon Bedrock and the necessary model permissions.
2. **Memory and Timeout**: The Lambda function is configured with 2048MB memory and a 900-second timeout. If you're processing complex prompts, you may need to adjust these settings in the `template.yaml` file.
3. **Dependencies**: If you modify the dependencies, make sure to update the `requirements.txt` file and rebuild the application.

## Cleanup

To delete the application that you created, use the AWS CLI:

```bash
sam delete --stack-name "mcp-lambda"
```

## Resources

- [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Strands Agents Documentation](https://github.com/amazon-science/strands-agents)
- [Model Completion Protocol (MCP) Documentation](https://github.com/aws-samples/aws-mcp-examples)
