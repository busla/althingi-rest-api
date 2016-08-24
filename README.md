# althingi-rest-api
REST API fyrir gögn Alþingis.

Django REST þjónusta sem skilar gögnum frá Alþingi. Til að nota þjónustuna þarftu að kalla í <a href="https://github.com/busla/althingi-scraper">althingi-scraper</a> sem skafar XML frá Alþingi.

# Uppsetning
* pip install -r requirements.txt
* python manage.py makemigrations api
* python manage.py migrate
* python manage.py createsuperuser
* python manage.py runserver

# Kalla í sköfuna
Til að sækja öll gögn fyrir löggjafarþing kallarðu í sköfuna sem vistar öll gögn í DB og venslar saman. Þetta gæti tekið nokkrar mínútur. Núverandi löggjafarþing er 145.

```
$ http://localhost:8000/spider/session/[löggjafarþing]/all
```

# Skoða gögn
Eftir að þessu er lokið geturðu skoðað gögnin:

* http://localhost:8000/sessions/
* http://localhost:8000/issues/
* http://localhost:8000/parties/
* http://localhost:8000/members/
* http://localhost:8000/committees/
* http://localhost:8000/committee-meetings/
* http://localhost:8000/petitions/
* http://localhost:8000/signatures/
* http://localhost:8000/seats/

