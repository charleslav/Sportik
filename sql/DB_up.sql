# noinspection SqlCurrentSchemaInspectionForFile

#Creation de la Database
DROP DATABASE IF EXISTS Sportik;
CREATE DATABASE IF NOT EXISTS Sportik;
USE Sportik;

#Index
#index optimisation login request via Customer
CREATE INDEX index_c_usermail ON Customer(username, email);

#index mettant a jour article et panier utilisateur specifique via Cart.
CREATE INDEX index_cart_cid_bmid ON Cart(cid, brand_model_id);

#index filtrant les commandes par statut et date
CREATE INDEX index_orders_status_date ON Orders(payment_status, order_date);

#Creation des tables #1
CREATE TABLE IF NOT EXISTS Customer (cid integer AUTO_INCREMENT,
                       name varchar(35) NOT NULL,
                       username varchar(50) UNIQUE NOT NULL,
                       password varchar(500) NOT NULL,
                       age tinyint NOT NULL check(age >= 16),
                       email varchar(40) UNIQUE NOT NULL,
                       customer_adress varchar(255) NOT NULL,
                       creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                       card_total_price integer DEFAULT 0,
                       PRIMARY KEY(cid));
ALTER TABLE Customer AUTO_INCREMENT=2000000;

CREATE TABLE IF NOT EXISTS Discount (did integer AUTO_INCREMENT ,
                      discount_rate decimal DEFAULT NULL,
                      start_date date NOT NULL,
                      end_date date NOT NULL,
                      is_active BOOLEAN DEFAULT FALSE NOT NULL,                               /* va etre activer comme true lorsque start_date va etre hit, false lorsque end_date va hit */
                      PRIMARY KEY(did));
ALTER TABLE Discount AUTO_INCREMENT=4000000;


#Changer order et regarder le datatype de is_featured pour le bool
CREATE TABLE IF NOT EXISTS Provider (provider_id integer AUTO_INCREMENT ,
                       provider_name varchar(100) NOT NULL,
                       is_featured bool NOT NULL,
                       featured_image varchar(250) NOT NULL,
                       PRIMARY KEY (provider_id));
ALTER TABLE  Provider AUTO_INCREMENT=3000000;

#Creation des tables #2
CREATE TABLE IF NOT EXISTS Brand(bid integer AUTO_INCREMENT,
                     brand_name varchar(100) NOT NULL,
                     brand_rating integer NOT NULL,
                     brand_image varchar(250) NOT NULL,
                     description varchar(2000) NOT NULL,
                     provider_id INTEGER,
                     PRIMARY KEY (bid),
                     FOREIGN KEY (provider_id) REFERENCES Provider(provider_id),
                     constraint CT_Rating_Range CHECK (brand_rating BETWEEN 0 AND 5));
ALTER TABLE Brand AUTO_INCREMENT=7000000;

#Cette table prend toutes les attributs de Brand. Là où il y a DEFAULT NULL, un trigger va venir inserer les donnes necessaires pour la completion de cette table
CREATE TABLE IF NOT EXISTS Brand_Model (bmid integer AUTO_INCREMENT ,
                           brand_model_name varchar(200) UNIQUE NOT NULL,
                           price decimal DEFAULT 0 NOT NULL,
                           quantity integer NOT NULL,
                           isInStock BOOLEAN DEFAULT TRUE NOT NULL,
                           discount_id integer DEFAULT NULL,
                           packaging_id integer NOT NULL,
                           brand_id integer NOT NULL,
                           brand_name varchar(100) DEFAULT NULL,
                           brand_rating integer DEFAULT NULL,
                           brand_image varchar(250) DEFAULT NULL,
                           description varchar(2000) DEFAULT NULL,
                           PRIMARY KEY (bmid),
                           FOREIGN KEY (brand_id) REFERENCES Brand(bid),
                           FOREIGN KEY (discount_id) REFERENCES Discount(did));
ALTER TABLE Brand_Model AUTO_INCREMENT=8000000;

CREATE TABLE IF NOT EXISTS Customer_review (crid integer AUTO_INCREMENT,
                              customer_id integer,
                              brand_model_id integer,
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              brand_rating_review varchar(1000),
                              PRIMARY KEY(crid),
                              FOREIGN KEY (customer_id) REFERENCES Customer(cid),
                              FOREIGN KEY (brand_model_id) REFERENCES Brand_Model(bmid));
