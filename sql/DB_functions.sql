#Trigger après insertion de la table Product_Model pour venir inserer les donnes de Product dans la table Product_Model
#Puisque cette table herite de Product

DELIMITER //

CREATE TRIGGER after_product_model_insert
AFTER INSERT
ON Product_Model FOR EACH ROW
BEGIN
    IF NEW.product_name IS NULL OR NEW.description_product IS NULL OR NEW.product_image IS NULL THEN
        DECLARE variable_product_name VARCHAR(100);
        DECLARE variable_description_product VARCHAR(2000);
        DECLARE variable_product_image VARCHAR(250);
        
        SELECT product_name, description_product, product_image 
        INTO variable_product_name, variable_description_product, variable_product_image 
        FROM Product 
        WHERE pid = NEW.product_id;
        
        IF NEW.product_name IS NULL THEN
            SET NEW.product_name = variable_product_name;
        END IF;
        
        IF NEW.description_product IS NULL THEN
            SET NEW.description_product = variable_description_product;
        END IF;
        
        IF NEW.product_image IS NULL THEN
            SET NEW.product_image = variable_product_image;
        END IF;
    END IF;
END //

