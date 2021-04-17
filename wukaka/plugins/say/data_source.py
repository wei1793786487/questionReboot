import pymongo

myclient = pymongo.MongoClient("mongodb://192.168.1.112:27017/")
mydb = myclient["questions"]
wulala = mydb["say"]


def findSource(question):
    return  wulala.find({"question": question})


def insert_one(qusetion,anwser,uid):
    wulala.insert_one({"question":qusetion,"anwser":anwser,"uid":uid})



