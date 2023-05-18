A small utility to help do start, stop and tag actions in an IaC stack for cost optimization purpose.
Stackoperator now support CloudFormation and Terraform stack.
It's a great idea to use stackoperator with [Instance Scheduler on AWS](https://aws.amazon.com/solutions/implementations/instance-scheduler-on-aws) solution by tagging stoppable resources created by IaC stack.

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
startcfnstack --stackname <CloudFormation_Stack_Name>
stopcfnstack --stackname <CloudFormation_Stack_Name>
tagcfnstack --stackname <CloudFormation_Stack_Name>
starttfstack [--statefile <Terraform_Stack_StateFile>]
stoptfstack [--statefile <Terraform_Stack_StateFile>]
tagtfstack [--statefile <Terraform_Stack_StateFile>]