import os
import settings.config
from utils import db_url
from sqlalchemy import create_engine, text
from flask import Flask, jsonify, request,Blueprint
import pandas as pd

calculation = Blueprint('calculation', __name__)



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
        # if request.headers['Content-Type'] == 'application/json':
        #     _json = request.json
        # else:
        #     return {'message': 'Unsupported meadia type, accepts application/json'}, 415
        _json={}
        _json["email"] = "prasade.uk@gail.com"
        engine = create_engine(db_url)
        conn = engine.connect()
        data = pd.read_sql("SELECT country, industry_category, total_experience_in_year as experience FROM candidates where email = '"+_json["email"]+"'", con = conn)
        experience = pd.read_sql(" select * from experience ",con=conn)
        #sectors = pd.read_sql ("SELECT name, percentage FROM sectors" , con = conn)
        sectors = pd.read_sql (text("select * from sectors where name like '%"+data["industry_category"][0]+"%'") , con = conn)
        
        country = pd.read_sql("SELECT country, 18000 as min_sal, 24000 as max_sal  FROM currency where country = '"+data["country"][0]+"'", con = conn)
        df = calculate_salaries(country, data["experience"][0],experience, data["industry_category"][0],sectors)
        
        #print(df.to_dict('records'))
    except:
        return {"error":"true", "message":"Unable to run calculation"}, 400
    finally:
        conn.close()
        engine.dispose()
        print()
    return {"result":df.to_dict('records')}, 200

@calculation.route('/missing', methods=['POST'])
def missing_fields():
    try:
        missing = []
        # if request.headers['Content-Type'] == 'application/json':
        #     _json = request.json
        # else:
        #     return {'message': 'Unsupported meadia type, accepts application/json'}, 415
        _json={}
        _json["email"] = "prasade.uk@gail.com"
        engine = create_engine(db_url)
        conn = engine.connect()
        data = pd.read_sql("SELECT country, industry_category, total_experience_in_year as experience FROM candidates where email = '"+_json["email"]+"'", con = conn)
        if len(data['country'])==0:
            missing.append('country')
        if len(data['industry_category'])==0:
            missing.append('industry')
        if len(data['experience'])==0:
            missing.append('experience')
    finally:
        conn.close()
        engine.dispose()
        print()
    return {"missing":missing}, 200







