import pymongo



myclient = pymongo.MongoClient("mongodb://192.168.1.112:27017/")
mydb = myclient["questions"]
questionlist = mydb["questionlist"]
question = mydb["question"]
Ranking = mydb["Ranking"]


def addRanking(id:int,name:str):
    by_id = findRackingById(id)
    if(by_id==None):
        print("没找到，新建")
        Ranking.insert_one({"id":id,"source":1,"name":name})
    else:
        print("找打了")
        old_name = by_id.get("name")
        source_ = by_id.get("source") + 1
        Ranking.update_one({"id":id},{"$set":{"source":source_}})
        if(old_name==None or old_name!=name):
         Ranking.update_one({"id": id}, {"$set": {"name": name}})

def findRackingById(id):
    return Ranking.find_one({"id": id})

def getlist():
    return questionlist.find()


def add(mydict):
    x = question.insert_one(mydict)

def add_list(mydict):
    x = questionlist.insert_one(mydict)

def findQusone(arry,type=1):
   results = list(map(int, arry))
   return question.find(
       {"exid": {"$in": results},"question_types": type},{"question":1,"question_standard_answer":1,"_id":0,"answer":1,"question_types":1,"question_analyze":1})

def findQlistLike(value,type:int,):
    tpp=""
    if(type==0):
        tpp="exercise"
    else:
        tpp="paper"

    return questionlist.find({"$and": [{"title": {'$regex': value}},{"mold": {'$regex': tpp}}]})



