# CI/CD for Service Catalog products using AWS CodeCommit, AWS CodePipeline, AWS CodeBuild with CDK

The purpose of this repository is to demo how can we analyze and securize our Terraform code using a CI/CD Pipeline with a fully AWS services managed.

**Requirements**

- CDK installed: Getting started with the AWS CDK (Ensure the minimal version 1.103.0 to make it works)
- AWS Account
- IAM User or IAM role with permissions to create AWS Resources.
- Git installed: Git installation
- Clone this repo! : git clone https://github.com/aws-samples/aws-cdk-tfsec
- Python CDK required libraries: (install with pip install -r requirements.txt)

**Pre-Requisites**
- Add the value of the hub account to the [cdk.json](cdk.json) hub_account

- Create an SSM parameter string list with the accounts to share for your different Portfolios. Add this value to the [cdk.json](cdk.json) value. For example: /service-catalog/shared-accounts-ecs would be for shared_accounts_ecs


- Modify the [cdk.json](cdk.json) for the pipeline_account id and region to especify where in which environment you want to deploy this demo.

## Architecture
![service-catalog-architecture](images/cicd_service_catalog.png)

## Provisioning the infrastructure

Clone the repo in your local machine. Then, bootstrap and deploy the CDK stack following the next steps

```
git clone https://github.com/aws-samples/cdk-service-catalog-pipeline
cd aws-cdk-service-catalog
pip install -r requirements.txt
cdk bootstrap aws://account_id/eu-west-1
cdk deploy
```

The infrastructure creation takes around 3-5 minutes due the AWS CodePipelines and referenced repository creation. Once the CDK has deployed the infrastructure, clone the new AWS CodeCommit repos that have already been created and push this code into the repo. You can get the repository URL to push the code from the outputs of the stack that we just created. Connect(https://docs.aws.amazon com/codecommit/latest/userguide/how-to-connect.html), commit, and push code to this repository as described here:

```
cd ..
git clone https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/service-catalog-repo
cd service-catalog-repo
git checkout -b main
cp -aR ../cdk-service-catalog-pipeline/* .
git add .
git commit -am "First commit"
git push --set-upstream origin main
```



![cicd_pipeline](images/cicd_pipeline.png)

## Adding a new Portfolio to the Pipeline

To add a new Portfolio to the Pipeline, we recommend creating a new class under [cdk_service_catalog](cdk_service_catalog) similar to [cdk_service_catalog_ecs_stack.py](cdk_service_catalog/cdk_service_catalog_ecs_stack.py). Once the new class is created with the products that we want to associate, we instantiate the new class inside [cdk_pipelines.py](cdk_pipelines/cdk_pipelines.py) and add it inside the wave in the stage. 
There are two ways to create portfolio products. One, like the [ECS example](cdk_service_catalog/cdk_service_catalog_ecs_stack.py) creating a Cloudformation template and the second one, the [Storage example](cdk_service_catalog/cdk_service_catalog_storage_stack.py) creating its own CDK stack that will be transformed into a template for the portfolio product.

## Clean up

After completing your demo, delete your stack using the CDK cli:
```
cdk destroy --all
```

## Conclusion

This code demonstrated how can we accelerate our Service Catalog deployments by building a CI/CD pipeline using self-managed services on AWS and CDK Pipelines

## Warning

Running this demo may result in charges to your AWS account.
Provisioning the supplied Products through ServiceCatalog will create AWS Services which will be billed to your account.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.


