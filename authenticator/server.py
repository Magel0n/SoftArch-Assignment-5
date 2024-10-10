import sys
import tkinter as tk

from uuid import uuid4
import datetime

import yaml

sys.path.append("../shared")

from concurrent import futures

import grpc
import xee_pb2 as pb2
import xee_pb2_grpc as pb2_grpc

from pymongo import MongoClient

class Handler(pb2_grpc.AuthenticatorServicer):
    def __init__(self, mongo_ip):
        super().__init__()

        client = MongoClient(mongo_ip)
        self.db = client.xee_db

    def AuthUser(self, request, context):
        expiration_time = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(minutes=10)

        self.db.tokens.delete_many({"date": {"$lt": expiration_time}})
        
        user = self.db.tokens.find_one({"username": request.username})
        if user is not None:
            context.set_details("User is already logged in")
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return pb2.Empty()
        
        token = str(uuid4())
        self.db.tokens.insert_one({"token":token, "username":request.username, "date": datetime.datetime.now(tz=datetime.timezone.utc)})
        
        return pb2.AuthDetails(token=token)

    def RevokeToken(self, request, context):
        if not request.HasField("token"):
            context.set_details("No token provided")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return pb2.Empty()

        token = request.token

        self.db.tokens.delete_one({"token":token})
        return pb2.Empty()
        

if __name__ == "__main__":
    with open("../shared/config.yaml", "r") as conf_yaml:
        config = yaml.safe_load(conf_yaml)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_AuthenticatorServicer_to_server(Handler(config["mongo-ip"]), server)
    server.add_insecure_port(config['service-ips']["auth"])
    try:
        server.start()
        while True:
            server.wait_for_termination()
    except grpc.RpcError as e:
        print(f"Unexpected Error: {e}")
    except KeyboardInterrupt:
        server.stop(grace=10)
        print("Shutting Down...")
