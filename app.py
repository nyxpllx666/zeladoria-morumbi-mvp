from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Dados fictícios em memória para o protótipo (simulando o PostgreSQL)
categorias = ["Saúde (UBS/UPA)", "Asfalto e Vias", "Iluminação Pública", "Lixo e Limpeza", "Outros"]
ocorrencias = [
    {"protocolo": "2026-0891", "data": "12/11/2026", "categoria": "Asfalto e Vias", "endereco": "Rua X, esquina com Y", "descricao": "Buraco enorme causando acidentes.", "status": "Nova"}
]

@app.route('/')
def index():
    # Tela 1: Formulário Principal
    return render_template('index.html', categorias=categorias)

@app.route('/enviar', methods=['POST'])
def enviar():
    # Ação de salvar a denúncia
    nova_ocorrencia = {
        "protocolo": f"2026-{random.randint(1000, 9999)}",
        "data": "12/11/2026",
        "categoria": request.form.get('categoria'),
        "endereco": request.form.get('endereco'),
        "descricao": request.form.get('descricao'),
        "status": "Nova"
    }
    ocorrencias.insert(0, nova_ocorrencia)
    return redirect(url_for('sucesso', protocolo=nova_ocorrencia['protocolo']))

@app.route('/sucesso')
def sucesso():
    # Tela 3: Alerta de Sucesso
    protocolo = request.args.get('protocolo')
    return render_template('sucesso.html', protocolo=protocolo)

@app.route('/admin')
def admin():
    # Tela 2: Painel Administrativo
    return render_template('admin.html', ocorrencias=ocorrencias, categorias=categorias)

if __name__ == '__main__':
    app.run(debug=True)