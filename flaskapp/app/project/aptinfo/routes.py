#################
#### imports ####
#################
from project import sjx
from flask import render_template, jsonify, json, request, app, url_for, redirect, flash,  g
from . import aptinfo_blueprint
import flask_sijax
from functools import wraps

from .util.modelhandler import ModelHandler
from .util.crawlhandler import CrawlHandler
from .util.sijaxhandler import SijaxHandler

md = ModelHandler()
cr = CrawlHandler()


################
#### routes ####
################

@aptinfo_blueprint.route('/')
def aptinfo_init():
    # base prior /project/template/base.html
    # https://stackoverflow.com/a/11234284
    return render_template('/index.html' )

@aptinfo_blueprint.route('/createtable')
def createtable():
    print('테이블 생성 진입')
    md.createtable()
    return redirect(url_for('aptinfo_blueprint.index'))

@aptinfo_blueprint.route('/crawldata/' )
def crawldata():

    city = ['서울특별시',
    '부산광역시',
    '대구광역시',
    '인천광역시',
    '광주광역시',
    '대전광역시',
    '울산광역시',
    '세종특별자치시',
    '경기도',
    '강원도',
    '충청북도',
    '충청남도',
    '전라북도',
    '전라남도',
    '경상북도',
    '경상남도',
    '제주특별자치도',]


    from pandas.core.frame import DataFrame
    for c in city:
        sigungu_list = md.get_all_sigungu_keyword_list(c)
        for s in sigungu_list :
            print(s, end=" ")
            dong_list = md.get_all_dong_keyword_list(s)
            cnt = 0
            for d in dong_list:
                bjd_list: list = md.get_bjd_list(d)
                apt_list , bldCode_list = cr.crawl_apt_list(bjd_list)
                aptinfo_list_df = cr.crawl_apt_info(apt_list, bldCode_list)
                md.insert_all_rows(aptinfo_list_df)
                cnt +=1
            print(d+'완료', end=" ")
            print(cnt)
        print(c+'완료')
    return redirect(url_for('aptinfo_blueprint.index'))

@flask_sijax.route(aptinfo_blueprint, '/')
def index():
    if g.sijax.is_sijax_request:
        # mass sijax function registration.
        # https://pythonhosted.org/Sijax/usage.html#mass-function-registration
        g.sijax.register_object(SijaxHandler)
        return g.sijax.process_request()
    return render_template('index.html')




