from aws_cdk import (
    Stack,
    CfnParameter,
    Tags,
    aws_servicecatalog as servicecatalog,
    aws_iam as iam,
    aws_s3 as s3,
    aws_ecs as ecs,
    aws_ssm as ssm
)
from constructs import Construct
import sys


class ECSCluster(servicecatalog.ProductStack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        # Parameters for the Product Template
        cluster_name = CfnParameter(self, "clusterName", type="String", description="The name of the ECS cluster")
        container_insights_enable = CfnParameter(self, "container_insights", type="String",default="False",allowed_values=["False","True"],description="Enable Container Insights")
        vpc = CfnParameter(self, "vpc", type="AWS::EC2::VPC::Id", description="VPC")

        ecs.Cluster(self,"ECSCluster_template",enable_fargate_capacity_providers=True,cluster_name=cluster_name.value_as_string,container_insights=bool(container_insights_enable.value_as_string),vpc=vpc)
        ## add more features into your ECS cluster following the CDK doc: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ecs/README.html
        Tags.of(self).add("key", "value")


class CdkServiceCatalogECSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        accounts = self.node.try_get_context("shared_accounts_ecs")
        roles = self.node.try_get_context("roles")
        users = self.node.try_get_context("users")
        groups = self.node.try_get_context("groups")

        portfolio = servicecatalog.Portfolio(self, "ECS_Portfolio",
            display_name="ECS_Portfolio",
            provider_name="Platform Team",
            description="ECS Portfolio"
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


        ecs_cluster = servicecatalog.CloudFormationProduct(self, "ECS_Cluster_Product",
            product_name="ECS Cluster",
            owner="Platform Team",
            product_versions=[
                servicecatalog.CloudFormationProductVersion(
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(ECSCluster(self, "ECSClusterTemplate")),
                    product_version_name="v1",                    
                    validate_template = True
                )
            ],
            description = "ECS Cluster provisioning Product",
            support_email = "support@youremail.com",
            support_url = "https://doc.youremail.com/"
        )
       
        ecs_task = servicecatalog.CloudFormationProduct(self, "ECS_Task",
            product_name="ECS Task Definition",
            owner="Platform Team",
           product_versions=[
                servicecatalog.CloudFormationProductVersion(
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_asset("products/ecs/ecs-task.yml"),
                    product_version_name="v1",
                    validate_template = True
                )
            ],
            description = "ECS Task Definition provisioning Product",
            support_email = "support@youremail.com",
            support_url = "https://doc.youremail.com/"
        )

        portfolio.add_product(ecs_cluster)

        # General tags applied to all resources created on this scope (self)
        Tags.of(self).add("key", "value")
