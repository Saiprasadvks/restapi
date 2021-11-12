from fastapi import FastAPI
import psycopg2
from datetime import datetime
import pandas as pd
from typing import List, Optional, Set, Any, Dict
from pydantic import BaseModel
import uvicorn


app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    password: str

def DB_connect():
    conn=psycopg2.connect(
    host = "192.168.168.131",
    port = "5432",
    database = "test1",
    user = "test",
    password = "test")
    return conn

@app.post('/insert')
def insert(data: User):
    now = datetime.now()
    conn = DB_connect()
    cur = conn.cursor()
    print(conn)
    cur.execute("INSERT INTO web (username, password, email, created_on, last_login) VALUES(%s, %s, %s, %s, %s) RETURNING *;", (data.name, data.email, data.password, now, None))
    detail = cur.fetchone()
    conn.commit()
    cur.close()
    return detail

@app.post('/delete')
def insert(data: User):
    now = datetime.now()
    conn = DB_connect()
    cur = conn.cursor()
    print(conn)
    cur.execute("DELETE FROM web WHERE username = %s;", (data.name,))
    conn.commit()
    cur.close()
    return "User deleted successfully"

if __name__ == "__main__":
    uvicorn.run(app='api:app', host="127.0.0.1", port=4006, reload=True)
