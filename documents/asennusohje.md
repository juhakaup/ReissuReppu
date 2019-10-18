# Sovelluksen asentaminen

Sovellus on tarkoitettu pääasiassa käytettäväksi web-sovelluksena nettiselaimen kautta. Sovelluksen voi kuitenkin asentaa myös omalle koneelle, kokeilua tai muokkaamista varten.

Nämä asennusohjeet käsittelevät asentamista linux-ympäristössä.

#### Asentaminen paikallisesti

Ohjelman paikallista asentamista ja ajamista varten käyttäjällä tulee olla asennettuna python3 ja sqlite3, sekä mahdollisesti git.

**Lataaminen omalle koneelle**

Lataa sovellus zip-tiedostona githubista 'Clone or download' -linkin takaa. Pura tiedosto haluamaasi kansioon.
Vaihtoehtoisesti voit kloonata projektin omalle koneellesi komennolla:

	$ git clone https://github.com/juhakaup/ReissuReppu.git
Tällöin koneellasi tulee olla asennettuna myös git.	

**Asennus**

Navigoi komentorivillä kansioon johon purit zip-paketin tai kloonasit projektin.
Mene kansioon ReissuReppu.
Luo virtuaaliympäristö ja käynnistä se komennoilla:

	$ python3 -m venv venv
	$ source venv/bin/activate
Komentorivillä pitäisi nyt lukea (venv) rivin alussa, virtuaaliympäristön käynnissäolon merkiksi.

Asenna nyt sovelluksen tarvitsemat paketit komennolla:

	(venv) $ pip install -r requirements.txt

Jos asennuksessa ilmenee ongelmia voit yrittää päivittää itse pip -sovelluksen komennolla:

	(venv) $ pip install --upgrade pip

**Ohjelman ajaminen**

Jos kaikki paketit asentuivat onnistuneesti, sovellus voidaan nyt käynnistää komennolla:

	(venv) $ python run.py
Sovelluksen pitäisi olla nyt käynnissä ja komentorivillä teksti:
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Ennen sovellukseen käyttämistä, pitää sen tietokantaan vielä lisätä tiedot käyttäjärooleista.
Avaa tietokanta sqlite3:lla ja lisää käyttäjäroolit.

	$ sqlite3 application/gearlists.db 
	sqlite> INSERT INTO role (role) VALUES ('ADMIN'), ('USER');
	sqlite> .exit

Sovellusta voi nyt käyttää nettiselaimella osoitteessa: http://127.0.0.1:5000/

**Administrator oikeuksien lisääminen käyttäjälle**

Jotta sovelluksen admin-tason työkaluihin pääsisi käsiksi, täytyy jonkin käyttäjän rooleihin lisätä tämä taso. Tämä onnistuu jälleen sqliten avulla. Esimerkissä lisätään käyttäjätaso käyttäjälle jonka id on 1.

	$ sqlite3 application/gearlists.db 
	sqlite> INSERT INTO user_roles (user_id, role_id) VALUES (1,1);
	sqlite> .exit
	
#### Asentaminen Herokuun
Asenna ohjelma ensin paikallisesti, yllä olevien ohjeiden mukaan.

Tämän jälkeen, luo käyttäjätunnus herokuun ja asenna Herokun CLI työkalut.
Ohjeita tähän löytyy täältä: https://devcenter.heroku.com/articles/heroku-cli

Kun olet asentanut työkalut, kirjaudu komentorivillä tilillesi ohjeiden mukaan.

Ennen projektin siirtämistä, pitää Herokuun luoda paikka uudelle sovellukselle.
Tämä onnistuu myös nettiselaimen kautta, mutta luo paikka komentorivillä:

	$ heroku create sovelluksen-nimi

Komentorivillä näet sovelluksen osoitteen herokussa.
Lisää sovellus vielä gittiin:

	$ git remote add heroku sovelluksen-osoite

Kommitoi tekemäsi muutokset ja siirrä sovellus verkkoon:

	$ git add .
	$ git commit -m "Sovelluksen siirto herokuun"
	$ git push heroku master
	
Sovellus on nyt verkossa.

Herokuun täytyy vielä määritellä ympäristömuuttuja ja luoda tietokanta jotta sovellus toimisi oikein.

	$ heroku config:set HEROKU=1
	$ heroku addons:add heroku-postgresql:hobby-dev

Palvelimen tietokantaan on vielä lisättävä käyttäjäroolit.

	$ heroku pg:psql
	DATABASE=> INSERT INTO role (role) VALUES ('ADMIN'), ('USER');
	DATABASE=> \q
	
Sovellus on nyt käytettävissä nettiselaimella herokun antamassa osoitteessa.