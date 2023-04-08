import json
from flask import Flask
from flask import request
from flask import make_response
import requests
import uuid
import random
import hazelcast

app = Flask(__name__)


@app.route("/facade_service", methods=['POST'])
def facade_post():
    message_json = request.get_json()
    send_message = str(message_json['message'])
    random_uuid = uuid.uuid4()
    uuid_str = str(random_uuid)
    send_to_log = {'message': send_message, 'uuid': uuid_str}
    requests.post(url=random.choice(logging_services_addresses), json=send_to_log)
    response = make_response("Success")
    # add to que
    queue.put(send_to_log)
    return response


@app.route("/facade_service", methods=['GET'])
def facade_get():
    logging_service = requests.get(url=random.choice(logging_services_addresses))
    messages_service = requests.get(random.choice(messages_services_addresses))
    return_string = "logging_service:" + logging_service.text + "\n messages_service: " + messages_service.text
    return return_string


if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue").blocking()
    logging_services_addresses = ["http://localhost:5001/logging_service", "http://localhost:5002/logging_service",
                                  "http://localhost:5003/logging_service"]
    messages_services_addresses = ["http://localhost:5004/messages_service", "http://localhost:5005/messages_service"]
    app.run(host="localhost",
            port=5000,
            debug=False)
