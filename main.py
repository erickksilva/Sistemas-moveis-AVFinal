import os
from flask import Flask, request, render_template
import json
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['GET'])
def raiz():
    return render_template('index.html')


#LISTA
@app.route('/pessoas/token=12345qwert', methods=['GET'])
def pessoas():

    con = sqlite3.connect('ado.db')
    print("Banco de dados aberto com sucesso")
    lista = con.cursor()

    lista.execute('''SELECT * FROM pessoa;''')
    result = lista.fetchall()

    con.commit()

    con.close()

    return json.dumps(result)


#inserir pessoa
@app.route('/alocarpessoa/token=12345qwert')
def alocarpessoa():
    return render_template('pessoa.html')


#alocando uma nova pessoa no BD
@app.route('/novapessoa', methods=['POST', 'GET'])
def novapessoa():
    msg = "msg"
    if request.method == 'POST':
        try:
            nome = request.form["nome"]
            sobrenome = request.form["sobrenome"]
            cpf = request.form["cpf"]
            email = request.form["email"]
            

            with sqlite3.connect("ado.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO pessoa (nome,sobrenome,cpf,email) VALUES (?,?,?,?)",
                    (nome, sobrenome, cpf, email))
                con.commit()
                msg = "Inserção feita com sucesso"
        except:
            con.rollback()
            msg = "Erro ao inserir operação"
        finally:
            return render_template("result.html", msg=msg)
            con.close()
          
#Remover pessoa por CPF
@app.route('/removepessoa/token=12345qwert/<int:cpf>', methods=['GET'])
def removerpessoa(cpf):
    con = sqlite3.connect('ado.db')
    lista = con.cursor()
    lista2 = con.cursor()
    lista.execute('DELETE from pessoa where cpf = %d;' % cpf)
    lista2.execute('''SELECT * FROM pessoa;''')
    result = lista2.fetchall()
    con.commit()

    con.close()
    return json.dumps(result)


#Pesquisa por CPF
@app.route('/pessoa/token=12345qwert/<int:cpf>', methods=['GET'])
def pessoacpf(cpf):
  
    con = sqlite3.connect('ado.db')
    lista = con.cursor()
    lista2 = con.cursor()
    lista.execute('SELECT * FROM pessoa where cpf = %d;' % cpf)
    lista2.execute('''SELECT * FROM pessoa;''')
    result = lista.fetchall()
    con.commit()

    con.close()

  
    return json.dumps(result)
  


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
