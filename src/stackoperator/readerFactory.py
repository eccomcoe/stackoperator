from stackoperator.tfReader import *
from stackoperator.cfnReader import *
from stackoperator.resourcegroupReader import *

class readerFactory:
    @staticmethod
    def create_reader(reader_type,stackname=''):
        if reader_type.lower() == "cloudformation" or reader_type.lower() == "cfn":
            return cfnReader(stackname)
        elif reader_type.lower() == "terraform" or reader_type.lower() == "tf":
            return tfReader()
        elif reader_type.lower() == "resourcegroup" or reader_type.lower() == "rsg":
            return resourcegroupReader(stackname)
        else:
            raise ValueError("Unknown reader type")