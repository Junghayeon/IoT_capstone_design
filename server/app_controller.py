from flask import Flask, request, json, jsonify, Response
import pymysql
import sqlite3
import time
import sys
app = Flask(__name__)

def check_duplicate_view(user_id, video_id):
    db.execute('SELECT COUNT(*) FROM UserViewedVideos WHERE user_id = ? AND video_id = ?', (user_id, video_id))
    result = db.fetchone()
    return result[0] > 0

@app.route("/reset", methods=["GET"])
def reset():
    db.execute("DROP TABLE IF EXISTS USERS")
    db.execute("DROP TABLE IF EXISTS INTER_T")
    db.execute("DROP TABLE IF EXISTS REC_SOCIAL")
    db.execute("DROP TABLE IF EXISTS REC_HEAL")
    db.execute("DROP TABLE IF EXISTS ADMINISTRATOR")
    db.execute("DROP TABLE IF EXISTS UserViewedVideos")

    db.execute("CREATE TABLE IF NOT EXISTS USERS(id text, age integer, gender text, status text, interest text)")
    db.execute("CREATE TABLE IF NOT EXISTS INTER_T(id integer, name text, 기타 integer, 요리 integer, 바둑 integer, 미술 integer, 운동 integer, 영화 integer, 건강 integer, 교양 integer, 상담 integer)")
    db.execute("CREATE TABLE IF NOT EXISTS REC_SOCIAL(num integer, tag text, act text, title text, date text, desc text)")
    db.execute("CREATE TABLE IF NOT EXISTS REC_HEAL(num integer, tag text, movie text, title text, date text, desc text)")
    db.execute("CREATE TABLE IF NOT EXISTS ADMINISTRATOR(administ_id text, pw text, phone text, id text)")
    db.execute("CREATE TABLE IF NOT EXISTS UserViewedVideos(user_id text, video_id text, CONSTRAINT pk_UserViewedVideoes PRIMARY KEY (user_id, video_id));")
    conn.commit()
    response = {
        "result": "ok",
        "message": "Database reset successful"
    }
    return jsonify(response)

@app.route("/post_social_data", methods=["POST"])
def post_social():
    db.execute("SELECT num from REC_SOCIAL;")
    rows = db.fetchall()
    number = len(rows) + 1
    params = request.get_json()
    json_obj = json.dumps(params)
    json_obj = json.loads(json_obj)
    for key, val in json_obj.items():
        if(key == "tag"):
            insert_tag = val
        elif(key == "act"):
            insert_act = val
        elif(key == "title"):
            insert_title = val
        elif(key == "date"):
            insert_date = val
        elif(key == "desc"):
            insert_desc = val
    sql = "INSERT INTO REC_SOCIAL VALUES(?, ?, ?, ?, ?, ?);"
    vals = (number, insert_tag, insert_act, insert_title, insert_date, insert_desc)
    db.execute(sql, vals)
    conn.commit()
    response = {
            "result" : "ok"
            }
    return jsonify(response)

@app.route("/add_user", methods=["POST"])
def add_user():
    db.execute("SELECT id from INTER_T;")
    rows = db.fetchall()
    number = len(rows) + 1
    params = request.get_json()
    json_obj = json.dumps(params)
    json_obj = json.loads(json_obj)

    for key, val in json_obj.items():
        if(key == "id"):
            insert_id = val
        elif(key == "age"):
            insert_age = val
        elif(key == "gender"):
            insert_gender = val
        elif(key == "status"):
            insert_status = val
        elif(key == "interest"):
            insert_inter = val
        elif(key == "admin_id"):
            admin_id = val

    sql_admin = "SELECT pw, phone FROM ADMINISTRATOR WHERE administ_id = ?"
    db.execute(sql_admin, (admin_id,))
    admin_data = db.fetchone()

    sql = "INSERT INTO USERS VALUES(?, ?, ?, ?, ?);"
    vals = (insert_id, insert_age, insert_gender, insert_status, insert_inter)
    db.execute(sql, vals)

    sql_admin = "INSERT INTO ADMINISTRATOR VALUES(?, ?, ?, ?);"
    vals_admin = (admin_id, admin_data[0], admin_data[1], insert_id)
    db.execute(sql_admin, vals_admin)

    sql_inter_t = "INSERT INTO INTER_T values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    vals_inter_t = (number, insert_id, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    db.execute(sql_inter_t, vals_inter_t)

    conn.commit()
    
    response = {
        "result": "ok"
    }
    return jsonify(response)

