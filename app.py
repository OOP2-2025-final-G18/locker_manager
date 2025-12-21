from flask import Flask, render_template, request
import datetime
 
app = Flask(__name__)
 
# --- 1. ロッカーの配置定義 (Lockerテーブル相当) ---
# row, col を指定することで11, 12番を右端に配置
lockers_info = {
    i: {"name": str(i), "row": (0 if i<=5 else 1)+1, "col": (i-1)%5+1} for i in range(1, 11)
}
lockers_info[11] = {"name": "11", "row": 1, "col": 7}
lockers_info[12] = {"name": "12", "row": 2, "col": 7}
 
# --- 2. 利用状況データ (LockerOperationテーブル相当) ---
# retrieve_at が None なら「使用中」、値があれば「空き」
operations = {
    2: {"password": "1234", "retrieve_at": None},
    9: {"password": "5678", "retrieve_at": None},
}
 
# 状態判定ヘルパー
def get_status(locker_id):
    op = operations.get(locker_id)
    if op and op["retrieve_at"] is None:
        return "occupied" # 使用中
    return "vacant" # 空き
 
@app.route('/')
def index():
    return render_template(
        'index.html',
        info=lockers_info,
        ops=operations,
        get_status=get_status
    )
 
# --- 預け入れルーティング ---
@app.route('/lockers/deposit', methods=['GET', 'POST'])
def lockers_deposit():
    target_id = None
    pin = None
    if request.method == 'POST':
        target_id = int(request.form.get('locker_id'))
        pin = request.form.get('pin')
        operations[target_id] = {"password": pin, "retrieve_at": None}
        print(f"【LOG】預入確定: {target_id}番, PIN: {pin}")
    return render_template('lockers-deposit.html', info=lockers_info, ops=operations,
                           get_status=get_status, target_id=target_id, pin=pin)
 
# --- 取り出しルーティング ---
@app.route('/lockers/retrieve', methods=['GET', 'POST'])
def lockers_retrieve():
    target_id = None
    passed_code = None
    if request.method == 'POST':
        target_id = int(request.form.get('locker_id'))
        passed_code = request.form.get('passcode')
        # 取り出し完了処理
        
        if target_id in operations:
            operations[target_id]["retrieve_at"] = datetime.datetime.now()
        print(f"【LOG】取出実行: {target_id}番, 入力PIN: {passed_code}")
    return render_template('lockers-retrive.html', info=lockers_info, ops=operations,
                           get_status=get_status, target_id=target_id, passed_code=passed_code)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
 