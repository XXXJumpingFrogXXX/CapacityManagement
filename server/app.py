from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

# 需要返回六个数组：
#     实际值\\
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
periods = {"futureDay": 30 * 24, "futureWeek": 30 * 24 * 7, "futureHalfMonth": 30 * 24 * 15, "futureMonth": 30 * 24 * 30}
num = 6
time = "futureDay"


def getpath(num):
    if num in range(1, 10):
        path = "0" + str(num)
    else:
        path = str(num)
    result_path = r"final_data\0{}-result.csv".format(path)
    return result_path


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


def get_outliner():
    result_path = getpath(num)
    error_path = result_path.replace("result", "outliner")
    outliners = pd.read_csv(error_path)[:point_end]
    outliners["id"] = range(1, len(outliners)+1)
    json_list = []
    cols = ["id", "ds", "raw_data", "status"]
    for row in outliners.itertuples():
        json_dict = {}
        for index in range(0, 4):
            json_dict[cols[index]] = getattr(row, cols[index])
        json_list.append(json_dict)

    return json_list


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


# sanity check route
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


@app.route("/period", methods=["POST", "GET"])
def period():
    response = {}
    global time
    if request.method == "GET":
        response['all_data'] = fetchByTime()
    elif request.method == "POST":
        post_data = request.get_json()
        time = post_data.get("time")
        response["all_data"] = fetchByTime()
    return jsonify(response)


if __name__ == '__main__':
    app.run()
