import subprocess
import sys
from datetime import datetime, timedelta, timezone
import calendar
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import getpass
import logging
from typing import List, Tuple

# Constantes
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
DATE_FORMAT = '%Y-%m-%d'
DATE_FORMAT_DISPLAY = '%d/%m/%Y'

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para instalar o pacote, se necessário
def install(package: str) -> None:
  subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Verifica e instala bibliotecas necessárias
try:
  from dotenv import load_dotenv
except ModuleNotFoundError:
  logging.info("Módulo 'dotenv' não encontrado. Instalando automaticamente...")
  install('python-dotenv')
  from dotenv import load_dotenv

try:
  import holidays
except ModuleNotFoundError:
  logging.info("Módulo 'holidays' não encontrado. Instalando automaticamente...")
  install('holidays')
  import holidays

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações
filename = os.getenv('MONEYLOG_FILE')
sender_email = os.getenv('SENDER_EMAIL')
receiver_email = os.getenv('RECEIVER_EMAIL')

# Verifica se as variáveis de ambiente necessárias estão definidas
if not filename or not sender_email or not receiver_email:
  logging.error("As variáveis de ambiente MONEYLOG_FILE, SENDER_EMAIL e RECEIVER_EMAIL devem estar definidas.")
  sys.exit(1)

# Obtém o fuso horário local
try:
  from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:
  from pytz import timezone as ZoneInfo  # Para versões anteriores

local_tz_name = os.getenv('TIMEZONE', 'America/Sao_Paulo')
try:
  local_tz = ZoneInfo(local_tz_name)
except Exception as e:
  logging.error(f"Fuso horário inválido: {local_tz_name}. Erro: {e}")
  sys.exit(1)

# Obtém as datas de hoje e amanhã com fuso horário
today = datetime.now(local_tz)
tomorrow = today + timedelta(days=1)
today_date = today.strftime(DATE_FORMAT)
tomorrow_date = tomorrow.strftime(DATE_FORMAT)

def get_weekends_and_holidays(start_date: datetime, end_date: datetime) -> List[str]:
  """Obtém finais de semana e feriados em um intervalo de datas."""
  weekends_holidays = []
  feriados = holidays.Brazil()
  delta = timedelta(days=1)
  current_date = start_date

  while current_date <= end_date:
      day_of_week = current_date.weekday()

      if day_of_week == 5:
          weekends_holidays.append(f"{current_date.strftime(DATE_FORMAT_DISPLAY)}: Sábado")
      elif day_of_week == 6:
          weekends_holidays.append(f"{current_date.strftime(DATE_FORMAT_DISPLAY)}: Domingo")
      
      if current_date in feriados:
          nome_feriado = feriados.get(current_date)
          weekends_holidays.append(f"{current_date.strftime(DATE_FORMAT_DISPLAY)}: Feriado ({nome_feriado})")
      
      current_date += delta

  return weekends_holidays

def ler_arquivo(filename: str) -> List[Tuple[str, str, str, str]]:
  """Lê o arquivo e retorna as linhas relevantes."""
  lines_with_dates = []
  is_tomorrow_section = False

  try:
      with open(filename, 'r') as file:
          for line in file:
              if re.match(rf'^({today_date}|{tomorrow_date})', line):
                  if not is_tomorrow_section and tomorrow_date in line:
                      lines_with_dates.append((' ', ' ', ' ', ' '))
                      is_tomorrow_section = True

                  columns = line.strip().split('\t')
                  # Verifica se a linha tem o número esperado de colunas
                  if len(columns) >= 7:
                      data = columns[0]
                      valor = columns[1]
                      status = columns[4] if len(columns) > 4 else '(--)'
                      coluna7 = columns[6] if len(columns) > 6 else '(sem coluna 7)'
                      lines_with_dates.append((data, valor, status, coluna7))
                  else:
                      logging.warning(f"Linha ignorada por formato incorreto: {line.strip()}")
      logging.info(f"Linhas com datas encontradas: {len(lines_with_dates)}")
  except FileNotFoundError:
      logging.error(f"Arquivo não encontrado: {filename}")
      raise

  return lines_with_dates

def formatar_linhas(lines_with_dates: List[Tuple[str, str, str, str]]) -> List[str]:
  """Formata as linhas para exibição."""
  sorted_lines = sorted(
      [line for line in lines_with_dates if line[0].strip()],
      key=lambda x: datetime.strptime(x[0], DATE_FORMAT)
  )

  final_lines = []
  for line in sorted_lines:
      if tomorrow_date in line[0] and not any(l[0].strip() == '' for l in final_lines):
          final_lines.append((' ', ' ', ' ', ' '))
      final_lines.append(line)

  logging.info(f"Linhas finais antes de calcular max_lens: {len(final_lines)}")

  if not final_lines:
      logging.error("Nenhuma linha encontrada para formatar.")
      return []

  # Verifica se as linhas estão consistentes e não vazias
  clean_lines = [line for line in final_lines if all(line)]
  if not clean_lines:
      logging.error("Todas as linhas estão vazias ou inconsistentes.")
      return []

  try:
      max_lens = [max(len(str(line[i])) for line in clean_lines) for i in range(4)]
  except ValueError:
      logging.error("Erro ao calcular max_lens: sequência vazia.")
      return []

  formatted_lines = []
  for line in final_lines:
      if line[0].strip() == '':
          formatted_lines.append('')
      else:
          formatted_line = f"{str(line[0]).rjust(max_lens[0])} {str(line[1]).rjust(max_lens[1])} {str(line[2]).rjust(max_lens[2])} {str(line[3]).ljust(max_lens[3])}"
          formatted_lines.append(formatted_line)

  return formatted_lines

