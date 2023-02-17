from flask import Flask,jsonify
from flask import request
from flask import abort,redirect
from flask import send_file
import json
import re
from ronglian_sms_sdk import SmsSDK
##产生验证码图片文件和清理图片文件
from captcha.image import ImageCaptcha
import random,string
import os
import shutil
app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#短信接口用
accId = '2c9488768610eb8001862c51056a0569'
accToken = 'c02f944d8cb44e7f935fda417c10b723'
appId = '2c9488768610eb8001862c51066c0570'
keyCaptcha=''
chr4=''
##接口1
@app.route('/position/<geohash>')
def getGeoHash(geohash):
    latitude=geohash.split(",")[0]
    longitude=geohash.split(",")[1]
    copy={}
    with open('shops.json','r',encoding='utf-8') as f:
        a = f.read()
        if a.startswith(u'\ufeff'):
            a = a.encode('utf8')[3:].decode('utf8')
        shops = json.loads(a)
        for shop in shops:
            if(shop['latitude']==float(latitude)):
                copy=shop
    geohash_shop={
      "code": 0,
      "data": {
        "address": copy['address'],
        "city": match_city(copy["address"]),
        "geohash": geohash,
        "latitude": latitude,
        "longitude": longitude,
        "name": copy["name"]
      }
    }
    return jsonify(geohash_shop)
def match_city(city):
    if(city.find("省"))==-1:
        m=re.match('(.+\u5e02).+',city)
    else:
        m=re.match('[\u4e00-\u9fa5]*?\u7701+?(.+\u5e02).+',city)
    return m.group(1)

##接口2
@app.route('/index_category')
def getByCategory():
    with open('index_category.json','r',encoding='utf-8') as f:
        a = f.read()
        if a.startswith(u'\ufeff'):
            a = a.encode('utf8')[3:].decode('utf8')
    shops = json.loads(a)
    category_shop={
	  "code": 0,
	  "data": shops
	}
    return jsonify(category_shop)


#接口3
@app.route('/shops')
def getByPosition():
    lat=request.args["latitude"]
    lon=request.args["longitude"]
    copy={}
    with open('shops.json','r',encoding='utf-8') as f:
        a = f.read()
        if a.startswith(u'\ufeff'):
            a = a.encode('utf8')[3:].decode('utf8')
        shops = json.loads(a)
##        for shop in shops:
##            if(shop['latitude']==float(lat)and shop['longitude']==float(lon)):
##                copy=shop
    position_shop={
	  "code": 0,
	  'data':shops
##          [
##              {
##                "name": copy["name"],
##                'address':copy['address'],
##                "id": copy["id"],
##                'latitude': copy['latitude'],
##                'longitude': copy['longitude'],
##                'location': copy['location'],
##                'phone': copy['phone'],
##                'category': copy['category'],
##                'supports': copy['supports'],
##                'status': copy['status'],
##                'recent_order_num': copy['recent_order_num'],
##                'rating_count': copy['rating_count'],
##                'rating': copy['rating'],
##                'promotion_info': copy['promotion_info'],
##                'piecewise_agent_fee': copy['piecewise_agent_fee'],
##                'opening_hours': copy['opening_hours'],
##                'license': copy['license'],
##                'is_new': copy['is_new'],
##                'is_premium': copy['is_premium'],
##                'image_path': copy['image_path'],
##                'identification': copy['identification'],
##                'float_minimum_order_amount': copy['float_minimum_order_amount'],
##                'float_delivery_fee': copy['float_delivery_fee'],
##                'distance': copy['distance'],
##                'order_lead_time': copy['order_lead_time'],
##                'description': copy['description'],
##                'delivery_mode': copy['delivery_mode'],
##                'activities': copy['activities'],
##              }
##            ]
	}
    return jsonify(position_shop)

