from flask import json
from flask_wtf import FlaskForm as rtform
from project import db
from sqlalchemy.schema import CreateSchema
import pymysql

pymysql.install_as_MySQLdb()

import pandas as pd

from ..models.aptinfo import AptInfo
from ..models.bjdinfo import BjdInfo


# 크로울 다루는 책임을 가진 클래스
class ModelHandler():

    def __init__(self):
        # pickle relative path
        # https://stackoverflow.com/questions/40416072/reading-file-using-relative-path-in-python-project/40416154
        import os.path
        path = os.path.abspath(os.path.dirname(__file__))
        self.bjdCode_path = os.path.join(path, '../models/bjdCode.csv')

    def testdb(self):
        try:
            BjdInfo.query.all()

            return '<h1>It works.</h1>'
        except Exception as e:
            print('테스트 sql 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)

    def createtable(self):

        from sqlalchemy import event, DDL
        from sqlalchemy.schema import CreateSchema
        # event.listen(db.metadata, 'before_create', CreateSchema('my_schema'))

        event.listen(db.metadata, 'before_create',
                     DDL("CREATE SCHEMA IF NOT EXISTS used_car CHARACTER SET = utf8mb4;"))
        event.listen(db.metadata, 'before_create',
                     DDL("CREATE SCHEMA IF NOT EXISTS 법정동정보 CHARACTER SET = utf8mb4;"))
        event.listen(db.metadata, 'before_create',
                     DDL("CREATE SCHEMA IF NOT EXISTS 아파트정보 CHARACTER SET = utf8mb4;"))

        try:
            from ..models.aptinfo import AptInfo
            from ..models.bjdinfo import BjdInfo
            db.create_all()
            result = '<h1>It works.</h1>'
        except Exception as e:
            print('테이블 생성 오류')
            print(e.args)
            result = '<h1>Something is broken.</h1>' + str(e.args)

        try:
            from ..models.aptinfo import AptInfo
            from ..models.bjdinfo import BjdInfo
            import csv

            with open(self.bjdCode_path, mode='r', encoding='utf-8') as f:
                df = pd.read_csv(filepath_or_buffer=self.bjdCode_path, encoding='utf-8')
                df.to_sql(name="법정동정보", con=db.engine, if_exists='replace')
            result = 'nothing'

        except Exception as e:

            print('테이블 생성 오류')
            print(e.args)
            result = '<h1>Something is broken.</h1>' + str(e.args)

        return result

    def get_bjd_list(self, keyword):
        try:

            bjdqr : list[BjdInfo] = db.session.query(BjdInfo.법정동코드).filter(
                BjdInfo.법정동명.like('%'+keyword+'%'))

            bjd_list: list = pd.read_sql(bjdqr.statement, bjdqr.session.bind)['법정동코드'].tolist()

            bjdqr2 : list[BjdInfo] = db.session.query(BjdInfo.법정동코드).filter(
                BjdInfo.법정동명.like('%'+keyword+'%')).all()

            bjd_list2:list =[tp[0] for tp in bjdqr2]

            return bjd_list
        except Exception as e:
            print('데이터 가져오기 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)

    def get_all_dong_keyword_list(self, sgg):
        try:
            dongqr : list[BjdInfo] = db.session.query(BjdInfo.법정동명).filter(
                BjdInfo.법정동명.like('%'+sgg+'%'))

            dongqr_list: list = pd.read_sql(dongqr.statement, dongqr.session.bind)['법정동명'].tolist()

            new_dong = []
            for sgg in dongqr_list:
                new_dong.append(sgg.split()[1])
            dongqr_list = list(set(new_dong))

            return dongqr_list
        except Exception as e:
            print('데이터 가져오기 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)

    def get_all_sigungu_keyword_list(self, city):
        try:

            sggqr : list[BjdInfo] = db.session.query(BjdInfo.법정동명).filter(
                BjdInfo.법정동명.like('%'+city+'%'))

            sgg_list: list = pd.read_sql(sggqr.statement, sggqr.session.bind)['법정동명'].tolist()

            new_sgg = []
            for sgg in sgg_list:
                new_sgg.append(sgg.split()[1])
            sgg_list = list(set(new_sgg))

            return sgg_list
        except Exception as e:
            print('데이터 가져오기 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)

    def get_apt_info_df(self, keyword, columns):

        try:
            # http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters
            from sqlalchemy import or_

            # http://docs.sqlalchemy.org/en/latest/orm/loading_columns.html#load-only-cols
            from sqlalchemy.orm import load_only
            aptqr : list[AptInfo]
            if not columns:
                aptqr = db.session.query(AptInfo).filter(or_(AptInfo.법정동주소.like('%'+keyword+'%'), AptInfo.도로명주소.like('%'+keyword+'%')))
            else:
                aptqr = db.session.query(AptInfo).options(load_only(*columns)).filter(or_(AptInfo.법정동주소.like('%'+keyword+'%'), AptInfo.도로명주소.like('%'+keyword+'%')))

            aptinfo_list_df = pd.read_sql(aptqr.statement, aptqr.session.bind).drop(columns=['index'])


            # 으어!!!!!! It takes 3 hours to find out!! Fuck!!!
            # need to now pandas from basic!!!
            # split is very very useful I think!!
            # https://stackoverflow.com/questions/14745022/how-to-split-a-column-into-two-columns
            # I want to try expand option.. but can't set it's columns name!
            z = aptinfo_list_df['사용승인일'].str.split('-').str[0].apply(func=lambda x: str(2018-int(x)))

            def extyear(series):
                return series['사용승인일'].str.split('-').str[0].apply(func=lambda x: str(2018-int(x)))

            # https://stackoverflow.com/a/49278320/5443084
            from datetime import datetime
            n = datetime.now()

            order = ["연번","아파트이름",	"법정동주소","연차","동수",	"세대수", "복도유형","관리사무소연락처",	"일차",	"요일",	"금액",	"문어발",	"장수",	"비고"]

            # reset index!! wow
            y = aptinfo_list_df \
                .assign(연차=lambda x: extyear(x),일차='',요일='',금액='',문어발='',장수='',비고='')\
                .drop(columns=['사용승인일'])\
                .reindex(columns=order)

            # set type
            y["연차"] = y["연차"].astype('int')
            y["동수"] = y["동수"].astype('int')
            y["세대수"] = y["세대수"].astype('int')

            # filterling by range
            # http://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/
            y = y.sort_values(by=['연차'], axis=0)

            # todo supply range selection interface
            # https://stackoverflow.com/questions/31617845/how-to-select-rows-in-a-dataframe-between-two-values-in-python-pandas
            # y = y[(y['연차'] >= 10) & (y['연차'] <= 15)].reset_index(drop=True)
            y = y[y['연차'] >= 16].reset_index(drop=True)

            # add index to new colums
            # https://stackoverflow.com/a/20461206/5443084
            # y.reindex(columns=order)
            y['연번'] = y.index
            print(y)

            return y
        except Exception as e:
            print('아파트 정보 가져오기 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)

    def insert_all_rows(self,aptinfo_list_df):

        from sqlalchemy.types import VARCHAR
        try:
            # df = pd.DataFrame(aptinfo_list_df)
            # set type
            # df["year"] = df["year"].astype('int')
            # df["miles"] = df["miles"].astype('int')
            # df["photos"] = df["photos"].astype('int')
            # df["video"] = df["video"].astype('int')
            # df["star"] = df["star"].astype('float')
            # df["review_no"] = df["review_no"].astype('int')
            # # df["price"] = df["price"].astype('int')
            aptinfo_list_df.to_sql(name="아파트정보", con=db.engine, if_exists='append',index_label='index', dtype={None:VARCHAR(5)})
            # dummy for debugging.
            a = 1;
        except Exception as e:
            print('데이터 가져오기 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)
