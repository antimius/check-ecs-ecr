## Audience

You use AWS ECS and ECR to store container images. Lifecycle rules in ECR might have deleted images that are still being used by running tasks. This tool will tell you if you are missing images in your container registry that will cause problems when ECS container instances are upgraded or if containers need to be replaced.

## Overview

For all ECS clusters in a given AWS account, the running tasks are checked. If a task references an ECR image, the ECR registry will be checked if the image is still available. Broken images are listed in a table format. By default the 'us-east-1' region is used. Custom profiles can be used for ECS and separately for ECR.

## Usage

### Command Line

First, you'll need to install the dependencies in `requirements.txt`:

    pip install -r requirements.txt

Or, when using pipenv:

    pipenv install

Then, run the `ecr-check.py` script:

    python ecr-check.py

You can also pass a custom AWS profile name, or region:

    python ecr-check.py \
        --profile personal \
        --region us-east-1 \

If your ECR repository is in a different account:

    python ecr-check.py \
        --profile personal \
        --region us-east-1 \
        --ecr_profile ecr

## Credits

Dylan Sather (https://github.com/dylburger) for the format I used for creating this tool.
