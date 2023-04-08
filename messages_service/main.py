import sys
import threading
from flask import Flask
from flask import make_response
import hazelcast

app = Flask(__name__)


@app.route("/messages_service", methods=['GET'])
def messages_get():
    return_messages = str(list(dict.values()))
    return return_messages


def def_thread():
    while True:
        if not queue.is_empty():
            head = queue.take()
            dict.update({head['uuid']: head['message']})
            print(str(head), sys.stdout)
            print(str(dict), sys.stdout)


if __name__ == "__main__":
    dict = {}
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue").blocking()
    consumer_thread = threading.Thread(target=def_thread)
    consumer_thread.start()
    app.run(host="localhost",
            port=5005,
            debug=False)
