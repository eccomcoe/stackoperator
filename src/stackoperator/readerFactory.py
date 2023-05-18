from stackoperator.tfReader import *
from stackoperator.cfnReader import *

class readerFactory:
    @staticmethod
    def create_reader(reader_type,stackname=''):
        if reader_type.lower() == "cloudformation" or reader_type.lower() == "cfn":
            if stackname == '':
                raise ValueError("Stackname not specified")
            return cfnReader(stackname)
        elif reader_type.lower() == "terraform" or reader_type.lower() == "tf":
            return tfReader()
        else:
            raise ValueError("Unknown reader type")