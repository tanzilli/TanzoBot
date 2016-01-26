#Telegram Physical Computing

## Modulo di autorizzazione tanzocheck.py

Il modulo tanzocheck.py consente di implementare un semplice sistema 
di autorizzazione basato sull'id dell'utente chiamante.

Il programma tanzocheck_test.py consente di provarlo al volo
e capire come integrarlo nel proprio Bot.

E' possibile definire un super utente ed uno o piu' utenti normali.

Diventa super utente automaticamente il primo che manda un messaggio al Bot.

Il super utente poi puo' chiedere una One Time Password con il 
comando /otp che se usata da altri utenti abilita l'accesso al Bot 
come utenti normali

Il super utente puo' anche revocare l'autorizzazione a tutti gli utenti-

Il programma di tanzocheck_test.py al momento non salva le autorizzazioni
su file  per cui quando il programma viene rilanciato si riparte daccapo.

Info su http://www.acmesystems.it/tpc

2016 (c) Sergio Tanzilli

