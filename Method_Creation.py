import sys
import boto3

# This method find VPC Link Id
def find_vpc_link_id(client, vpcname):
    response = client.get_vpc_links()
    
    for items in response['items']:
        #print(items)
        if items['name'] == vpcname:
            return items['id']

# This method find MethodType in Given Resource
def find_method(client,RestAPIId,ResourceId,MethodType):

    try:
        response = client.get_method(
            restApiId=RestAPIId,
            resourceId=ResourceId,
            httpMethod=MethodType
        )
        return response['ResponseMetadata']['HTTPStatusCode']
        
    except:
        return None

# This method set-up put method request Parameters

def create_put_method_requestParameter(Headers,Required):
    
    value = False
    requestParameters = {}
    
    if Required == 'Y':
        value = True
    else:
        value = False
    
    for header in Headers:
        key = 'method.request.header.' + header
        requestParameters[key] = value

    #print('put method requestParameters: ' , requestParameters)
    return requestParameters

# This method add Request Path Param in Method Request

def add_request_path_put_method_requestParameters(requestParameters,EndResourceName,Required):
    
    EndResourceName = EndResourceName.replace("{", "").replace("}", "")
    value = False
    
    if Required == 'Y':
        value = True
    else:
        value = False
    
    key = 'method.request.path.' + EndResourceName

    requestParameters[key] = value
    
    return requestParameters


# This method set up put integration request Parameters

def create_put_integration_requestParameters(Headers,Method_Header):
    
    requestParameters = {}
    
    for index, header in enumerate(Headers):
        if header != 'x-api-key':
            key = 'integration.request.header.' + Method_Header[index]
            value = 'method.request.header.' +  header
            requestParameters[key] = value

    return requestParameters
    
# This method add path param in Integration Request

def add_request_path_put_integration_requestParameters(requestParameters,EndResourceName):
    
    EndResourceName = EndResourceName.replace("{", "").replace("}", "")
    
    key = 'integration.request.path.' + EndResourceName
    value = 'method.request.path.' +  EndResourceName
    requestParameters[key] = value
    
    return requestParameters    

# This method create Method in Given Resource

def create_method(client,RestAPIId,ParentResourceId,resource,apiData):

    IsMethodPresent = find_method(client,RestAPIId,ParentResourceId,resource['MethodType'])
    
    if IsMethodPresent is None:
        
        responseArray =  create_main_method(client,RestAPIId,ParentResourceId,resource,apiData)
        print('Method ' , resource['MethodType'] , ' Created: ' , responseArray)
        
        optionResponseArray = create_option_method(client,RestAPIId,ParentResourceId,resource,apiData)
        
    else:
        print('Method ', resource['MethodType'] , ' Already Present')

# This Method create Main Method 

