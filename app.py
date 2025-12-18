from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# =========================
# トップ（なくてもいいが動作確認用）
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


# =========================
# ロッカー：預け入れ
# =========================
@app.route('/lockers/deposit', methods=['GET', 'POST'])
def lockers_deposit():
    if request.method == 'POST':
        pin = request.form.get('pin')
        print('【預け入れ】暗証番号:', pin)

        # POST時は screen2 を表示
        return render_template(
            'lockers-deposit.html',
            screen='processing'
        )

    # GET時は screen1 を表示
    return render_template(
        'lockers-deposit.html',
        screen='input'
    )


# =========================
# ロッカー：取り出し
# =========================
@app.route('/lockers/retrieve', methods=['GET'])
def lockers_retrieve():
    return render_template('lockers-retrive.html')


@app.route('/lockers/retrieve/done', methods=['POST'])
def lockers_retrieve_done():
    passcode = request.form.get('passcode')

    # 動作確認用
    print('【取り出し】暗証番号:', passcode)

    return '''
    <h2>取り出し完了</h2>
    <a href="/">トップへ戻る</a>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)