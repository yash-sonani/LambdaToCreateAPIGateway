import sys
import boto3

from Read_File import read_xls,read_api_detail,read_Resource_Method_detail
from RestAPI_Creation import create_rest_api
from Resource_Method_Creation import create_resource_method

def lambda_handler(event, context):
    # TODO implement
    
    
    client = boto3.client('apigateway')
    
    bucketName = 'bucket_name' # Update with your bucket name
    filePath = 'apigw_detail.xls'  # Update with your detials file name
    
    workbook = read_xls(bucketName,filePath)
    
    # Read Rest API Detail
    apiData = read_api_detail(workbook)
    
    print('apiData: ' , apiData)
    
    # Creation of Rest API
    try:
        RestAPIId = create_rest_api(client,apiData)
    except:
        print('Exception in Rest API Creation: ' , sys.exc_info())
    
    # Create Resourse-Method 
    rmData = read_Resource_Method_detail(workbook)
    
    print('rmData: ' , rmData)
    
    # Create Resourse and Method
    Response = create_resource_method(client,RestAPIId,apiData,rmData)
    

    return {
        'body': 'Lambda Works!!!'
    }




