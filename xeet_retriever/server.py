import sys
import tkinter as tk

import yaml

sys.path.append("../shared")

from concurrent import futures

import grpc
import xee_pb2 as pb2
import xee_pb2_grpc as pb2_grpc

from pymongo import MongoClient

class Handler(pb2_grpc.RetrieverServicer):
    def __init__(self, mongo_ip):
        super().__init__()

        client = MongoClient(mongo_ip)
        self.db = client.xee_db

    def RetrieveFeed(self, request, context):
        if not request.HasField("token"):
            user = None
        else:
            user = self.db.tokens.find_one({"token": request.token})
            if user is not None:
                user = user["username"]
        
        xeets = [i for i in self.db.xeets.find().limit(10).sort({"$natural":-1})]
        xeets = [pb2.XeetData(id=str(i["_id"]), poster=i["poster"], text=i["text"], likes=len(i["likes"]), liked=(user in i["likes"])) for i in xeets]
        
        return pb2.Feed(feed=xeets)


if __name__ == "__main__":
    with open("../shared/config.yaml", "r") as conf_yaml:
        config = yaml.safe_load(conf_yaml)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RetrieverServicer_to_server(Handler(config["mongo-ip"]), server)
    server.add_insecure_port(config['service-ips']["get"])
    try:
        server.start()
        while True:
            server.wait_for_termination()
    except grpc.RpcError as e:
        print(f"Unexpected Error: {e}")
    except KeyboardInterrupt:
        server.stop(grace=10)
        print("Shutting Down...")
