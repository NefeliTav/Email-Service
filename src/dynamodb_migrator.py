import boto3
from project.settings import DB_ENDPOINT, DB_TABLE


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=DB_ENDPOINT)

    table = dynamodb.create_table(
        TableName=DB_TABLE,
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    return table


my_table = create_table()
my_table.meta.client.get_waiter('table_exists').wait(TableName=DB_TABLE)
print(my_table.table_status)
print(my_table.item_count)
