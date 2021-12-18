CREATE USER 'admin' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON autoservice . * TO 'admin';

CREATE USER staff_manager IDENTIFIED BY 'staff_manager';
GRANT INSERT ON autoservice.masters TO 'staff_manager';
GRANT SELECT ON autoservice.masters TO 'staff_manager';
GRANT UPDATE ON autoservice.masters TO 'staff_manager';

GRANT INSERT ON autoservice.types_masters TO 'staff_manager';
GRANT SELECT ON autoservice.types_masters TO 'staff_manager';
GRANT UPDATE ON autoservice.types_masters TO 'staff_manager';

GRANT SELECT ON autoservice.cars TO 'staff_manager';
GRANT SELECT ON autoservice.orders TO 'staff_manager';
GRANT SELECT ON autoservice.order_services TO 'staff_manager';
GRANT SELECT ON autoservice.services TO 'staff_manager';


CREATE USER client_manager IDENTIFIED BY 'client_manager';
GRANT INSERT ON autoservice.clients TO 'client_manager';
GRANT SELECT ON autoservice.clients TO 'client_manager';
GRANT UPDATE ON autoservice.clients TO 'client_manager';

GRANT INSERT ON autoservice.cars TO 'client_manager';
GRANT SELECT ON autoservice.cars TO 'client_manager';
GRANT UPDATE ON autoservice.cars TO 'client_manager';

GRANT INSERT ON autoservice.orders TO 'client_manager';
GRANT SELECT ON autoservice.orders TO 'client_manager';
GRANT UPDATE ON autoservice.orders TO 'client_manager';

GRANT INSERT ON autoservice.order_services TO 'client_manager';
GRANT SELECT ON autoservice.order_services TO 'client_manager';
GRANT UPDATE ON autoservice.order_services TO 'client_manager';

GRANT SELECT ON autoservice.services TO 'client_manager';
GRANT SELECT ON autoservice.masters TO 'client_manager';
GRANT SELECT ON autoservice.types_masters TO 'client_manager';

