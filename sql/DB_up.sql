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

#Creation des tables
CREATE TABLE Product(pid integer AUTO_INCREMENT NOT NULL,
                     product_name varchar(100) NOT NULL,
                     product_rating integer NOT NULL,
                     product_image varchar(250) NOT NULL,
                     description varchar(2000) NOT NULL,
                     provider_id INTEGER NOT NULL,
                     PRIMARY KEY (pid),
                     FOREIGN KEY (provider_id) REFERENCES Provider(provider_id),
                     constraint CT_Rating_Range CHECK (product_rating BETWEEN 0 AND 5));

CREATE TABLE Product_Model (pmid integer AUTO_INCREMENT NOT NULL,
                           product_name varchar(200) UNIQUE NOT NULL,
                           price decimal DEFAULT 0 NOT NULL,
                           quantity integer NOT NULL,
                           upc varchar(13) UNIQUE NOT NULL,  #doute x2
                           sku varchar(14) UNIQUE NOT NULL,  #doute x2
                           PRIMARY KEY (pmid));

CREATE TABLE Category (catid integer AUTO_INCREMENT NOT NULL,
                       category_name varchar(30) NOT NULL,
                       parent_category_id varchar(20),
                       PRIMARY KEY (catid)); #CATEGORIE DUNE CATÉGORIE

CREATE TABLE Customer (cid integer AUTO_INCREMENT NOT NULL,
                       name varchar(35) NOT NULL,
                       username varchar(50) UNIQUE NOT NULL,
                       password varchar(50) NOT NULL,
                       age tinyint NOT NULL check(age > 16),
                       email varchar(40) UNIQUE NOT NULL,
                       creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       card_total_price integer DEFAULT 0,
                       PRIMARY KEY(cid));

CREATE TABLE Customer_review (crid integer AUTO_INCREMENT NOT NULL,
                              customer_id integer,
                              productModel_id integer,
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              item_rating_review varchar(1000) UNIQUE,
                              PRIMARY KEY(crid),
                              FOREIGN KEY (customer_id) REFERENCES Customer(cid),
                              FOREIGN KEY (productModel_id) REFERENCES Product_Model(pmid));#STARS ?

#Changer order et regarder le datatype de is_featured pour le bool
CREATE TABLE Provider (provider_id integer AUTO_INCREMENT NOT NULL,
                       provider_name varchar(100) NOT NULL,
                       is_featured bool NOT NULL,
                       provider_order_number integer NOT NULL,
                       featured_image varchar(250) NOT NULL,
                       PRIMARY KEY (provider_id));

CREATE TABLE Product_Packaging (ppid integer AUTO_INCREMENT NOT NULL,
                               dimension varchar(25) NOT NULL DEFAULT 5,
                               weight decimal NOT NULL DEFAULT 1,
                               packaging_material varchar(30) NOT NULL,
                               PRIMARY KEY (ppid));

CREATE TABLE Discount (did integer AUTO_INCREMENT NOT NULL,
                      discount_rate decimal DEFAULT NULL,
                      discount_amount decimal DEFAULT NULL,
                      start_date date,
                      end_date date,
                      PRIMARY KEY(did));

CREATE TABLE Product_Model_Image (product_model_image_id INTEGER AUTO_INCREMENT NOT NULL,
                                 thumbnail varchar(250) NOT NULL,
                                 image varchar(250) NOT NULL,
                                 PRIMARY KEY(product_model_image_id));

CREATE TABLE Orders (order_id integer AUTO_INCREMENT NOT NULL,
                     payment_method varchar(20) NOT NULL,
                     payment_status ENUM ('Succes', 'In Progress', 'Denied') NOT NULL,
                     order_date DATE NOT NULL,
                     order_status ENUM ('Succes', 'In Progress', 'Canceled') NOT NULL,
                     PRIMARY KEY (order_id));

CREATE TABLE Cart  (pmid integer NOT NULL,
                    cid integer NOT NULL,
                    item_total DECIMAL(10,2) DEFAULT NULL,
                    quantity integer DEFAULT 1 NOT NULL,
                    item_discount_total DECIMAL(10,2) DEFAULT NULL,
                    FOREIGN KEY (pmid) REFERENCES Product_Model(pmid),
                    FOREIGN KEY (cid) REFERENCES Customer(cid)
                    );

CREATE TABLE Product_isClassifiedAs_Category (pid integer NOT NULL,
                                              catid integer NOT NULL,
                                              FOREIGN KEY (pid) REFERENCES Product(pid),
                                              FOREIGN KEY (catid) REFERENCES Category(catid));
