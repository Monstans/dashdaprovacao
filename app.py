from flask import Flask, render_template, request, session, redirect, url_for
import json
import os
import mysql.connector

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KET")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME", "sisu_db")
DB_PORT = int(os.environ.get("DB_PORT", 4000))

ARQUIVO_NOMES = 'cursos.json'
ARQUIVO_DADOS = 'banco_de_dados_completo.json'
CACHE_DETALHES = {}

def salvar_lead_mysql(nome, email, telefone):
    conexao = None
    cursor = None
    try:
        conexao = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=DB_PORT,
            ssl_verify_identity=False,
            ssl_ca=''
        )
        
        if conexao.is_connected():
            cursor = conexao.cursor()
            sql = "INSERT INTO leads (nome, email, telefone) VALUES (%s, %s, %s)"
            valores = (nome, email, telefone)
            cursor.execute(sql, valores)
            conexao.commit()
            print(f"Lead salvo: {nome}")

    except mysql.connector.Error as erro:
        print(f"Erro ao conectar: {erro}")
        
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def carregar_banco_de_dados():
    global CACHE_DETALHES
    print("Carregando banco de dados")
    
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                CACHE_DETALHES = json.load(f)
            print(f"Sucesso! {len(CACHE_DETALHES)} fichas de cursos carregadas.")
        except Exception as e:
            print(f"Erro ao ler o banco de dados JSON: {e}")
    else:
        print(f"O arquivo {ARQUIVO_DADOS} não foi encontrado na pasta.")

carregar_banco_de_dados()

def carregar_cursos_local():
    if not os.path.exists(ARQUIVO_NOMES):
        return {}
    try:
        with open(ARQUIVO_NOMES, 'r', encoding='utf-8') as arquivo:
            dados_json = json.load(arquivo)
            return dict(sorted(dados_json.items(), key=lambda x: x[1]))
    except Exception as e:
        print(f"Erro no JSON: {e}")
        return {}

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = None
    erro = None
    cursos_disponiveis = carregar_cursos_local()
    curso_atual_nome = "Selecione um curso"

    if request.method == 'POST':
        try:
            nome_lead = request.form.get('nome_lead')
            email_lead = request.form.get('email_lead')
            telefone_lead = request.form.get('telefone_lead')

            if nome_lead and email_lead:
                salvar_lead_mysql(nome_lead, email_lead, telefone_lead)

            curso_id = request.form.get('curso_id')
            curso_atual_nome = cursos_disponiveis.get(curso_id, "Curso Selecionado")

            print("\n" + "="*40)
            
            dados = CACHE_DETALHES.get(curso_id)
            
            if dados:
                ranking = []
                lista_para_loop = []
                
                if isinstance(dados, dict):
                    lista_para_loop = dados.values()
                elif isinstance(dados, list):
                    lista_para_loop = dados

                nota = {
                    'redacao': float(request.form.get('redacao', '0').replace(',', '.')),
                    'natureza': float(request.form.get('natureza', '0').replace(',', '.')),
                    'humanas': float(request.form.get('humanas', '0').replace(',', '.')),
                    'linguagens': float(request.form.get('linguagens', '0').replace(',', '.')),
                    'matematica': float(request.form.get('matematica', '0').replace(',', '.'))
                }

                for info in lista_para_loop:
                    if not isinstance(info, dict): continue      
                    try:
                        if 'no_ies' not in info: continue

                        p_cn = float(str(info.get('nu_peso_cn') or 1).replace(',', '.'))
                        p_ch = float(str(info.get('nu_peso_ch') or 1).replace(',', '.'))
                        p_l  = float(str(info.get('nu_peso_l') or 1).replace(',', '.'))
                        p_m  = float(str(info.get('nu_peso_m') or 1).replace(',', '.'))
                        p_r  = float(str(info.get('nu_peso_r') or 1).replace(',', '.'))

                        nota_final = (
                            nota['natureza'] * p_cn + nota['humanas'] * p_ch +
                            nota['linguagens'] * p_l + nota['matematica'] * p_m +
                            nota['redacao'] * p_r
                        )
                        soma_pesos = p_cn + p_ch + p_l + p_m + p_r
                        media = nota_final / soma_pesos if soma_pesos > 0 else 0

                        ranking.append({
                            "faculdade": info.get('no_ies', 'Desconhecida'),
                            "campus": info.get('no_campus', 'Campus único'),
                            "local": f"{info.get('no_municipio_campus')}-{info.get('sg_uf_ies')}",
                            "media": f"{media:.1f}",
                            "media_float": media
                        })
                    except Exception:
                        continue

                resultados = sorted(ranking, key=lambda x: x['media_float'], reverse=True)
                
                if not resultados:
                    erro = "Nenhuma oferta encontrada."
            else:
                erro = "Curso não encontrado no banco de dados."

        except Exception as e:
            print(f"Erro Crítico: {e}")
            erro = f"Ocorreu um erro: {str(e)}"

    return render_template('index.html', 
                           resultados=resultados, 
                           erro=erro, 
                           cursos=cursos_disponiveis, 
                           curso_selecionado=curso_atual_nome)

def mascarar(texto):
    if not texto or len(texto) < 5:
        return "***"
    return f"{texto[:2]}****{texto[-2:]}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    senha_demo = os.environ.get("ADMIN_PASSWORD", "Senha não configurada")
    
    if request.method == 'POST':
        senha_digitada = request.form.get('senha')
        if senha_digitada and senha_digitada == ADMIN_PASSWORD:
            session['usuario_logado'] = True
            return redirect(url_for('admin'))
        else:
            erro = "Senha incorreta."
    
    return render_template('login.html', erro=erro, senha_demo=senha_demo)

@app.route('/admin')
def admin():
    if not session.get('usuario_logado'):
        return redirect(url_for('login'))
    
    leads_seguros = []
    conexao = None
    
    try:
        conexao = mysql.connector.connect(
            host=DB_HOST, 
            user=DB_USER, 
            password=DB_PASS, 
            database=DB_NAME, 
            port=DB_PORT,
            ssl_verify_identity=False, 
            ssl_ca=''
        )
        if conexao.is_connected():
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM leads ORDER BY id DESC")
            dados = cursor.fetchall()
            
            for lead in dados:
                leads_seguros.append({
                    'id': lead['id'],
                    'nome': lead['nome'],
                    'email': mascarar(lead['email']),
                    'telefone': mascarar(lead['telefone']),
                    'data_registro': lead.get('data_registro', '-')
                })
            
            cursor.close()
    except Exception as e:
        print(f"Erro no Admin: {e}")
    finally:
        if conexao and conexao.is_connected():
            conexao.close()

    return render_template('admin.html', leads=leads_seguros)

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)