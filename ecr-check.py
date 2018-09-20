import argparse
import time
from terminaltables import DoubleTable
from termcolor import colored
from ecr_factory.ECR import ECSCheckECRClient

WAIT_TIME = 10

def table_broken_images(broken_images):
    table_data = [list(map(lambda x : colored(x, attrs=['bold']), ["Status", "Task definition", "Image"]))]
    for b in broken_images:
        table_data.append([colored('NOT FOUND', 'red'), b['task'], b['image']])
    table_instance = DoubleTable(table_data)
    return table_instance.table

def configure_argument_parser():
    """ Configures options for our argument parser,
        returns parsed arguments
    """
    default_profile = 'default'
    default_region = 'us-east-1'

    parser = argparse.ArgumentParser()

    # Help strings from ACM.Client Boto 3 docs
    parser.add_argument(
        '--profile',
        default=default_profile,
        help="The name tied to your boto profile (default: '%s')" %
        (default_profile),
    )

    parser.add_argument(
        '--ecr_profile',
        default=default_profile,
        help="The name tied to your boto profile (to use for ECR). Use if your ECR repo is in another account (default: '%s')" %
        (default_profile),
    )

    parser.add_argument(
        '--region',
        default=default_region,
        help=
        "The region in which you want to create your certificate (default: '%s')"
        % (default_region),
    )

    return parser.parse_args()


args = configure_argument_parser()

ecr_client = ECSCheckECRClient(args.profile, args.ecr_profile, args.region)

broken = ecr_client.check_tasks()
print(table_broken_images(broken))