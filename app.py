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


# =========================
# ロッカー：預け入れ
# =========================
@app.route('/lockers/deposit', methods=['GET', 'POST'])
def lockers_deposit():
    if request.method == 'POST':
        pin = request.form.get('pin')
        print('【預け入れ】暗証番号:', pin)

        # 2画面目を表示
        return render_template(
            'lockers-deposit.html',
            show_screen='screen2'
        )

    # 1画面目を表示
    return render_template(
        'lockers-deposit.html',
        show_screen='screen1'
    )


# =========================
# ロッカー：取り出し
# =========================
@app.route('/lockers/retrieve')
def lockers_retrieve():
    return render_template('lockers-retrive.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)