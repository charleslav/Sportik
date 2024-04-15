#Procesure pour chercher un produit dans les product models
DELIMITER //
CREATE PROCEDURE Search(IN productToSearch VARCHAR(100))
    BEGIN
       SELECT DISTINCT bmid, brand_id, price, quantity, discount_id, brand_rating FROM Brand_Model
            WHERE brand_model_name LIKE concat('%', productToSearch, '%');
    END //
DELIMITER ;

#Procedure qui permettera de mettre a jour la table Checkout a chaque fois qu'un utilisateur modifie le nombre de produit qu'il veut.
#Pour trouver le bon checkoud_id dans la table C_Picked_Items, il faut : SELECT checkout_id FROM Checkout WHERE customer_id = 'le customer_id'
DELIMITER //
CREATE PROCEDURE updateCheckout(IN p_checkout_id INTEGER)
BEGIN
    DECLARE productsTotal DECIMAL(10,2);
    DECLARE productsTotalDiscount DECIMAL(10, 2);
    DECLARE orderTotal DECIMAL(10, 2);
    DECLARE taxPrice DECIMAL(10, 2);
    DECLARE finalPrice DECIMAL(10,2);

    SET productsTotal = (SELECT SUM(order_total) FROM C_Picked_Items WHERE checkout_id = p_checkout_id);
    SET productsTotalDiscount = (SELECT SUM(order_total_discount) FROM C_Picked_Items WHERE checkout_id = p_checkout_id);
    #SET orderTotal = productsTotal * (SELECT quantity FROM c_picked_items WHERE checkout_id = NEW.checkout_id AND brand_model_id = NEW.brand_model_id);
    SET taxPrice = (productsTotal * (1 + 0.15)) - productsTotal;
    SET finalPrice = (productsTotal * (1 + 0.15)) - productsTotalDiscount;

    UPDATE Checkout SET tax_price = taxPrice, total_discount = productsTotalDiscount, order_total = productsTotal, total_price=finalPrice
    WHERE checkout_id = p_checkout_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateStockQuantityAfterPurchase(IN p_checkout_id INTEGER)
BEGIN
    curseur: BEGIN

    #Check si le Checkout ID qu'on passe est bon.
    IF NOT EXISTS (SELECT 1 FROM Checkout WHERE checkout_id = p_checkout_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid checkout ID';
        LEAVE curseur;
    END IF;

    #Update la quantite de brand model
    UPDATE Brand_Model bm
    INNER JOIN C_Picked_Items cpi ON bm.bmid = cpi.brand_model_id
    SET bm.quantity = bm.quantity - cpi.quantity
    WHERE cpi.checkout_id = p_checkout_id;

    END curseur;
    COMMIT;
END //

DELIMITER ;
