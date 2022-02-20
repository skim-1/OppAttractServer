from flask import Flask, request, jsonify
from flask_cors import cross_origin
import json

app = Flask(__name__)

def cast_sum(arr):
    s = 0
    for i in range(len(arr)):
        s+=int(arr[i])
    return s


def import_json():
    with open('./profile.json') as f:
        return json.load(f)


def dump_json(injson):
    with open('./profile.json', 'w') as f:
        json.dump(injson, f)


@app.route('/')
def index():
    return "<h1>Opposites Attract API</h1>"


@app.route('/edit-profile', methods=['POST'])
@cross_origin()
def edit_profile():
    if request.method == 'POST':
        f = dict(request.json)

        user_exists = False

        to_dump = import_json()
        for i in range(1, len(to_dump["users"]) + 1):
            if f["name"] == to_dump["users"][i]["name"]:
                user_exists = True
                to_dump["users"][i] = f
                break

        if not user_exists:
            to_dump["users"].append(f)

        dump_json(to_dump)

        return jsonify(to_dump)


@app.route('/friends', methods=['GET', 'POST'])
@cross_origin()
def friends_priority_list():
    if request.method == 'POST':
        f = dict(request.json)
        score = cast_sum(f["answers"])

        to_dump = dict(import_json())
        items = to_dump["users"]
        print(items)
        prioritized = sorted(items, key=lambda user: abs(score - cast_sum(user["answers"])))
        # prioritized = []
        # cin = 0
        # for x in items:
        #     for x in items:
        #         if x["order"] == cin:
        #             prioritized.append(x)
        #     cin += 1
        for i in range(len(prioritized)):
            prioritized[i]["order"] = i + 1

        dump_json({"users" : prioritized})
        return jsonify({"users" : prioritized})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)