from collections import defaultdict
from urllib.parse import urlparse

from aws_cdk import (
    aws_s3 as s3,
    aws_ssm as ssm,
    aws_codepipeline as codepipeline,
    aws_codecommit as codecommit,
    pipelines as pipelines,
    aws_codepipeline_actions as codepipeline_actions,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_iam as iam,
    core as cdk
)

from cdk_service_catalog.cdk_service_catalog_ecs_stack import CdkServiceCatalogECSStack
from cdk_service_catalog.cdk_service_catalog_storage_stack import CdkServiceCatalogStorageStack

class ECSServiceCatalog(cdk.Stage):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = CdkServiceCatalogECSStack(self, 'ECSPortfolio')

class StorageServiceCatalog(cdk.Stage):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = CdkServiceCatalogStorageStack(self, 'StoragePortfolio')

class CdkPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hub_account = self.node.try_get_context("hub_account")
        hub_region = self.node.try_get_context("region")
        repo = codecommit.Repository(self, "Repo", repository_name = "service-catalog-repo", description="CDK Code with Service Catalog products")


        pipeline = pipelines.CodePipeline(self, "Pipeline",
            pipeline_name=f'cdk-service-catalog-pipeline',
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.code_commit(repo,"main"),
                commands=[ "npm install -g aws-cdk && pip install -r requirements.txt", "cdk synth"]
            ))

        wave = pipeline.add_wave("HubAccount")
        wave.add_stage(
            ECSServiceCatalog(
                self,
                'ECS',
                env={
                    'account': hub_account,
                    'region': hub_region
                }
            )
        )
        wave.add_stage(
            StorageServiceCatalog(
                self,
                'Storage',
                env={
                    'account': hub_account,
                    'region': hub_region
                }
            )
        )
       
        # General tags applied to all resources created on this scope (self)
        cdk.Tags.of(self).add("key", "value")