from flask import current_app

from project import db
from sqlalchemy.schema import CreateSchema
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

import _pickle as pickle  # encrypt

import pandas as pd

from ..models.usedcar import UsedCar


# 크로울 다루는 책임을 가진 클래스
class ModelHandler():
    # constructor take <class 'bs4.element.Tag'>


    def testdb(self):
        try:
            UsedCar.query.all()

            return '<h1>It works.</h1>'
        except Exception as e:
            print('테스트 sql 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)

    def create_schemas(self):
        """ Note that this function run a SQL Statement available just in
            PostgreSQL 9.3+
        """

        db.session.execute(CreateSchema('used_car'))
        # db.session.execute('CREATE SCHEMA IF NOT EXISTS used_car')

        db.session.commit()

    def createtable(self):

        try:
            self.create_schemas()
            db.session.execute()
            db.session.commit()
        except:
            a = 1  # todo remove meaningless ..

        try:
            from ..models.usedcar import UsedCar

            db.create_all()
            return '<h1>It works.</h1>'
        except Exception as e:
            print('테이블 생성 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)

    def insert_all_rows(self, rows):

        try:
            df = pd.DataFrame(rows)

            # prevent empty
            # what is this code do?
            df = df[df["price"] != ""]
            df = df[df["brand"] != ""]

            # set type
            df["year"] = df["year"].astype('int')
            df["miles"] = df["miles"].astype('int')
            df["photos"] = df["photos"].astype('int')
            df["video"] = df["video"].astype('int')
            df["star"] = df["star"].astype('float')
            df["review_no"] = df["review_no"].astype('int')
            df["price"] = df["price"].astype('int')

            df.to_sql(name="used_car", con=db.engine, if_exists='replace')
            return '<h1>It works.</h1>'
        except Exception as e:
            print('데이터 삽입 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)

    def get_df_has_all(self):

        try:
            # https://beomi.github.io/2017/10/21/SQLAlchemy-Query-to-Pandas-DataFrame/
            # query means all records
            queryset = UsedCar.query
            # use sqlalchemy's statement & session.
            df = pd.read_sql(queryset.statement, queryset.session.bind)
            return df
        except Exception as e:
            print('데이터 삽입 오류')
            print(e.args)
            return '<h1>Something is broken.</h1>' + str(e.args)
