#Procesure pour chercher un produit dans les product models
DELIMITER //
CREATE PROCEDURE Search(IN productToSearch VARCHAR(100))
    BEGIN
       SELECT DISTINCT bmid, brand_id, price, quantity, discount_id, brand_rating FROM Brand_Model
            WHERE brand_model_name LIKE concat('%', productToSearch, '%');
    END //
DELIMITER ;

#Procedure qui permettera de mettre a jour la table Checkout a chaque fois qu'un utilisateur modifie le nombre de produit qu'il veut.
DELIMITER //
CREATE PROCEDURE updateCheckout(IN p_checkout_id INTEGER)
BEGIN
    DECLARE productsTotal DECIMAL(10,2);
    DECLARE productsTotalDiscount DECIMAL(10, 2);
    DECLARE orderTotal DECIMAL(10, 2);
    DECLARE finalPrice DECIMAL(10,2);

    SET productsTotal = (SELECT SUM(order_total) FROM C_Picked_Items WHERE checkout_id = p_checkout_id);
    SET productsTotalDiscount = (SELECT SUM(order_total_discount) FROM C_Picked_Items WHERE checkout_id = p_checkout_id);
    #SET orderTotal = productsTotal * (SELECT quantity FROM c_picked_items WHERE checkout_id = NEW.checkout_id AND brand_model_id = NEW.brand_model_id);
    SET finalPrice = (productsTotal * (1 + 0.15)) - productsTotalDiscount;

    UPDATE Checkout SET total_discount = productsTotalDiscount, order_total = productsTotal, total_price=finalPrice
    WHERE checkout_id = p_checkout_id;
END //
DELIMITER ;

CALL updateCheckout(11000000);