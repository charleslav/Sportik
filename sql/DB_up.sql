#Creation de la Database
CREATE DATABASE Sportik;
USE Sportik;
/*
Pour les auto increment (W3 Schools)

In Oracle the code is a little bit more tricky.

You will have to create an auto-increment field with the sequence object (this object generates a number sequence).

Use the following CREATE SEQUENCE syntax:
CREATE SEQUENCE seq_person
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;
*/

#Creation des tables #1
CREATE TABLE IF NOT EXISTS Category (catid integer AUTO_INCREMENT NOT NULL,
                       category_name varchar(30) NOT NULL,
                       parent_category_id varchar(20),
                       PRIMARY KEY (catid)); #CATEGORIE DUNE CATÉGORIE
ALTER TABLE Category AUTO_INCREMENT=1000000;
INSERT INTO Category(catid,category_name,parent_category_id) VALUES ();

CREATE TABLE IF NOT EXISTS Customer (cid integer AUTO_INCREMENT NOT NULL,
                       name varchar(35) NOT NULL,
                       username varchar(50) UNIQUE NOT NULL,
                       password varchar(50) NOT NULL,
                       age tinyint NOT NULL check(age > 16),
                       email varchar(40) UNIQUE NOT NULL,
                       customer_adress varchar(255) UNIQUE NOT NULL,
                       creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                       card_total_price integer DEFAULT 0,
                       PRIMARY KEY(cid));
ALTER TABLE Customer AUTO_INCREMENT=2000000;
INSERT INTO Customer(cid, name, username, password, age, email, customer_adress, creation_date, card_total_price) VALUES ();

#Changer order et regarder le datatype de is_featured pour le bool
CREATE TABLE IF NOT EXISTS Provider (provider_id integer AUTO_INCREMENT NOT NULL,
                       provider_name varchar(100) NOT NULL,
                       is_featured bool NOT NULL,
                       provider_order_number integer NOT NULL,
                       featured_image varchar(250) NOT NULL,
                       PRIMARY KEY (provider_id));
ALTER TABLE  Provider AUTO_INCREMENT=3000000;
INSERT INTO Provider(provider_id, provider_name, is_featured, provider_order_number, featured_image) VALUES ();

CREATE TABLE IF NOT EXISTS Product_Packaging (ppid integer AUTO_INCREMENT NOT NULL,
                               dimension varchar(25) NOT NULL DEFAULT 5,
                               weight decimal NOT NULL DEFAULT 1,
                               packaging_material varchar(30) NOT NULL,
                               PRIMARY KEY (ppid));
ALTER TABLE Product_Packaging AUTO_INCREMENT=3000000;
INSERT INTO Product_Packaging(ppid, dimension, weight, packaging_material) VALUES ();

CREATE TABLE IF NOT EXISTS Discount (did integer AUTO_INCREMENT NOT NULL,
                      discount_rate decimal DEFAULT NULL,
                      discount_amount decimal DEFAULT NULL,
                      start_date date,
                      end_date date,
                      PRIMARY KEY(did));
ALTER TABLE Discount AUTO_INCREMENT=4000000;
INSERT INTO Discount(did, discount_rate, discount_amount, start_date, end_date) VALUES ();

CREATE TABLE IF NOT EXISTS Product_Model_Image (product_model_image_id INTEGER AUTO_INCREMENT NOT NULL,
                                 thumbnail varchar(250) NOT NULL,
                                 image varchar(250) NOT NULL,
                                 PRIMARY KEY(product_model_image_id));
ALTER TABLE Product_Model_Image AUTO_INCREMENT=5000000;
INSERT INTO Product_Model_Image(product_model_image_id, thumbnail, image) VALUES ();

CREATE TABLE IF NOT EXISTS Orders (order_id integer AUTO_INCREMENT NOT NULL,
                     payment_method varchar(20) NOT NULL,
                     payment_status ENUM ('Succes', 'In Progress', 'Denied') NOT NULL,
                     order_date DATE NOT NULL,
                     order_status ENUM ('Succes', 'In Progress', 'Canceled') NOT NULL,
                     PRIMARY KEY (order_id));
