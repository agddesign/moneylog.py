# moneylog.py

portfolio script Python

Este script em Python automatiza o gerenciamento financeiro ao processar informações extraídas de um arquivo moneylog.html, um aplicativo gratuito e multiplataforma disponível em https://aurelio.net/moneylog/portable/#download. O script organiza datas de vencimento em ordem crescente para o dia atual e o seguinte, identificando também finais de semana e feriados do mês atual e do próximo, permitindo planejamento financeiro antecipado e seguro, gerando um relatório estruturado, enviado por e-mail.

As senhas de app do Gmail devem ser conseguidas neste link: https://myaccount.google.com/apppasswords?rapt=AEjHL4MN0wbhEPXDK7Pc4634UNf81SV0GGdj1-Bzq0aZ1h4XOQ-SM7KVUCjf2BSPiXnxUpRjdwaPvnDkn9L4fXjdU9D9ImM40YV9fmnzSPdCEkQyUqBC6gM

INSTRUÇÕES DE USO:

- Baixe o moneylog no link https://aurelio.net/moneylog/portable/
- Renomeie-o para simplesmente moneylog.html
- faça seus lançamentos separando cada coluna por um TAB.
  
- Ex.: cole em seu moneylog.html estes lançamentos abaixo e substitua <TAB> por um TAB real de seu teclado. Coloque as datas do dia e do dia seguinte, antes de experimentar rodar o script. O script roda da mesma forma para um arquivo moneylog.txt com apenas os lançamentos, fazendo pequena alteração para que o mesmo encontre o arquivo .txt. Funciona muito bem para quem é minimalista e quer experimentar guardar seus registros contábeis num arquivo de texto puro.
  
- 2024-11-18<TAB>-100,00<TAB>categoria1,categoria2<TAB>|<TAB>(--)<TAB>xxxx xxxxxxx-x<TAB>descrição da despesa ou da receita
- 2024-11-19<TAB>-500,00<TAB>categoria1,categoria2<TAB>|<TAB>(--)<TAB>xxxx xxxxxxx-x<TAB>descrição da despesa ou da receita
- 2024-11-15<TAB>-210,00<TAB>categoria1,categoria2<TAB>|<TAB>(--)<TAB>xxxx xxxxxxx-x<TAB>descrição da despesa ou da receita
- 2024-11-25<TAB>+100,00<TAB>categoria1,categoria2<TAB>|<TAB>(--)<TAB>xxxx xxxxxxx-x<TAB>descrição da despesa ou da receita
- 2024-11-23<TAB>+800,00<TAB>categoria1,categoria2<TAB>|<TAB>(--)<TAB>xxxx xxxxxxx-x<TAB>descrição da despesa ou da receita
- 2024-12-23<TAB>+800,00<TAB>categoria1,categoria2<TAB>|<TAB>(--)<TAB>xxxx xxxxxxx-x<TAB>descrição da despesa ou da receita

- Crie uma senha de app no gmail https://myaccount.google.com/apppasswords?rapt=AEjHL4MN0wbhEPXDK7Pc4634UNf81SV0GGdj1-Bzq0aZ1h4XOQ-SM7KVUCjf2BSPiXnxUpRjdwaPvnDkn9L4fXjdU9D9ImM40YV9fmnzSPdCEkQyUqBC6gM
- Coloque a senha dentro do arquivo .env
- Estando os três arquivos dentro da mesma pasta: moneylog.py, moneylog.html e .env, basta rodar o script moneylog.py (No Mac OS é python3 moneylog.py
- Se tudo estiver correto, você verá a execução no Terminal e receberá na sua conta gmail, o seu primeiro relatório contendo o resultado da execução do script.
