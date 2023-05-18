import boto3

class cfnReader:
    def __init__(self, StackName):
        self.stackname = StackName

    def list_stoppable_resources(self,StackName="",filterstatus='running'):
        # Initialize AWS clients
        cf_client = boto3.client('cloudformation')
        ec2_client = boto3.client('ec2')
        rds_client = boto3.client("rds") 
        asg_client = boto3.client('autoscaling')

        if StackName == "":
            StackName = self.stackname
        ec2_instances = []
        rds_instances = []
        asg_resources = []

        # Get the resources in the specified stack
        resources = cf_client.list_stack_resources(StackName=StackName)

        # Filter resources
        allec2_instances = [
            r['PhysicalResourceId'] for r in resources['StackResourceSummaries'] if r['ResourceType'] == 'AWS::EC2::Instance'
        ]
        for ec2_instanceid in allec2_instances:
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

        allrds_instances = [
            r['PhysicalResourceId'] for r in resources['StackResourceSummaries'] if r['ResourceType'] == 'AWS::RDS::DBInstance'
        ]
        for rds_identifier in allrds_instances:
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

        allasg_resources = [
            r['PhysicalResourceId'] for r in resources['StackResourceSummaries'] if r['ResourceType'] == 'AWS::AutoScaling::AutoScalingGroup'
        ]
        for asg_id in allasg_resources:
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

        nested_stacks = [
            r['PhysicalResourceId'] for r in resources['StackResourceSummaries'] if r['ResourceType'] == 'AWS::CloudFormation::Stack'
        ]

        # Stop resources in the nested stacks
        for nested_stack in nested_stacks:
            print(f"Stopping resources in Nested Stack: {nested_stack}")
            ec2_nested,rds_nested,asg_nested = self.list_stoppable_resources(nested_stack)
            ec2_instances = ec2_instances + ec2_nested
            rds_instances = rds_instances + rds_nested
            asg_resources = asg_resources + asg_nested

        return ec2_instances,rds_instances,asg_resources