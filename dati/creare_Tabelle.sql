CREATE TABLE IF NOT EXISTS auto.venditore (
  id_venditore int NOT NULL AUTO_INCREMENT,
  nome_venditore VARCHAR(255) NOT NULL,
  stato VARCHAR(255) NOT NULL,
  citta VARCHAR(255) NOT NULL,
  provincia VARCHAR(255) NOT NULL,
  via VARCHAR(255) not null ,
  num_civico INT not null,
  telefono1 VARCHAR(25),
  telefono2 VARCHAR(25),
  telefono3 VARCHAR(25),
  DATA_LOAD Timestamp,
  DATA_CHANGE Timestamp,
  PRIMARY KEY (id_venditore)
);

CREATE TABLE IF NOT EXISTS auto.annuncio (
  id_annuncio int NOT NULL AUTO_INCREMENT,
  condizione VARCHAR(50) NOT NULL,
  marca VARCHAR(255) NOT NULL,
  modello VARCHAR(255) NOT NULL,
  prezzo decimal NOT NULL,
  km decimal not null ,
  data_immatr VARCHAR(25) not null,
  link VARCHAR(500),
  sito VARCHAR(50),
  proprietari int,
  DATA_LOAD Timestamp,
  DATA_CHANGE Timestamp,
  PRIMARY KEY (id_annuncio)
);

CREATE TABLE IF NOT EXISTS auto.tipo_auto (
  id_tipo_auto int NOT NULL AUTO_INCREMENT,
  emmissioni decimal(18,2),
  consumo_misto VARCHAR(50) ,
  consumo_urbano VARCHAR(50) ,
  consumo_extra_urbano VARCHAR(50) ,
  trasmissione VARCHAR(40),
  carburante VARCHAR(40),
  potenza VARCHAR(40),
  carrozzeria VARCHAR(40),
  DATA_LOAD Timestamp,
  DATA_CHANGE Timestamp,
  PRIMARY KEY (id_tipo_auto)
);


ALTER TABLE auto.venditore
add column id_annuncio int NOT NULL ,
add column id_tipo_auto int NOT NULL ,
ADD FOREIGN KEY (id_annuncio) REFERENCES annuncio(id_annuncio),
ADD FOREIGN KEY (id_tipo_auto) REFERENCES tipo_auto(id_tipo_auto);

ALTER TABLE auto.annuncio
add column id_venditore int NOT NULL ,
add column id_tipo_auto int NOT NULL ,
ADD FOREIGN KEY (id_venditore) REFERENCES venditore(id_venditore),
ADD FOREIGN KEY (id_tipo_auto) REFERENCES tipo_auto(id_tipo_auto);


ALTER TABLE auto.tipo_auto 
add column id_annuncio int NOT NULL ,
add column id_venditore int NOT NULL ,
ADD FOREIGN KEY (id_annuncio) REFERENCES annuncio(id_annuncio),
ADD FOREIGN KEY (id_venditore) REFERENCES venditore(id_venditore);



