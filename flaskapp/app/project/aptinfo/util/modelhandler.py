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
