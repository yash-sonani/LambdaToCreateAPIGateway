import boto3
import xlrd
from xlrd.book import open_workbook_xls


def read_xls(bucketName,filePath):
    
    # Read File From S3 Bucket
    s3Client = boto3.client('s3')
    data = s3Client.get_object(Bucket=bucketName, Key=filePath)

    content = data['Body'].read()

    # Read xls File for API-Gateway Detail
    workbook = open_workbook_xls(file_contents=content)
    
    return workbook

def read_api_detail(workbook):
    
    data = {}
    
    sheet1 = workbook.sheet_by_index(0)
    
    data['APIGW_Name'] = sheet1.cell_value(0,1).strip()
    data['APIGW_Des'] = sheet1.cell_value(1,1).strip()
    data['Connection_Type'] = sheet1.cell_value(2,1).strip()
    data['VPC_Name'] = sheet1.cell_value(3,1).strip()
    data['Stage_Name'] = sheet1.cell_value(4,1).strip()
    data['Deployment_Name'] = sheet1.cell_value(5,1).strip()
    data['Header_Required'] = sheet1.cell_value(8,1).strip()
    data['EndPointConfig'] = sheet1.cell_value(10,1).strip()
    data['APIKeySource'] = sheet1.cell_value(11,1).strip()
    
    ResponseList = []
    index = 1
    while index < sheet1.ncols :
        ResponseList.append(sheet1.cell_value(9,index).strip())
        index = index + 1
    
    data['GWResponse'] = ResponseList        
    
    HeaderList = []
    index = 1
    while index < sheet1.ncols :
        HeaderList.append(sheet1.cell_value(6,index).strip())
        index = index + 1
    
    data['Headers'] = HeaderList        
    
    MethodHeaderList = []
    index = 1
    while index < sheet1.ncols :
        try:
            MethodHeaderList.append(sheet1.cell_value(7,index).strip())
            index = index + 1
        except:
            print('')
            
    data['Method_Header'] = MethodHeaderList        
    
    #print(data)
                
    return data
    
    
def read_Resource_Method_detail(workbook):
    
    data = []
    sheet2 = workbook.sheet_by_index(1)
    
    TotalRows = sheet2.nrows
    
    index = 1
    
    while index < TotalRows:
        
        row = {}
        
        try:
            row['RootResourceName'] = sheet2.cell_value(index,0)
            
            if len(row['RootResourceName']) < 1 :
                row['RootResourceName'] = '/'
            
        except:
            row['RootResourceName'] = '/'
        

        row['SubResourceNameList'] = sheet2.cell_value(index,1).split('/')
        row['MethodType'] = sheet2.cell_value(index,2)
        row['EndPointURL'] = sheet2.cell_value(index,3)
          
        data.append(row)
        
        index = index + 1
    
    return data
