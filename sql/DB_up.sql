#Creation de la Database
CREATE DATABASE Sportik;
USE Sportik;

#Creation des tables
CREATE TABLE Product(pid integer NOT NULL DEFAULT 0,
                     product_name varchar(100) NOT NULL,
                     product_rating integer NOT NULL,
                     product_image LONGBLOB NOT NULL, #LONGBLOB permet le stockage d'image de moins de 1mb par défaut, mais peut être changé dans le parametre du serveur
                     description varchar(2000) NOT NULL,
                     PRIMARY KEY (pid),
                     constraint CT_Rating_Range CHECK (product_rating BETWEEN 0 AND 5));

CREATE TABLE Product_Model (pmid integer,
                           product_name varchar(200) UNIQUE NOT NULL,
                           price decimal DEFAULT 0 NOT NULL,
                           product_rating decimal NOT NULL,
                           quantity integer NOT NULL,
                           upc varchar(13) UNIQUE NOT NULL,  #doute x2
                           sku varchar(14) UNIQUE NOT NULL,  #doute x2
                           PRIMARY KEY (pmid));

CREATE TABLE Category (catid integer,
                       category_name varchar(30) NOT NULL,
                       parent_category_id varchar(20),
                       PRIMARY KEY (catid)); #CATEGORIE DUNE CATÉGORIE

CREATE TABLE Customer (cid integer,
                       name varchar(35) NOT NULL,
                       username varchar(50) UNIQUE NOT NULL,
                       password varchar(50) NOT NULL,
                       age tinyint NOT NULL check(age > 16),
                       email varchar(40) UNIQUE NOT NULL,
                       creation_date DATE,
                       card_total_price integer DEFAULT 0,
                       PRIMARY KEY(cid));

CREATE TABLE Customer_review (crid integer,
                             created_at DATE NOT NULL,
                             item_rating_review varchar(1000) UNIQUE,
                             PRIMARY KEY(crid));#STARS ?

#Changer order et regarder le datatype de is_featured pour le bool
CREATE TABLE Provider (provider_id integer NOT NULL DEFAULT 0,
                       provider_name varchar(100) NOT NULL,
                       is_featured bool NOT NULL,
                       provider_order_number integer NOT NULL,
                       featured_image LONGBLOB NOT NULL,
                       PRIMARY KEY (provider_id));

CREATE TABLE Product_Packaging (ppid integer NOT NULL,
                               dimension varchar(25) NOT NULL DEFAULT 5,
                               weight decimal NOT NULL DEFAULT 1,
                               packaging_material varchar(30) NOT NULL,
                               PRIMARY KEY (ppid));

CREATE TABLE Discount (did integer NOT NULL,
                      discount_rate decimal DEFAULT NULL,
                      discount_amount decimal DEFAULT NULL,
                      start_date date,
                      end_date date,
                      PRIMARY KEY(did));

CREATE TABLE Product_Model_Image (pmid INTEGER,
                                 thumbnail varchar(400) NOT NULL,
                                 image LONGBLOB NOT NULL,
                                 PRIMARY KEY(pmid));

CREATE TABLE Orders (order_id integer NOT NULL,
                     payment_method varchar(20) NOT NULL,
                     payment_status varchar(12) NOT NULL,
                     order_date DATE NOT NULL,
                     order_status varchar(20) NOT NULL,
                     PRIMARY KEY (order_id));
