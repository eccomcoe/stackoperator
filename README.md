A small utility to help do start, stop and tag actions in an IaC stack for cost optimization purpose.  
Stackoperator now support CloudFormation,Terraform stack,as well Resource Group.  
It's a great idea to use stackoperator with [Instance Scheduler on AWS](https://aws.amazon.com/solutions/implementations/instance-scheduler-on-aws) solution by tagging stoppable resources created by IaC stack.  

## Use cases:
- During the POC testing process of solutions deployed using CloudFormation or Terraform, toggle related resources with one click to save testing costs.
- For solutions deployed using CloudFormation or Terraform, save operation costs by tagging toggleable resources and controlling their runtime using the Instance Scheduler on AWS solution.
- Batch Start,Stop and Tag toggleable resources in a resource group.

## Prerequisites:
Before using stackoperator script, please make sure correct AWS credential in envs, using [aws-vault](https://github.com/99designs/aws-vault) to store and switch AWS credentials is recommend.

## Install
```
pip install stackoperator
```

## Upgrade
```
pip install --upgrade stackoperator
```

## Usage
### Start stopped resources in a given CloudFormation Stack
```
startcfnstack --stackname <CloudFormation_Stack_Name>  
```
### Stop stoppable running resources in a given CloudFormation Stack
```
stopcfnstack --stackname <CloudFormation_Stack_Name>  
```
### Tag stoppable running resources in a given CloudFormation Stack
```
tagcfnstack --tags "Key1=Value1,Key2=Value2" --stackname <CloudFormation_Stack_Name>  
```
### Start stopped resources in Terraform Stack (at current path)
```
starttfstack [--statefile <Terraform_Stack_StateFile>]  
```
### Stop stoppable running resources in Terraform Stack (at current path)
```
stoptfstack [--statefile <Terraform_Stack_StateFile>]  
```
### Tag stoppable running resources in Terraform Stack (at current path)
```
tagtfstack --tags "Key1=Value1,Key2=Value2" [--statefile <Terraform_Stack_StateFile>]  
```
### Start stopped resources in Resrouce Group
```
startresourcegroup --groupname <Resource_Group_Name>   
```
### Stop stoppable running resources in Resource Group
```
startresourcegroup --groupname <Resource_Group_Name>    
```
### Tag stoppable running resources in Resource Group
```
tagresourcegroup --tags "Key1=Value1,Key2=Value2" --groupname <Resource_Group_Name>
```