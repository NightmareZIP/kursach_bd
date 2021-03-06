#DROP DATABASE autoservice;
CREATE DATABASE IF NOT EXISTS autoservice;
USE autoservice;
CREATE TABLE IF NOT EXISTS clients (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, second_name VARCHAR(255) NOT NULL, last_name VARCHAR(255), phone_number VARCHAR(255) NOT NULL UNIQUE );
CREATE TABLE IF NOT EXISTS cars(id INT AUTO_INCREMENT PRIMARY KEY, owner_id integer, name VARCHAR(255) NOT NULL, car_number VARCHAR(255) NOT NULL UNIQUE,
	CONSTRAINT FK_id_client FOREIGN KEY (owner_id)
			REFERENCES clients(id)
			ON DELETE CASCADE ON UPDATE CASCADE);


CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY,
	car_id INTEGER,
	CONSTRAINT FK_id_cars FOREIGN KEY (car_id)
			REFERENCES cars(id)
			ON DELETE CASCADE ON UPDATE CASCADE,
			creation_date DATE NOT NULL,
			final_date DATE DEFAULT NULL);
CREATE TABLE IF NOT EXISTS masters (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, second_name VARCHAR(255) NOT NULL, last_name VARCHAR(255), phone_number VARCHAR(255) NOT NULL UNIQUE);

#CREATE TABLE IF NOT EXISTS service_types (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL UNIQUE);

#Разделение на типы и виды услуг,виды входят в типы
CREATE TABLE IF NOT EXISTS service_types (

	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL UNIQUE);
			
#Информаация по услуге
CREATE TABLE IF NOT EXISTS services (
	id INT AUTO_INCREMENT PRIMARY KEY, 
    type_id INTEGER NOT NULL,
	CONSTRAINT FK_type_serv FOREIGN KEY (type_id)
			REFERENCES service_types(id)
			ON DELETE CASCADE ON UPDATE CASCADE,
	name VARCHAR(255) NOT NULL UNIQUE, price DECIMAL(13,2) NOT NULL CHECK (price > 0));

CREATE TABLE IF NOT EXISTS types_masters (
	master_id INT NOT NULL, 
    type_id INT NOT NULL,
	CONSTRAINT FK_serv FOREIGN KEY (type_id)
			REFERENCES service_types(id)
			ON DELETE CASCADE ON UPDATE CASCADE);
            
CREATE TABLE IF NOT EXISTS order_services (
	service_id INTEGER,
	CONSTRAINT FK_id_services FOREIGN KEY (service_id)
			REFERENCES services(id)
			ON DELETE CASCADE ON UPDATE CASCADE,
	order_id INTEGER,
		CONSTRAINT FK_id_orders FOREIGN KEY (order_id)
		REFERENCES orders(id)
		ON DELETE CASCADE ON UPDATE CASCADE,
    master_id INTEGER,
	CONSTRAINT FK_id_masters FOREIGN KEY (master_id)
	REFERENCES masters(id)
	ON DELETE SET NULL ON UPDATE SET NULL);