def create_main_method(client,RestAPIId,ResourceId,data,apiData):
    
    # Fetching Values    
    MethodType = data['MethodType']
    URL = data['EndPointURL']
    Connection_Type = apiData['Connection_Type']
    vpcname = apiData['VPC_Name']
    EndResourceName = 'NA'
    length = len(data['SubResourceNameList'])-1
    if length > 0:
        EndResourceName = data['SubResourceNameList'][length]
    
    responseArray = []
    
    ConnectionId = ''
    
    if Connection_Type == 'VPC_LINK':
        ConnectionId = find_vpc_link_id(client,vpcname)
        print('ConnectionId: ' , ConnectionId)
        
    if EndResourceName.find('{') == 0 and EndResourceName.find('}') != 0:
            PathParam = 'Y'        
    
    put_method_requestParameters = create_put_method_requestParameter(apiData['Headers'],apiData['Header_Required'])
    
    
    if PathParam == 'Y':
        put_method_requestParameters = add_request_path_put_method_requestParameters(put_method_requestParameters,EndResourceName,apiData['Header_Required'])
    
    
    # This will create method
    Method_Response = client.put_method(
        restApiId = RestAPIId,
        resourceId = ResourceId,
        httpMethod = MethodType,
        apiKeyRequired = False,
        authorizationType = 'none',
        requestParameters = put_method_requestParameters
    )
    
    responseArray.append(Method_Response['ResponseMetadata']['HTTPStatusCode'])

    #This will create Method Integration
    
    put_integration_requestParameters = create_put_integration_requestParameters(apiData['Headers'],apiData['Method_Header'])

    if PathParam == 'Y':
        put_integration_requestParameters = add_request_path_put_integration_requestParameters(put_integration_requestParameters,EndResourceName)
    


    Method_Integration_Response = client.put_integration(
        restApiId = RestAPIId,
        resourceId = ResourceId,
        httpMethod = MethodType,
        type='HTTP',
        integrationHttpMethod = MethodType,
        uri = URL,
        connectionType=Connection_Type,
        connectionId= ConnectionId,
        requestParameters=put_integration_requestParameters,
        passthroughBehavior='WHEN_NO_MATCH',
    )

    responseArray.append(Method_Integration_Response['ResponseMetadata']['HTTPStatusCode'])

    # This will create Method Response
    
    Method_Res_Response = client.put_method_response(
        restApiId = RestAPIId,
        resourceId = ResourceId,
        httpMethod = MethodType,
        statusCode = '200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin' : True
        },
        responseModels={
            'application/json' : 'Empty'
        }
    )

    responseArray.append(Method_Res_Response['ResponseMetadata']['HTTPStatusCode'])

    # This will Add Method Integration Response

    Method_Integration_Res_Response = client.put_integration_response(
        restApiId = RestAPIId,
        resourceId = ResourceId,
        httpMethod = MethodType,
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin' : "'*'"
        }
    )

    responseArray.append(Method_Integration_Res_Response['ResponseMetadata']['HTTPStatusCode'])

    return responseArray

# This Method create Option Method for CORS
    
def create_option_method(client,RestAPIId,ResourceId,data,apiData):
    
    responseArray = []
    
    MethodType = data['MethodType']
    headers = ''
    
    for items in apiData['Headers']:
        headers = headers + ',' + items
    
    #print('Headers: ' , headers)
    
    # This will create method

    Method_Response = client.put_method(
        restApiId = RestAPIId,
        resourceId = ResourceId,
        httpMethod = 'OPTIONS',
        authorizationType = 'none'
    )

    
    responseArray.append(Method_Response['ResponseMetadata']['HTTPStatusCode'])

	#This will create Method Integration

    Method_Integration_Response = client.put_integration(
        restApiId = RestAPIId,
        resourceId = ResourceId,
        httpMethod = 'OPTIONS',
        type='MOCK',
        passthroughBehavior='WHEN_NO_MATCH',
        requestTemplates={
        'application/json': '{"statusCode": 200}'
        }
    )

    responseArray.append(Method_Integration_Response['ResponseMetadata']['HTTPStatusCode'])

    Method_Res_Response = client.put_method_response(
        restApiId = RestAPIId,
        resourceId = ResourceId,
        httpMethod = 'OPTIONS',
        statusCode = '200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin' : True,
            'method.response.header.Access-Control-Allow-Headers' : True,
            'method.response.header.Access-Control-Allow-Methods' : True
        },
        responseModels={
            'application/json' : 'Empty'
        }
    )

    responseArray.append(Method_Res_Response['ResponseMetadata']['HTTPStatusCode'])

    # This will Add Method Integration Response
    Method_Integration_Res_Response = client.put_integration_response(
        restApiId = RestAPIId,
        resourceId = ResourceId,
        httpMethod = 'OPTIONS',
        statusCode = '200',
        responseParameters={
            "method.response.header.Access-Control-Allow-Origin" : "'*'",
            "method.response.header.Access-Control-Allow-Headers" : "'Content-Type,X-Amz-Date,X-Api-Key,X-Amz-Security-Token%s'" % headers,
            "method.response.header.Access-Control-Allow-Methods" : "'%s,OPTIONS'" % MethodType
        }
    )

    responseArray.append(Method_Integration_Res_Response['ResponseMetadata']['HTTPStatusCode'])

    return responseArray
