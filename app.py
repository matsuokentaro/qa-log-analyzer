from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>QA Log Analyzer</h1>

    <form action="/analyze" method="post" enctype="multipart/form-data">
        <input type="file" name="logfile">
        <input type="submit" value="解析">
    </form>
    """

@app.route("/analyze", methods=["POST"])
def analyze():

    logfile = request.files["logfile"]

    content = logfile.read().decode("utf-8")

    lines = content.splitlines()

    error_lines = []
    warning_lines = []

    warning_count = 0

    for line in lines:

        if "ERROR" in line:
            error_lines.append(line)

        if "WARNING" in line:
            warning_count += 1
            warning_lines.append(line)


    total_lines = len(lines)

    error_count = len(error_lines)

    error_rate = round((error_count / total_lines) * 100, 1)

    error_html = ""

    for error in error_lines:
        error_html += f'<li class="error-card">{error}</li>'

    warning_html = ""

    for warning in warning_lines:
        warning_html += f"""
        <li class="warning-card">
        {warning}
        </li>
    """

    return f"""
    <html>
    <head>
    <link rel="stylesheet" href="/static/style.css">

    <h1 style="color:#333;text-align:center;">QA Log Analyzer</h1>

    <p>
    ログファイルを解析し、
    ERROR・WARNINGを集計します。
    </p>
    </head>

    <body style=" font-family: Arial;
    background-color:#f4f6f9;
    padding:30px;
    max-width:1200px;
    margin:auto;">



    <div style="
        display:flex;
        gap:20px;
        margin-bottom:30px;
    ">

        <div style="
            background:white;
            padding:20px;
            width:200px;
            border-radius:10px;
            box-shadow:0 2px 5px rgba(0,0,0,0.2);
        ">
            <h3>📄 総ログ数</h3>
            <h2>{total_lines}</h2>
        </div>

        <div style="
            background:#ff4d4d;
            color:white;
            padding:20px;
            width:200px;
            border-radius:10px;
            box-shadow:0 2px 5px rgba(0,0,0,0.2);
        ">
            <h3>❌ ERROR</h3>
            <h2>{error_count}</h2>
        </div>

        <div style="
            background:#ffc107;
            padding:20px;
            width:200px;
            border-radius:10px;
            box-shadow:0 2px 5px rgba(0,0,0,0.2);
        ">
            <h3>⚠️ WARNING</h3>
            <h2>{warning_count}</h2>
        </div>

        <div style="
            background:#28a745;
            color:white;
            padding:20px;
            width:200px;
            border-radius:10px;
            box-shadow:0 2px 5px rgba(0,0,0,0.2);
        ">
            <h3>📊 エラー率</h3>
            <h2>{error_rate}%</h2>
        </div>

    </div>

    <h2>🚨 エラー一覧</h2>

    <ul style="padding:0;">
        {error_html}
    </ul>

    <h2>⚠️ WARNING一覧</h2>

    <ul style="padding:0;">
        {warning_html}
    </ul>

    <a href="/"style="background:#007bff;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;">戻る</a>

</body>
</html>
    """
if __name__ == "__main__":
    app.run(debug=True)