@app.route("/post_admin", methods=["POST"])
def post_admin():
    params = request.get_json()
    json_obj = json.dumps(params)
    json_obj = json.loads(json_obj)
    for key, val in json_obj.items():
        if(key == "administ_id"):
            insert_admin_id = val
        elif(key == "pw"):
            insert_pw = val
        elif(key == "phone"):
            insert_phone = val
        elif(key == "id"):
            insert_id = val
    sql = "INSERT INTO ADMINISTRATOR VALUES(?, ?, ?, ?);"
    vals = (insert_admin_id, insert_pw, insert_phone, insert_id)
    db.execute(sql, vals)
    conn.commit()
    response = {
            "result" : "ok"
            }
    return jsonify(response)

@app.route("/post_healing_data", methods=["POST"])
def rec_heal():
    db.execute("SELECT num from REC_HEAL;")
    rows = db.fetchall()
    number = len(rows) + 1
    params = request.get_json()
    json_obj = json.dumps(params)
    json_obj = json.loads(json_obj)
    for key, val in json_obj.items():
        if(key == "tag"):
            insert_tag = val
        elif(key == "movie"):
            insert_movie = val
        elif(key == "title"):
            insert_title = val
        elif(key == "date"):
            insert_date = val
        elif(key == "desc"):
            insert_desc = val
    sql = "INSERT INTO REC_HEAL VALUES(?, ?, ?, ?, ?, ?);"
    vals = (number, insert_tag, insert_movie, insert_title, insert_date, insert_desc)
    db.execute(sql, vals)
    conn.commit()
    response = {
            "result" : "ok"
            }
    return jsonify(response)

@app.route("/get_inter_t", methods=["GET"])
def get_inter_t():    
    sql = "SELECT * FROM INTER_T"
    db.execute(sql)
    rows = db.fetchall()
    results = []
    for row in rows:
        result = {
            "id": row[0],
            "name": row[1],
            "기타": row[2],
            "요리": row[3],
            "바둑": row[4],
            "미술": row[5],
            "운동": row[6],
            "영화": row[7],
            "건강": row[8],
            "교양": row[9],
            "상담": row[10]
        }
        results.append(result)
    json_str = json.dumps(results, ensure_ascii=False)
    response = Response(json_str, content_type="application/json; charset=utf-8")
    return response

@app.route("/add_user_viewed_video", methods=["POST"])
def add_user_viewed_video():
    params = request.get_json()
    json_obj = json.dumps(params)
    json_obj = json.loads(json_obj)
    
    user_id = json_obj.get("user_id")
    video_id = json_obj.get("video_id")

    if not user_id or not video_id:
        response = {
            "result": "error",
            "message": "Invalid request body"
        }
        return jsonify(response), 400

    if check_duplicate_view(user_id, video_id):
        response = {
            "result": "error",
            "message": "Video already viewed by the user"
        }
        return jsonify(response), 409

    sql = "INSERT INTO UserViewedVideos VALUES (?, ?)"
    db.execute(sql, (user_id, video_id))
    conn.commit()

    response = {
        "result": "ok",
        "message": "User viewed video added successfully"
    }
    return jsonify(response)

@app.route("/get_interest_user/<user_name>", methods=["GET"])
def get_interest_useser(user_name):
    sql = "SELECT 기타, 요리, 바둑, 미술, 운동, 영화, 건강, 교양, 상담 FROM INTER_T WHERE name=?"
    db.execute(sql, (user_name,))
    row = db.fetchone()
    if row:
        result = row
        json_str = json.dumps(result, ensure_ascii=False)
        response = Response(json_str, content_type="application/json; charset=utf-8")
    return response

@app.route("/get_social_tag/<tag>", methods=["GET"])
def get_social_tag(tag):
    sql = "SELECT title FROM REC_SOCIAL WHERE tag=?"
    db.execute(sql, (tag,))
    rows = db.fetchall()
    results = []
    for row in rows:
        results.append(row[0])
    json_str = json.dumps(results, ensure_ascii=False)
    response = Response(json_str, content_type="application/json; charset=utf-8")
    return response

@app.route("/update_inter_t/<string:inter_name>", methods=["POST"])
def update_inter_t(inter_name):
    params = request.get_json()
    json_obj = json.dumps(params)
    json_obj = json.loads(json_obj)
    
    update_values = []
    for key, val in json_obj.items():
        update_values.append(f"{key}={val}")

    if update_values:
        sql = f"UPDATE INTER_T SET {', '.join(update_values)} WHERE name=?"
        db.execute(sql, (inter_name,))
        conn.commit()
        response = {
            "result": "ok",
            "message": "INTER_T table updated successfully"
        }
    else:
        response = {
            "result": "error",
            "message": "No update values provided"
        }

    return jsonify(response)



