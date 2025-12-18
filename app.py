from flask import Flask, render_template, request

app = Flask(__name__)

# =========================
# トップ
# =========================
@app.route('/')
def index():
    return '''
    <h1>ロッカー管理システム</h1>
    <ul>
        <li><a href="/lockers/deposit">預け入れ</a></li>
        <li><a href="/lockers/retrieve">取り出し</a></li>
    </ul>
    '''


@app.route('/lockers/deposit')
def lockers_deposit():
   
    return render_template('lockers-deposit.html')


# =========================
# 取り出し（変更なし）
# =========================
@app.route('/lockers/retrieve')
def lockers_retrieve():
    return render_template('lockers-retrieve.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)