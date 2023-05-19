import boto3
import argparse
from stackoperator.readerFactory import *
from stackoperator.cfnReader import *
from stackoperator.tfReader import *
from stackoperator.batchOperator import *

def start_cfnstack():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Start all startable resources in CloudFormation stack.')
    parser.add_argument('--stackname', dest='StackName', help='CloudFormation stack name.')
    args = parser.parse_args()

    factory = readerFactory()
    reader = factory.create_reader('cfn',args.StackName)
    ec2_list,rds_list,asg_list = reader.list_stoppable_resources(filterstatus='stopped')

    operator = batchOperator()
    operator.batch_start_resources(ec2_list,rds_list,asg_list)

def stop_cfnstack():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Stop all stopable resources in CloudFormation stack.')
    parser.add_argument('--stackname', dest='StackName', help='CloudFormation stack name.')
    args = parser.parse_args()

    factory = readerFactory()
    reader = factory.create_reader('cfn',args.StackName)
    ec2_list,rds_list,asg_list = reader.list_stoppable_resources()

    operator = batchOperator()
    operator.batch_stop_resources(ec2_list,rds_list,asg_list)

def start_tfstack():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Start all startable resources in Terraform stack.')
    parser.add_argument('--statefile', help='Terraform state file name.', dest='StateFile', default='terraform.tfstate')
    args = parser.parse_args()

    # To get all defaults:
    all_defaults = {}
    for key in vars(args):
        all_defaults[key] = parser.get_default(key)

    factory = readerFactory()
    reader = factory.create_reader('tf',args.StateFile)
    ec2_list,rds_list,asg_list = reader.list_stoppable_resources(filterstatus='stopped')

    operator = batchOperator()
    operator.batch_start_resources(ec2_list,rds_list,asg_list)

def stop_tfstack():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Stop all stoppable resources in Terraform stack.')
    parser.add_argument('--statefile', help='Terraform state file name.', dest='StateFile', default='terraform.tfstate')
    args = parser.parse_args()

    # To get all defaults:
    all_defaults = {}
    for key in vars(args):
        all_defaults[key] = parser.get_default(key)

    factory = readerFactory()
    reader = factory.create_reader('tf',args.StateFile)
    ec2_list,rds_list,asg_list = reader.list_stoppable_resources()

    operator = batchOperator()
    operator.batch_stop_resources(ec2_list,rds_list,asg_list)

def start_resourcegroup():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Start all startable resources in a Resource Group.')
    parser.add_argument('--groupname', help='Resource Group name.', dest='GroupName')
    args = parser.parse_args()

    factory = readerFactory()
    reader = factory.create_reader('rsg',args.GroupName)
    ec2_list,rds_list,asg_list = reader.list_stoppable_resources(filterstatus='stopped')

    operator = batchOperator()
    operator.batch_start_resources(ec2_list,rds_list,asg_list)

def stop_resourcegroup():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Stop all startable resources in a Resource Group.')
    parser.add_argument('--groupname', help='Resource Group name.', dest='GroupName')
    args = parser.parse_args()

    factory = readerFactory()
    reader = factory.create_reader('rsg',args.GroupName)
    ec2_list,rds_list,asg_list = reader.list_stoppable_resources()

    operator = batchOperator()
    operator.batch_stop_resources(ec2_list,rds_list,asg_list)

def tag_cfnstack():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Tag all stoppable resources in CloudFormation stack.')
    parser.add_argument('--stackname', dest='StackName', help='CloudFormation stack name.')
    parser.add_argument('--tags', dest='Tags', help='Tags to apply to resources. Format: key1=value1,key2=value2')
    args = parser.parse_args()

    factory = readerFactory()
    reader = factory.create_reader('cfn',args.StackName)
    ec2_list,rds_list,asg_list = reader.list_stoppable_resources(filterstatus='both')

    operator = batchOperator()
    operator.batch_tag_resources(ec2_list,rds_list,asg_list,parse_tags(args.Tags))

def tag_tfstack():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Tag all startable resources in Terraform stack.')
    parser.add_argument('--statefile', help='Terraform state file name.', dest='StateFile', default='terraform.tfstate')
    parser.add_argument('--tags', dest='Tags', help='Tags to apply to resources. Format: key1=value1,key2=value2')
    args = parser.parse_args()
    factory = readerFactory()
    reader = factory.create_reader('tf',args.StateFile)
    ec2_list,rds_list,asg_list = reader.list_stoppable_resources(filterstatus='both')

    operator = batchOperator()
    operator.batch_tag_resources(ec2_list,rds_list,asg_list,parse_tags(args.Tags))

def tag_resourcegroup():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Tag all stoppable resources in Resource Group.')
    parser.add_argument('--groupname', help='Resource Group name.', dest='GroupName')
    parser.add_argument('--tags', dest='Tags', help='Tags to apply to resources. Format: key1=value1,key2=value2')
    args = parser.parse_args()

    factory = readerFactory()
    reader = factory.create_reader('rsg',args.GroupName)
    ec2_list,rds_list,asg_list = reader.list_stoppable_resources(filterstatus='both')

    operator = batchOperator()
    operator.batch_tag_resources(ec2_list,rds_list,asg_list,parse_tags(args.Tags))

def parse_tags(tag_string):  
    tag_list = tag_string.split(',')  
    tags = []  
  
    for tag in tag_list:  
        key, value = tag.split('=')  
        tags.append({  
            'Key': key.strip(),  
            'Value': value.strip()  
        })  
  
    return tags 
