import sys
import boto3

from Resource_Creation import create_resource,find_resource_id
from Method_Creation import create_method

def create_resource_method(client,RestAPIId,apiData,rmData):
    
    # Traverse through each entry of rmData 
    
    RootId = find_resource_id(client,RestAPIId,'/','/')
    print('RootId: ' , RootId)
    
    for item in rmData:
        
        RootResourceId = create_resource(client,RestAPIId,RootId,item['RootResourceName'])
        
        print('RootResourceName ', item['RootResourceName'] , '  RootResourceId: ', RootResourceId)
        
        ParentResourceId = RootResourceId
        
        # Traverse through Sub resources
        
        for resource in item['SubResourceNameList']:
            
            SubResourceId = create_resource(client,RestAPIId,ParentResourceId,resource)
            
            ParentResourceId = SubResourceId
            
        # Create Method and Enable CORS
        
        Response = create_method(client,RestAPIId,ParentResourceId,item,apiData)
