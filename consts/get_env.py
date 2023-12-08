import os
import boto3
from dotenv import load_dotenv
load_dotenv()

AWS_PROD_HIERARCHY = "/uwclubs/prod/"

def get_parameter(param_name):
    """
    This function reads a secure parameter from AWS' SSM service.
    The request must be passed a valid parameter name, as well as 
    temporary credentials which can be used to access the parameter.
    The parameter's value is returned.
    """
    # Create the SSM Client
    ssm = boto3.client('ssm',
        region_name='us-east-2'
    )
    param_name = AWS_PROD_HIERARCHY + param_name
    # Get the requested parameter
    response = ssm.get_parameters(
        Names=[
            param_name,
        ],
        WithDecryption=True
    )
    
    # Store the credentials in a variable
    credentials = response['Parameters'][0]['Value']

    return credentials

def get_env(param_name: str):
    var_from_env = os.getenv(param_name)
    if var_from_env is None:
        var_from_aws = get_parameter(param_name)
        return var_from_aws
    else:
        return var_from_env
