import boto3
import os

def download_pic(pic_name, bucket_name, des_path):
    """
    Function to download a pic from an S3 bucket
    """
    s3 = boto3.client(
        's3', 
        aws_access_key_id=os.getenv('aws_access_key_id'),
        aws_secret_access_key=os.getenv('aws_secret_access_key'), 
        aws_session_token=os.getenv('aws_session_token')
    )
    
    # Create destination directory if it doesn't exist
    os.makedirs(des_path, exist_ok=True)
    
    local_file_path = os.path.join(des_path, pic_name)

    try:
        s3.download_file(bucket_name, pic_name, local_file_path)
        print(f"Successfully downloaded {pic_name} to {local_file_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")

