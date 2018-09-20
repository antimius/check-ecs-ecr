import boto3
import ecr_factory.aws_helpers

class ECSCheckECRClient():
    def __init__(self, profile='default', ecr_profile='default', region='us-east-1'):
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.ecr_session = boto3.Session(profile_name=ecr_profile, region_name=region)
        self.ecs_client = self.session.client('ecs')
        self.ecr_client = self.ecr_session.client('ecr')
        self.region = region

    def get_clusters(self):
        """ Return a list of all ECS clusters in the region
        """
        return self.ecs_client.list_clusters()['clusterArns']

    def get_task_list(self, cluster):
        """ Returns a list of all running ECS task ARNs
        """
        task_paginator = self.ecs_client.get_paginator('list_tasks')
        task_page_iterator = task_paginator.paginate(cluster=cluster)
        return task_page_iterator

    def get_tasks(self, cluster, tasks):
        """ Returns a description of a list of task ARNs in a cluster
        """
        task_descriptions = self.ecs_client.describe_tasks(cluster=cluster,
            tasks=tasks)
        return task_descriptions['tasks']

    def get_images(self, cluster):
        """ Returns a list of image dicts contained in the task definition for a list of tasks
            format: { task: task definition name, image: registry/repository:tag }
        """
        images = []
        for task_page in self.get_task_list(cluster):
            for task in self.get_tasks(cluster, task_page['taskArns']):
                task_definition = self.ecs_client.describe_task_definition(
                    taskDefinition=task['taskDefinitionArn']
                )
                for container_definition in task_definition['taskDefinition']['containerDefinitions']:
                    images.append({'task': task['taskDefinitionArn'].split('/')[1],
                        'image': container_definition['image']})
        return images

    def is_ecr(self, image):
        """ Returns true if an image is stored in ECR
        """
        return "dkr.ecr."+self.region+".amazonaws.com/" in image

    def check_ecr(self, repository, tag):
        """ Returns true if an image and tag is available in ECR
        """
        r = self.ecr_client.batch_get_image(repositoryName=repository,
            imageIds=[{'imageTag': tag}])
        return len(r['images']) > 0

    def check_tasks(self):
        """ Check all tasks that are in state RUNNING or PENDING for ECR tasks
        """
        broken_tasks = []
        for c in self.get_clusters():
            for image in self.get_images(c):
                if(self.is_ecr(image['image'])):
                    (repository, tag) = image['image'].split('/', 1)[1].split(':')
                    if(not self.check_ecr(repository, tag)):
                        broken_tasks.append(image)
        return broken_tasks