@app.route("/get_user/<user_id>", methods=["GET"])
def get_uesr(user_id):
    sql = "SELECT id, status FROM USERS WHERE id=?"
    db.execute(sql, (user_id,))
    row = db.fetchone()
    if row:
        result = row
        json_str = json.dumps(result, ensure_ascii=False)
        response = Response(json_str, content_type="application/json; charset=utf-8")
    return response

@app.route("/get_admin_manage_user/<string:admin_id>", methods=["GET"])
def get_admin_manage_user(admin_id):
    sql = f"SELECT id FROM ADMINISTRATOR WHERE administ_id='{admin_id}'"
    db.execute(sql)
    rows = db.fetchall()
    results = []
    for row in rows:
        results.append(row[0])
    json_str = json.dumps(results, ensure_ascii=False)
    response = Response(json_str, content_type = "application/json; charset=utf-8")
    return response

@app.route("/get_rec_social", methods=["GET"])
def get_rec_social():
    sql = "SELECT * FROM REC_SOCIAL"
    db.execute(sql)
    rows = db.fetchall()
    results = []
    for row in rows:
        result = {
            "num": row[0],
            "tag": row[1],
            "act": row[2],
            "title" : row[3],
            "date" : row[4],
            "desc" : row[5]
        }
        results.append(result)
    json_str = json.dumps(results, ensure_ascii=False)
    response = Response(json_str, content_type="application/json; charset=utf-8")
    return response

@app.route("/get_rec_heal", methods=["GET"])
def get_rec_heal():
    sql = "SELECT * FROM REC_HEAL"
    db.execute(sql)
    rows = db.fetchall()
    results = []
    for row in rows:
        result = {
            "num": row[0],
            "tag": row[1],
            "movie": row[2],
            "title" : row[3],
            "date" : row[4],
            "desc" : row[5]
        }
        results.append(result)
    json_str = json.dumps(results, ensure_ascii=False)
    response = Response(json_str, content_type="application/json; charset=utf-8")
    return response

@app.route("/get_admin_pw/<admin_id>", methods=["GET"])
def get_admin_pw(admin_id):
    sql = "SELECT pw FROM ADMINISTRATOR WHERE administ_id=?"
    db.execute(sql, (admin_id,))
    row = db.fetchone()
    if row:
        result = {"admin_id": admin_id, "pw": row[0]}
        json_str = json.dumps(result, ensure_ascii=False)
        response = Response(json_str, content_type="application/json; charset=utf-8")
        return response
    else:
        return "아이디가 없습니다", 404
    
@app.route("/get_rec_heal_tag/<string:movie>", methods=["GET"])
def get_rec_heal_tag(movie):
    movie_fullname = "https://youtu.be/" + movie
    sql = f"SELECT tag FROM REC_HEAL WHERE movie='{movie_fullname}'"
    db.execute(sql)
    row = db.fetchone()
    if row:
        result = row
        json_str = json.dumps(result, ensure_ascii=False)
        response = Response(json_str, content_type="application/json; charset=utf-8")
    return response

@app.route("/get_rec_heal/<string:tag>", methods=["GET"])
def get_rec_heal_by_tag(tag):
    sql = f"SELECT movie FROM REC_HEAL WHERE tag='{tag}'"
    db.execute(sql)
    rows = db.fetchall()
    results = []
    for row in rows:
        results.append(row[0])
    json_str = json.dumps(results, ensure_ascii=False)
    response = Response(json_str, content_type="application/json; charset=utf-8")
    return response

if __name__ == "__main__":
    conn = sqlite3.connect('IOT_CAPSTONE.db', check_same_thread=False)
    db = conn.cursor()
    db.execute("SELECT * from sqlite_master WHERE type=\"table\" AND name=\"iot_capstone\"")
    rows = db.fetchall()
    if not rows:
        db.execute("CREATE TABLE IF NOT EXISTS USERS(id text, age integer, gender text, status text, interest text)")
        db.execute("CREATE TABLE IF NOT EXISTS INTER_T(id integer, name text, 기타 integer, 요리 integer, 바둑 integer, 미술 integer, 운동 integer, 영화 integer, 건강 integer, 교양 integer, 상담 integer)")
        db.execute("CREATE TABLE IF NOT EXISTS REC_SOCIAL(num integer, tag text, act text, title text, date text, desc text)")
        db.execute("CREATE TABLE IF NOT EXISTS REC_HEAL(num integer, tag text, movie text, title text, date text, desc text)")
        db.execute("CREATE TABLE IF NOT EXISTS ADMINISTRATOR(administ_id text, pw text, phone text, id text)")
        db.execute("CREATE TABLE IF NOT EXISTS UserViewedVideos(user_id text, video_id text, CONSTRAINT pk_UserViewedVideoes PRIMARY KEY (user_id, video_id));")
        conn.commit()
    app.run(debug = True, host='0.0.0.0', port=20000)
    conn.close()
