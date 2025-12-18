from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

# ==========================================
# 1. ロッカーの初期状態管理 (Loop資料準拠)
# ==========================================
# 配置情報: 11, 12番は右端(col:7)に配置
lockers_info = {
    i: {"name": str(i), "row": (0 if i<=5 else 1)+1, "col": (i-1)%5+1} for i in range(1, 11)
}
lockers_info[11] = {"name": "11", "row": 1, "col": 7}
lockers_info[12] = {"name": "12", "row": 2, "col": 7}

# 利用状況シミュレーション (retrieve_at が None なら使用中)
# 初期状態で 2番と 9番を使用中に設定
operations = {
    2: {"password": "1234", "deposit_at": "2025-12-18 10:00", "retrieve_at": None},
    9: {"password": "5678", "deposit_at": "2025-12-18 11:00", "retrieve_at": None},
}

# 状態判定ヘルパー関数
def get_locker_status(locker_id):
    op = operations.get(locker_id)
    if op and op["retrieve_at"] is None:
        return "occupied" # 使用中(青/灰)
    return "vacant" # 空き(緑)

# =========================
# 2. 各ページルーティング
# =========================

@app.route('/')
def index():
    return '''
    <h1>ロッカー管理システム</h1>
    <ul>
        <li><a href="/lockers/deposit">預け入れ </a></li>
        <li><a href="/lockers/retrieve">取り出し　</a></li>
    </ul>
    '''

# --- 預け入れ ---
@app.route('/lockers/deposit', methods=['GET', 'POST'])
def lockers_deposit():
    # operations は関数の外で定義されたグローバル変数である必要があります
    global operations 
    
    target_id = None
    pin = None
    
    if request.method == 'POST':
        # フォームからデータを受け取る
        target_id = int(request.form.get('locker_id'))
        pin = request.form.get('pin')
        
        # データを更新（retrieve_at を None にすることで「使用中」にする）
        operations[target_id] = {
            "password": pin, 
            "deposit_at": datetime.datetime.now(), 
            "retrieve_at": None
        }
        return render_template('lockers-deposit.html', info=lockers_info, ops=operations, target_id=target_id, pin=pin)

    return render_template('lockers-deposit.html', info=lockers_info, ops=operations)
# --- 取り出し ---
@app.route('/lockers/retrieve', methods=['GET', 'POST'])
def lockers_retrieve():
    target_id = None
    passed_code = None
    if request.method == 'POST':
        target_id = int(request.form.get('locker_id'))
        passed_code = request.form.get('passcode')
        
        # 【注意事項対応】コンソールに暗証番号を表示
        print(f"【LOG】取り出し実行 - ID: {target_id}, 入力PIN: {passed_code}")
        
        # 取り出し処理 (retrieve_atを更新して空きにする)
        if target_id in operations:
            operations[target_id]["retrieve_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return render_template('lockers-retrive.html', 
                           info=lockers_info, 
                           get_status=get_locker_status,
                           target_id=target_id,
                           passed_code=passed_code,
                           page_type='retrieve')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)