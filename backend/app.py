from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
# Essencial: Libera o Nginx para conversar com o Python
CORS(app)

MOCK_API_URL = "https://69d1e3825043d95be9714026.mockapi.io/pessoas/Pessoas"

@app.route('/api/pessoas', methods=['GET'])
def get_pessoas():
    try:
        response = requests.get(MOCK_API_URL)
        response.raise_for_status()
        dados = response.json()

        clientes = []
        funcionarios = []

        for p in dados:
            # 1. Pega a categoria não importa como o Faker ou você salvou
            cat_bruta = p.get('Categoria') or p.get('categoria') or ""
            cat = str(cat_bruta).strip().lower()

            # 2. Cria um registro limpo (Prioriza Maiúsculas, depois minúsculas, depois fallback)
            registro_limpo = {
                "id":       p.get("id"),
                "Nome":     p.get("Nome")     or p.get("nome")     or "Desconhecido",
                "CPF":      p.get("CPF")      or p.get("cpf")      or "Sem CPF",
                "CEP":      p.get("CEP")      or p.get("cep")      or "-",
                "Telefone": p.get("Telefone") or p.get("telefone") or "-"
            }

            # 3. Separa nas listas corretas
            if 'cliente' in cat or 'tinderbox' in cat:
                clientes.append(registro_limpo)
            elif 'funcionario' in cat or 'funcionário' in cat or 'mobility' in cat:
                funcionarios.append(registro_limpo)
            else:
                # ✅ CORREÇÃO: Categoria desconhecida gerada pelo Faker
                # Loga o valor inesperado para facilitar o debug
                # e usa Clientes como fallback para não perder o registro
                print(f"[AVISO] Categoria desconhecida: '{cat_bruta}' — ID {p.get('id')} jogado em Clientes como fallback")
                clientes.append(registro_limpo)

        return jsonify({
            "clientes":     clientes,
            "funcionarios": funcionarios
        })

    except Exception as e:
        print(f"Erro no GET: {e}")
        return jsonify({"erro": str(e)}), 500


@app.route('/api/pessoas', methods=['POST'])
def salvar_pessoa():
    try:
        novo_registro = request.json
        print(f"Recebido do Formulário: {novo_registro}")

        response = requests.post(MOCK_API_URL, json=novo_registro)
        response.raise_for_status()

        return jsonify(response.json()), 201

    except Exception as e:
        print(f"Erro no POST: {e}")
        return jsonify({"erro": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)