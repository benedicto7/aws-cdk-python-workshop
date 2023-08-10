from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    CfnOutput,
)
from .hitcounter import HitCounter

class CdkPythonTestStack(Stack):
    @property
    def hc_endpoint(self):
        return self._hc_endpoint
    
    # @property
    # def hc_viewer_url(self):
    #     return self._hc_viewer_url
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # queue = sqs.Queue(
        #     self, "CdkPythonTestQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "CdkPythonTestTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))

        # Defines an AWS Lambda resource
        hello = _lambda.Function(self,
                                     "HelloHandler",
                                     runtime=_lambda.Runtime.PYTHON_3_7,
                                     code=_lambda.Code.from_asset('lambda'),
                                     handler='hello.handler'
        )

        hello_with_counter = HitCounter(self,
                                        'HelloHitCounter',
                                        downstream=hello
        )

        gateway = apigw.LambdaRestApi(self,
                            'Endpoint',
                            handler=hello_with_counter._handler,
        )

        self._hc_endpoint = CfnOutput(
            self, 'GatewayUrl',
            value=gateway.url
        )

        # self._hc_viewer_url = CfnOutput(
        #     self, 'TableViewerUrl',
        #     value=tv.endpoint
        # )