ALTER TABLE Customer_review AUTO_INCREMENT=9000000;


CREATE TABLE IF NOT EXISTS Cart  (brand_model_id integer ,
                    cid integer NOT NULL,
                    quantity integer DEFAULT 1 NOT NULL,
                    order_total DECIMAL(10,2) DEFAULT NULL,
                    order_total_discount DECIMAL(10,2) DEFAULT NULL,
                    FOREIGN KEY (brand_model_id) REFERENCES Brand_Model(bmid),
                    FOREIGN KEY (cid) REFERENCES Customer(cid));
ALTER TABLE Cart AUTO_INCREMENT=10000000;
#INSERT INTO Cart(pmid, cid, total_amount, quantity, item_discount_total) VALUES ();

CREATE TABLE IF NOT EXISTS Brand_model_image (brand_model_image_id INTEGER AUTO_INCREMENT ,
                                brand_model_id integer NOT NULL,
                                image_type ENUM('thumbnail', 'main', 'gallery', 'zoomed') NOT NULL DEFAULT 'main', /*selectionner on veut presenter les images a quel endroit */
                                 image varchar(250) NOT NULL,
                                 PRIMARY KEY(brand_model_image_id),
                                 FOREIGN KEY(brand_model_id) REFERENCES Brand_Model(bmid));
ALTER TABLE Brand_model_image AUTO_INCREMENT=5000000;

#Cette table est la finalisation d'un achat. Elle stock les donnees d'une transaction.
CREATE TABLE IF NOT EXISTS Orders (order_id INTEGER AUTO_INCREMENT,
                                   payment_method ENUM('Bank Card', 'Credit Cart', 'In Cash') NOT NULL,
                                   payment_status ENUM ('Succes', 'In Progress', 'Denied') NOT NULL DEFAULT 'In Progress',
                                   order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                                   PRIMARY KEY (order_id));
ALTER TABLE Orders AUTO_INCREMENT=12000000;


#Cette table s'affiche avant de finaliser achat, par exemple quand on clique sur checkout pour voir les details d'un potientiel achat

CREATE TABLE IF NOT EXISTS Checkout (checkout_id INTEGER AUTO_INCREMENT,
                                          customer_id INTEGER,
                                          tax_rate DECIMAL(2,2) DEFAULT 0.15,
                                          tax_price DECIMAL(10, 2),
                                          total_discount DECIMAL (10, 2) DEFAULT NULL,
                                          order_total DECIMAL(10, 2) DEFAULT NULL,
                                          total_price DECIMAL(10, 2) DEFAULT NULL,
                                          PRIMARY KEY (checkout_id),
                                          FOREIGN KEY (customer_id) REFERENCES Customer(cid));
ALTER TABLE Checkout AUTO_INCREMENT=11000000;

#Cette table permet d'afficher les produits qui seront ajoute au panier d'un client.
#On peut savoir quel client a ajoute le produit a cause de son lien avec la table Transit_Order
CREATE TABLE IF NOT EXISTS C_Picked_Items (cpid integer AUTO_INCREMENT,
                     checkout_id INTEGER NOT NULL,
                     customer_id INTEGER NOT NULL,
                     brand_model_id INTEGER NOT NULL,
                     quantity INTEGER NOT NULL,
                     order_total DECIMAL(10, 2) NOT NULL,
                     order_total_discount DECIMAL(10, 2) NOT NULL,
                     PRIMARY KEY (cpid));
ALTER TABLE C_Picked_Items AUTO_INCREMENT=6000000;

ALTER TABLE C_Picked_Items
ADD FOREIGN KEY (checkout_id) REFERENCES Checkout(checkout_id),
ADD FOREIGN KEY (brand_model_id) REFERENCES Brand_Model(bmid),
ADD FOREIGN KEY (customer_id) REFERENCES Customer(cid);

CREATE TABLE IF NOT EXISTS Token(customer_id integer,
                                is_active BOOLEAN DEFAULT FALSE,
                                token varchar(250) DEFAULT NULL,
                                FOREIGN KEY (customer_id) REFERENCES Customer(cid));


