# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 15:04:20 2022

@author: RAM
"""
import requests
import os
import pandas as pd 
import json
import pymysql
import settings.config
from sqlalchemy import create_engine
import json
from flask import Flask, jsonify, request,Blueprint
from utils import db_url

# db_host = os.environ.get('host')
# db_user = os.environ.get('user')
# db_password = os.environ.get('password')
# db_database = os.environ.get('database')
# inp_exp = 2
# # db_exp['min_exp']  , max_exp
# # Connect to the database

# db_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_database}'

cv_parse = Blueprint('cv_parse', __name__)



# with open('C:/Users/RAM/Desktop/Salary Calculator/obj.json') as json_data:
#     js_str = json.load(json_data)



def df_to_db(js_str, conn):
    try:
        json_dict ={}
        js_obj = js_str['ResumeParserData']

        json_dict["title"] = js_obj["Name"]["TitleName"] #if 'TitleName' in js_obj else ''
        json_dict["full_name"] = js_obj["Name"]["FullName"] #if 'FullName' in js_obj else ''
        json_dict["email"] = js_obj["Email"][0]["EmailAddress"] #if 'EmailAddress' in js_obj else ''
        json_dict["phone"] = js_obj['PhoneNumber'][0] #if 'PhoneNumber' in js_obj else ''
        json_dict["country_code"] = js_obj['Address'][0]["ZipCode"] #if 'Address' in js_obj else ''
        #json_dict["date_of_birth"] = js_obj["DateOfBirth"]
        json_dict["gender"] = js_obj['Gender']
        json_dict["hobbies"] = js_obj["Hobbies"]
        json_dict["job_profile"] = js_obj["SegregatedExperience"][0]['JobProfile']["Title"]
        json_dict["address"] =''
        json_dict["city"] = js_obj["Address"][0]["City"]
        json_dict["state"] =''
        json_dict["country"]=js_obj["Nationality"]
        json_dict["zip"]=''
        json_dict['executive_summary'] = js_obj["ExecutiveSummary"]
        json_dict['management_summary'] = js_obj['ManagementSummary']
        json_dict["first_name"] = js_obj["Name"]["FirstName"]
        json_dict["middle_name"] = js_obj["Name"]["MiddleName"]
        json_dict["last_name"] = js_obj["Name"]["LastName"]

        json_dict["father_name"] = js_obj["FatherName"]
        json_dict["mother_name"] = js_obj["MotherName"]
        json_dict["marital_status"] = js_obj["MaritalStatus"]
        json_dict["nationality"] = js_obj["Nationality"]
        try:
            json_dict["preferred_country"] = js_obj["PreferredLocation"][0]
        except:
            json_dict["preferred_country"] = ''
        try:
            json_dict["present_country"] = js_obj["CurrentLocation"][0]
        except:
            json_dict["present_country"] = ''

        json_dict["work_autherization"] = ""
        json_dict["currency"] = ""

        json_dict['language_known'] = js_obj["LanguageKnown"][0]["Language"]

        json_dict["unique_iD"] = js_obj["UniqueID"]

        json_dict['license_no'] = js_obj["LicenseNo"]

        json_dict["passport_no"] = js_obj["PassportDetail"]["PassportNumber"]
        json_dict["pan_no"] = js_obj["PanNo"]
        json_dict["visa_status"] = js_obj["VisaStatus"]
        json_dict["alternate_email"] = js_obj["Email"][0]["EmailAddress"]
        json_dict["cover_letter"] = js_obj["Coverletter"]

        json_dict["certification"] = js_obj["Certification"]

        json_dict["publication"] = js_obj["Publication"]

        try:
            json_dict["current_location"] = js_obj["CurrentLocation"][0]
        except:
            json_dict["current_location"] = ''

        try:
            json_dict["preferred_location"] = js_obj["PreferredLocation"][0]
        except:
            json_dict["preferred_location"] = ''

        json_dict["availability"] = js_obj["Availability"]

        json_dict["objectives"] = js_obj["Objectives"]

        json_dict["candidate_references"]=''  # check on this

        json_dict["candidate_achievements"]=js_obj["Achievements"]

        #json_dict["parsing_date"] = js_obj["ParsingDate"]

        json_dict["resume_language"] = js_obj["ResumeLanguage"]["Language"]

        json_dict["resume_file_name"] = ''

        try:
            json_dict["formatted_address"] = js_obj["Address"][0]["FormattedAddress"]
        except:
            json_dict["formatted_address"] =""

        """
        json_dict["permanent_address"] = ""
        json_dict["permanent_city"] = ""
        json_dict["permanent_state"] = ""
        json_dict["permanent_country"] = ""
        json_dict["permanent_zip_code"] = ""
        json_dict["formatted_permanent_address"] = ""
        """
        json_dict["industry_category"] = js_obj["Category"]
        json_dict["industry_sub_category"] = js_obj["SubCategory"]

        json_dict["qualification"] = js_obj["SegregatedQualification"][0]["Degree"]["DegreeName"]
        """
        json_dict["note"] =''
        json_dict["current_salary"] =""
        json_dict["expected_salary"] = ""
        """
        json_dict["total_experience_in_year"] =  js_obj["WorkedPeriod"]["TotalExperienceInYear"]
        json_dict["summary"] = js_obj["Summary"]
        """
        json_dict["path"] = ""
        json_dict["asset_id"] = ""
        json_dict["vendor_id"] = ""
        json_dict["created_at"] = ""
        json_dict["updated_at"] = ""
        json_dict["is_alive"] = ""
        json_dict["is_privatearea"] = ""

        """
        json_dict["html_code"] = js_obj["HtmlResume"]
        json_dict["buyout"] = ""
        #json_dict["currentservingnotice"] = "" 
        #json_dict["vendor_user_id"] = ""
        json_dict["edit_summary"] = ""

        # json_dict["mask"] = ""
        # json_dict["is_active_private"] = ""
        json_dict["loomembeded"] = ""

        data=pd.DataFrame(json_dict, index=[0])
        data.to_sql(name='candidates', con = conn, index=False,  if_exists='append')
        return "success"

    except:
        return "no"

@cv_parse.route('/cv/parse', methods=['POST'])
def perse_cv():
    try:
        if request.headers['Content-Type'] == 'application/json':
            _json = request.json
        else:
            return {'message': 'Unsupported meadia type, accepts application/json'}, 415
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
        engine = create_engine(db_url)
        conn = engine.connect()

        response = requests.request("POST", url, headers=headers, data=payload)
        js_str = json.loads(response.text)
        try:
            del js_str['ResumeParserData']['TemplateOutput']["TemplateOutputData"]
        except:
            pass
        df_to_db(js_str,conn)
        return {"message":"File uploaded successfully"}, 200
    except:
        return {"error":"true", "message":"Unable to parse CV"}, 400
    finally:
        conn.close()
        engine.dispose()




