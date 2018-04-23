#################
#### imports ####
#################

from flask import render_template, jsonify, json, request, app
from . import usedcar_blueprint

from .util.crawlhandler import CrawlHandler
from .util.modelhandler import ModelHandler
from .util.machinehandler import MachineHandler

md = ModelHandler()
cr = CrawlHandler()
mc = MachineHandler()

################
#### routes ####
################

@usedcar_blueprint.route('/')
def usedcar_init():
    return render_template('/usedcar/index.html', )

@usedcar_blueprint.route('/createtable')
def createtable():
    print('테이블 생성 진입')
    return md.createtable()

@usedcar_blueprint.route('/crawldata/<int:start>/<int:end>')
def crawldata(start, end):

    md.createtable()

    ch = CrawlHandler()

    if start is None or end is None:
        rows = ch.get_rows(1, 3)
    else:
        rows = ch.get_rows(start, end)

    result = md.insert_all_rows(rows)
    return result



@usedcar_blueprint.route('/dotrain')
def do_train():

    train_df = md.get_df_has_all()
    # return train_df.to_json()
    mc.dump_database(train_df)
    train_df_dropped = mc.pick_most_common_brands(train_df)

    shape = train_df_dropped.shape
    #return str(shape) # (0, 15)

    mc.dump_actual_car_info(train_df_dropped)

    dummy_df = mc.make_dummy_category_df(train_df_dropped)
    number_df = mc.make_normarize_number_df(train_df_dropped)



    return 'dh'

    # #  return [X_train,y_train , X_train1, X_test1, y_train1, y_test1, k_fold]
    # learning_ingrediants = mc.merge_for_base_train_(dummy_df,number_df)
    #
    # # colmuns will use as target
    # mc.dump_target_list(learning_ingrediants.X_train1)
    # mc.dump_columns(learning_ingrediants.X_train1)
    #
    # ml = mc.get_learning_model(learning_ingrediants)
    # # score = mc.check_learning_model_time(ml, learning_ingrediants)
    # mc.dump_ml(ml)


# API
@usedcar_blueprint.route("/predict/" , methods=["POST"])
def predict():
    from flask import request, jsonify
    import numpy as np
    import pandas as pd
    import _pickle as pickle  # encrypt

    mc.load_plks()

    ml = mc.model
    columns = mc.columns
    target_list = mc.target_list
    actual_car_info = mc.actual_car_info
    database = mc.database

    target = pd.DataFrame(columns = columns)

    brand = request.values.get("brand")
    model = request.values.get("model")
    year = request.values.get("year")
    miles = request.values.get("miles")

    brand = str(brand).lower()
    model = str(model).lower()
    year = int(year)
    miles = int(miles)

    cdx = 0
    for col in columns:
        if col == 'brand'+"_"+brand:
            break;
        cdx += 1

    sdx = 0
    for col in columns:
        if col == 'model'+"_"+model:
            break;
        sdx += 1

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

    same_model = actual_car_info[actual_car_info["model"]==model]
    year_price = same_model[["year", "price"]]
    year_price_list = year_price.groupby("year").agg({'price':np.mean}).astype('int')
    year_price_list = year_price_list.reset_index()
    year_price_list["year"] = year_price_list["year"].apply(lambda x: str(x) )
    year_price_list["price"] = year_price_list["price"].apply(lambda x: str(x) )
    year_list = year_price_list["year"]
    price_list = year_price_list["price"]
    same_brand = actual_car_info[actual_car_info["brand"]==brand]
    same_brand = list(set(same_brand["model"]))
    same_brand.sort()


    result = {"status": 200, "price":price, "year_list": list(year_list), "price_list":list(price_list), "same_brand":same_brand}
    print(result)
    return jsonify(result)






