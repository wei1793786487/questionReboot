import random

import pymongo

myclient = pymongo.MongoClient("mongodb://192.168.1.112:27017/")
mydb = myclient["questions"]
Ranking = mydb["Ranking"]


async def findSource(id):
    return Ranking.find().sort("source", -1)
