from apscheduler.schedulers.background import BackgroundScheduler
from news_parser import analisar_e_salvar_feeds

def iniciar_agendador():
    """
    Inicializa e inicia o agendador de tarefas em segundo plano para atualizar os feeds periodicamente.
    """
    agendador = BackgroundScheduler()
    # Agenda a tarefa para ser executada a cada hora
    agendador.add_job(analisar_e_salvar_feeds, 'interval', hours=1)
    agendador.start()
    print("Agendador de tarefas em segundo plano iniciado. Os feeds serão atualizados a cada hora.")