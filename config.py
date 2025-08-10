# -*- coding: utf-8 -*-

"""
Centralized configuration for the application.
"""

# Database configuration
DATABASE_URL = "sqlite:///news.db"

# Keywords for filtering articles
PALAVRAS_CHAVE = {
    "privacidade", "privacy", "dados pessoais", "proteção de dados", "lgpd", 
    "gdpr", "vazamento de dados", "cibersegurança", "cybersecurity", "segurança digital",
    "criptografia", "encryption", "vigilância", "surveillance", "biometria",
    "reconhecimento facial", "ética em IA", "neutralidade da rede", "leak", "leaked"
}