import aws_cdk as cdk

from hello_lambda.hello_lambda_stack import HelloLambdaStack


app = cdk.App()
HelloLambdaStack(app, "HelloLambdaStack",)
app.synth()