def criar_corpo_email(
  formatted_lines: List[str], 
  weekends_and_holidays_current: List[str], 
  weekends_and_holidays_next: List[str],
  total_feriados_current: int,
  total_finais_de_semana_current: int,
  total_feriados_next: int,
  total_finais_de_semana_next: int
) -> str:
  """Cria o corpo do email com totais separados por mês."""
  email_body = "<pre>\n"
  email_body += "\n"
  email_body += "\n".join(formatted_lines)
  email_body += "\n"
  
  # Informações do mês atual
  email_body += "\n"
  email_body += "\n".join(weekends_and_holidays_current)
  email_body += f"\n\nTotal de feriados encontrados no mês atual: {total_feriados_current}"
  email_body += f"\nTotal de finais de semana encontrados no mês atual: {total_finais_de_semana_current}"
  
  # Informações do próximo mês
  email_body += "\n\n"
  email_body += "\n".join(weekends_and_holidays_next)
  email_body += f"\n\nTotal de feriados encontrados no próximo mês: {total_feriados_next}"
  email_body += f"\nTotal de finais de semana encontrados no próximo mês: {total_finais_de_semana_next}"
  
  email_body += "\n</pre>"
  return email_body

def enviar_email(sender_email: str, receiver_email: str, subject: str, body: str) -> None:
  """Envia o email."""
  message = MIMEMultipart()
  message['From'] = sender_email
  message['To'] = receiver_email
  message['Subject'] = subject
  message.attach(MIMEText(body, 'html'))

  password = os.getenv('EMAIL_PASSWORD')
  if not password:
      password = getpass.getpass(prompt='Digite sua senha de e-mail: ')

  try:
      with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
          server.login(sender_email, password)
          server.sendmail(sender_email, receiver_email, message.as_string())
      logging.info("Email enviado com sucesso!")
  except smtplib.SMTPAuthenticationError:
      logging.error("Erro de autenticação ao enviar o email. Verifique suas credenciais.")
  except smtplib.SMTPException as e:
      logging.error(f"Erro ao enviar o email: {e}")

def main() -> None:
  try:
      lines_with_dates = ler_arquivo(filename)
      formatted_lines = formatar_linhas(lines_with_dates)
      
      if not formatted_lines:
          logging.warning("Nenhuma linha formatada para enviar no email.")
          return
      
      current_year = today.year
      current_month = today.month

      # Determina o próximo mês e ano, considerando a virada de ano
      if current_month == 12:
          next_month = 1
          next_month_year = current_year + 1
      else:
          next_month = current_month + 1
          next_month_year = current_year

      # Define as datas de início e fim para o mês atual e próximo
      start_date_current = datetime(current_year, current_month, 1, tzinfo=local_tz)
      end_date_current = datetime(current_year, current_month, calendar.monthrange(current_year, current_month)[1], tzinfo=local_tz)

      start_date_next = datetime(next_month_year, next_month, 1, tzinfo=local_tz)
      end_date_next = datetime(next_month_year, next_month, calendar.monthrange(next_month_year, next_month)[1], tzinfo=local_tz)

      # Obtém finais de semana e feriados do mês atual e do próximo mês
      weekends_and_holidays_current = get_weekends_and_holidays(start_date_current, end_date_current)
      weekends_and_holidays_next = get_weekends_and_holidays(start_date_next, end_date_next)

      # Calcula os totais de feriados e finais de semana para cada mês
      total_feriados_current = sum(1 for item in weekends_and_holidays_current if 'Feriado' in item)
      total_finais_de_semana_current = sum(1 for item in weekends_and_holidays_current if 'Sábado' in item or 'Domingo' in item)

      total_feriados_next = sum(1 for item in weekends_and_holidays_next if 'Feriado' in item)
      total_finais_de_semana_next = sum(1 for item in weekends_and_holidays_next if 'Sábado' in item or 'Domingo' in item)

      email_body = criar_corpo_email(
          formatted_lines, 
          weekends_and_holidays_current, 
          weekends_and_holidays_next,
          total_feriados_current,
          total_finais_de_semana_current,
          total_feriados_next,
          total_finais_de_semana_next
      )
      enviar_email(sender_email, receiver_email, 'moneylog', email_body)
  except FileNotFoundError:
      logging.error(f"Erro: O arquivo '{filename}' não foi encontrado.")
  except Exception as e:
      logging.error(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
  main()
