from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.gcgk5vj.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    
    doc = {
        'title' : ogtitle,
        'desc' : ogdesc,
        'image' : ogimage,
        'url' : url_receive,
        'comment' : comment_receive,
        'star' : star_receive
    }
    db.movies.insert_one(doc)
    
    return jsonify({'msg':'저장 완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    all_movies = list(db.movies.find({},{'_id':False}))
    return jsonify({'result':all_movies})

@app.route("/movie", methods=["PUT"])
def movie_edit():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    ncomment_receive = request.form['ncomment_give']
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    
    doc = {
        'title': ogtitle,
        'desc': ogdesc,
        'image': ogimage,
        'comment': ncomment_receive,
        'star': star_receive
    }
    
    # Check if the comment exists and update it
    if db.movies.find_one({'comment': comment_receive}):
        db.movies.update_one({'comment': comment_receive}, {'$set': doc})
        return jsonify({'msg': '수정 완료!'})
    
    # Return error message if the comment is not found
    return jsonify({'msg': '수정할 댓글을 찾을 수 없습니다!'})

@app.route("/movie", methods=["DELETE"])
def movie_delete():
    comment_receive = request.form['comment_give']
    
    db.movies.delete_one({'comment':comment_receive})
    db.comments.delete_many({'key':comment_receive})
    
    return jsonify({'msg':'삭제 완료!'})

@app.route("/comment", methods=["POST"
def comment_post():
    key_receive = request.form['key_give']
    name_receive = request.form['name_give']
    content_receive = request.form['content_give']
    agree_receive = request.form['agree_give']
        
    doc = {
        'key' : key_receive,
        'name' : name_receive,
        'content' : content_receive,
        'agree' : agree_receive
    }
    db.comments.insert_one(doc)
    
    return jsonify({'msg':'댓글 저장 완료!'})

@app.route("/comment", methods=["GET"])
def comment_get():
    all_comments = list(db.comments.find({}, {'_id':False}))
    return jsonify({'result': all_comments})

@app.route("/comment", methods=["PUT"])
def comment_edit():  
    name_receive = request.form['name_give']
    content_receive = request.form['ocontent_give']
    ncontent_receive = request.form['ncontent_give']
    agree_receive = request.form['agree_give']
    
    doc = {
        'name' : name_receive,
        'content' : ncontent_receive,
        'agree' : agree_receive
    }
    
    db.comments.update_one({'content':content_receive},{'$set':doc})
    return jsonify({'msg':'댓글 수정 완료!'})

@app.route("/comment", methods=["DELETE"])
def comment_delete():
    content_receive = request.form['content_give']
    
    db.comments.delete_one({'content':content_receive})
    return jsonify({'msg':'삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)