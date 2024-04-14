#Trigger avant insertion de la table Product_Model pour venir inserer les donnes de Product dans la table Product_Model
#Puisque cette table herite de Product

DELIMITER //
CREATE TRIGGER insertBrandInBrandModel BEFORE INSERT ON Brand_Model
FOR EACH ROW
    BEGIN
        DECLARE  productName VARCHAR(100);
        DECLARE  productRating INTEGER;
        DECLARE  productImage VARCHAR(250);
        DECLARE  descriptionProduct VARCHAR(2000);

        SET productName = (SELECT brand_name FROM Brand WHERE bid = NEW.brand_id);
        SET productRating = (SELECT brand_rating FROM Brand WHERE bid = NEW.brand_id);
        SET productImage = (SELECT brand_image FROM Brand WHERE bid = NEW.brand_id);
        SET descriptionProduct = (SELECT description FROM Brand WHERE bid = NEW.brand_id);

        SET NEW.brand_name = productName;
        SET NEW.brand_rating = productRating;
        SET NEW.brand_image = productImage;
        SET NEW.description = descriptionProduct;
    END //
DELIMITER ;



#Trigger lorsqu’un client désire ajouter un nouvel article dans son panier,gâchette pour vérifier si la quantité en inventaire est suffisante.
# Si ce n’est pas le cas, un message d’erreur indiquant que la quantité en inventaire est insuffisante est lancé

DELIMITER //
CREATE TRIGGER CheckQuantityWhenInsertBrandModelInCart BEFORE INSERT ON Cart
FOR EACH ROW
    BEGIN
        DECLARE qtyOfBrandModel INTEGER;
        SET qtyOfBrandModel = (SELECT quantity FROM Brand_Model WHERE bmid = NEW.brand_model_id);
        IF qtyOfBrandModel < NEW.quantity THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Product is Out Of Stock';
        END IF;
    END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER checkProductQuantityDuringUpdate BEFORE UPDATE ON Cart
    FOR EACH ROW
    BEGIN
        DECLARE qtyOfBrandModel INTEGER;
        SET qtyOfBrandModel = (SELECT quantity FROM Brand_Model WHERE bmid = NEW.brand_model_id);
        IF qtyOfBrandModel < NEW.quantity THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Product is Out Of Stock';
        END IF;
    END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER CheckMultipleSameProductsInCart BEFORE INSERT ON Cart
FOR EACH ROW
    BEGIN
        IF (SELECT COUNT(*) FROM Cart WHERE brand_model_id = NEW.brand_model_id AND cid = NEW.cid) > 0
        THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Product is already in your Cart';
        END IF;
    END //
DELIMITER ;


#Création de trigger qui permet d'avoir un apercu du prix total d'un order
#Ce Trigger sert plus de visualisation lors de l'ajout de nouveaux produits par un Customer
DELIMITER //
CREATE TRIGGER insertCustomerPickedItemsInCheckout AFTER INSERT ON Cart
FOR EACH ROW
    BEGIN
        DECLARE p_checkout_id INTEGER;
        SET p_checkout_id = (SELECT checkout_id FROM Checkout WHERE customer_id = NEW.cid AND order_id IS NULL);
        IF p_checkout_id IS NULL THEN
            INSERT INTO Checkout (customer_id) VALUES (NEW.cid);
            SET p_checkout_id = LAST_INSERT_ID();
        END IF;
        INSERT INTO C_Picked_Items(checkout_id, customer_id, brand_model_id, quantity, order_total, order_total_discount)
                    VALUES (p_checkout_id, NEW.cid, NEW.brand_model_id, NEW.quantity, NEW.order_total, NEW.order_total_discount);
    END //
DELIMITER ;

#Ce trigger permet de mettre a jour les info dans le panier vers la table c_picked_items (customer_picked_items)
DELIMITER //
CREATE TRIGGER UpdateCustomerPickedItemsAfterUpdateInCart AFTER UPDATE ON Cart
FOR EACH ROW
    BEGIN
        UPDATE c_picked_items SET quantity = NEW.quantity
                              WHERE checkout_id = (SELECT checkout_id FROM Checkout WHERE customer_id = NEW.cid AND order_id IS NULL)
                                AND brand_model_id = NEW.brand_model_id;
    END //
DELIMITER ;

DROP TRIGGER UpdateCustomerPickedItemsAfterUpdateInCart;

#Ce trigger permet de mettre a jour le panier lorsque le Customer enleve dans le panier un item
DELIMITER //
CREATE TRIGGER UpdateCartQuantityAfterUpdateInCheckout AFTER DELETE ON Cart
FOR EACH ROW
    BEGIN
        DELETE FROM c_picked_items WHERE checkout_id = (SELECT checkout_id FROM Checkout WHERE customer_id = OLD.cid AND
                                                         order_id IS NULL) AND brand_model_id = OLD.brand_model_id;
    END //
DELIMITER ;

