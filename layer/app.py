#!/usr/bin/env python3

import aws_cdk as cdk

from layer.canary_stack import CanaryStack
from layer.layer_stack import LayerStack

app = cdk.App()

POWERTOOLS_VERSION: str = app.node.try_get_context("version")
PYTHON_VERSION: str = app.node.try_get_context("pythonVersion")
p86 = PYTHON_VERSION.replace(".", "")
SSM_PARAM_LAYER_ARN: str = f"/layers/powertools-layer-v3-x86-arn-{p86}"
SSM_PARAM_LAYER_ARM64_ARN: str = f"/layers/powertools-layer-v3-arm64-arn-{p86}"

if not POWERTOOLS_VERSION:
    raise ValueError(
        "Please set the version for Powertools for AWS Lambda (Python) by passing the '--context version=<version>' parameter to the CDK "
        "synth step."
    )


LayerStack(
    app,
    f"LayerV3Stack-{p86}",
    powertools_version=POWERTOOLS_VERSION,
    python_version=PYTHON_VERSION,
    ssm_parameter_layer_arn=SSM_PARAM_LAYER_ARN,
    ssm_parameter_layer_arm64_arn=SSM_PARAM_LAYER_ARM64_ARN,
)

CanaryStack(
    app,
    f"LayerV3Stack-{p86}",
    powertools_version=POWERTOOLS_VERSION,
    python_version=PYTHON_VERSION,
    ssm_paramter_layer_arn=SSM_PARAM_LAYER_ARN,
    ssm_parameter_layer_arm64_arn=SSM_PARAM_LAYER_ARM64_ARN,
)

app.synth()
