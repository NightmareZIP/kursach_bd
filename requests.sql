#Все услуги и цены
SELECT name, price FROM services GROUP BY name, price;
#Список машин в автосервисе
SELECT * FROM cars;

#Услуги для данной машины
SELECT * FROM services
WHERE id IN	(SELECT service_id FROM order_services
	WHERE order_id IN (SELECT id FROM orders
		WHERE  car_id = (SELECT id FROM cars
								WHERE car_number = '2')));
                                
#Расчет стоимости услуг по всем заказам
SELECT SUM(price) FROM services
WHERE id IN (SELECT service_id FROM order_services 
	WHERE order_id = (SELECT id FROM orders
		WHERE car_id IN (SELECT id FROM cars WHERE owner_id IN (SELECT id FROM clients
								WHERE clients.name = 'Энакин'))));

#Расчет сум по отдельным заказам                                
SELECT 'Тони' as custumer, o_c_s.order_id, o_c_s.car_number, services.name, SUM(services.price) as sum  
FROM services, (SELECT order_services.service_id, order_car.order_id, order_car.name, order_car.car_number 
				FROM order_services, (SELECT orders.id as order_id , selected_cars.name, selected_cars.car_number 
									FROM orders, (SELECT  cars.id, cars.name, cars.car_number  
													FROM cars
													WHERE cars.id IN (SELECT id 
																	FROM cars 
                                                                    WHERE owner_id IN (SELECT id 
																						FROM clients
																						WHERE clients.name = 'Тони'))
												) AS selected_cars
									WHERE orders.car_id = selected_cars.id
                                    ) AS order_car
				WHERE order_car.order_id = order_services.order_id) AS o_c_s
	WHERE services.id = o_c_s.service_id
    GROUP BY o_c_s.order_id;
 

 #Выбор проделанной мастером работы а период
 SELECT orders.id, services.price, orders.creation_date, orders.final_date
 FROM services, orders, (SELECT service_id, order_id 
						 FROM order_services  
						WHERE master_id = (SELECT id 
										   FROM masters
										    WHERE masters.second_name = 'Никитыч')
						) AS cur_s_o
WHERE services.id = cur_s_o.service_id
AND
orders.id = cur_s_o.order_id
AND 
orders.final_date IS NOT NULL
AND 
orders.final_date BETWEEN DATE_SUB(NOW(), INTERVAL 365 DAY) AND NOW() ;
                    
