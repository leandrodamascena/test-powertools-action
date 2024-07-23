#!/usr/bin/env python3

import aws_cdk as cdk

from layer.canary_stack import CanaryStack
from layer.layer_stack import LayerStack

app = cdk.App()

POWERTOOLS_VERSION: str = app.node.try_get_context("version")
PYTHON_VERSION: str = app.node.try_get_context("pythonVersion")
SSM_PARAM_LAYER_ARN: str = "/layers/powertools-layer-v2-arn"
SSM_PARAM_LAYER_ARM64_ARN: str = "/layers/powertools-layer-v2-arm64-arn"

if not POWERTOOLS_VERSION:
    raise ValueError(
        "Please set the version for Powertools for AWS Lambda (Python) by passing the '--context version=<version>' parameter to the CDK "
        "synth step."
    )

p86 = PYTHON_VERSION.replace(".", "")

LayerStack(
    app,
    f"LayerV2Stack-{p86}",
    powertools_version=POWERTOOLS_VERSION,
    python_version=PYTHON_VERSION,
    ssm_parameter_layer_arn=SSM_PARAM_LAYER_ARN,
    ssm_parameter_layer_arm64_arn=SSM_PARAM_LAYER_ARM64_ARN,
)

CanaryStack(
    app,
    "CanaryV2Stack",
    powertools_version=POWERTOOLS_VERSION,
    ssm_paramter_layer_arn=SSM_PARAM_LAYER_ARN,
    ssm_parameter_layer_arm64_arn=SSM_PARAM_LAYER_ARM64_ARN,
)

app.synth()