#接口4
@app.route('/search_shops')
def getByKey():
    json_data = request.json
    keyword=request.args["keyword"]
    location=request.args["geohash"]
    latitude=location.split(",")[0]
    longitude=location.split(",")[1]
    copy=[]
    with open('shops.json','r',encoding='utf-8') as f:
        a = f.read()
        if a.startswith(u'\ufeff'):
            a = a.encode('utf8')[3:].decode('utf8')
        shops = json.loads(a)
        for shop in shops:
            if shop["name"].find(keyword)!=-1:
                copy.append(shop)
    key_shop={
        "code":0,
        "data":copy
        }
    print(key_shop)
    return jsonify(key_shop)

#接口5
@app.route('/captcha')
def getSvg():
    path_data = os.path.abspath('.\\image')
    del_file(path_data)
    global chr4
##    return '''    <svg xmlns="http://www.w3.org/2000/svg" width="150" height="50">
##      <path d="M18 7 C93 15,83 48,133 44" stroke="#76dfdf" fill="none"/>
##      <path fill="#a18ae4"
##            d="M53.11 33.27L53.16 33.32L53.18 33.33Q53.05 36.18 51.87 40.82L51.89 40.84L51.77 40.72Q49.99 41.26 48.39 42.06L48.36 42.03L48.47 42.14Q51.12 35.15 50.85 27.73L50.88 27.76L50.85 27.73Q50.49 20.25 47.41 13.51L47.30 13.41L47.43 13.54Q49.38 14.80 51.25 15.37L51.33 15.45L51.28 15.40Q53.46 22.42 53.46 29.09L53.35 28.97L53.35 28.97Q53.44 30.51 53.37 31.99L53.34 31.97L53.36 31.99Q54.48 30.75 59.70 25.80L59.75 25.86L59.57 25.68Q60.68 25.68 61.67 25.61L61.70 25.63L63.71 25.40L63.84 25.52Q60.61 28.47 56.31 32.24L56.39 32.32L56.35 32.28Q59.74 35.05 66.21 40.88L66.11 40.78L66.23 40.90Q63.58 40.08 60.61 39.89L60.53 39.81L60.47 39.75Q57.99 37.69 53.12 33.27ZM63.09 42.52L63.13 42.55L62.99 42.42Q67.71 43.26 70.84 45.20L70.94 45.30L70.98 45.34Q69.76 44.01 67.13 41.61L67.05 41.53L67.14 41.62Q67.37 41.70 67.64 41.81L67.55 41.73L67.48 41.66Q65.45 39.70 63.20 37.80L63.27 37.87L58.88 34.01L58.91 34.04Q63.71 29.66 66.15 26.77L66.23 26.86L66.22 26.84Q64.97 26.88 62.49 27.15L62.60 27.26L62.45 27.11Q64.01 25.63 64.70 24.79L64.82 24.91L64.88 24.97Q61.94 25.30 59.46 25.30L59.64 25.48L59.47 25.31Q58.22 26.77 55.48 29.43L55.39 29.34L55.43 29.37Q55.33 23.49 54.34 17.67L54.38 17.71L54.31 17.63Q53.64 17.50 52.16 17.24L52.28 17.36L52.26 17.34Q52.14 16.65 51.69 15.16L51.53 15.01L51.56 15.03Q48.88 14.19 46.63 12.62L46.78 12.77L46.70 12.69Q50.15 19.52 50.49 27.63L50.42 27.56L50.49 27.63Q50.83 35.55 47.83 42.79L47.78 42.74L47.74 42.70Q48.60 42.57 49.93 41.93L49.81 41.80L49.79 41.78Q49.53 42.59 48.88 44.03L49.02 44.17L48.86 44.01Q51.85 43.08 53.98 42.70L53.84 42.56L53.81 42.53Q54.42 40.05 54.91 35.79L55.07 35.95L55.05 35.93Q57.70 38.23 63.14 42.57Z"/>
##      <path d="M6 10 C81 37,86 26,136 21" stroke="#44d8b3" fill="none"/>
##      <path fill="#a5ec5f"
##            d="M32.52 41.02L32.37 40.87L32.40 40.89Q31.11 39.22 29.81 36.14L29.84 36.17L27.66 30.98L27.72 31.04Q26.21 35.12 25.60 36.42L25.47 36.29L25.51 36.33Q24.06 39.25 22.46 41.16L22.45 41.15L22.46 41.16Q22.11 41.19 21.34 41.30L21.27 41.23L21.35 41.30Q21.26 33.79 15.44 27.86L15.45 27.86L15.50 27.91Q13.70 26.04 11.68 24.56L11.73 24.60L11.84 24.71Q13.54 25.12 15.40 25.42L15.46 25.48L15.57 25.59Q21.54 30.46 22.99 36.70L23.05 36.76L23.01 36.72Q23.89 34.87 25.07 31.67L24.99 31.58L25.05 31.64Q26.50 27.99 27.07 26.69L27.02 26.65L28.30 26.51L28.32 26.54Q29.16 28.21 30.34 31.49L30.38 31.53L30.35 31.50Q31.66 35.13 32.31 36.54L32.34 36.58L32.40 36.63Q34.26 30.38 39.74 25.81L39.66 25.73L39.63 25.70Q40.87 25.65 43.61 25.08L43.71 25.18L43.66 25.13Q35.06 31.18 33.88 41.16L33.86 41.14L33.13 40.94L33.17 40.98Q32.74 40.86 32.40 40.90ZM35.44 43.41L37.42 43.52L37.56 43.66Q37.21 42.09 37.21 40.57L37.10 40.46L37.10 40.45Q37.10 37.22 38.51 33.99L38.60 34.08L38.58 34.05Q40.62 29.59 44.73 26.51L44.70 26.48L44.67 26.44Q43.38 26.64 41.51 26.98L41.57 27.03L41.52 26.98Q43.55 25.40 44.84 24.48L44.93 24.57L42.45 25.06L42.41 25.02Q41.14 25.20 39.81 25.35L39.85 25.39L39.72 25.26Q34.67 29.61 32.73 34.64L32.63 34.54L32.64 34.55Q32.02 32.41 30.65 28.14L30.75 28.24L30.68 28.18Q30.35 28.18 30.08 28.18L30.10 28.20L29.51 28.15L29.51 28.15Q29.49 27.94 28.69 26.19L28.62 26.12L26.60 26.15L26.52 26.07Q25.59 28.91 23.50 34.54L23.45 34.50L23.45 34.50Q22.30 30.99 19.22 27.72L19.12 27.61L19.15 27.64Q18.77 27.53 18.46 27.49L18.62 27.65L17.99 27.48L18.01 27.49Q17.15 26.67 15.36 25.07L15.35 25.06L15.45 25.17Q12.20 24.43 10.53 23.94L10.61 24.02L10.53 23.94Q21.22 31.35 20.83 41.66L20.89 41.72L20.95 41.78Q21.11 41.75 21.47 41.71L21.49 41.73L21.49 41.73Q21.72 41.56 21.91 41.56L21.91 41.56L22.08 41.73Q22.05 41.55 22.24 43.64L22.18 43.59L24.03 43.33L24.12 43.42Q26.62 40.52 28.86 34.77L28.97 34.87L28.92 34.83Q30.36 38.62 32.22 41.29L32.28 41.35L32.34 41.40Q32.61 41.34 32.88 41.36L32.81 41.29L32.90 41.37Q33.08 41.31 33.34 41.31L33.48 41.44L35.37 43.33Z"/>
##      <path fill="#97e7d3"
##            d="M82.61 40.36L82.61 40.36L82.57 40.32Q81.12 40.35 79.56 39.93L79.54 39.91L79.61 39.98Q78.47 39.15 78.32 37.51L78.26 37.46L78.34 37.53Q78.27 37.31 78.46 34.68L78.48 34.70L78.49 34.71Q79.49 34.50 81.51 34.12L81.52 34.13L81.35 34.91L81.30 34.86Q81.02 36.59 82.43 37.17L82.34 37.08L82.37 37.11Q83.27 37.56 85.37 37.56L85.20 37.39L85.32 37.51Q86.86 37.30 87.05 37.23L87.16 37.33L87.16 37.33Q88.07 37.17 88.79 36.68L88.68 36.57L88.68 36.57Q90.22 35.75 90.03 33.65L89.84 33.47L89.95 33.57Q89.74 31.12 88.01 29.56L87.93 29.48L88.09 29.64Q86.22 27.94 83.75 27.94L83.80 27.99L83.88 27.85L83.82 27.78Q84.11 27.66 84.99 27.58L85.12 27.72L85.01 27.60Q86.91 27.48 88.28 26.25L88.26 26.23L88.36 26.33Q89.74 25.11 89.90 23.24L89.82 23.16L89.89 23.23Q89.85 22.77 89.85 22.43L89.90 22.48L89.88 22.46Q89.91 20.97 88.54 20.05L88.53 20.05L88.62 20.14Q87.42 19.36 85.82 19.47L85.81 19.46L85.67 19.32Q84.40 19.19 83.18 19.61L83.19 19.62L83.23 19.66Q81.87 20.28 81.57 21.42L81.55 21.41L81.40 21.25Q81.35 22.16 81.42 22.92L81.29 22.78L81.39 22.88Q80.29 22.58 78.23 21.85L78.30 21.93L78.23 21.85Q78.14 20.32 78.18 19.48L78.12 19.42L78.10 19.40Q78.20 17.87 79.27 17.18L79.21 17.12L79.28 17.19Q80.66 16.56 82.26 16.56L82.35 16.65L82.31 16.61Q85.41 16.51 88.57 16.78L88.60 16.80L88.60 16.81Q93.62 17.19 93.32 20.95L93.35 20.99L93.30 20.94Q93.32 22.51 92.82 24.07L92.86 24.11L92.79 24.04Q91.85 27.09 89.49 28.01L89.59 28.11L89.59 28.11Q92.13 28.56 92.74 31.91L92.80 31.97L92.67 31.84Q92.91 32.99 92.99 35.01L93.09 35.11L93.01 35.03Q93.15 39.47 88.54 39.93L88.64 40.03L88.53 39.92Q87.98 40.17 82.69 40.43ZM87.88 42.66L87.72 42.50L87.87 42.65Q88.36 42.57 91.22 42.65L91.36 42.79L91.24 42.67Q93.01 42.76 94.64 42.11L94.71 42.18L94.65 42.12Q95.78 41.11 95.59 39.36L95.57 39.35L95.64 39.42Q95.60 38.15 95.29 36.40L95.17 36.28L95.25 36.36Q94.44 31.78 92.50 30.14L92.57 30.22L92.47 29.92L92.38 29.80L92.39 29.81Q94.07 28.29 94.83 23.91L94.95 24.03L94.82 23.90Q94.87 23.46 94.99 22.51L94.94 22.46L94.98 22.50Q95.16 21.85 95.09 21.16L94.92 20.99L94.99 21.06Q94.90 19.46 93.61 18.77L93.61 18.77L93.40 18.64L93.43 18.66Q93.09 17.64 91.94 17.10L92.09 17.25L91.97 17.13Q90.47 16.46 85.33 16.16L85.41 16.25L85.43 16.26Q83.70 16.13 82.10 16.13L82.19 16.22L82.13 16.16Q80.43 16.06 78.91 16.71L79.02 16.82L78.89 16.69Q77.84 17.62 77.84 19.37L77.70 19.23L77.85 19.37Q77.75 18.86 78.01 22.21L78.03 22.22L78.02 22.22Q78.27 22.23 79.90 22.84L79.98 22.92L79.89 22.83Q80.00 23.48 79.97 23.97L79.89 23.90L79.87 23.88Q79.94 24.44 79.97 24.97L80.00 24.99L79.90 24.89Q81.77 25.35 83.79 25.47L83.78 25.46L83.73 25.41Q83.61 23.35 84.71 22.51L84.80 22.60L84.81 22.61Q85.72 22.04 87.74 21.81L87.76 21.83L87.75 21.82Q88.82 21.74 89.39 21.93L89.44 21.99L89.41 21.95Q89.49 22.12 89.53 22.23L89.49 22.19L89.41 22.29L89.62 22.96L89.63 22.97Q89.51 23.05 89.48 23.20L89.58 23.30L89.61 23.33Q89.41 24.93 87.89 26.11L87.90 26.11L87.99 26.21Q87.07 27.12 85.06 27.31L85.04 27.29L84.99 27.24Q84.17 27.30 83.30 27.30L83.31 27.31L83.32 27.32Q83.37 27.68 83.52 28.36L83.67 28.52L83.60 28.44Q85.27 28.36 86.72 29.08L86.82 29.19L86.58 29.06L85.21 29.44L85.13 29.36Q85.11 29.65 85.23 30.26L85.23 30.26L85.29 30.32Q87.47 30.30 89.19 31.63L89.06 31.51L89.02 31.46Q89.41 32.01 89.72 33.64L89.61 33.53L89.57 33.50Q89.79 36.46 86.86 36.88L86.96 36.98L86.92 36.94Q84.75 37.12 84.17 37.09L84.30 37.21L84.13 37.04Q83.87 37.13 83.34 37.05L83.27 36.98L83.22 36.48L83.40 36.08L83.48 35.75L83.53 35.45L83.34 35.27Q82.47 35.42 81.67 35.61L81.58 35.52L81.73 35.67Q81.74 35.49 81.74 35.30L81.70 35.26L81.70 35.26Q81.73 35.06 81.73 34.84L81.78 34.88L81.72 34.82Q81.68 34.33 81.84 33.61L81.89 33.66L81.85 33.62Q80.06 33.92 78.19 34.27L78.21 34.29L78.24 34.31Q78.06 34.63 77.95 35.75L78.05 35.86L78.08 35.88Q77.85 36.89 77.85 37.50L77.89 37.54L77.85 37.50Q77.95 39.58 79.32 40.34L79.43 40.45L79.40 40.42Q80.86 42.68 85.58 42.49L85.52 42.43L85.50 42.41Q86.20 42.34 87.72 42.50Z"/>
##      <path fill="#e43ee4"
##            d="M115.54 40.11L115.59 40.16L113.14 33.25L113.17 33.29Q108.85 20.74 102.91 14.35L102.96 14.40L102.90 14.33Q104.99 15.47 107.58 16.08L107.53 16.03L107.59 16.09Q112.75 22.40 117.09 35.15L117.02 35.08L117.09 35.15Q120.09 26.99 120.77 25.40L120.80 25.42L120.82 25.44Q123.19 19.82 126.01 16.51L125.88 16.38L125.84 16.33Q127.96 16.02 130.59 15.14L130.67 15.23L130.60 15.16Q126.13 19.87 123.09 27.10L123.06 27.08L122.98 26.99Q121.68 30.76 117.99 40.27L117.88 40.17L117.97 40.26Q117.41 40.26 116.84 40.23L116.86 40.25L116.73 40.12Q116.16 40.12 115.59 40.16ZM120.66 42.64L120.66 42.64L120.65 42.63Q123.37 32.56 124.93 28.52L124.95 28.54L124.91 28.50Q128.05 20.95 132.47 16.08L132.41 16.02L132.41 16.01Q131.30 16.32 129.21 17.04L129.20 17.03L130.52 15.88L130.34 15.70Q130.96 15.06 131.57 14.41L131.54 14.39L131.67 14.52Q128.85 15.51 125.85 16.08L125.84 16.07L125.76 15.99Q121.37 21.31 117.49 32.77L117.53 32.81L117.48 32.76Q113.78 22.59 110.58 18.21L110.61 18.24L110.77 18.39Q110.27 18.20 109.40 18.05L109.32 17.98L109.48 18.13Q109.19 17.70 107.59 15.64L107.61 15.66L107.67 15.72Q104.67 14.97 101.97 13.56L101.97 13.55L101.94 13.52Q108.58 20.62 112.95 33.41L112.84 33.30L112.83 33.28Q114.15 37.05 115.33 40.62L115.33 40.62L115.30 40.59Q115.79 40.78 116.63 40.67L116.60 40.64L116.53 40.57Q116.89 41.27 117.57 42.60L117.54 42.57L117.55 42.58Q118.32 42.44 119.05 42.51L119.07 42.54L119.07 42.53Q119.98 42.72 120.74 42.72Z"/>
##    </svg>'''
    chr_all = string.ascii_letters + string.digits
    chr_4 = ''.join(random.sample(chr_all, 4))
    chr4=chr_4
    print('cap',chr4)
    image = ImageCaptcha().generate_image(chr_4)
    image=image.resize((150,50))
    image.save('./image/%s.jpg' % chr_4)
    return send_file('./image/%s.jpg' % chr_4, mimetype='image/gif')

