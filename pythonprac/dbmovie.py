from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.ssvirwm.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta



#'리바운드'의 영화 평점을 0으로 만들기
db.movies.update_one({'title':'리바운드'},{'$set':{'star':0}})