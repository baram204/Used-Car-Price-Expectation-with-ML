from flask import current_app
import pandas as pd
import pymysql

pymysql.install_as_MySQLdb()
# import MySQLdb

import numpy as np

from ..models.usedcar import UsedCar

from .modelhandler import ModelHandler

import _pickle as pickle  # encrypt

from collections import Counter


# 기계와 연관된 책임을 가진 클래스
class MachineHandler:
    def __init__(self):

        # pickle relative path
        # https://stackoverflow.com/questions/40416072/reading-file-using-relative-path-in-python-project/40416154
        import os.path
        path = os.path.abspath(os.path.dirname(__file__))
        self.pw_path = os.path.join(path, '../models/pw.plk')
        self.model_path = os.path.join(path, '../models/model.plk')
        self.columns_path = os.path.join(path, '../models/column.plk')
        self.target_list_path = os.path.join(path, '../models/target_list.plk')
        self.actual_car_info_path = os.path.join(path, '../models/actual_car_info.plk')
        self.database_path = os.path.join(path, '../models/database.plk')

    def load_plks(self):

        with open(self.pw_path, 'rb') as f:
            self.pw = pickle.load(f)

        # model = model.fit(X_train1, y_train1)
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        # Train 데이터의 컬럼이름들 (dummy 컬럼 + 숫자 컬럼 이름)
        # columns = pd.DataFrame(columns = [X_train1.columns])
        with open(self.columns_path, 'rb') as f:
            self.columns = pickle.load(f)
        # target_list = np.zeros_like(X_train.loc[0])
        with open(self.target_list_path, 'rb') as f:
            self.target_list = pickle.load(f)
        with open(self.actual_car_info_path, 'rb') as f:
            self.actual_car_info = pickle.load(f)
        with open(self.database_path, 'rb') as f:
            self.database = pickle.load(f)

        self.brand_group = list(set(self.database["brand"]))
        self.model_group = list(set(self.database["model"]))

    def pick_most_common_brands(self, train_df):
        brand_list = []
        for brand in Counter(train_df.brand).most_common(30):
            brand_list.append(brand[0])
        idx_list = []
        idx = 0
        for i in train_df["brand"]:
            if i not in brand_list:
                idx_list.append(idx)
            idx += 1
        train_df_dropped = train_df.drop(idx_list)
        train_df_dropped.reset_index(drop=True, inplace=True)
        train_df_dropped = train_df_dropped.drop("index", axis=1)

        return train_df_dropped

    def make_dummy_category_df(self, dataframe):
        categorical_features = ['brand', 'model']
        dummy_cat = pd.get_dummies(dataframe[categorical_features])
        return dummy_cat

    def make_normarize_number_df(self, dataframe):
        # numerical_features = ['year', 'miles', 'price']
        numerical_features = ['year','miles','price']
        normalize_num = np.log1p(dataframe[numerical_features])
        return normalize_num

    def merge_and_get_ingrediants(self, dummy_cat, normalize_num):
        # pre_train = pd.merge(normalize_num, dummy_cat)
        X_train_0 = normalize_num.join(dummy_cat)
        y_train = X_train_0["price"]
        X_train = X_train_0.drop("price", axis=1)

        from sklearn.model_selection import KFold
        from sklearn.cross_validation import train_test_split

        k_fold = KFold(n_splits=10, shuffle=True, random_state=2018)
        X_train1, X_test1, y_train1, y_test1 = train_test_split(X_train, y_train)

        return [X_train, y_train, X_train1, X_test1, y_train1, y_test1, k_fold]

    def get_learning_model(self, learning_ingrediants):
        li = learning_ingrediants

        from xgboost import XGBRegressor
        from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor

        X_train = li.X_train
        y_train = li.y_train
        y_train1 = li.y_train1
        y_test1 = li.y_test1
        k_fold = li.k_fold

        ml = XGBRegressor(n_estimators=1000, learning_rate=0.05, verbose=False)
        return ml

    # todo find linux time in windows, using magic % keword
    def check_learning_model_time(self, ml, learning_ingrediants):

        li = learning_ingrediants
        X_train = li.X_train
        y_train = li.y_train
        k_fold = li.k_fold
        from sklearn.model_selection import cross_val_score
        # %time score = cross_val_score(ml, X_train, y_train, cv=k_fold, n_jobs=-1, scoring="r2").mean()
        # score = "Score = {0:.5f}".format(score)
        score = "Score is dummy"
        return score

    def draw_plot(self, ml, X_test1, y_test1):

        from matplotlib import pyplot as plt
        y_pred = ml.predict(X_test1)
        plt.figure(figsize=(10, 5))
        plt.scatter(y_test1, y_pred, s=20)
        plt.title('Predicted vs. Actual')
        plt.xlabel('Actual Sale Price')
        plt.ylabel('Predicted Sale Price')

        plt.plot([min(y_test1), max(y_test1)], [min(y_test1), max(y_test1)])
        plt.tight_layout()

    def dump_database(self, dataframe):
        with open(self.database_path, 'wb') as f:
            pickle.dump(dataframe, f)

    def dump_ml(self, ml):
        with open(self.model_path, "wb") as f:
            pickle.dump(ml, f)

    def dump_actual_car_info(self, dataframe):
        with open(self.actual_car_info_path, "wb") as f:
            actual_car_info = dataframe[["brand", "model", "year", "miles", "price"]]
            pickle.dump(actual_car_info, f)

    def dump_columns(self, X_train1):
        columns = pd.DataFrame(columns=[X_train1.columns])
        pickle.dump(columns, open(self.columns_path, 'rb'))

    def dump_target_list(self, X_train):
        target_list = np.zeros_like(X_train.loc[0])
        pickle.dump(target_list, open(self.target_list_path, 'rb'))

    def expect_price(self, target_list, target, form, ml, actual_car_info):
        brand = str(form["brand"]).lower()
        model = str(form["model"]).lower()
        year = int(form["year"])
        miles = int(form["miles"])

        cdx = 0
        for col in target:
            if col == 'brand' + "_" + brand:
                break;
            cdx += 1
        cdx

        sdx = 0
        for col in target:
            if col == 'model' + "_" + model:
                break;
            sdx += 1
        sdx

        target_list[cdx] = 1
        target_list[sdx] = 1
        target_list[0] = year
        target_list[1] = miles

        for i in range(1):
            target.loc[i] = target_list

        numerical_features = ['year', 'miles']
        target[numerical_features] = np.log1p(target[numerical_features])

        price_log = ml.predict(target)
        price = np.exp(price_log)
        price = int(price)

        same_model = actual_car_info[actual_car_info["model"] == model]
        year_price = same_model[["year", "price"]]
        year_price_list = year_price.groupby("year").agg({'price': np.mean}).astype('int')
        year_price_list = year_price_list.reset_index()
        year_price_list["year"] = year_price_list["year"].apply(lambda x: str(x))
        year_price_list["price"] = year_price_list["price"].apply(lambda x: str(x))
        year_list = year_price_list["year"]
        price_list = year_price_list["price"]
        same_brand = actual_car_info[actual_car_info["brand"] == brand]
        same_brand = list(set(same_brand["model"]))
        same_brand.sort()

        result = {"status": 200, "price": price, "year_list": list(year_list), "price_list": list(price_list),
                  "same_brand": same_brand}

        return result
