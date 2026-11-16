import pytest
from app import app, categorias, ocorrencias

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- TESTES UNITÁRIOS ---
def test_categorias_iniciais():
    assert "Saúde (UBS/UPA)" in categorias
    assert "Asfalto e Vias" in categorias
    assert len(categorias) == 5

def test_estrutura_ocorrencia_inicial():
    assert len(ocorrencias) >= 1
    assert "protocolo" in ocorrencias[0]
    assert "status" in ocorrencias[0]

# --- TESTES DE INTEGRAÇÃO ---
def test_rota_inicial_status_200(client):
    resposta = client.get('/')
    assert resposta.status_code == 200
    assert b"Associa" in resposta.data

def test_envio_ocorrencia_e_redirecionamento(client):
    dados = {
        "categoria": "Asfalto e Vias",
        "endereco": "Av. Mário Filho, 1500",
        "descricao": "Teste automatizado de buraco na via"
    }
    resposta = client.post('/enviar', data=dados, follow_redirects=True)
    assert resposta.status_code == 200
    assert b"Protocolo:" in resposta.data
    assert any(oc["endereco"] == "Av. Mário Filho, 1500" for oc in ocorrencias)

def test_painel_admin_exibe_ocorrencia(client):
    resposta = client.get('/admin')
    assert resposta.status_code == 200
    assert b"Av. M" in resposta.data