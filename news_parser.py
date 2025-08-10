import feedparser
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse as parse_date
from database import Artigo, Feed
from config import DATABASE_URL, PALAVRAS_CHAVE

def artigo_existe(session, link):
    """Verifica se um artigo com o link fornecido já existe na base de dados."""
    return session.query(Artigo).filter(Artigo.link == link).count() > 0

def analisar_e_salvar_feeds():
    """
    Analisa os feeds RSS, filtra os artigos por palavras-chave e salva-os na base de dados.
    """
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    feeds = session.query(Feed).all()
    if not feeds:
        print("Nenhum feed RSS encontrado na base de dados. Adicione feeds para começar.")
        session.close()
        return

    contagem_novos_artigos = 0

    for feed_item in feeds:
        url = feed_item.url
        try:
            feed = feedparser.parse(url)
            # Usa o nome do feed do banco de dados como fallback
            nome_fonte = getattr(feed.feed, 'title', feed_item.nome or 'Fonte Desconhecida')
            url_fonte = getattr(feed.feed, 'link', url)

            for entrada in feed.entries:
                titulo = entrada.title
                link = entrada.link
                resumo = entrada.summary
                
                # Verifica se alguma palavra-chave está presente no título ou no resumo
                if any(palavra in titulo.lower() or palavra in resumo.lower() for palavra in PALAVRAS_CHAVE):
                    if not artigo_existe(session, link):
                        data_publicacao = parse_date(entrada.published)
                        
                        stmt = insert(Artigo).values(
                            titulo=titulo,
                            link=link,
                            resumo=resumo,
                            data_publicacao=data_publicacao,
                            nome_fonte=nome_fonte,
                            url_fonte=url_fonte,
                            tags=", ".join([kw for kw in PALAVRAS_CHAVE if kw in titulo.lower() or kw in resumo.lower()])
                        )
                        session.execute(stmt)
                        contagem_novos_artigos += 1
        except Exception as e:
            print(f"Erro ao processar o feed {url}: {e}")

    session.commit()
    session.close()
    print(f"Foram encontrados e salvos {contagem_novos_artigos} novos artigos.")

if __name__ == '__main__':
    analisar_e_salvar_feeds()