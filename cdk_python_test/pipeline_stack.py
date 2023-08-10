from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,
)
from pipeline_stage import PipelineStage

class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repo called WorkshopRepo
        repo = codecommit.Repository(self,
                                    'WorkshopRepo',
                                    repository_name="WorkshopRepo"
        )

        pipeline = pipelines.CodePipeline(self,
                                        "Pipeline",
                                        synth=pipelines.ShellStep(
                                            "Synth",
                                            input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                                            commands=[
                                                "npm install -g aws-cdk", # install cdk cli on codebuild
                                                "pip install -r requirements.txt" # instruct codebuild to install required packages
                                                "cdk synth",
                                            ]
                                        )
        )

        # deploy = PipelineStage(self, "Deploy")
        # deploy_stage = pipeline.add_stage(deploy)

        deploy = PipelineStack(self, "Deploy")
        deploy_stage = pipeline.add_stage(deploy)

        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestAPIGatewayEndpoint",
                env_from_cfn_outputs={
                    "ENDPOINT_URL": deploy.hc_endpoint
                },
                commands=[
                    "curl -Ssf $ENDPOINT_URL",
                    "curl -Ssf $ENDPOINT_URL/hello",
                    "curl -Ssf $ENDPOINT_URL/test",
                ],
            )
        )
        
        # deploy_stage.add_post(
        #     pipelines.ShellStep(
        #         "TestViewerEndpoint",
        #         env_from_cfn_outputs={
        #             "ENDPOINT_URL": deploy.hc_viewer_url
        #         },
        #         commands=["curl -Ssf $ENDPOINT_URL"],
        #     )
        # )
