from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from database import Artigo, Feed
from config import DATABASE_URL
from scheduler import iniciar_agendador

app = Flask(__name__)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    """
    Exibe a página principal com o feed de notícias, com suporte para pesquisa.
    """
    session = Session()
    query = request.args.get('q')
    try:
        if query:
            search_term = f"%{query}%"
            artigos = session.query(Artigo).filter(
                or_(
                    Artigo.titulo.ilike(search_term),
                    Artigo.resumo.ilike(search_term),
                    Artigo.tags.ilike(search_term)
                )
            ).order_by(Artigo.data_publicacao.desc()).all()
        else:
            artigos = session.query(Artigo).order_by(Artigo.data_publicacao.desc()).all()
    except Exception as e:
        print(f"A base de dados ainda não está pronta ou a consulta falhou: {e}")
        artigos = []
    finally:
        session.close()

    return render_template('index.html', artigos=artigos, query=query)

@app.route('/feeds', methods=['GET', 'POST'])
def gerir_feeds():
    """
    Exibe a página para gerir os feeds RSS e processa a adição de novos feeds.
    """
    session = Session()
    try:
        if request.method == 'POST':
            url = request.form['url']
            nome = request.form.get('nome')  # .get() para o caso de o nome ser opcional
            if url:
                novo_feed = Feed(url=url, nome=nome)
                session.add(novo_feed)
                session.commit()
                return redirect(url_for('gerir_feeds'))

        feeds = session.query(Feed).order_by(Feed.nome).all()
    except Exception as e:
        print(f"Erro ao gerir feeds: {e}")
        session.rollback()
        feeds = []
    finally:
        session.close()
    
    return render_template('feeds.html', feeds=feeds)

@app.route('/feeds/delete/<int:feed_id>', methods=['POST'])
def apagar_feed(feed_id):
    """
    Apaga um feed RSS da base de dados.
    """
    session = Session()
    try:
        feed_para_apagar = session.query(Feed).filter(Feed.id == feed_id).one()
        session.delete(feed_para_apagar)
        session.commit()
    except Exception as e:
        print(f"Erro ao apagar feed: {e}")
        session.rollback()
    finally:
        session.close()
    
    return redirect(url_for('gerir_feeds'))

if __name__ == '__main__':
    iniciar_agendador()
    app.run(debug=True, use_reloader=False)