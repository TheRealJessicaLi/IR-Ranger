#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from pymongo import MongoClient

#def lambda_handler(event, context):
if __name__ == "__main__":

    # connect to bucket on s3
    client=boto3.client('rekognition')
    s3 = boto3.resource('s3')
    str_bucket = 'newdatadaddy'
    str_old_bucket = 'archivedaddy'
    bucket = s3.Bucket(str_bucket)

    # connect to mongodb on ec2
    client_db = MongoClient('mongodb://root:EA9jXzCpOnOP@ec2-18-191-182-197.us-east-2.compute.amazonaws.com:27017')
    db=client_db['animals']
    db['animals'].delete_many({})
    db['urls'].delete_many({})
    print(db.list_collection_names())

    url_col = db['urls']

    # iterate through the one photo in the bucket
    for obj in bucket.objects.all():
        filename = obj.key
        url_col.insert_one({'filename':filename,'random':0})
                
        # do object analysis
        response = client.detect_labels(Image={'S3Object':{'Bucket':str_bucket,'Name':filename}})
        dict_count = {}
        
        # look at example
        for label in response['Labels']:

            # case person
            if label['Name'] == 'Person':
                instance_count = 0
                for instance in label['Instances']:
                    instance_count += 1
                if instance_count > 0:
                    dict_count[label['Name']] = instance_count
                continue

            # case animal
            list_parent = label['Parents']
            # iterate through parent labels to check for 'Animal'
            for parent in list_parent:
                if 'Animal' == parent['Name']:
                    # if it's an animal, count the number of instances of it
                    instance_count = 0
                    for instance in label['Instances']:
                        instance_count += 1
                    if instance_count > 0:
                        dict_count[label['Name']] = instance_count
                    # stop checking parent labels
                    break

        ani_col = db['animals']
        for key,value in dict_count.items():
            #print(key + ": " + str(value))
            ani_col.insert_one({'species':key,'count':value})
        
        #Copy image to another bucket and remove from the original
        s3.Object(str_old_bucket,filename).copy_from(CopySource=str_bucket+'/'+filename)
        s3.Object(str_bucket,filename).delete()

    for document in url_col.find():
        print('three')
        print(document)

    for document in ani_col.find():
        print('three')
        print(document)

