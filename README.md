# **Moneylog.py: Gerenciamento Financeiro Automatizado**

Este script em Python automatiza o gerenciamento financeiro pessoal, processando informações extraídas de um arquivo `moneylog.html`. Ele organiza datas de vencimento em ordem crescente para o dia atual e o seguinte, identificando finais de semana e feriados do mês atual e do próximo. A solução permite planejamento financeiro antecipado e seguro, gerando relatórios estruturados enviados diretamente para o e-mail.

## **Requisitos**
1. **Moneylog**: Baixe o [Moneylog](https://aurelio.net/moneylog/portable/#download) e renomeie o arquivo para `moneylog.html`.
2. **Python 3**: Certifique-se de ter Python 3 instalado no seu sistema.
3. **Senha de app do Gmail**: Gere sua senha no [painel de configurações do Google](https://myaccount.google.com/apppasswords?rapt=AEjHL4MN0wbhEPXDK7Pc4634UNf81SV0GGdj1-Bzq0aZ1h4XOQ-SM7KVUCjf2BSPiXnxUpRjdwaPvnDkn9L4fXjdU9D9ImM40YV9fmnzSPdCEkQyUqBC6gM) e insira-a no arquivo `.env`.

## **Instruções de Uso**
1. **Prepare o Arquivo `moneylog.html`**:
   - Faça lançamentos financeiros, separando cada coluna por um TAB.
   - Exemplo de lançamentos:
     ```plaintext
      2024-11-18;-100,00;categoria1,categoria2;|;(--);xxxx xxxxxxx-x;descrição da despesa ou da receita
      2024-11-19;-500,00;categoria1,categoria2;|;(--);xxxx xxxxxxx-x;descrição da despesa ou da receita
      2024-11-15;-210,00;categoria1,categoria2;|;(--);xxxx xxxxxxx-x;descrição da despesa ou da receita
      2024-11-25;+100,00;categoria1,categoria2;|;(--);xxxx xxxxxxx-x;descrição da despesa ou da receita
     ```
   - Dica: Substitua os separadores `;` por TABs reais no seu teclado.

2. **Configuração do Arquivo `.env`**:
   - Crie o arquivo `.env` na mesma pasta do script.
   - Adicione a senha gerada no Gmail ao arquivo `.env`, no formato:
     ```plaintext
     EMAIL_PASSWORD='sua_senha_de_app_aqui'
     ```

3. **Execução do Script**:
   - Certifique-se de que os arquivos `moneylog.py`, `moneylog.html` e `.env` estão na mesma pasta.
   - Execute o script:
     ```bash
     python3 moneylog.py
     ```
   - No MacOS e Linux, use `python3`. No Windows, pode ser `python`.

4. **Resultados**:
   - A execução será exibida no terminal.
   - O relatório será enviado automaticamente para o e-mail configurado no `.env`.

## **Personalização**
- Para usuários minimalistas, o script também suporta arquivos de texto simples (`moneylog.txt`), exigindo apenas ajustes menores no código.
- Fique à vontade para adaptar o script às suas necessidades!

## **Contribuição**
Sinta-se livre para contribuir com melhorias, sugerir funcionalidades ou relatar problemas no repositório.
