# if no need subclassing, cPickle shows better speed.


# plk is password safe lock files.

# model
# model = model.fit(X_train1, y_train1)
def init():
    with open("./models/model.plk","rb") as f:
        global ml
        ml = pickle.load(f)

# Train 데이터의 컬럼이름들 (dummy 컬럼 + 숫자 컬럼 이름)
# columns = pd.DataFrame(columns = [X_train1.columns])
def columns():
    with open("./models/column.plk","rb") as c:
        global columns
        columns = pickle.load(c)

# target_list = np.zeros_like(X_train.loc[0])
def target_list():
    with open("./models/target_list.plk","rb") as t:
        global target_list
        target_list = pickle.load(t)

def actual_car_info():
    with open("./models/actual_car_info.plk","rb") as a:
        global actual_car_info
        actual_car_info = pickle.load(a)

def database():
    with open("./models/database.plk","rb") as d:
        global database
        database = pickle.load(d)

init()
columns()
target_list()
actual_car_info()
database()

brand_group = list(set(database["brand"]))
model_group = list(set(database["model"]))