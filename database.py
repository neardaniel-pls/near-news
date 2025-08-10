from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()

class Artigo(Base):
    __tablename__ = 'artigos'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False)
    resumo = Column(Text)
    data_publicacao = Column(DateTime, nullable=False)
    nome_fonte = Column(String)
    url_fonte = Column(String)
    tags = Column(String)

class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    nome = Column(String)

def init_db():
    """
    Inicializa a base de dados, cria as tabelas e popula com feeds iniciais se não existirem.
    """
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Base de dados inicializada e tabelas criadas.")

    # Popula a tabela de feeds com valores iniciais se estiver vazia
    Session = sessionmaker(bind=engine)
    session = Session()
    
    if session.query(Feed).count() == 0:
        feeds_iniciais = [
            Feed(nome='Privacidade Digital', url='https://www.privacidade.digital/rss'),
            Feed(nome='Schneier on Security', url='https://www.schneier.com/blog/atom.xml'),
            Feed(nome='Electronic Frontier Foundation', url='https://www.eff.org/rss/updates.xml'),
            Feed(nome='Privacy International', url='https://www.privacyinternational.org/rss.xml')
        ]
        session.add_all(feeds_iniciais)
        session.commit()
        print(f"{len(feeds_iniciais)} feeds iniciais adicionados à base de dados.")
    
    session.close()

if __name__ == '__main__':
    init_db()