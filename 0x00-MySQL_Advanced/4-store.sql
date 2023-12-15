-- a SQL script that creates a trigger that decreases the quantity of an
-- item after adding a new order.
CREATE TRIGGER decrease
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.quantity_ordered
    WHERE item_id = NEW.item_id;
END;