#Ce trigger permet d'obtenir le prix total d'une commande et de finaliser le prix dans la table checkout
DELIMITER //
CREATE TRIGGER produceTotalCPickedItems AFTER INSERT ON C_Picked_Items
FOR EACH ROW
    BEGIN
        DECLARE p_checkout_id INTEGER;
        DECLARE productsTotal DECIMAL(10,2);
        DECLARE productsTotalDiscount DECIMAL(10, 2);
        DECLARE orderTotal DECIMAL(10, 2);
        DECLARE finalPrice DECIMAL(10,2);

        SET productsTotal = (SELECT SUM(order_total) FROM C_Picked_Items WHERE checkout_id = NEW.checkout_id);
        SET productsTotalDiscount = (SELECT SUM(order_total_discount) FROM C_Picked_Items WHERE checkout_id = NEW.checkout_id);
        #SET orderTotal = productsTotal * (SELECT quantity FROM c_picked_items WHERE checkout_id = NEW.checkout_id AND brand_model_id = NEW.brand_model_id);
        SET finalPrice = (productsTotal * (1 + 0.15)) - productsTotalDiscount;

        SELECT checkout_id INTO p_checkout_id FROM Checkout WHERE customer_id =
                                                          (SELECT customer_id FROM Checkout WHERE checkout_id = NEW.checkout_id)
                                                           AND order_id IS NULL;
        UPDATE Checkout SET  total_discount = productsTotalDiscount, order_total = productsTotal, total_price=finalPrice
                             WHERE checkout_id = p_checkout_id;
    END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER CustomerPickedItemsOrderTotalAfterUpdate AFTER UPDATE ON Cart
FOR EACH ROW
    BEGIN
        DECLARE qty INTEGER;
        DECLARE orderTotal decimal(10,2);
        DECLARE orderTotalDiscount decimal(10,2);

        SET qty = (SELECT quantity FROM Cart WHERE brand_model_id = NEW.brand_model_id AND cid = NEW.cid);
        SET orderTotal = (SELECT order_total FROM Cart WHERE brand_model_id = NEW.brand_model_id AND cid = NEW.cid);
        SET orderTotalDiscount = (SELECT order_total_discount FROM Cart WHERE brand_model_id = NEW.brand_model_id AND cid = NEW.cid);

        UPDATE c_picked_items SET order_total = qty * orderTotal WHERE brand_model_id = NEW.brand_model_id AND customer_id = NEW.cid;
        UPDATE c_picked_items SET order_total_discount = qty * orderTotalDiscount WHERE brand_model_id = NEW.brand_model_id AND customer_id = NEW.cid;
    END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER CustomerPickedItemsOrderTotal AFTER INSERT ON Cart
FOR EACH ROW
    BEGIN
        DECLARE qty INTEGER;
        DECLARE orderTotal decimal(10,2);
        DECLARE orderTotalDiscount decimal(10,2);

        SET qty = (SELECT quantity FROM Cart WHERE brand_model_id = NEW.brand_model_id AND cid = NEW.cid);
        SET orderTotal = (SELECT order_total FROM Cart WHERE brand_model_id = NEW.brand_model_id AND cid = NEW.cid);
        SET orderTotalDiscount = (SELECT order_total_discount FROM Cart WHERE brand_model_id = NEW.brand_model_id AND cid = NEW.cid);

        UPDATE c_picked_items SET order_total = qty * orderTotal WHERE brand_model_id = NEW.brand_model_id AND customer_id = NEW.cid;
        UPDATE c_picked_items SET order_total_discount = qty * orderTotalDiscount WHERE brand_model_id = NEW.brand_model_id AND customer_id = NEW.cid;
    END //
DELIMITER ;

/* Test

*/

INSERT INTO Cart(cid, brand_model_id, quantity, order_total, order_total_discount) VALUES (2000001 ,8000002, 1, 207, 30);
UPDATE Cart SET quantity = 4 WHERE brand_model_id = 8000002 AND cid = 2000001;
UPDATE Brand_Model SET quantity = 20 WHERE bmid = 8000002;
INSERT INTO Cart(cid, brand_model_id, quantity, order_total, order_total_discount) VALUES (2000001 ,8000003, 1, 207, 30);
INSERT INTO Cart(cid, brand_model_id, quantity, order_total, order_total_discount) VALUES (2000002 ,8000002, 1, 207, 30);
INSERT INTO Cart(cid, brand_model_id, quantity, order_total, order_total_discount) VALUES (2000002 ,8000012, 1, 207, 30);
INSERT INTO Cart(cid, brand_model_id, quantity, order_total, order_total_discount) VALUES (2000003 ,8000002, 1, 207, 30);
INSERT INTO Cart(cid, brand_model_id, quantity, order_total, order_total_discount) VALUES (2000004 ,8000006, 1, 207, 30);
INSERT INTO Cart(cid, brand_model_id, quantity, order_total, order_total_discount) VALUES (2000001 ,8000002, 1, 207, 30);
DELETE FROM Cart WHERE brand_model_id = 8000012;
SELECT * FROM cart;
SELECT * FROM c_picked_items;
SELECT * FROM brand_model;
SELECT * FROM checkout;
CALL updateCheckout(11000000);
SELECT * FROM orders;

#SELECT * FROM customer;
