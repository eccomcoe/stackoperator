import boto3

class resourcegroupReader:
    def __init__(self, GroupName):
        if GroupName == '':
            raise ValueError("GroupName not specified")
        self.groupname = GroupName

    def list_stoppable_resources(self,GroupName="",filterstatus='running'):
        # Initialize AWS clients
        cf_client = boto3.client('cloudformation')
        ec2_client = boto3.client('ec2')
        rds_client = boto3.client("rds") 
        asg_client = boto3.client('autoscaling')

        if GroupName == "":
            GroupName = self.groupname

        # 获取Resource Group中的资源  
        resource_groups_client = boto3.client("resource-groups")  
        response = resource_groups_client.list_group_resources(GroupName=GroupName)  
        
        ec2_instances = []
        rds_instances = []
        asg_resources = []
        
        # 遍历资源并将它们添加到相应的列表中  
        for resource in response["Resources"]:  
            resource_type = resource["Identifier"]["ResourceType"]  
            resource_arn = resource["Identifier"]["ResourceArn"]
        
            if resource_type == "AWS::EC2::Instance":  
                ec2_instanceid = resource_arn.split(":")[-1].split("/")[-1]  
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

            elif resource_type == "AWS::RDS::DBInstance":  
                rds_identifier = resource_arn.split(":")[-1].split("/")[-1]  
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

            elif resource_type == "AWS::AutoScaling::AutoScalingGroup":  
                asg_id = resource_arn.split(":")[-1].split("/")[-1]  
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