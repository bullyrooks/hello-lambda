import os

from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway)
from aws_cdk import aws_ssm as ssm
from aws_cdk.aws_apigateway import (
    ApiKey,
    UsagePlan,
    RestApi,
    ThrottleSettings,
    LambdaIntegration)
from aws_cdk.aws_ecr import Repository
from constructs import Construct


class HelloLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        image_tag = os.getenv("IMAGE_TAG", "latest")
        hello_lambda_ecr_image = _lambda.DockerImageCode.from_ecr(
            repository=Repository.from_repository_name(self,
                                                       "hello-lambda-repository",
                                                       "hello-lambda"),
            tag_or_digest=image_tag
        )
        hello_lambda_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="hello-lambda-lambda",
            # Function name on AWS
            function_name="hello-lambda",
            # Use aws_cdk.aws_lambda.DockerImageCode.from_image_asset to build
            # a docker image on deployment
            code=hello_lambda_ecr_image,
        )

        hello_lambda_api = apigateway.LambdaRestApi(self, "hello-lambda-api",
                                                        rest_api_name="Hello Lambda",
                                                        handler=hello_lambda_lambda,
                                                        proxy=False)

        hello_lambda_api.root.add_method("GET")
