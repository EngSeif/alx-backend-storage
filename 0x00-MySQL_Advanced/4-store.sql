-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

DELIMITER $$

CREATE TRIGGER quantity_after_adding_new_order
AFTER INSERT ON orders 
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
end $$

DELIMITER ;
