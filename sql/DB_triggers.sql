-- noinspection SqlDialectInspectionForFile

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

        IF NEW.brand_id IS NOT NULL THEN
        SELECT brand_name, brand_rating, brand_image, description INTO productName, productRating, productImage, descriptionProduct
        FROM Brand
        WHERE bid = NEW.brand_id;


#         SET productName = (SELECT brand_name FROM Brand WHERE bid = NEW.brand_id);
#         SET productRating = (SELECT brand_rating FROM Brand WHERE bid = NEW.brand_id);
#         SET productImage = (SELECT brand_image FROM Brand WHERE bid = NEW.brand_id);
#         SET descriptionProduct = (SELECT description FROM Brand WHERE bid = NEW.brand_id);

        IF productName IS NULL THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'productName not found.';
        ELSE
            SET NEW.brand_name = productName;
            SET NEW.brand_rating = productRating;
            SET NEW.brand_image = productImage;
            SET NEW.description = descriptionProduct;
        END IF;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Product info is missing.';
DELIMITER ;

#Trigger lorsqu’un client désire ajouter un nouvel article dans son panier,gâchette pour vérifier si la quantité en inventaire est suffisante.
# Si ce n’est pas le cas, un message d’erreur indiquant que la quantité en inventaire est insuffisante est lancé

DELIMITER //
CREATE TRIGGER CheckQuantityBeforeCartOperation BEFORE INSERT OR UPDATE ON Cart
FOR EACH ROW
    BEGIN
        DECLARE qtyOfBrandModel INTEGER;
        SET qtyOfBrandModel = (SELECT quantity FROM Brand_Model WHERE bmid = NEW.brand_model_id);
        IF qtyOfBrandModel < NEW.quantity THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Product is Out Of Stock';
        END IF;
    END //
DELIMITER ;

# DELIMITER //
# CREATE TRIGGER checkProductQuantityDuringUpdate BEFORE UPDATE ON Cart
#     FOR EACH ROW
#     BEGIN
#         DECLARE qtyOfBrandModel INTEGER;
#         SET qtyOfBrandModel = (SELECT quantity FROM Brand_Model WHERE bmid = NEW.brand_model_id);
#         IF qtyOfBrandModel < NEW.quantity THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Product is Out Of Stock';
#         END IF;
#     END //
# DELIMITER ;

DELIMITER //
CREATE TRIGGER CheckMultipleSameProductsInCart BEFORE INSERT ON Cart
FOR EACH ROW
    BEGIN
        DECLARE brandModelID INTEGER;
        SET brandModelID = NEW.brand_model_id;
        IF brandModelID IN (SELECT brand_model_id FROM Cart)
            THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Product is already in your Cart';
        END IF;
    END //
DELIMITER ;

#Création de trigger qui permet d'avoir un apercu du prix total d'un order
#Ce Trigger sert plus de visualisation lors de l'ajout de nouveaux produits par un Customer
DELIMITER //
CREATE TRIGGER SyncCartwPickedItems AFTER INSERT OR UPDATE ON Cart
FOR EACH ROW
    BEGIN
        DECLARE p_checkout_id INTEGER;
        SET p_checkout_id = (SELECT checkout_id FROM Checkout WHERE customer_id = NEW.cid AND order_id IS NULL);
        IF p_checkout_id IS NULL THEN
            INSERT INTO Checkout (customer_id) VALUES (NEW.cid);
            SET p_checkout_id = LAST_INSERT_ID();
        END IF;

        IF EXISTS(SELECT 1 FROM C_Picked_Items WHERE checkout_id=p_checkout_id AND brand_model_id = NEW.brand_model_id) THEN
            UPDATE C_Picked_Items SET quantity = NEW.quantity, order_total = NEW.order_total, order_total_discount = NEW.order_total_discount
            WHERE checkout_id = p_checkout_id AND brand_model_id = NEW.brand_model_id;
        ELSE
            INSERT INTO C_Picked_Items(checkout_id, brand_model_id, quantity, order_total, order_total_discount)
            VALUES (p_checkout_id, NEW.brand_model_id, NEW.quantity, NEW.order_total, NEW.order_total_discount);
        END IF;
    END //
DELIMITER ;

# #Ce trigger permet de mettre a jour les info dans le panier vers la table c_picked_items (customer_picked_items)
# DELIMITER //
# CREATE TRIGGER UpdateCustomerPickedItemsAfterUpdateInCart AFTER UPDATE ON Cart
# FOR EACH ROW
#     BEGIN
#         UPDATE c_picked_items SET quantity = NEW.quantity, order_total = NEW.order_total,
#                                   order_total_discount = NEW.order_total_discount
#                               WHERE checkout_id = (SELECT checkout_id FROM Checkout WHERE customer_id = NEW.cid AND order_id IS NULL)
#                                 AND brand_model_id = NEW.brand_model_id;
#     END //
# DELIMITER ;

