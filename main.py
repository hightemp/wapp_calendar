from flask import g, Flask, render_template, request, send_file, redirect, session, jsonify
import os
import re
from werkzeug.utils import secure_filename

from flask import Response
from jinja2 import Template, FunctionLoader, Environment, BaseLoader
from flask import Flask
import mimetypes
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict
import zipfile
from gtts import gTTS
from datetime import datetime

# NOTE: Константы
UPLOAD_PATH_REL = "static/uploads"
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), UPLOAD_PATH_REL)
DATABASE = './wapp_calendar.database.db'

# NOTE: Переменные
bFirstStart = not os.path.isfile(DATABASE)
app = Flask(__name__)
db = SqliteDatabase(DATABASE)

# NOTE: Модели
class Event(Model):
    name: CharField()
    
db.connect()

if (bFirstStart):
    db.create_tables([Event])

# NOTE: Хелперы
def parse_get(args):
    data = {}

    for u, v in args.lists():
        if hasattr(v, "__len__"):
            for k in v:
                data[u] = k
                if k == '':
                    del data[u]
        else:
            data[u] = v
            if v == '':
                del data[u]

    return data

def parse_multi_form(form):
    data = {}
    for url_k, v in form.lists():
        if ('' in v):
            continue
        v = v[0]

        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i+1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v

    return data



def fnPrepareFormFields(aFields, cCls, sSelID):
    kls = globals()[cCls]
    oItem = {}
    if sSelID != "" and int(sSelID) > 0:
        try:
            oItem = kls.get_by_id(sSelID)
            oItem = model_to_dict(oItem, recurse=False, backrefs=False)
        except:
            pass

    for sK, oV in aFields.items():
        if sSelID==0:
            aFields[sK]['value'] = ''
        else:
            if sK in oItem and oItem[sK]:
                aFields[sK]['value'] = oItem[oV['field_name']]
            else:
                aFields[sK]['value'] = ''
    return aFields

def readfile(sFilePath):
    with zipfile.ZipFile(os.path.dirname(__file__)) as z:
        # print(z.namelist())
        with z.open(sFilePath) as f:
            print("[!] "+f.name)
            # print("[!] "+f.read().decode("utf-8"))
            return f.read()
    return "ERROR"

@app.route("/zip/static/<path:path>", methods=['GET', 'POST'])
def zip_static(path):
    oR = Response(readfile("static/"+path), mimetype=mimetypes.guess_type(path)[0])
    oR.headers['Cache-Control'] = 'max-age=60480000, stale-if-error=8640000, must-revalidate'
    return oR

@app.route("/calendar", methods=['GET', 'POST'])
def calendar():
    sBaseURL = request.url

    return render_template(
        'calendar.html', 
        sBaseURL=sBaseURL,
    )

@app.route("/days", methods=['GET', 'POST'])
def days():
    sBaseURL = request.url

    return render_template(
        'days.html', 
        sBaseURL=sBaseURL,
    )

@app.route("/", methods=['GET', 'POST'])
def index():
    sBaseURL = request.url

    oArgs = parse_get(request.args)
    oArgsLists = parse_multi_form(request.args)

    return render_template(
        'index.html', 
        sBaseURL=sBaseURL,
    )

def number_to_words(n):
    n = int(n)
    f = {1 : 'один', 2 : 'два', 3 : 'три', 4 : 'четыре', 5 : 'пять',
    6 : 'шесть', 7 : 'семь', 8 : 'восемь', 9 : 'девять'}
    l = {10 : 'десять', 20 : 'двадцать', 30 : 'тридцать', 40 : 'сорок',
    50 : 'пятьдесят', 60 : 'шестьдесят', 70 : 'семьдесят',
    80 : 'восемьдесят', 90 : 'девяносто'}
    s = {11 : 'одиннадцать', 12 : 'двенадцать', 13 : 'тринадцать',
    14 : 'четырнадцать', 15 : 'пятнадцать', 16 : 'шестнадцать',
    17 : 'семнадцать', 18 : 'восемнадцать', 19 : 'девятнадцать'}
    n1 = n % 10
    n2 = n - n1
    if (n < 10):
        return f.get(n)
    elif (n >= 10 and n2 == 0):
        return l.get(n)
    elif (n > 20):
        return l.get(n2) + ' ' + f.get(n1)
    else:
        return 'Введено число, которое не лежит в [1:99]!'

def conv(n): 
    n = int(n)
    es = ['', 'а', 'ов']
    n = n % 100
    if n>=11 and n<=19:
        s=es[2] 
    else:
        i = n % 10
        if i == 1:
            s = es[0] 
        elif i in [2,3,4]:
            s = es[1] 
        else:
            s = es[2] 
    return s 

@app.route("/generate_sounds", methods=['GET', 'POST'])
def generate_sounds():
    for sH in range(1, 24):
        if sH<10:
            sH = "0"+str(sH)
        sP = f'./static/time/{sH}.mp3'
        sSH = number_to_words(sH)
        tts = gTTS(f"{sSH} час{conv(sH)}", lang="ru")
        tts.save(sP)
    return "OK"

@app.route("/time_speaker", methods=['GET', 'POST'])
def time_speaker():
    now = datetime.now()
    sPronounseTime = ""
    sH = now.strftime("%H")
    sM = now.strftime("%M")
    sS = now.strftime("%S")
    if (sM=="00"):
        sP = f'./static/time/{sH}.mp3'
        if not os.path.isfile(sP):
            sSH = number_to_words(sH)
            tts = gTTS(f"{sSH} часов", lang="ru")
            tts.save(sP)
        sPronounseTime = sP

    return render_template(
        'ptime.html', 
        sPronounseTime=sPronounseTime,
    )
