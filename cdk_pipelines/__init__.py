from collections import defaultdict
from urllib.parse import urlparse

from aws_cdk import (
    aws_s3 as s3,
    aws_codepipeline as codepipeline,
    aws_codecommit as codecommit,
    pipelines as pipelines,
    aws_codepipeline_actions as codepipeline_actions,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_iam as iam,
    core
)

from cdk_service_catalog.cdk_service_catalog_ecs_stack import CdkServiceCatalogECSStack

class ECSServiceCatalog(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = CdkServiceCatalogECSStack(self, 'ECS')

class CdkPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_artifact = codepipeline.Artifact()
        assembly_artifact = codepipeline.Artifact()

        hub_region = self.node.try_get_context("region")
        hub_account = self.node.try_get_context("hub_account")

        repo = codecommit.Repository(self, "Repo", repository_name = "service-catalog-repo", description="CDK Code with Service Catalog products")

        pipeline = pipelines.CdkPipeline(
            self,
            'Pipeline',
            cross_account_keys=True,
            cloud_assembly_artifact=assembly_artifact,
            pipeline_name=f'cdk-service-catalog-pipeline',


            source_action=codepipeline_actions.CodeCommitSourceAction(
                action_name="CodeCommit",
                repository=repo,
                output=source_artifact
            ),
            synth_action=pipelines.SimpleSynthAction.standard_npm_synth(
                source_artifact=source_artifact,
                cloud_assembly_artifact=assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                synth_command='cdk synth',        
            )
        )
        pipeline.add_application_stage(
            ECSServiceCatalog(
                self,
                'Hub-Account',
                env={
                    'account': hub_account,
                    'region': hub_region
                }
            )
        )
        # Example to deploy the Stage in another account or region
        # pipeline.add_application_stage(
        #     ECSServiceCatalog(
        #         self,
        #         'Shared_account',
        #         environment="qa",
        #         env={
        #             'account': hub_account,
        #             'region': hub_region
        #         }
        #     )
        # )
        
