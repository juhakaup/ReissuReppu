#Sovelluksen asentaminen

Sovellus on tarkoitettu pääasiassa käytettäväksi web-sovelluksena nettiselaimen kautta. Sovelluksen voi kuitenkin asentaa myös omalle koneelle, kokeilua tai muokkaamista varten.

Nämä asennusohjeet käsittelevät asentamista linux-ympäristössä.

####Asentaminen paikallisesti

Ohjelman paikallista asentamista ja ajamista varten käyttäjällä tulee olla asennettuna python3 ja sqlite, sekä mahdollisesti git.

** Lataaminen omalle koneelle**
Lataa sovellus zip-tiedostona githubista 'Clone or download' -linkin takaa. Pura tiedosto haluamaasi kansioon.
Vaihtoehtoisesti voit kloonata projektin omalle koneellesi komennolla:

	$ git clone https://github.com/juhakaup/ReissuReppu.git
Tällöin koneellasi tulee olla asennettuna myös git.	

** Asennus **
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

** Ohjelman ajaminen **
Jos kaikki paketit asentuivat onnistuneesti, sovellus voidaan nyt käynnistää komennolla:

	(venv) $ python run.py
Sovelluksen pitäisi olla nyt käynnissä ja komentorivillä teksti:
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Sovellusta voi nyt käyttää nettiselaimella osoitteessa: http://127.0.0.1:5000/

####Asentaminen Herokuun
mitä tarvitsee git, heroku
Tilin luominen, ympäristömuuttujan määrittäminen, tietokannan luominen, uppaaminen