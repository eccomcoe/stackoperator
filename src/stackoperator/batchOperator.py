import boto3
import argparse
from stackoperator import readerFactory

class batchOperator:
    def __get_current_partition(self):  
        sts = boto3.client('sts')  
        identity = sts.get_caller_identity()  
        arn = identity['Arn']  
        partition = arn.split(":")[1]  
        return partition  

    def batch_stop_resources(self,ec2,rds,asg):
        ec2_client = boto3.client('ec2')
        rds_client = boto3.client('rds')
        asg_client = boto3.client('autoscaling')

        # Stop EC2 instances
        if ec2:
            for instance_id in ec2:
                print(f"Stopping EC2 Instance: {instance_id}")
                ec2_client.stop_instances(InstanceIds=[instance_id])

        # Stop RDS instances
        if rds:
            for rds_instance in rds:
                print(f"Stopping RDS Instance: {rds_instance}")
                rds_client.stop_db_instance(DBInstanceIdentifier=rds_instance)

        # Update Auto Scaling Groups
        if asg:
            for asg_name in asg:
                print(f"Updating Auto Scaling Group: {asg_name}")
                # Get the original min size and desired capacity from the ASG
                asg_details = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])['AutoScalingGroups'][0]
                original_min_size = asg_details['MinSize']
                original_desired_capacity = asg_details['DesiredCapacity']

                asg_client.create_or_update_tags(
                    Tags=[
                        {
                            'Key': 'auto:MinSize',
                            'PropagateAtLaunch': False,
                            'ResourceId': asg_name,
                            'ResourceType': 'auto-scaling-group',
                            'Value': str(original_min_size),
                        },
                        {
                            'Key': 'auto:DesiredCapacity',
                            'PropagateAtLaunch': False,
                            'ResourceId': asg_name,
                            'ResourceType': 'auto-scaling-group',
                            'Value': str(original_desired_capacity),
                        },

                    ]
                )
                asg_client.update_auto_scaling_group(AutoScalingGroupName=asg_name, MinSize=0, DesiredCapacity=0)

        print("All stoppable resources within the CloudFormation stack have been stopped.")

    def batch_start_resources(self,ec2,rds,asg):
        ec2_client = boto3.client('ec2')
        rds_client = boto3.client('rds')
        asg_client = boto3.client('autoscaling')

        # Start EC2 instances
        if ec2:
            for instance_id in ec2:
                print(f"Starting EC2 Instance: {instance_id}")
                ec2_client.start_instances(InstanceIds=[instance_id])

        # Start RDS instances
        if rds:
            for rds_instance in rds:
                print(f"Starting RDS Instance: {rds_instance}")
                rds_client.start_db_instance(DBInstanceIdentifier=rds_instance)

        # Update Auto Scaling Groups
        if asg:
            asgs = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=asg)
            for asg_item in asgs['AutoScalingGroups']:
                # Get the original min size and desired capacity from the ASG
                asg_tags = asg_item['Tags']
                for tag in asg_tags:
                    if tag['Key'] == 'auto:MinSize':
                        original_min_size = tag['Value']
                    if tag['Key'] == 'auto:DesiredCapacity':
                        original_desired_capacity = tag['Value']
                print(f"Updating Auto Scaling Group: {asg_item['AutoScalingGroupName']} ({original_min_size}, {original_desired_capacity})")
                asg_client.update_auto_scaling_group(
                    AutoScalingGroupName=asg_item['AutoScalingGroupName'],
                    MinSize=int(original_min_size),
                    DesiredCapacity=int(original_desired_capacity)
                )

        print("All startable resources within the CloudFormation stack have been started.")

    def batch_tag_resources(self,ec2,rds,asg,tags=''):
        if tags == '':
            raise ValueError("Tags not specified")
        ec2_client = boto3.client('ec2')
        rds_client = boto3.client('rds')
        
        # Add tags to EC2 instances
        if ec2:
            for instance_id in ec2:
                print(f"Adding tags to EC2 Instance: {instance_id}")
                ec2_client.create_tags(Resources=[instance_id], Tags=tags)

        # Add tags to RDS instances
        if rds:
            for rds_instance in rds:
                print(f"Adding tags to RDS Instance: {rds_instance}")
                rds_client.add_tags_to_resource(ResourceName=f"arn:{self.__get_current_partition()}:rds:{boto3.Session().region_name}:{boto3.client('sts').get_caller_identity()['Account']}:db:{rds_instance}", Tags=tags)

        print("Tags have been added to all stoppable resources within the CloudFormation stack.")
