from aws_cdk import (
    Stack,
    CfnParameter,
    Tags,
    aws_servicecatalog as servicecatalog,
    aws_iam as iam,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_efs as efs
)
from constructs import Construct
import sys

class S3(servicecatalog.ProductStack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        bucket_name = CfnParameter(self, "bucketName", type="String", description="The name of the S3 Bucket")
        versioned_enable = CfnParameter(self, "versionedEnable", type="String",default="False",allowed_values=["False","True"],description="Whether this bucket should have versioning turned on or not")

        s3.Bucket(self,"S3Bucket_template",bucket_name=bucket_name.value_as_string,versioned=bool(versioned_enable.value_as_string))
        
        # add more features into your S3 Bucket following the CDK doc: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/README.html
        Tags.of(self).add("key", "value")

class CdkServiceCatalogStorageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        accounts = self.node.try_get_context("shared_accounts_storage")
        roles = self.node.try_get_context("roles")
        users = self.node.try_get_context("users")
        groups = self.node.try_get_context("groups")

        portfolio = servicecatalog.Portfolio(self, "Storage_Portfolio",
            display_name="Storage_Portfolio",
            provider_name="Platform Team",
            description="Storage Portfolio"
        )

        #Provision portfolio to shared accounts.
        for acc in accounts:
            portfolio.share_with_account(acc)
        
        
        #Permissions
        for r in roles:
            role=iam.Role.from_role_arn(self,r,role_arn=r)
            portfolio.give_access_to_role(role)

        for g in groups:
            group=iam.Group.from_group_arn(self,g,group_arn=g)
            portfolio.give_access_to_group(group)

        for u in users:
            user=iam.User.from_user_arn(self,u,user_arn=u)
            portfolio.give_access_to_user(user)


        s3_bucket = servicecatalog.CloudFormationProduct(self, "S3_Bucket_Product",
            product_name="S3 Bucket",
            owner="Platform Team",
            product_versions=[
                servicecatalog.CloudFormationProductVersion(
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(S3(self, "S3Template")),
                    product_version_name="v1",                    
                    validate_template = True
                )
            ],
            description = "S3 Bucket Product",
            support_email = "support@youremail.com",
            support_url = "https://doc.youremail.com/"
        )
       
        portfolio.add_product(s3_bucket)

        # General tags applied to all resources created on this scope (self)
        Tags.of(self).add("key", "value")
