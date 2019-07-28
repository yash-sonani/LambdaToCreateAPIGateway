import boto3

# This method find existing API-Gateway
def find_rest_api(client,ApiGatewayName):

    response = client.get_rest_apis()

    for items in response['items']:
        if items['name'] == ApiGatewayName:
            return (items['id'])

    return None            

# This method create Rest-API
def create_rest_api(client,data):
    
    RestAPIId = find_rest_api(client, data['APIGW_Name'])
    
    if RestAPIId is None:

        restAPIResponce = client.create_rest_api(
            name = data['APIGW_Name'],
            description = data['APIGW_Des'],
            version = 'V1',
            apiKeySource = data['APIKeySource'],
            endpointConfiguration={
                'types': [
                    data['EndPointConfig']
                ]
            }
        )
    
        RestAPIId = restAPIResponce['id']
        
        print('Rest API Created With ID: ' , RestAPIId)
    
        return RestAPIId
    
    return RestAPIId        
