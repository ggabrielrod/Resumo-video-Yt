"""
Monitor de Preço/Promoção - Template Base
-------------------------------------------
Monitora o preço de um produto numa página e avisa via Telegram
quando o preço cair abaixo de um valor-alvo.
 
DEPENDÊNCIAS:
    pip install requests beautifulsoup4 schedule
 
COMO CONFIGURAR:
1. Preencha PRODUTO_URL com o link do produto
2. Ache o seletor CSS certo do preço (veja instruções abaixo)
3. Configure TELEGRAM_TOKEN e TELEGRAM_CHAT_ID (veja instruções abaixo)
4. Ajuste PRECO_ALVO
5. Rode: python monitor_promocao.py
"""
 
import requests
from bs4 import BeautifulSoup
import schedule
import time
import json
import os
from datetime import datetime
 
# ========== CONFIGURAÇÕES ==========
PRODUTO_URL = "https://www.exemplo.com/produto/teclado-aula-68he"
PRODUTO_NOME = "Teclado AULA Win 68HE Max"
PRECO_ALVO = 250.00  # avisa quando o preço for <= esse valor
 
# Seletor CSS onde fica o preço na página (varia de site pra site)
# Exemplo Kabum: 'h4.finalPrice'
# Exemplo Amazon: 'span.a-price-whole'
# Use o inspetor do navegador (F12) pra achar o seletor certo
SELETOR_PRECO = "span.price"
 
# Telegram Bot (crie um bot com @BotFather no Telegram, é grátis)
TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI"
 
INTERVALO_HORAS = 3  # de quanto em quanto tempo checar
ARQUIVO_HISTORICO = "historico_precos.json"
 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
 
 
def buscar_preco():
    """Faz o request na página e extrai o preço."""
    resp = requests.get(PRODUTO_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
 
    soup = BeautifulSoup(resp.text, "html.parser")
    elemento = soup.select_one(SELETOR_PRECO)
 
    if not elemento:
        raise ValueError("Seletor não encontrou o preço. Confira SELETOR_PRECO.")
 
    texto = elemento.get_text(strip=True)
    # Limpa "R$ 1.299,90" -> 1299.90
    limpo = texto.replace("R$", "").replace(".", "").replace(",", ".").strip()
    return float(limpo)
 
 
def enviar_telegram(mensagem):
    """Envia notificação via Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
    requests.post(url, data=payload, timeout=10)
 
 
def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
 
 
def salvar_historico(historico):
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)
 
 
def checar_preco():
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    print(f"[{agora}] Checando preço...")
 
    try:
        preco_atual = buscar_preco()
    except Exception as e:
        print(f"Erro ao buscar preço: {e}")
        return
 
    print(f"Preço encontrado: R$ {preco_atual:.2f}")
 
    historico = carregar_historico()
    historico.append({"data": agora, "preco": preco_atual})
    salvar_historico(historico)
 
    if preco_atual <= PRECO_ALVO:
        msg = (
            f"🚨 PROMOÇÃO! {PRODUTO_NOME}\n"
            f"Preço atual: R$ {preco_atual:.2f}\n"
            f"Alvo: R$ {PRECO_ALVO:.2f}\n"
            f"{PRODUTO_URL}"
        )
        enviar_telegram(msg)
        print("Notificação enviada!")
 
 
if __name__ == "__main__":
    print(f"Monitorando: {PRODUTO_NOME}")
    print(f"Preço-alvo: R$ {PRECO_ALVO:.2f}")
    print(f"Checando a cada {INTERVALO_HORAS}h. Ctrl+C pra parar.\n")
 
    checar_preco()  # roda uma vez imediatamente
    schedule.every(INTERVALO_HORAS).hours.do(checar_preco)
 
    while True:
        schedule.run_pending()
        time.sleep(60)
