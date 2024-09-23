import json
import response
import boto3        #used to invoke foundation models
import botocore.config
from datetime import datetime

def blog_generate_using_bedrock(blogtopic:str)->str:

    # Function to generate a blog

    prompt = f"""<s>[INST]Human: Write a 200 word blog on the topic {blogtopic}
    Assistant: [/INST]
    """

    body = {
        "prompt": prompt,
        "max_gen_len": 512,
        "temperature": 0.5,
        "top_p": 0.9
    }

    try:
        bedrock = boto3.client("bedrock-runtime", region_name="us-west-2", config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))
        # Call to foundation Model
        response = bedrock.invoke_model(body=json.dumps(body), modelId="meta.llama3-8b-instruct-v1:0")

        response_content = response.get('body').read()
        response_data = json.loads(response_content)

        print(response_data)
        blog_details = response_data['generation']

        return blog_details
    
    except Exception as e:
        print(f"Error generating the blog: {e}")
        # All prints are logged in AWS CloudWatch
        return ""


def save_blog_s3(s3_key, s3_bucket, generated_blog):
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = generated_blog)
        print("Blog saved to the S3 Bucket")

    except Exception as e:
        print("Error in saving the blog to the S3 Bucket")



def lambda_handler(event, context):
    event = json.loads(event['body'])
    blogtopic = event['blog_topic']

    generated_blog = blog_generate_using_bedrock(blogtopic=blogtopic)

    if(generated_blog):
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = 'aws_bedrock_project1'
        save_blog_s3(s3_key, s3_bucket, generated_blog)
    else:
        print("A blog was failed to be generated")

    
    return{
        'statusCode': 200,
        'body': json.dumps('Blog Generation successful')
    }