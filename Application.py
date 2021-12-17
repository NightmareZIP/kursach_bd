from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import sql_test


class Text_window(ttk.Frame):
    def __init__(self, master, DB, *args, left_menu, options, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.DB = DB
        self.options = options
        self.master = master
        self.command = options['command']
        self.text_w = False
        if options['is_input']:

            self.create_input_area()
        else:
            self.execute(self.options['command'])

    def execute(self, formated_command):
        # print(formated_command)
        if (self.text_w):
            self.l_res.pack_forget()
            self.l_res.destroy()

        self.text_w = True
        columns, res = self.DB.execute(formated_command)
        columns, res = self.DB.execute(formated_command)
        if columns == -1:
            messagebox.showinfo("Ошибка", "Проверьте данные")
            self.text_w = False
            return
        self.l_res = ttk.Treeview(self, show="headings")
        self.l_res['columns'] = columns

        for i in columns:
            self.l_res.column(i, anchor=CENTER)
            self.l_res.heading(i, text=i)

        ysb = Scrollbar(self, orient=VERTICAL, command=self.l_res.yview)
        self.l_res.configure(yscroll=ysb.set)
        for i in res:
            self.l_res.insert("", END, values=i)

        self.l_res.pack(fill=BOTH, expand=1)

    def create_input_area(self):
        f = Frame(self)
        if (self.options['is_input']['select']):
            q_d = self.options['is_input']['select']
            ent = q_d['entity']
            fields = q_d['fields']
            self.checkboxes = q_d['checkboxes']
            lab = Label(f, text=q_d['label'])
            lab.pack(side=TOP)
            if self.checkboxes:
                c_f = Frame(f)
                self.v = StringVar(c_f, "1")
                for (text, val) in self.checkboxes:
                    Radiobutton(c_f, text=text, variable=self.v,
                                value=val).pack(side=LEFT)
                c_f.pack(side=TOP)
            querry_f = ', '.join(fields)
            querry = "SELECT {} FROM {}".format(querry_f, ent)
            h, res = self.DB.execute(querry)

            for elem in res:
                elem = list(map(str, elem))
                data = [elem[0]]
                action_with_arg = partial(self.run_formated_command,
                                          self.command, data)

                r = Button(f,
                           text=' '.join(list(elem)),
                           command=action_with_arg)
                r.pack(side=TOP, fill=BOTH, expand=1)

        # self.inp = Entry(f)
        # self.inputs = [self.inp]
        # b = Button(f,
        #            text='Ввод',
        #            command=lambda: self.run_formated_command(
        #                self.command, self.inputs))
        # self.inp.pack(side=LEFT)
        # b.pack(side=RIGHT)
        f.pack(side=LEFT)

    def run_formated_command(self, command, inputs):
        self.inputs = inputs[:]
        if self.checkboxes: self.inputs.append(self.v.get())
        f_command = command.format(*self.inputs)

        self.execute(f_command)


class Types(ttk.Frame):
    def __init__(self, master, *args, DB, queries, **kwargs):

        super().__init__(master, *args, **kwargs)
        self.DB = DB
        self.is_w = False
        self.master = master
        self.mod_f = Frame(master)

        l_f = Frame(self, background='red')

        buttons = []
        for button in queries.keys():
            opt = queries[button]
            action_with_arg = partial(self.create_request_section, opt)
            r = Button(l_f, text=button, command=action_with_arg)
            r.pack(side=TOP, fill=BOTH, expand=1)

        l_f.pack(side=LEFT, fill=BOTH)

    def create_request_section(self, options):
        if self.is_w:
            self.w.pack_forget()
            self.w.destroy()
        self.w = Text_window(self.master,
                             DB=self.DB,
                             left_menu=self,
                             options=options)
        self.w.pack(fill=BOTH, expand=1, side=RIGHT)
        self.is_w = True


class Main_application(ttk.Frame):
    def __init__(self, master, *args, **kwargs):

        super().__init__(master, *args, **kwargs)

        self.master = master
        self.chose_f = Frame(self)

        a_action_with_arg = partial(self.click_callback, 'admin')
        a_button = Button(self.chose_f,
                          text='Зайти под админом',
                          command=a_action_with_arg)
        a_button.pack(side=TOP, fill=BOTH, expand=1)

        s_m_action_with_arg = partial(self.click_callback, 's_m')
        s_m_button = Button(self.chose_f,
                            text='Зайти под менеджером персонала',
                            command=s_m_action_with_arg)
        s_m_button.pack(side=TOP, fill=BOTH, expand=1)

        c_m_action_with_arg = partial(self.click_callback, 'admin')
        c_m_button = Button(self.chose_f,
                            text='Зайти под менеджером клиентов',
                            command=c_m_action_with_arg)
        c_m_button.pack(side=TOP, fill=BOTH, expand=1)
        self.chose_f.pack(side=TOP, fill=BOTH, expand=1, anchor=CENTER)

    def eneter_db(self, login, password):
        data = {
            'host': "127.0.0.1",
            'user': login,
            'password': password,
            'database': "autoservice"
        }
        return sql_test.DB(data)

    def click_callback(self, mode):
        self.chose_f.pack_forget()
        self.chose_f.destroy()
        if mode == 'admin':
            login = 'root'
            password = 'qwerty123'
            queries = {
                "Список услуг": {
                    'command':
                    "SELECT name, price FROM services GROUP BY name, price;",
                    'is_input': False
                },
                "Список машин": {
                    'command': "SELECT * FROM cars;",
                    'is_input': False
                },
                "Информация о машине": {
                    'command': """SELECT * FROM services
                                WHERE id IN	(SELECT service_id FROM order_services
                                    WHERE order_id IN (SELECT id FROM orders
                                        WHERE  car_id = (SELECT id FROM cars
                                                                WHERE id = '{}')));""",
                    'is_input': {
                        'select': {
                            'label': 'Выберите машину',
                            'entity': 'cars',
                            'fields': ['id', 'name', 'car_number'],
                            'checkboxes': (())
                        }
                    }
                },
                "Информация о работе мастера за период": {
                    'command':
                    """ SELECT orders.id, services.name, services.price, orders.creation_date, orders.final_date
                    FROM services, orders, (SELECT service_id, order_id 
						 FROM order_services  
						WHERE master_id = (SELECT id 
										   FROM masters
										    WHERE masters.id = {})
						) AS cur_s_o
                    WHERE services.id = cur_s_o.service_id
                    AND
                    orders.id = cur_s_o.order_id
                    AND 
                    orders.final_date IS NOT NULL
                    AND 
                    orders.final_date BETWEEN DATE_SUB(NOW(), INTERVAL {} DAY) AND NOW() ;""",
                    'is_input': {
                        'select': {
                            'label':
                            'Выберите период и мастера',
                            'entity':
                            'masters',
                            'fields':
                            ['id', 'name', 'second_name', 'last_name'],
                            'checkboxes': (('день', 1), ('месяц', 30),
                                           ('квартал', 91), ('год', 365))
                        }
                    }
                },
                "Рассчет стоимости услуг": {
                    'command':
                    """SELECT  o_c_s.order_id, o_c_s.car_number, SUM(services.price) as sum  
                                            FROM services, (SELECT order_services.service_id, order_car.order_id, order_car.name, order_car.car_number 
                                                            FROM order_services, (SELECT orders.id as order_id , selected_cars.name, selected_cars.car_number 
                                                                                FROM orders, (SELECT  cars.id, cars.name, cars.car_number  
                                                                                                FROM cars
                                                                                                WHERE cars.id IN (SELECT id 
                                                                                                                FROM cars 
                                                                                                                WHERE owner_id IN (SELECT id 
                                                                                                                                    FROM clients
                                                                                                                                    WHERE clients.id = {}))
                                                                                            ) AS selected_cars
                                                                                WHERE orders.car_id = selected_cars.id
                                                                                ) AS order_car
                                                            WHERE order_car.order_id = order_services.order_id) AS o_c_s
                                                WHERE services.id = o_c_s.service_id
                                                GROUP BY o_c_s.order_id;""",
                    'is_input': {
                        'select': {
                            'label': 'Выберите клиента',
                            'entity': 'clients',
                            'fields':
                            ['id', 'name', 'second_name', 'last_name'],
                            'checkboxes': (())
                        }
                    }
                },
            }
        elif mode == 's_m':
            login = 'staff_manager'
            password = 'staff_manager'
            queries = {
                "Список услуг": {
                    'command':
                    "SELECT name, price FROM services GROUP BY name, price;",
                    'is_input': False
                },
                "Информация о работе мастера за период": {
                    'command':
                    """ SELECT orders.id, services.name, services.price, orders.creation_date, orders.final_date
                    FROM services, orders, (SELECT service_id, order_id 
						 FROM order_services  
						WHERE master_id = (SELECT id 
										   FROM masters
										    WHERE masters.id = {})
						) AS cur_s_o
                    WHERE services.id = cur_s_o.service_id
                    AND
                    orders.id = cur_s_o.order_id
                    AND 
                    orders.final_date IS NOT NULL
                    AND 
                    orders.final_date BETWEEN DATE_SUB(NOW(), INTERVAL {} DAY) AND NOW() ;""",
                    'is_input': {
                        'select': {
                            'label':
                            'Выберите период и мастера',
                            'entity':
                            'masters',
                            'fields':
                            ['id', 'name', 'second_name', 'last_name'],
                            'checkboxes': (('день', 1), ('месяц', 30),
                                           ('квартал', 91), ('год', 365))
                        }
                    }
                },
            }
        elif mode == 'c_m':
            login = 'client_manager'
            password = 'client_manager'
            queries = {
                "Список услуг": {
                    'command':
                    "SELECT name, price FROM services GROUP BY name, price;",
                    'is_input': False
                },
                "Список машин": {
                    'command': "SELECT * FROM cars;",
                    'is_input': False
                },
                "Информация о машине": {
                    'command': """SELECT * FROM services
                                WHERE id IN	(SELECT service_id FROM order_services
                                    WHERE order_id IN (SELECT id FROM orders
                                        WHERE  car_id = (SELECT id FROM cars
                                                                WHERE id = '{}')));""",
                    'is_input': {
                        'select': {
                            'label': 'Выберите машину',
                            'entity': 'cars',
                            'fields': ['id', 'name', 'car_number'],
                            'checkboxes': (())
                        }
                    }
                },
                "Рассчет стоимости услуг": {
                    'command':
                    """SELECT  o_c_s.order_id, o_c_s.car_number, SUM(services.price) as sum  
                                            FROM services, (SELECT order_services.service_id, order_car.order_id, order_car.name, order_car.car_number 
                                                            FROM order_services, (SELECT orders.id as order_id , selected_cars.name, selected_cars.car_number 
                                                                                FROM orders, (SELECT  cars.id, cars.name, cars.car_number  
                                                                                                FROM cars
                                                                                                WHERE cars.id IN (SELECT id 
                                                                                                                FROM cars 
                                                                                                                WHERE owner_id IN (SELECT id 
                                                                                                                                    FROM clients
                                                                                                                                    WHERE clients.id = {}))
                                                                                            ) AS selected_cars
                                                                                WHERE orders.car_id = selected_cars.id
                                                                                ) AS order_car
                                                            WHERE order_car.order_id = order_services.order_id) AS o_c_s
                                                WHERE services.id = o_c_s.service_id
                                                GROUP BY o_c_s.order_id;""",
                    'is_input': {
                        'select': {
                            'label': 'Выберите клиента',
                            'entity': 'clients',
                            'fields':
                            ['id', 'name', 'second_name', 'last_name'],
                            'checkboxes': (())
                        }
                    }
                },
            }
        db = self.eneter_db(login, password)
        if not db.is_error:
            f = Types(self, DB=db, queries=queries)
            f.pack(fill=BOTH, side=LEFT)



root = Tk()
root.title("Автосервис")

root.minsize(800, 400)
app = Main_application(root)
app.pack(fill=BOTH, expand=1)
root.mainloop()
