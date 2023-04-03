# Setup
## Create the ECR repository
Create an ECR repo with the same name as the github repo
## Add secrets
 * `GH_TOKEN`
 * `AWS_ACCESS_KEY_ID`
 * `AWS_SECRET_ACCESS_KEY`
 * `AWS_REGION`
## Update the cookiecutter.json file
 Updating this file triggers the cookiecutter template update.  You should
 at the very minimum change the service name (human readable, pretty format)