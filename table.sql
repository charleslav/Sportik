#Creation de la Database
CREATE DATABASE Sportik;
USE Sportik;

#Creation des tables
CREATE TABLE Product(pid integer NOT NULL DEFAULT 0, product_name varchar(100) NOT NULL,  product_rating integer NOT NULL, product_image varchar(250) NOT NULL, description varchar(2000) NOT NULL,
                    constraint PK_ProductID PRIMARY KEY (pid),
                    constraint CT_Rating_Range CHECK (product_rating BETWEEN 0 AND 5)
                    );

#Changer order et regarder le datatype de is_featured pour le bool
CREATE TABLE Provider (sid integer NOT NULL DEFAULT 0, provider_name varchar(100) NOT NULL, is_featured bool NOT NULL, order integer NOT NULL, featured_image varchar(250) NOT NULL);

CREATE TABLE Discount(did integer NOT NULL PRIMARY KEY,
discount_rate decimal DEFAULT NULL,
discount_amount decimal DEFAULT NULL, start_date date, end_date date);

CREATE TABLE Product_Packaging(ppid integer PRIMARY KEY,
dimension varchar(50) NOT NULL DEFAULT 5,
weight decimal NOT NULL DEFAULT 1,
packaging_material varchar(30) NOT NULL);

CREATE TABLE Category (catid integer PRIMARY KEY ,
category_name varchar(30) NOT NULL,
parent_category_id varchar(20));                                                     #CATEGORIE DUNE CATÉGORIE

CREATE TABLE Customer(id integer PRIMARY KEY ,
name varchar(35) NOT NULL,
username varchar(50) UNIQUE NOT NULL,
password varchar(50) NOT NULL,
age tinyint NOT NULL check(age > 16),
email varchar(40) UNIQUE NOT NULL,
creation_date date,
card_total_price integer DEFAULT 0);

CREATE TABLE Customer_review(commid integer PRIMARY KEY,
created_at date NOT NULL, item_rating_review varchar(1000) UNIQUE);                                #STARS ?

CREATE TABLE Product_Model_Image(pmid INTEGER PRIMARY KEY,
thumbnail varchar(400) NOT NULL,
image varchar(400) NOT NULL);

CREATE TABLE Product_Model(id integer PRIMARY KEY,
product_name varchar(200) UNIQUE NOT NULL,
price decimal DEFAULT 0 NOT NULL,
prodduct_rating decimal NOT NULL,
quantity integer NOT NULL,
upc varchar(500) UNIQUE NOT NULL,                                                          #doute x2
sku varchar(500) UNIQUE NOT NULL);                                                         #doute x2
