# aws-sam-etl-cicd

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders:

- functions - Code for the application's Lambda functions to poll data from twitter.
- statemachines - Definition for the state machine that orchestrates the data polling workflow.
- tests - Unit tests for the Lambda functions' application code.
- template.yaml - A template that defines the application's AWS resources.
(we are going to translate this into terraform)

This application creates a data polling workflow which runs on a pre-defined schedule (note that the schedule is disabled by default to avoid incurring charges). 

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
sam-app$ pip install -r tests/requirements.txt --user
# unit test
sam-app$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
sam-app$ AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```
