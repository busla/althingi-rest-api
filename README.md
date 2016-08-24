# Althingi REST Api (ARI)
REST API fyrir gögn Alþingis.

Django REST þjónusta sem skilar gögnum frá Alþingi. Til að nota þjónustuna þarftu einnig <a href="https://github.com/busla/althingi-scraper">Alþingissköfuna</a> sem skafar XML frá Alþingi.


Markmiðið með ARA er að greina gögn frá Alþingi sem mögulegt er að nýta í margvíslegum tilgangi. ARI er sjálfstætt framhald af <a href="https://github.com/BjarniRunar/rynir">Alþingisrýninum</a> sem tók saman tölfræði um atkvæði þingmanna, sérstaklega fjarveru þeirra og flokkshollustu (eða uppreisnarseggi).

Alþingi er með opið gagnasafn með öllum þessum gögnum en ARI sækir þau og geymir í eigin gagnasafni til að auðvelda úrvinnslu.

ARI er mjög skalanlegur og auðvelt að bæta við tölfræðiútreikningum fyrir nokkurn veginn hvað sem er. Hægt er að óska eftir útreikningum með því að hafa samband við höfund. Við bætum þeim á *í vinnslu* listann hér fyrir neðan.

Hægt er að sækja öll gögn með því að kalla í ARA:

* Löggjafarþing
* Mál
* Þingmenn
* Flokkar
* Þingsetur
* Atkvæðagreiðslur
* Atkvæði
* Nefndir
* Nefndarfundir 


## Útreikningar - lokið
* Heildarfjöldi atkvæða hvers og eins Alþingismanns
* Heildarfjöldi fjarvista (*fjarverandi* og *boðaði fjarvist* tekið saman)
* Heildarfjöldi atkvæða eftir tegund (*já*, *nei*, *greiðir ekki atkvæði*, *fjarverandi*, *boðaði fjarvist*)

## Útreikningar - í vinnslu
* Uppreisnarseggir
* Flokkshollusta
* Flokkur sem skrópar mest
* Þingmaður lengst á þingi
* Þingmaður styst á þingi
* Fjöldi nefndarfunda milli þinga
* Þingmaður talar lengst
* Þingmaður talar styst
* Þingmanni í nöp við málaflokk
* ... þínar tillögur?

# Fikta í ARA
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

