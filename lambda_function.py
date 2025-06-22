import boto3
import pandas as pd
import io
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_in = 's3-data-entrada-covid-brayner573'
    bucket_out = 's3-data-salida-covid-brayner573'
    key = 'DataCovid_LimpioCLOUD.xlsx'
    output_key = 'data_transformada.json'

    obj = s3.get_object(Bucket=bucket_in, Key=key)
    df = pd.read_excel(io.BytesIO(obj['Body'].read()))

    
    df = df.dropna()  

    data_json = df.to_dict(orient='records')
    json_bytes = json.dumps(data_json).encode('utf-8')

    s3.put_object(Bucket=bucket_out, Key=output_key, Body=json_bytes)

    return {
        'statusCode': 200,
        'body': f"Archivo procesado y guardado como {output_key}"
    }
