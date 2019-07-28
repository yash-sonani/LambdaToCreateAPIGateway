import sys
import boto3

def find_resource_id(client,RestAPIId,ParentId,ResourceName):
        
    rootResource = client.get_resources(
        restApiId = RestAPIId,
	    limit = 500
    )
    
    if ResourceName == '/':
        for res in rootResource['items'] :
            if res['path'] == '/' :
                    return res['id']

    else:
        for res in rootResource['items']:
            if res['path'] != '/' :
                if res['pathPart'] == ResourceName and res['parentId'] == ParentId:
                    return res['id']
        
    return None
    
 

def create_resource(client,RestAPIId,ParentId,ResourceName):
    
    ResourceId = find_resource_id(client,RestAPIId,ParentId,ResourceName)
    
    if ResourceId is None:
        ResourceResponse = client.create_resource(
            restApiId = RestAPIId,
            parentId = ParentId,
            pathPart= ResourceName
        )
        
        ResourceId = ResourceResponse['id']
        
        print('Root Resource ' , ResourceName , ' Created with ID: ', ResourceId)
        
    return ResourceId
