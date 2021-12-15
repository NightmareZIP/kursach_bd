DELIMITER //
CREATE TRIGGER `check_order_service_master` BEFORE INSERT ON `order_services`
FOR EACH ROW BEGIN
   IF  NEW.master_id NOT IN (SELECT master_id 
				FROM types_masters 
				WHERE type_id = (SELECT type_id 
								FROM services 
                                WHERE id = NEW.service_id)) THEN KILL QUERY CONNECTION_ID(); 
	END IF;
END //
DELIMITER ;
SHOW TRIGGERS