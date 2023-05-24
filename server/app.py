from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

# 需要返回六个数组：
#     实际值
#     预测上限
#     预测下限
#     日期
#     状态

# 后端返回api包括
#     文件名称
#     预测步长
#     具体数据

# configuration
DEBUG = True

# instantiate the app and enable CORS
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

point_end = 10801
periods = {"futureDay": 30 * 24, "futureWeek": 30 * 24 * 7, "futureMonth": 30 * 24 * 30,
           "futureSixMonths": 30 * 24 * 30 * 6}
num = 6
time = "futureDay"

sheets = ["test-aiops-hbase-203", "test-bpfp-bs-engine2-ft", "test-rr_offline_qf_cluster"]
sheet_num = 0
sheet_time = "futureWeek"
sheet_periods = {"futureDay": 1, "futureWeek": 7, "futureMonth": 30,
                 "futureHalfMonths": 15}


# excel文件路径
def getpath(num):
    if num in range(1, 10):
        path = "0" + str(num)
    else:
        path = str(num)
    result_path = r"final_data\0{}-result.csv".format(path)
    return result_path


# csv文件转为json
def csv2json():
    result_path = getpath(num)
    result = pd.read_csv(result_path)[:point_end]
    date, predict, predict_lower, predict_upper, raw_data, status = result["ds"], result["yhat"], result["yhat_lower"], \
                                                                    result["yhat_upper"], result["raw_data"].dropna(), \
                                                                    result[
                                                                        "status"].dropna()
    dic = {"date": date.tolist(), "predict": predict.tolist(), "predict_lower": predict_lower.tolist(),
           "predict_upper": predict_upper.tolist(), "raw_data": raw_data.tolist(), "status": status.tolist()}
    return dic


# 得到csv文件中的异常值
def get_outliner():
    result_path = getpath(num)
    error_path = result_path.replace("result", "outliner")
    outliners = pd.read_csv(error_path)[:point_end]
    outliners["id"] = range(1, len(outliners) + 1)
    json_list = []
    cols = ["id", "ds", "raw_data", "status"]
    for row in outliners.itertuples():
        json_dict = {}
        for index in range(0, 4):
            json_dict[cols[index]] = getattr(row, cols[index])
        json_list.append(json_dict)

    return json_list


# 通过不同的预测时间步长返回不同的预测数据
def fetchByTime():
    result_path = getpath(num)
    result = pd.read_csv(result_path)[:(point_end + periods[time])]
    date, predict, predict_lower, predict_upper, raw_data, status = result["ds"], result["yhat"], result["yhat_lower"], \
                                                                    result["yhat_upper"], result["raw_data"].dropna(), \
                                                                    result[
                                                                        "status"].dropna()
    dic = {"date": date.tolist(), "predict": predict.tolist(), "predict_lower": predict_lower.tolist(),
           "predict_upper": predict_upper.tolist(), "raw_data": raw_data.tolist(), "status": status.tolist()}
    return dic


# 通过改变文件索引，返回不同的预测数据
def fetchByNum():
    data_path = r"data-3.1\{}.csv".format(sheets[sheet_num])
    data = pd.read_csv(data_path)
    count = len(data["actual"].dropna())
    data = data[:count]
    date, predict, actual = data["ds"], data["predict"], data["actual"].dropna()
    dic = {"date": date.tolist(), "predict": predict.tolist(), "actual": actual.tolist()}
    return dic


# 通过改变预测步长，返回不同的预测数据
def fetchByPeriod():
    data_path = r"data-3.1\{}.csv".format(sheets[sheet_num])
    data = pd.read_csv(data_path)
    count = len(data["actual"].dropna())
    data = data[:(count + sheet_periods[sheet_time])]
    date, predict, actual = data["ds"], data["predict"], data["actual"].dropna()
    dic = {"date": date.tolist(), "predict": predict.tolist(), "actual": actual.tolist()}
    return dic


# 3.2-文件索引
@app.route('/data', methods=['GET', 'POST'])
def data():
    response = {}
    if request.method == "GET":
        response['all_data'] = csv2json()
        response['outliner'] = get_outliner()
    elif request.method == "POST":
        global num
        post_data = request.get_json()
        num = post_data.get("num")
        response['all_data'] = csv2json()
        response['outliner'] = get_outliner()
    return jsonify(response)


# 3.2-时间步长
@app.route("/period", methods=["POST", "GET"])
def period():
    response = {}
    global sheet_time
    if request.method == "GET":
        response['all_data'] = fetchByTime()
    elif request.method == "POST":
        post_data = request.get_json()
        sheet_time = post_data.get("sheet_time")
        response["all_data"] = fetchByTime()
    return jsonify(response)


# 3.1-文件索引
@app.route("/predict", methods=["POST", "GET"])
def predict():
    response = {}
    global sheet_num
    if request.method == "GET":
        response['all_data'] = fetchByNum()
        response["name"] = sheets[sheet_num]
    elif request.method == "POST":
        post_data = request.get_json()
        sheet_num = post_data.get("sheet_num")
        response["all_data"] = fetchByNum()
        response["name"] = sheets[sheet_num]
    return jsonify(response)


# 3.1-时间步长
@app.route("/sheet_period", methods=["POST", "GET"])
def sheet_period():
    response = {}
    global sheet_time
    if request.method == "GET":
        response['all_data'] = fetchByPeriod()
        response["name"] = sheets[sheet_num]
    elif request.method == "POST":
        post_data = request.get_json()
        sheet_time = post_data.get("sheet_time")
        response["all_data"] = fetchByPeriod()
        response["name"] = sheets[sheet_num]
    return jsonify(response)


if __name__ == '__main__':
    app.run()
