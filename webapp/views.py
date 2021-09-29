from django.shortcuts import render
from webapp.services import watson_discovery
from webapp.services import excel_reader_services
from webapp.services import postgresql_services
from webapp.utils import *
from django.shortcuts import redirect
import csv
import os
import boto3
from django.http import HttpResponse
import pandas
from django.core.files.storage import FileSystemStorage
from builtins import len

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_FOLDER = os.path.join(BASE_DIR, "resources","csv")
            

def index(request):
    if "GET" == request.method:
        return render(request, 'webapp/convert_csv_new.html')
    else:
        data_new = []
        data_shozoku = []
        data_people = []
        data_user = []
        if len(request.FILES) > 2:
            for key in request.FILES:
                if request.FILES[key].name[0:3] == '70A':
                    df = pandas.read_csv(request.FILES[key],dtype={'ID_NO': str})
                    data_people = df.values.tolist()

                elif request.FILES[key].name[0:3] == '70B':
                    df = pandas.read_csv(request.FILES[key],usecols=[1,3,23],dtype={'OA_NO': str} )
                    data_shozoku = df.values.tolist()   
                    data_new = read_data_csv(data_shozoku)
                else:
                    df = pandas.read_csv(request.FILES[key],encoding = "ISO-8859-1")
                    data_user = df.values.tolist()
                try:
                    save_file(request.FILES[key].name,request.FILES[key])
                except ValueError:
                    pass       
        else:
            for key in request.FILES:
                if  request.FILES[key].name[0:3] == '70A':
                    df = pandas.read_csv(request.FILES[key],dtype={'ID_NO': str})
                    data_people = df.values.tolist()
                    data_shozoku = read_data_shozoku()
                    data_user = read_data_user()
                    data_new = read_data_csv(data_shozoku)
                    
                elif request.FILES[key].name[0:3] == '70B':
                    data_people = read_data_people()
                    data_user = read_data_user()
                    df = pandas.read_csv(request.FILES[key],usecols=[1,3,23],dtype={'OA_NO': str})    
                    data_shozoku =  df.values.tolist()
                    data_new = read_data_csv(data_shozoku)
                else:
                    data_people = read_data_people()
                    data_shozoku = read_data_shozoku()
                    data_new = read_data_csv(data_shozoku)
                    df = pandas.read_csv(request.FILES[key],encoding = "ISO-8859-1")
                    data_user = df.values.tolist() 
                try:    
                    save_file(request.FILES[key].name,request.FILES[key])
                except ValueError:
                    pass           
        convert_file_csv_to_other(data_people,data_new)
        data_list = read_convert_file();
        write_user_csv(data_list,data_user)
        with open(CSV_FOLDER + '/' + 'new_file.csv',encoding="utf-8_sig" ,newline='') as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=new_file.csv'
        return response 
  
    
