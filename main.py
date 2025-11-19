from flask import Flask, render_template, request, redirect, session
import sqlite3
import calendar
from datetime import datetime

app = Flask(__name__)
app.secret_key = "senha_solicitada"

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "visitante" in request.form:
            session.pop("admin", None)  # garante que não é admin
            return redirect("/agenda")  

        senha = request.form["senha"]
        if senha == "elizete":
            session["admin"] = True
            return redirect("/")  
        else:
            return "Senha incorreta, tente novamente."

    return render_template("login.html")

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/ajuda")
def ajuda():
    return render_template("ajuda.html")

# ---------- NOVO EVENTO ----------
@app.route("/novo_evento", methods=["GET", "POST"])
def novo_evento():
    if not session.get("admin"):
        return redirect("/login")  

    if request.method == "POST":
        data = request.form["data"]
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]

        con = get_db()
        con.execute(
            "INSERT INTO eventos (data, titulo, descricao) VALUES (?, ?, ?)",
            (data, titulo, descricao)
        )
        con.commit()
        con.close()

        return redirect("/agenda")

    return """
    <form method="POST" style='margin:50px; font-size:18px;'>
        <label>Data:</label><br>
        <input type="date" name="data"><br><br>

        <label>Título:</label><br>
        <input type="text" name="titulo"><br><br>

        <label>Descrição:</label><br>
        <textarea name="descricao"></textarea><br><br>

        <button>Salvar Evento</button>
    </form>
    """

# ---------- AGENDA (ÚNICA ROTA) ----------
@app.route("/agenda")
def agenda():
    calendario_html, eventos, mes_nome, ano = preparar_agenda()
    mostrar_botao = session.get("admin", False)  # True se for admin, False se visitante
    return render_template("agenda.html",
                           mostrar_botao=mostrar_botao,
                           calendario_html=calendario_html,
                           eventos=eventos,
                           mes_nome=mes_nome,
                           ano=ano)

# ---------- FUNÇÕES AUXILIARES ----------
def preparar_agenda():
    con = get_db()
    eventos_db = con.execute("SELECT * FROM eventos").fetchall()
    con.close()
    eventos = {e["data"]: e for e in eventos_db}

    ano = datetime.now().year
    mes = datetime.now().month

    nome_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    mes_nome = nome_meses[mes - 1]

    calendario_html = gerar_calendario(ano, mes, eventos)

    return calendario_html, eventos, mes_nome, ano

def get_db():
    con = sqlite3.connect("agenda.db")
    con.row_factory = sqlite3.Row
    return con

def gerar_calendario(ano, mes, eventos=None):
    if eventos is None:
        eventos = {}

    cal = calendar.Calendar(firstweekday=6)
    semanas = cal.monthdatescalendar(ano, mes)

    html = '<table class="calendario">'
    html += '<tr>'
    for dia in ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]:
        html += f"<th>{dia}</th>"
    html += '</tr>'

    for semana in semanas:
        html += "<tr>"
        for dia in semana:
            data_str = dia.strftime("%Y-%m-%d")
            if dia.month != mes:
                html += f'<td style="background:#f5f5f5">{dia.day}</td>'
                continue

            html += "<td>"
            html += f"<div>{dia.day}</div>"

            if data_str in eventos:
                ev = eventos[data_str]
                html += f"""
                <div class='evento'>
                    <strong>{ev['titulo']}</strong><br>
                    {ev['descricao']}
                </div>
                """

            html += "</td>"
        html += "</tr>"

    html += "</table>"
    return html

if __name__ == '__main__':
    app.run(debug=True)
