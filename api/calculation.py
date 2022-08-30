# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 17:36:26 2022

@author: RAM
"""
import os
import settings.config
import requests
import json
from flask import Flask, jsonify, request,Blueprint
import pymysql.cursors
import pymysql
import pandas as pd

calculation = Blueprint('calculation', __name__)

db_host = os.environ.get('host')
db_user = os.environ.get('user')
db_password = os.environ.get('password')
db_database = os.environ.get('database')
inp_exp = 2
# db_exp['min_exp']  , max_exp
# Connect to the database
db_connection = pymysql.connect(host=db_host,
                             user=db_user,
                             password=db_password,
                             db=db_database,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



db_exp = pd.read_sql('select * from experience; ',con = db_connection)
db_countries = pd.read_sql('select * from currency; ',con = db_connection)

db_countries['min_sal'] = 18000
db_countries['max_sal'] = 24000

db_countries=db_countries.head(1)


db_connection.close()

# exp_range = db_exp[(db_exp['min_exp']< inp_exp) & (db_exp['max_exp']>=inp_exp)]

# exp_range=exp_range.reset_index(drop=True)
# print(exp_range)
# db_countries['out_min_min']=db_countries['min_sal']+(db_countries['min_sal']*(exp_range['min'][0]/100))
# db_countries['out_min_median']=db_countries['min_sal']+(db_countries['min_sal']*(exp_range['medium'][0]/100))
# db_countries['out_min_max']=db_countries['min_sal']+(db_countries['min_sal']*(exp_range['max'][0]/100))


# db_countries['out_max_min']=db_countries['max_sal']+(db_countries['max_sal']*(exp_range['min'][0]/100))
# db_countries['out_max_median']=db_countries['max_sal']+(db_countries['max_sal']*(exp_range['medium'][0]/100))
# db_countries['out_max_max']=db_countries['max_sal']+(db_countries['max_sal']*(exp_range['max'][0]/100))


# print(db_countries.to_dict('records'))



def calculate_salaries(db_countries, input_exp,db_exp,industry, db_sectors):
    input_exp= pd.to_numeric(input_exp)
    
    exp_range = db_exp[(db_exp['min_exp']< int(input_exp)) & (db_exp['max_exp']>= int(input_exp))]
    exp_range=exp_range.reset_index(drop=True)
    db_sectors=db_sectors.reset_index(drop=True)

    db_countries['out_min_min']=db_countries['min_sal']+(db_countries['min_sal']*(exp_range['min'][0]/100))
    db_countries['out_min_median']=db_countries['min_sal']+(db_countries['min_sal']*(exp_range['medium'][0]/100))
    db_countries['out_min_max']=db_countries['min_sal']+(db_countries['min_sal']*(exp_range['max'][0]/100))
    
    db_countries['out_max_min']=db_countries['max_sal']+(db_countries['max_sal']*(exp_range['min'][0]/100))
    db_countries['out_max_median']=db_countries['max_sal']+(db_countries['max_sal']*(exp_range['medium'][0]/100))
    db_countries['out_max_max']=db_countries['max_sal']+(db_countries['max_sal']*(exp_range['max'][0]/100))
    
    print(' stage 1 *******')
    #print(db_countries.to_dict('records'))
    
    if len(db_sectors)!=0:
        db_countries['out_min_min']= db_countries['out_min_min']+(db_countries['out_min_min']*(db_sectors['percentage'][0]/100))
        db_countries['out_min_median'] = db_countries['out_min_median']+(db_countries['out_min_median']*(db_sectors['percentage'][0]/100))
        db_countries['out_min_max']= db_countries['out_min_max']+(db_countries['out_min_max']*(db_sectors['percentage'][0]/100))
        
        db_countries['out_max_min']=db_countries['out_max_min']+(db_countries['out_min_min']*(db_sectors['percentage'][0]/100))
        db_countries['out_max_median']=db_countries['out_max_median']+(db_countries['out_min_min']*(db_sectors['percentage'][0]/100))
        db_countries['out_max_max']=db_countries['out_max_max']+(db_countries['out_min_min']*(db_sectors['percentage'][0]/100))
        
    return db_countries




@calculation.route('/calculation', methods=['POST'])
def run_calculation():
    try:
        flag=0
        missing_attributes =[]
        if request.headers['Content-Type'] == 'application/json':
            _json = request.json
        else:
            return {'message': 'Unsupported meadia type, accepts application/json'}, 415
        db_connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_database,charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        #file_data_64 = _json['data']
        url = "https://hirextra8.rchilli.com/RChilliParser/Rchilli/parseResumeBinary"

        payload = json.dumps({
          "filedata":  _json['data'],
          "filename": "sample.csv",
          "userkey": "Y0CPAOKBPGW",
          "version": "8.0.0",
          "subuserid": "Kumar Vuppala"
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # with open('C:/Users/RAM/Desktop/Salary Calculator/obj.json') as json_data:
        #     js_str = json.load(json_data)

        res_data = response.text
        try:
            del res_data['ResumeParserData']['TemplateOutput']["TemplateOutputData"]
        except:
            pass
        js_str = json.loads(res_data)
        
        industry = js_str['ResumeParserData']['Category']
        overall_exp = 9#js_str['ResumeParserData']['WorkedPeriod']['TotalExperienceInYear']
        #print('industry  ', industry, '  overall_exp  ',js_str['ResumeParserData']['WorkedPeriod'])
        db_sectors = pd.read_sql("select * from sectors where name like '%"+industry+"%'",con = db_connection)
        # print('******** db_sectors ************')
        # print(db_sectors)
        if industry=='' or industry==None or industry==' ':
            flag=1
            missing_attributes.append("industry")
        if overall_exp=='' or overall_exp==None or overall_exp==' ':
            flag =1
            missing_attributes.append("experience")
        
        if len(db_sectors)==0:
            flag =1
            missing_attributes.append("domain")
        if flag==1:
            return {"missing":missing_attributes}

        df = calculate_salaries(db_countries, overall_exp,db_exp, industry,db_sectors)
        res = {"result":df.to_dict('records')}
        #print(res)
    except:
        return{"error" : "true", "message" : " Unable to run calculation"}
    finally:
        db_connection.close()
        
    return res

@calculation.route('/rerun/calculation', methods=['POST'])
def rerun_calculation():
    try:
        flag=0
        missing_attributes =[]
        if request.headers['Content-Type'] == 'application/json':
            _json = request.json
        else:
            return {'message': 'Unsupported meadia type, accepts application/json'}, 415
        db_connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_database,charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        #file_data_64 = _json['data']
        url = "https://hirextra8.rchilli.com/RChilliParser/Rchilli/parseResumeBinary"

        payload = json.dumps({
          "filedata":  _json['data'],
          "filename": "sample.csv",
          "userkey": "Y0CPAOKBPGW",
          "version": "8.0.0",
          "subuserid": "Kumar Vuppala"
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # with open('C:/Users/RAM/Desktop/Salary Calculator/obj.json') as json_data:
        #     js_str = json.load(json_data)

        res_data = response.text
        try:
            del res_data['ResumeParserData']['TemplateOutput']["TemplateOutputData"]
        except:
            pass
        js_str = json.loads(res_data)
        
        industry = js_str['ResumeParserData']['Category']
        overall_exp = js_str['ResumeParserData']['WorkedPeriod']['TotalExperienceInYear']
        #print('industry  ', industry, '  overall_exp  ',js_str['ResumeParserData']['WorkedPeriod'])
        db_sectors = pd.read_sql("select * from sectors where name like '%"+industry+"%'",con = db_connection)
        # print('******** db_sectors ************')
        # print(db_sectors)
        if industry=='' or industry==None or industry==' ':
            industry=_json["industry"]
        if overall_exp=='' or overall_exp==None or overall_exp==' ':
            overall_exp = _json["experience"]
        
        if len(db_sectors)==0:
            db_sectors = _json["domain"]
        df = calculate_salaries(db_countries, overall_exp,db_exp, industry,db_sectors)
        res = {"result":df.to_dict('records')}
        #print(res)
    except:
        return{"error" : "true", "message" : " Unable to run calculation"}
    finally:
        db_connection.close()
        
    return res

