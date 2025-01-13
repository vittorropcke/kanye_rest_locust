import logging
import csv
from locust import HttpUser, task, between, events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variável global para armazenar o environment
global_environment = None

# Configurar arquivo CSV personalizado
@events.init.add_listener
def setup_csv(environment, **kwargs):
    global global_environment
    global_environment = environment  # Armazena o environment na variável global
    environment.custom_csv_file = open("custom_report.csv", "w", newline="", encoding="utf-8")
    environment.custom_csv_writer = csv.writer(environment.custom_csv_file)
    # Cabeçalhos do CSV
    environment.custom_csv_writer.writerow(["Request Type", "Name", "Response Time", "Response Length", "Response Text", "Exception"])

@events.request.add_listener
def log_request(request_type, name, response_time, response_length, response, exception, **kwargs):
    # Usa o environment armazenado na variável global
    if not global_environment:
        logger.error("Environment não encontrado.")
        return

    response_text = response.text[:500] if response and response.text else "No Response"
    # Escreve os dados no CSV
    global_environment.custom_csv_writer.writerow([request_type, name, response_time, response_length, response_text, exception])

@events.quitting.add_listener
def close_csv(environment, **kwargs):
    if hasattr(environment, "custom_csv_file"):
        environment.custom_csv_file.close()

class IloveUKanye(HttpUser):
    wait_time = between(1, 5)
    host = "https://api.kanye.rest"

    @task
    def say_me_anything(self):
        response = self.client.get("/")
        logger.info(f"GET / - Kanye: {response.text}")