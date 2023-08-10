#!/usr/bin/env python3

import aws_cdk as cdk
from cdk_python_test.pipeline_stack import PipelineStack
from cdk_python_test.cdk_python_test_stack import CdkPythonTestStack

app = cdk.App()
CdkPythonTestStack(app, "cdk-python-test")

app.synth()