ALTER TABLE Orders AUTO_INCREMENT=6000000;
INSERT INTO Orders(order_id, payment_method, payment_status, order_date, order_status) VALUES ();
#Creation des tables #2
CREATE TABLE IF NOT EXISTS Product(pid integer AUTO_INCREMENT NOT NULL,
                     product_name varchar(100) NOT NULL,
                     product_rating integer NOT NULL,
                     product_image varchar(250) NOT NULL,
                     description varchar(2000) NOT NULL,
                     provider_id INTEGER NOT NULL,
                     PRIMARY KEY (pid),
                     FOREIGN KEY (provider_id) REFERENCES Provider(provider_id),
                     constraint CT_Rating_Range CHECK (product_rating BETWEEN 0 AND 5));
ALTER TABLE Product AUTO_INCREMENT=7000000;
INSERT INTO Product(pid, product_name, product_rating, product_image, description, provider_id) VALUES ();

CREATE TABLE IF NOT EXISTS Product_Model (pmid integer AUTO_INCREMENT NOT NULL,
                           product_name varchar(200) UNIQUE NOT NULL,
                           price decimal DEFAULT 0 NOT NULL,
                           quantity integer NOT NULL,
                           product_id integer NOT NULL,
                           discount_id integer NOT NULL,
                           packaging_id integer NOT NULL,
                           upc varchar(13) UNIQUE NOT NULL,  #doute x2
                           sku varchar(14) UNIQUE NOT NULL,  #doute x2
                           PRIMARY KEY (pmid),
                           FOREIGN KEY (product_id) REFERENCES Product(pid),
                           FOREIGN KEY (discount_id) REFERENCES Discount(did),
                           FOREIGN KEY (packaging_id) REFERENCES Product_Packaging(ppid));
ALTER TABLE Product_Model AUTO_INCREMENT=8000000;
INSERT INTO Product_Model(pmid, product_name, price, quantity, product_id, discount_id, packaging_id, upc, sku) VALUES ();

CREATE TABLE IF NOT EXISTS Customer_review (crid integer AUTO_INCREMENT NOT NULL,
                              customer_id integer,
                              productModel_id integer,
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              item_rating_review varchar(1000),
                              PRIMARY KEY(crid),
                              FOREIGN KEY (customer_id) REFERENCES Customer(cid),
                              FOREIGN KEY (productModel_id) REFERENCES Product_Model(pmid));#STARS ?
ALTER TABLE Customer_review AUTO_INCREMENT=9000000;
INSERT INTO Customer_review(crid, customer_id, productModel_id, created_at, item_rating_review) VALUES ();

CREATE TABLE IF NOT EXISTS Cart  (pmid integer NOT NULL,
                    cid integer NOT NULL,
                    item_total DECIMAL(10,2) DEFAULT NULL,
                    quantity integer DEFAULT 1 NOT NULL,
                    item_discount_total DECIMAL(10,2) DEFAULT NULL,
                    FOREIGN KEY (pmid) REFERENCES Product_Model(pmid),
                    FOREIGN KEY (cid) REFERENCES Customer(cid));
ALTER TABLE Cart AUTO_INCREMENT=10000000;
INSERT INTO Cart(pmid, cid, item_total, quantity, item_discount_total) VALUES ();

/*
 Cette table permet de regrouper le Product et sa Categorie dans une table pour savoir quel est la categorie d'un produit
 */
CREATE TABLE IF NOT EXISTS Product_isClassifiedAs_Category (pid integer NOT NULL,
                                              catid integer NOT NULL,
                                              FOREIGN KEY (pid) REFERENCES Product(pid),
                                              FOREIGN KEY (catid) REFERENCES Category(catid));
ALTER TABLE Product_isClassifiedAs_Category AUTO_INCREMENT=11000000;
INSERT INTO Product_isClassifiedAs_Category(pid, catid) VALUES ();

/*
 Cette table permet de regrouper le Product Model et son type de Produit dans une table pour savoir quel variation de produit est associe
 a un produit.
 */
CREATE TABLE IF NOT EXISTS ProductModel_ISA_Product (product_model_id integer NOT NULL,
                                       product_id integer NOT NULL,
                                       FOREIGN KEY (product_model_id) REFERENCES Product_Model(pmid),
                                       FOREIGN KEY (product_id) REFERENCES Product(pid));
ALTER TABLE ProductModel_ISA_Product AUTO_INCREMENT=12000000;
INSERT INTO ProductModel_ISA_Product(product_model_id, product_id) VALUES ();