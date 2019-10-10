# Tietokanta

##Tietokantakaavio
![Tietokantakaavio](https://github.com/juhakaup/ReissuReppu/blob/master/documents/tsoha.png  "Tietokantakaavio")

##Create table lauseet
	CREATE TABLE account (
    	id INTEGER NOT NULL, 
		date_created DATETIME, 
		date_modified DATETIME, 
		name VARCHAR(100) NOT NULL, 
		email VARCHAR(100) NOT NULL, 
		password VARCHAR(144) NOT NULL, 
		PRIMARY KEY (id)
	);

	CREATE TABLE item (
		id INTEGER NOT NULL, 
		date_created DATETIME, 
		date_modified DATETIME, 
		name VARCHAR(100) NOT NULL, 
		user_id INTEGER NOT NULL, 
		category VARCHAR(100) NOT NULL, 
		brand VARCHAR(100) NOT NULL, 
		weight INTEGER NOT NULL, 
		volume NUMERIC(5) NOT NULL, 
		description VARCHAR(500) NOT NULL, 
		PRIMARY KEY (id), 
		FOREIGN KEY(user_id) REFERENCES account (id)
	);

	CREATE TABLE gearlist (
		id INTEGER NOT NULL, 
		date_created DATETIME, 
		date_modified DATETIME, 
		name VARCHAR(100) NOT NULL, 
		user_id INTEGER NOT NULL, 
		description VARCHAR(500) NOT NULL, 
		PRIMARY KEY (id), 
		FOREIGN KEY(user_id) REFERENCES account (id)
	);

	CREATE TABLE list_items (
		list_id INTEGER, 
		item_id INTEGER, 
		FOREIGN KEY(list_id) REFERENCES gearlist (id), 
		FOREIGN KEY(item_id) REFERENCES item (id)
	);
