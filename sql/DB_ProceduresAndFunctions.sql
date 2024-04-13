#Procesure pour chercher un produit dans les product models
DELIMITER //
CREATE PROCEDURE Search(IN productToSearch VARCHAR(100))
    BEGIN
       SELECT DISTINCT bmid, brand_id, price, quantity, discount_id, brand_rating FROM Brand_Model
            WHERE brand_model_name LIKE concat('%', productToSearch, '%');
    END //
DELIMITER ;