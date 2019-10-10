## Käyttötapaukset

**Rekisteröityminen**

+ Käyttäjä voi rekisteröityä palveluun
Uuden käyttäjän lisääminen tietokantaan:

		INSERT INTO account (name, email, password) VALUES ('käyttäjänimi', 'sähköpostiosoite', 'salasana');

**Kirjautuminen**

+ Käyttäjä voi kirjautua palveluun
+ Käyttäjä voi uloskirjautua palvelusta

**Varustelistat**

+ Käyttäjä voi tarkistella varustelistauksia
-Kaikki varustelistat yhteenlaskettuine painoineen ja tilavuuksineen saadaan kyselyllä:
		
		SELECT gearlist.id, gearlist.name, gearlist.description, account.name, SUM(item.weight), SUM(item.volume) 
			FROM gearlist 
			LEFT JOIN account ON gearlist.user_id = account.id 
			LEFT JOIN list_items ON gearlist.id = list_items.list_id 
			LEFT JOIN item ON list_items.item_id = item.id 
			WHERE NOT account.id = :user_id 
			GROUP BY gearlist.id, account.name);

kun parametrina annetaan user_id = -1.
Tällä kyselyllä saadaan listattua myös muut kun käyttäjän varustelistat, antamalla parametriksi käyttäjän id.

+ Rekisteröitynyt käyttäjä voi tarkistella omia varustelistojaan
-Käyttäjän omat varustelistat yhteenlaskettuine painoineen ja tilavuuksineen saadaan samankaltaisella kyselyllä:

		SELECT gearlist.id, gearlist.name, gearlist.description, account.name, SUM(item.weight), SUM(item.volume) 
			FROM gearlist 
			LEFT JOIN account ON gearlist.user_id = account.id 
			LEFT JOIN list_items ON gearlist.id = list_items.list_id 
			LEFT JOIN item ON list_items.item_id = item.id 
			WHERE account.id = :user_id 
			GROUP BY gearlist.id, account.name);

Tällä kertaa user_id on vaan kyselyssä ilman negaatiota.

+ Rekisteröitynyt käyttäjä voi luoda omia varustelistoja
-Varustelistan syöttäminen tietokantaan:

		INSERT INTO gearlist (name, user_id, description) VALUES ('Listan nimi', 'user_id', 'Kuvaus');


+ Rekisteröitynyt käyttäjä voi poistaa omia varustelistojaan
-Varustelistan poistaminen tietokannasta:

		DELETE FROM gearlist WHERE id = :gearlist_id;

+ Rekisteröitynyt käyttäjä voi muokata omia varustelistojaan

Varistelistaan voi lisätä varusteita jotka ovat käyttäjän omia ja joita ei ole vielä lisätty listaan. 
-Näiden hakeminen onnistuu seuraavalla kyselyllä:
			
		SELECT * FROM item 
		WHERE item.user_id = :user_id
		AND item.id NOT IN (SELECT list_items.item_id FROM list_items WHERE list_items.list_id IS :list_id);

- Varusteen lisääminen varustelistaan:

		INSERT INTO list_items (list_id, item_id) VALUES ('list_id' , 'item_id')

-Varusteen poistaminen varustelistasta:

	DELETE FROM list_items WHERE list_id = :list_id AND item_id = :item_id;	
	
**Varusteet**

+ Käyttäjä voi tarkistella varusteita listana
-Kaikki varusteet saadaan kyselyllä:

		SELECT * FROM item WHERE NOT user_id = :user_id;
		
Jossa parametrina annetaan user_id = -1. Samalla kyselyllä saadaan listattua muut kun käyttäjän varusteet, antamalla parametrina käyttäjän id:n.

-Käyttäjän omien varusteiden listaaminen onnistuu kyselyllä:

		SELECT * FROM item WHERE user_id = :user_id;
		
+ Rekisteröitynyt käyttäjä voi luoda omia varusteita
-Uuden varusteen lisääminen tietokantaan:

		INSERT INTO item (name, user_id, category, brand, weight, volume, description) VALUES ('nimi', 'user_id', 'kategoria', 'merkki', 'paino', 'tilavuus', 'kuvaus');

+ Rekisteröitynyt käyttäjä voi muokata omia varusteitaan
-Varusteen tietojen päivittäminen tietokannassa:

		UPDATE item 
		SET name = 'nimi',
		    category = 'kategoria',
		    brand = 'merkki',
		    weight = 'paino',
		    volume = 'tilavuus',
		    description = 'kuvaus'
		WHERE id = :item_id;

+ Rekisteröitynyt käyttäjä voi poistaa omia varusteitaan
-Varusteen poistaminen tietokannasta:

		DELETE FROM item WHERE item_id = :item_id;	

+ Rekisteröitynyt käyttäjä voi kopioida muiden tekemiä varusteita omaan listaansa
-Tietyn varusteen hakeminen tietokannasta:

		SELECT * FROM item WHERE id = :item_id;