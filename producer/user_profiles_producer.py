from pykafka import KafkaClient
import json
import requests
import uuid
import time


def generate_uuid():
    return str(uuid.uuid4())

def get_data():

    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]

    return res

def format_data(res):
    data = {}
    location = res['location']
    data['id'] = generate_uuid()
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['password'] = res['login']['password']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    data['nat'] = res['nat']


    return data

# #Kafka Script
client = KafkaClient(hosts="localhost:9092")

topic = client.topics['user_profiles']

producer = topic.get_sync_producer()

while True:
    res = get_data()
    message_res = format_data(res)
    producer.produce(json.dumps(message_res).encode('utf-8'))
    time.sleep(3)


