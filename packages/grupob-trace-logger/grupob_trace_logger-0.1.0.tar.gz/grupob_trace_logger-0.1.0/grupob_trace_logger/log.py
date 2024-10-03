# grupob_trace_logger/log.py
import traceback
from datetime import datetime
import requests
import json

class Log:
    def __init__(self, webhook_url: str, default_user: str = "Sem responsável definido", bot_name: str = "Robô sem nome definido") -> None:
        """
        Inicializa o logger com um webhook do Discord e valores padrão para o robô e o responsável.
        """
        self.webhook_url = webhook_url
        self.default_user = default_user
        self.bot_name = bot_name

    def register(self, e: Exception, arr: dict = None) -> None:
        """
        Registra o erro capturando os detalhes da exceção e envia para o Discord via webhook.
        """
        if arr is None:
            arr = {}

        tb = traceback.extract_tb(e.__traceback__)

        # Monta a estrutura de dados do erro
        error_data = {
            "filename": str(tb[-1].filename),
            "function": str(tb[-1].name),
            "type_error": str(type(e).__name__),
            "error": str(e),
            "line": tb[-1].lineno,
            "created_at": datetime.now(),
            "robo": arr.get('nome_robo', self.bot_name),
            "responsavel": arr.get('responsavel', self.default_user)
        }

        # Envia a mensagem para o Discord
        self.send_discord(error_data)

    def send_discord(self, error_data: dict) -> None:
        """
        Envia a mensagem de erro para um canal do Discord usando um webhook.
        """
        # Prepara a mensagem para o Discord
        data = {
            "embeds": [
                {
                    "title": "Problema",
                    "description": f":pushpin: {error_data['error']}",
                    "color": 15158332,  # Cor no formato decimal (hex e91e63)
                    "author": {
                        "name": error_data['robo'],
                        "icon_url": "https://w7.pngwing.com/pngs/567/444/png-transparent-robotics-chatbot-technology-robot-education-electronics-computer-program-humanoid-robot-thumbnail.png"
                    },
                    "fields": [
                        {"name": "Arquivo", "value": f":card_box: {error_data['filename']}", "inline": False},
                        {"name": "Linha", "value": str(error_data['line']), "inline": True},
                        {"name": "Função", "value": error_data['function'], "inline": True},
                        {"name": "Responsável", "value": error_data['responsavel'], "inline": False},
                        {"name": "Data e Hora", "value": f":calendar: {datetime.now().strftime('%d/%m/%Y %H:%M')}", "inline": False}
                    ]
                }
            ]
        }

        # Envia a requisição para o Discord
        response = requests.post(self.webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        
        if response.status_code == 204:
            print("Mensagem enviada com sucesso!")
        else:
            print(f"Falha ao enviar a mensagem. Status code: {response.status_code}")
