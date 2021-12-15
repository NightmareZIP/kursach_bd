USE autoservice;
#TEST
INSERT INTO cars (owner_id, name, car_number)
    VALUES
    (3,"Mark-4", "4");
INSERT INTO orders (car_id, creation_date, final_date)
VALUES
(5, '2021-09-01', '2021-11-01');  
INSERT INTO order_services (order_id, service_id, master_id)
	VALUES
		(5, 1, 1);
SELECT * FROM order_services;
INSERT INTO order_services (order_id, service_id, master_id)
	VALUES
		(5, 1, 3);
#END_TEST
INSERT INTO clients (name, second_name, last_name, phone_number)
    VALUES("Люк", "Скайвокер", "Энакинович", "88005553535"), 
    ("Энакин", "Скайвокер", "Силович", "1134124"),
    ("Тони", "Старк", "Говардович", '555-212-123'),
    ("Вито", "Карлеоне", "Дон", '7284194');
INSERT INTO cars (owner_id, name, car_number)
    VALUES
    (1,"X-wing", "12"), 
    (2,"TIE-fighter", 'K-232'),
    (3,"Mark-2", "2"),
    (4,"Mercedes", "AA0000A");
    
INSERT INTO orders (car_id, creation_date, final_date)
    VALUES
    (1, '2021-09-01', '2021-11-01'), 
    (2, '2021-11-20', '2021-11-30'),
    (3, '2021-12-05', '2021-12-10'),
    (4, '2021-12-14', NULL);
INSERT INTO masters (name, second_name, last_name, phone_number)
	VALUES("Иван", "Иванов", "Иванович", "8478129471"), 
		("Петр", "Цой", "Викторович", "9238239"),
		("Добрыня", "Никитыч", "Александрович", '2784129'),
		("Пушкин", "Блок", "Владимирович", '1231231');
        
INSERT INTO service_types (name)
	VALUES
		('Чистка'),
        ("Ремонт"),
        ("Тюннинг"),
        ("Тех обслуживание");
INSERT INTO types_masters (type_id, master_id)
VALUES
	(1, 1),
	(2, 2),
	(3, 3),
	(4, 4),
    (1, 2),
	(2, 3),
	(3, 4),
	(4, 1); 
INSERT INTO services (name, price, type_id)
	VALUES
		('Замена топлива', 1000, 3),
        ("Чистка солона", 2000, 1),
        ("Починка двигателя", 3000, 2),
        ("Тюннинг дисков", 4000.60, 3),
        ("Мойка", 500, 1),
        ("Починка электроники", 10000, 2);
INSERT INTO order_services (order_id, service_id, master_id)
	VALUES
		(1, 1, 3),
        (1, 4, 3),
        (2, 3, 2),
        (3, 2, 1),
        (3, 5, 2),
        (4, 6, 3);