#Ce trigger permet de mettre a jour le panier lorsque le Customer enleve dans le panier un item
DELIMITER //
CREATE TRIGGER UpdateCartQuantityAfterUpdateInCheckout AFTER DELETE ON Cart
FOR EACH ROW
    BEGIN
        DELETE FROM c_picked_items WHERE checkout_id = (SELECT checkout_id FROM Checkout WHERE customer_id = OLD.cid AND
                                                         order_id IS NULL) AND brand_model_id = OLD.brand_model_id;
    END //
DELIMITER ;

#Ce trigger permet de mettre a jour le panier. Celui-ci plus precisement la quantite

/* Test
INSERT INTO Cart(cid, brand_model_id, quantity, order_total, order_total_discount) VALUES (2000001 ,8000002, 1, 207, 30);
UPDATE Cart SET quantity = 4 WHERE brand_model_id = 8000002;
INSERT INTO Cart(cid, brand_model_id, quantity, order_total, order_total_discount) VALUES (2000001 ,8000002, 1, 207, 30);
DELETE FROM Cart WHERE brand_model_id = 8000002;
SELECT * FROM cart;
SELECT * FROM c_picked_items;
SELECT * FROM checkout;
SELECT * FROM orders;
*/
 #SELECT * FROM customer;


#Ce trigger permet d'obtenir le prix total d'une commande et de finaliser ]e prix dans la table checkout
DELIMITER //
CREATE TRIGGER produceTotalCheckout AFTER INSERT ON C_Picked_Items
FOR EACH ROW
    BEGIN
        DECLARE p_checkout_id INTEGER;
        DECLARE productsTotal DECIMAL(10,2);
        DECLARE productsTotalDiscount DECIMAL(10, 2);
        DECLARE orderTotal DECIMAL(10, 2);
        DECLARE finalPrice DECIMAL(10,2);

        SET productsTotal = (SELECT SUM(order_total) FROM C_Picked_Items WHERE checkout_id = NEW.checkout_id);
        SET productsTotalDiscount = (SELECT SUM(order_total_discount) FROM C_Picked_Items WHERE checkout_id = NEW.checkout_id);
        SET orderTotal = productsTotal * (SELECT quantity FROM c_picked_items WHERE checkout_id = NEW.checkout_id);
        SET finalPrice = (orderTotal * (1 + (SELECT tax_rate FROM Checkout WHERE checkout_id = NEW.checkout_id))) - productsTotalDiscount;

        SELECT checkout_id INTO p_checkout_id FROM Checkout WHERE customer_id =
                                                          (SELECT customer_id FROM Checkout WHERE checkout_id = NEW.checkout_id)
                                                           AND order_id IS NULL;
        UPDATE Checkout SET  total_discount = productsTotalDiscount, order_total = orderTotal, total_price=finalPrice
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

        SET qty = (SELECT quantity FROM Cart WHERE brand_model_id = NEW.brand_model_id);
        SET orderTotal = (SELECT order_total FROM Cart WHERE brand_model_id = NEW.brand_model_id);
        SET orderTotalDiscount = (SELECT order_total_discount FROM Cart WHERE brand_model_id = NEW.brand_model_id);

        UPDATE c_picked_items SET order_total = qty * orderTotal WHERE brand_model_id = NEW.brand_model_id;
        UPDATE c_picked_items SET order_total_discount = qty * orderTotalDiscount WHERE brand_model_id = NEW.brand_model_id;
    END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER CustomerPickedItemsOrderTotal AFTER INSERT ON Cart
FOR EACH ROW
    BEGIN
        DECLARE qty INTEGER;
        DECLARE orderTotal decimal(10,2);
        DECLARE orderTotalDiscount decimal(10,2);

        SET qty = (SELECT quantity FROM Cart WHERE brand_model_id = NEW.brand_model_id);
        SET orderTotal = (SELECT order_total FROM Cart WHERE brand_model_id = NEW.brand_model_id);
        SET orderTotalDiscount = (SELECT order_total_discount FROM Cart WHERE brand_model_id = NEW.brand_model_id);

        UPDATE c_picked_items SET order_total = qty * orderTotal WHERE brand_model_id = NEW.brand_model_id;
        UPDATE c_picked_items SET order_total_discount = qty * orderTotalDiscount WHERE brand_model_id = NEW.brand_model_id;
    END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER
