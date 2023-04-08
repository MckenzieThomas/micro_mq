from flask import Flask
from flask import request
from flask import make_response
import sys
import hazelcast

app = Flask(__name__)


@app.route("/logging_service", methods=['POST'])
def logging_post():
    message_json = request.get_json()
    got_message = message_json['message']
    got_uuid = message_json["uuid"]
    logging_map.put(got_uuid, got_message)
    print("Requested json", sys.stdout)
    print(request.get_json(), sys.stdout)
    response = make_response("Success")
    return response


@app.route("/logging_service", methods=['GET'])
def logging_get():
    return_messages = str(logging_map.values())
    return return_messages


if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    logging_map = client.get_map("logging_messages_map").blocking()
    app.run(host="localhost",
            port=5001,
            debug=False)
