# mcp-lambda

This project contains source code and supporting files for a serverless application that uses the Model Context Protocol (MCP) with AWS Lambda. MCP is Model Context Protocol, a standardized interface for interacting with AI models and tools.

This Lambda function uses the Strands agent framework to process prompts through an MCP server that provides access to AWS documentation tools. The application takes a text prompt as input and returns AI-generated responses based on AWS documentation.

The project includes the following files and folders:

- hello_world - Code for the application's Lambda function that implements the MCP client.
- events - Invocation events that you can use to invoke the function with sample prompts.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get started.

* [CLion](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [GoLand](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [WebStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [Rider](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PhpStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [RubyMine](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [DataGrip](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
mcp-lambda$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt` (including the Strands agent framework and AWS Documentation MCP server), creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test the MCP Lambda function by invoking it directly with a test event. The event should include a prompt that will be processed by the Strands agent using the Model Context Protocol (MCP). A sample event is included in the `events` folder.

Run the function locally and invoke it with the `sam local invoke` command:

```bash
mcp-lambda$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
mcp-lambda$ sam local start-api
mcp-lambda$ curl -X GET "http://localhost:3000/hello?prompt=Tell%20me%20about%20AWS%20Lambda"
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
mcp-lambda$ sam logs -n HelloWorldFunction --stack-name "mcp-lambda" --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
mcp-lambda$ pip install -r tests/requirements.txt --user
# unit test
mcp-lambda$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
mcp-lambda$ AWS_SAM_STACK_NAME="mcp-lambda" python -m pytest tests/integration -v
```

The unit tests verify that the MCP client is correctly initialized and that the Lambda function properly processes prompts through the Model Context Protocol (MCP) server. Integration tests validate the end-to-end functionality of the deployed Lambda function.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name "mcp-lambda"
```

## Understanding the Model Context Protocol (MCP)

The Model Context Protocol (MCP) is a standardized interface for interacting with AI models and tools. In this project, MCP is used to:

1. Connect the Lambda function to an MCP server that provides access to AWS documentation tools
2. Allow the Strands agent to discover and use tools available through the MCP server
3. Process user prompts and generate responses based on AWS documentation

The implementation in `hello_world/app.py` uses:
- `MCPClient` from the Strands library to create a client that connects to the MCP server
- `stdio_client` to establish communication with the MCP server process
- `Agent` from the Strands library to create an agent that can use the tools provided by the MCP server

When a request is received, the Lambda function:
1. Extracts the prompt from the event
2. Initializes the MCP client and connects to the AWS documentation MCP server
3. Lists available tools from the MCP server
4. Creates a Strands agent with these tools
5. Processes the prompt using the agent
6. Returns the response as a JSON object

For more information about the Model Context Protocol, refer to the documentation for the Strands library and the AWS Documentation MCP server.

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

For more information about the technologies used in this project:
- [Strands Agents Documentation](https://github.com/aws/strands-agents) - Framework for building AI agents
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) - Serverless compute service
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) - Fully managed service for foundation models

You can also use AWS Serverless Application Repository to deploy ready-to-use apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
