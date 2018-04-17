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
    return render_template('index.html', )

@usedcar_blueprint.route('/createtable')
def createtable():
    print('테이블 생성 진입')
    return md.createtable()

@usedcar_blueprint.route('/crawldata/<int:start>/<int:end>')
def crawldata(start, end):
    ch = CrawlHandler()

    if start is None or end is None:
        rows = ch.get_rows(1, 3)
    else:
        rows = ch.get_rows(start, end)

    md.insert_all_rows(rows)

@usedcar_blueprint.route('/dotrain')
def do_train():

    train_df = md.get_df_has_all()
    mc.dump_database(train_df)
    most_df = mc.pick_most_common_brands(train_df)
    mc.dump_actual_car_info(most_df)

    dummy_df = mc.make_dummy_category_df(most_df)
    number_df = mc.make_normarize_number_df(most_df)
    #  return [X_train,y_train , X_train1, X_test1, y_train1, y_test1, k_fold]
    learning_ingrediants = mc.merge_for_base_train_(dummy_df,number_df)

    # colmuns will use as target
    mc.dump_target_list(learning_ingrediants.X_train1)
    mc.dump_columns(learning_ingrediants.X_train1)

    ml = mc.get_learning_model(learning_ingrediants)
    # score = mc.check_learning_model_time(ml, learning_ingrediants)
    mc.dump_ml(ml)


@usedcar_blueprint.route('/predict/', methods=["POST"])
def expect_price():

    print('come predict')
    # brand = request.values.get("brand")
    # model = request.values.get("model")
    # year = request.values.get("year")
    # miles = request.values.get("miles")
    form = request.form

    mc.load_plks()

    target = mc.columns
    print(type(target))
    target_list = mc.target_list
    ml = mc.model
    actual_car_info = mc.actual_car_info
    # {"status": 200, "price":price, "year_list": list(year_list), "price_list":list(price_list), "same_brand":same_brand}
    result = mc.expect_price(target_list,target,form,ml, actual_car_info)

    return jsonify(result)