def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)
  

#接口6 账号密码登录
@app.route('/login_pwd',methods=["POST"])
def login():
    if request.method == 'POST':
    # 这样获取就可以了 
        json_data = request.json
        global chr4
        print("pwd",chr4)
        if( isinstance(json_data["name"], str)  and \
           isinstance(json_data["pwd"], str) and json_data["captcha"]==chr4):
            result={
                "code": 0,
                "data": {
                  "_id": "5a9cd9c6ad5b2d34d42b385d",
                  "name": "aaa"
                }
            }
        else:
            result={
        "code": 1,
        "msg": "用户名或密码不正确!"
        }
        print('账号密码登录结果',result)
        return jsonify(result)

#接口7
@app.route('/sendcode')
def sendCode():
    phone=request.args["phone"]
    if phone=='13065673700':
        global keyCaptcha
        keyCaptcha = ''.join(str(i) for i in random.sample(range(0, 9), 6)) 
        #send_message()
        print("短信验证码是",keyCaptcha)
        result=	{
            "code": 0,
	}
    else:
        result=	{
            "code": 1, 
            "msg": "短信验证码发送失败"
        }
    return jsonify(result)
def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = '13065673700'
    datas = (keyCaptcha, '1')
    resp = sdk.sendMessage(tid, mobile, datas)
    #print(resp)
#接口8 验证码登录
@app.route('/login_sms',methods=["POST"])
def loginSms():
    if request.method == 'POST':
    # 这样获取就可以了
        print('loginSms',keyCaptcha)
        json_data = request.json
        print(json_data['phone'],json_data["code"])
        if(json_data['phone']=='13065673700'\
           and json_data["code"]==keyCaptcha):
            result= {
                "code": 0,
                "data": {
                  "_id": "5a9cd9c6ad5b2d34d42b385d",
                  "phone": json_data['phone']
                }
            }
        else:
            result={
                "code": 1,
                "msg": "手机号或验证码不正确"
            }
        print('短信验证码登录结果',result)
        return jsonify(result)

#接口9 根据会话获取用户信息
@app.route('/userinfo')
def loginUserinfo():
    flag=True
    if(flag):
        result={
        "code": 0,
        "data": {
          "_id": "5a9cd9c6ad5b2d34d42b385d",
          "phone": "13065673700"
        }
        }
    else:
        result={
        "code": 1,
        "msg": "请先登陆"
        }
    return jsonify(result)

#接口10
@app.route('/logout')
def loginOut():
    result={
    "code": 0
    }
    return jsonify(result)

if __name__ == '__main__':
   app.run(port=int("3000"))
