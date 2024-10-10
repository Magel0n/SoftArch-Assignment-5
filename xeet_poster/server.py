import sys
import tkinter as tk

import yaml

sys.path.append("../shared")

from concurrent import futures

import grpc
import xee_pb2 as pb2
import xee_pb2_grpc as pb2_grpc

from pymongo import MongoClient

class Handler(pb2_grpc.PosterServicer):
    def __init__(self, mongo_ip):
        super().__init__()

        client = MongoClient(mongo_ip)
        self.db = client.xee_db

    def PostXeet(self, request, context):
        user = self.db.tokens.find_one({"token": request.token})
        if user is None:
            context.set_details("Invalid user")
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return pb2.Empty()
        
        self.db.xeets.insert_one({"poster":user["username"], "text":request.text, "likes":[user["username"]]})
        
        return pb2.Empty()


if __name__ == "__main__":
    with open("../shared/config.yaml", "r") as conf_yaml:
        config = yaml.safe_load(conf_yaml)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_PosterServicer_to_server(Handler(config["mongo-ip"]), server)
    server.add_insecure_port(config['service-ips']["post"])
    try:
        server.start()
        while True:
            server.wait_for_termination()
    except grpc.RpcError as e:
        print(f"Unexpected Error: {e}")
    except KeyboardInterrupt:
        server.stop(grace=10)
        print("Shutting Down...")
