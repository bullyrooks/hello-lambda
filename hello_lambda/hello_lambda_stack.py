import os

from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_certificatemanager as acm,
)
from aws_cdk.aws_apigateway import (
    ApiKey,
    UsagePlan,
    ThrottleSettings, SecurityPolicy, EndpointType)
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
        hello_lambda_domain_name = "helloworld-lambda.bullyrooks.com"
        # Create a certificate for the domain name
        hello_lambda_certificate = acm.Certificate.from_certificate_arn(
            self, "hello-lambda_certificate", certificate_arn="arn:aws:acm:us-west-2:108452827623:certificate/b9f3f882-162d-4a51-aaf8-07418f33bac6")

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
                                                    proxy=False,
                                                    api_key_source_type=apigateway.ApiKeySourceType.HEADER
                                                    )

        hello_lambda_api.add_domain_name(
            id="helloworld-lambda-domain",
            domain_name=hello_lambda_domain_name,
            certificate=hello_lambda_certificate,
            security_policy=SecurityPolicy.TLS_1_2,
            endpoint_type=EndpointType.REGIONAL,
        )

        hello_lambda_api.root.add_method("GET", api_key_required=True)

        # Create an API key
        app_integration_key = ApiKey(self, "App Integration Key", api_key_name="app-integration-key", enabled=True)

        # Create a usage plan
        development_usage_plan = UsagePlan(self,
                                           "App Integration Plan",
                                           throttle=ThrottleSettings(
                                               rate_limit=10,  # requests per second
                                               burst_limit=2  # maximum number of requests in a burst
                                           ),
                                           quota=apigateway.QuotaSettings(
                                               limit=200,  # number of requests
                                               period=apigateway.Period.DAY  # time period
                                           )
                                           )

        # Associate the API key with the usage plan
        development_usage_plan.add_api_key(app_integration_key)
        # Associate the API stage with the usage plan
        development_usage_plan.add_api_stage(
            api=hello_lambda_api,
            stage=hello_lambda_api.deployment_stage
        )
