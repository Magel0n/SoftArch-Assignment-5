import sys
import tkinter as tk

from uuid import uuid4

import yaml

sys.path.append("../shared")

from concurrent import futures

import grpc
import xee_pb2 as pb2
import xee_pb2_grpc as pb2_grpc

from pymongo import MongoClient
from bson import ObjectId

class Handler(pb2_grpc.LikerServicer):
    def __init__(self, mongo_ip):
        super().__init__()

        client = MongoClient(mongo_ip)
        self.db = client.xee_db

    def Like(self, request, context):
        user = self.db.tokens.find_one({"token": request.token})
        if user is None:
            context.set_details("Invalid user")
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return pb2.LikeUpdate(success=False, likes=-1)

        xeet = self.db.xeets.find_one({"_id": ObjectId(request.xeet_id)})
        hasLiked = user["username"] in xeet["likes"]

        if hasLiked == request.liked:
            mod = 0
            pass
        elif request.liked:
            mod = 1
            self.db.xeets.update_one({"_id": ObjectId(request.xeet_id)}, {"$push": {"likes": user["username"]}})
        else:
            mod = -1
            self.db.xeets.update_one({"_id": ObjectId(request.xeet_id)}, {"$pull": {"likes": user["username"]}})
        return pb2.LikeUpdate(success=True, likes=len(xeet["likes"]) + mod)


if __name__ == "__main__":
    with open("../shared/config.yaml", "r") as conf_yaml:
        config = yaml.safe_load(conf_yaml)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_LikerServicer_to_server(Handler(config["mongo-ip"]), server)
    server.add_insecure_port(config['service-ips']["like"])
    try:
        server.start()
        while True:
            server.wait_for_termination()
    except grpc.RpcError as e:
        print(f"Unexpected Error: {e}")
    except KeyboardInterrupt:
        server.stop(grace=10)
        print("Shutting Down...")
