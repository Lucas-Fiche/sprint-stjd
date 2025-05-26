from flask import Flask, render_template, request, flash, redirect, url_for, send_file, jsonify
from config import config
from peticao_service import gerar_peticao, salvar_peticao
import os

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Configuração
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    
    # Rotas
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/quem-somos')
    def quem_somos():
        return render_template('quem-somos.html')
    
    @app.route('/nucleo')
    def nucleo():
        return render_template('nucleo.html')
    
    @app.route('/eventos')
    def eventos():
        # Lista de eventos
        eventos_lista = [
            {
                'data': '15 JUN',
                'titulo': 'Workshop de Direito Desportivo',
                'descricao': 'Introdução aos conceitos básicos do Direito Desportivo e suas aplicações práticas.',
                'local': 'IDP - Auditório Principal'
            },
            {
                'data': '22 JUN',
                'titulo': 'Palestra: Justiça Desportiva no Brasil',
                'descricao': 'Análise do sistema de justiça desportiva brasileiro e casos práticos.',
                'local': 'IDP - Sala de Conferências'
            },
            {
                'data': '05 JUL',
                'titulo': 'Mesa Redonda: Atleta e Seus Direitos',
                'descricao': 'Discussão sobre os direitos fundamentais dos atletas e proteção jurídica.',
                'local': 'IDP - Auditório Principal'
            },
            {
                'data': '12 JUL',
                'titulo': 'Oficina Prática: Elaboração de Defesas',
                'descricao': 'Treinamento prático para elaboração de peças de defesa em tribunais desportivos.',
                'local': 'IDP - Laboratório Jurídico'
            }
        ]
        return render_template('eventos.html', eventos=eventos_lista)
    
    @app.route('/educacao')
    def educacao():
        # Conteúdos educacionais
        conteudos = [
            {
                'icone': '📚',
                'titulo': 'O que é Direito Desportivo?',
                'descricao': 'O Direito Desportivo é o ramo jurídico que regula as relações esportivas, abrangendo desde contratos de atletas até questões disciplinares e de organização esportiva.'
            },
            {
                'icone': '⚖️',
                'titulo': 'Justiça Desportiva',
                'descricao': 'Sistema autônomo que julga questões relacionadas às infrações disciplinares e às competições esportivas, garantindo o fair play e a aplicação das regras.'
            },
            {
                'icone': '📋',
                'titulo': 'Contratos de Atletas',
                'descricao': 'Regulamentação específica para vínculos entre atletas e clubes, incluindo direitos trabalhistas, transferências e cláusulas de rescisão.'
            },
            {
                'icone': '🏆',
                'titulo': 'Direitos dos Atletas',
                'descricao': 'Proteção jurídica aos profissionais do esporte, incluindo direitos trabalhistas, previdenciários e proteção contra discriminação.'
            },
            {
                'icone': '🔍',
                'titulo': 'Doping e Controle',
                'descricao': 'Regulamentação sobre substâncias proibidas, procedimentos de controle antidoping e consequências legais das infrações.'
            },
            {
                'icone': '🌐',
                'titulo': 'Direito Desportivo Internacional',
                'descricao': 'Normas que regem competições internacionais, transferências entre países e resolução de conflitos através do CAS (Corte Arbitral do Esporte).'
            }
        ]
        return render_template('educacao.html', conteudos=conteudos)
    
    @app.route('/contato', methods=['GET', 'POST'])
    def contato():
        if request.method == 'POST':
            # Verificar se é uma solicitação de geração de petição
            if 'gerar_peticao' in request.form:
                return processar_peticao()
        
        return render_template('contato.html')
    
    def processar_peticao():
        """Processa formulário de geração de petição"""
        try:
            # Coletar dados do formulário
            dados_cliente = {
                'nome': request.form.get('nome_peticao'),
                'clube': request.form.get('clube'),
                'competicao': request.form.get('competicao'),
                'acusacao': request.form.get('acusacao'),
                'contexto': request.form.get('contexto'),
                'pedidos': request.form.get('pedidos')
            }
            
            # Validar campos obrigatórios
            campos_obrigatorios = ['nome', 'clube', 'competicao', 'acusacao', 'contexto', 'pedidos']
            for campo in campos_obrigatorios:
                if not dados_cliente[campo]:
                    flash(f'O campo {campo.replace("_", " ").title()} é obrigatório.', 'error')
                    return render_template('contato.html')
            
            # Gerar petição usando IA
            resultado_peticao = gerar_peticao(dados_cliente)
            
            if resultado_peticao['sucesso']:
                nome_base = resultado_peticao['nome_arquivo']
                
                # Salvar petição nos dois formatos
                resultado_arquivo = salvar_peticao(
                    resultado_peticao['conteudo'], 
                    nome_base
                )
                
                if resultado_arquivo['sucesso']:
                    flash(f'🎉 Petição gerada com sucesso pelo Justinho!', 'success')
                    
                    # Gerar os dois links
                    download_docx = url_for('download_peticao', nome_arquivo=resultado_arquivo['arquivos']['docx'])
                    download_pdf = url_for('download_peticao', nome_arquivo=resultado_arquivo['arquivos']['pdf'])
                    
                    return render_template(
                        'contato.html',
                        download_docx=download_docx,
                        download_pdf=download_pdf,
                        nome_arquivo_base=nome_base
                    )
                else:
                    flash('❌ Erro ao salvar petição. Tente novamente.', 'error')
            else:
                flash(f'❌ Erro ao gerar petição: {resultado_peticao["erro"]}', 'error')
        
        except Exception as e:
            flash(f'❌ Erro interno: {str(e)}', 'error')
        
        return render_template('contato.html')
    
    @app.route('/download/<nome_arquivo>')
    def download_peticao(nome_arquivo):
        """Permite download da petição gerada"""
        try:
            caminho_arquivo = os.path.join('static', 'peticoes', nome_arquivo)
            if os.path.exists(caminho_arquivo):
                return send_file(caminho_arquivo, as_attachment=True)
            else:
                flash('❌ Arquivo não encontrado.', 'error')
                return render_template('contato.html')  # Renderizar ao invés de redirect
        except Exception as e:
            flash(f'❌ Erro no download: {str(e)}', 'error')
            return render_template('contato.html')  # Renderizar ao invés de redirect
    
    @app.route('/status_peticao', methods=['POST'])
    def status_peticao():
        """Endpoint para verificar status da geração (AJAX)"""
        return jsonify({'status': 'processando'})
    
    # Tratamento de erro 404
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)