import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/Nandapagameupix")
def manda_o_pix():

    return "<h2>QUEM NÃO DEVE NÃO TEME!</h2>"


def init_db():

    with sqlite3.connect("database.db") as conn:

        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS LIVROS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    image_url TEXT NOT NULL
                )
            """
        )


init_db()


@app.route("/doar", methods=["POST"])
def doar():

    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:

        conn.execute(f"""
        INSERT INTO LIVROS (titulo, categoria, autor, image_url)
        VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
        """)

    conn.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201


@app.route("/livros", methods=["GET"])
def listar_livros():

    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()

        livros_formatados = []

        for item in livros:
            dicionario_livros = {
                "id": item[0],
                "titulo": item[1],
                "categoria": item[2],
                "autor": item[3],
                "image_url": item[4]
            }
            livros_formatados.append(dicionario_livros)

    return jsonify(livros_formatados), 200


@app.route("/editar/<int:id>", methods=["PUT"])
def atualizar_livros(id):
    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        atualizacao = []
        parametro = []
        if titulo:
            atualizacao.append("titulo = ?")
            parametro.append(titulo)
        if categoria:
            atualizacao.append("categoria = ?")
            parametro.append(categoria)
        if autor:
            atualizacao.append("autor = ?")
            parametro.append(autor)
        if image_url:
            atualizacao.append("image_url = ?")
            parametro.append(image_url)

        if not atualizacao:
            return jsonify({'erro': "Nenhum dado foi fornecido para atualizar"}),400
                    
        parametro.append(id)

        update_dados = f"UPDATE livros SET {','.join(atualizacao)} WHERE id = ?"
        cursor.execute(update_dados, parametro)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'erro': "Tem certeza sobre o que mudou? Não vi nada!"}), 404
    return jsonify({'mensagem': "Agora confiamos que está tudo certo!"}), 200
    

if __name__ == "__main__":

    app.run(debug=True)
