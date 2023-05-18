import boto3
import os  
import json 

class tfReader:
    def __init__(self, StateFile='terraform.tfstate'):
        self.statefile = StateFile

    def __get_state_file_path(self,state_filename='terraform.tfstate'):
        current_dir = os.getcwd()
        state_file_path = os.path.join(current_dir, state_filename)
        return state_file_path

    def __read_terraform_state_file(self,file_path):  
        with open(file_path, 'r') as f:  
            terraform_state = json.load(f)  
        return terraform_state
    
    def list_stoppable_resources(self,stackname='terraform.tfstate',filterstatus='running'):
        terraform_state_file = self.__get_state_file_path(stackname)
        terraform_state = self.__read_terraform_state_file(terraform_state_file)
        resources = terraform_state['resources']  
        ec2_instances = []
        rds_instances = []
        asg_resources = []

        ec2_client = boto3.client('ec2')
        rds_client = boto3.client("rds") 
        asg_client = boto3.client('autoscaling')

        for resource in resources:  
            if 'registry.terraform.io/hashicorp/aws' in resource['provider'] and resource['mode'] == 'managed' and resource['type'] == 'aws_instance': 
                ec2_instanceid = resource['instances'][0]['attributes']['id']
                response = ec2_client.describe_instances(InstanceIds=[ec2_instanceid])

                # 获取EC2实例ID和状态
                instance_status = response['Reservations'][0]['Instances'][0]['State']['Name']

                # 根据筛选条件添加实例到列表
                if filterstatus == "both":
                    ec2_instances.append(ec2_instanceid)
                elif filterstatus == "running":
                    if instance_status == "running":
                        ec2_instances.append(ec2_instanceid)
                else:
                    if instance_status == "stopped":
                        ec2_instances.append(ec2_instanceid)

            if 'registry.terraform.io/hashicorp/aws' in resource['provider'] and resource['mode'] == 'managed' and resource['type'] == 'aws_db_instance': 
                rds_identifier = resource['instances'][0]['attributes']['identifier']
                # 获取RDS实例的信息  
                response = rds_client.describe_db_instances(DBInstanceIdentifier=rds_identifier)  
  
                # 检查RDS实例的状态  
                instance_status = response["DBInstances"][0]["DBInstanceStatus"]  
                if filterstatus == "both":
                    rds_instances.append(rds_identifier)
                elif filterstatus == "running":
                    if instance_status == "available":
                        rds_instances.append(rds_identifier) 
                else:
                    if instance_status == "stopped":
                        rds_instances.append(rds_identifier) 
                 
            #if 'registry.terraform.io/hashicorp/aws' in resource['provider'] and resource['mode'] == 'managed' and resource['type'] == 'aws_rds_cluster':  
            #    ec2_instances.append(resource)
            if 'registry.terraform.io/hashicorp/aws' in resource['provider'] and resource['mode'] == 'managed' and resource['type'] == 'aws_autoscaling_group': 
                asg_id = resource['instances'][0]['attributes']['id']
                
                asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_id])
                MinSize = asg_response['AutoScalingGroups'][0]['MinSize']
                DesiredCapacity = asg_response['AutoScalingGroups'][0]['DesiredCapacity']
                if filterstatus == "both":
                    asg_resources.append(asg_id)
                elif filterstatus == "running":
                    if MinSize > 0 and DesiredCapacity > 0:
                        asg_resources.append(asg_id) 
                else:
                    if MinSize == 0 and DesiredCapacity == 0:
                        asg_resources.append(asg_id) 
                
        return ec2_instances,rds_instances,asg_resources    