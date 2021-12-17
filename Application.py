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
            self.text_w = False

        columns, res = self.DB.execute(formated_command)
        if columns == -1:
            messagebox.showinfo("Ошибка", "Проверьте данные")
            self.text_w = False
            return
        if len(columns) == 0:
            messagebox.showinfo("Успешно", "Ввод успешен")
            self.text_w = False
            return
        if 'SELECT' not in formated_command: return
        self.text_w = True

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
        self.f = f
        if ('select' in self.options['is_input']):
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

        elif 'insert' in self.options['is_input']:
            q_d = self.options['is_input']['insert']
            ent = q_d['entity']
            fields = q_d['fields']
            self.checkboxes = q_d['checkboxes']
            lab = Label(f, text=q_d['label'])
            lab.pack(side=TOP)
            if self.checkboxes:
                c_f = Frame(f)
                l = Label(c_f, text=self.checkboxes[1])
                l.pack(side=TOP)
                querry_f = ', '.join(self.checkboxes[2])
                querry = "SELECT {} FROM {}".format(querry_f,
                                                    self.checkboxes[0])
                h, res = self.DB.execute(querry)
                self.v = StringVar(c_f, "1")
                for row in res:
                    row = list(map(str, row))
                    Radiobutton(c_f,
                                text=' '.join(list(row)),
                                variable=self.v,
                                value=row[0]).pack(side=TOP)
                c_f.pack(side=TOP)

            self.entries = []
            for (field, field_name) in fields:
                ent_f = Frame(f)
                l = Label(ent_f, text=field_name)
                l.pack(side=TOP)

                self.i = StringVar(ent_f, "")
                self.entries.append(self.i)
                ent = Entry(ent_f, textvariable=self.i)
                ent.pack(side=TOP)
                ent_f.pack(side=TOP)
            if self.checkboxes: self.entries.append(self.v)
            action_with_arg = partial(self.run_formated_command, self.command,
                                      self.entries, True)

            Button(f, text='Ввод', command=action_with_arg).pack(side=TOP)
        elif 'double_insert' in self.options['is_input']:
            q_d = self.options['is_input']['double_insert']
            ent = q_d['entity']
            self.checkboxes = q_d['checkboxes']
            self.entries = []
            cs_f = Frame(f)
            for box in self.checkboxes:

                c_f = Frame(cs_f)
                querry = """SELECT {} 
                            FROM {}
                            ;""".format(', '.join(box[1:]), box[0])
                h, res = self.DB.execute(querry)
                self.c = StringVar(c_f, "0")
                self.entries.append(self.c)
                for row in res:
                    row = list(map(str, row))
                    Radiobutton(c_f,
                                text=' '.join(list(row)),
                                variable=self.c,
                                value=row[0]).pack(side=TOP)
                c_f.pack(side=LEFT)
            cs_f.pack(side=TOP)
            action_with_arg = partial(self.run_formated_command, self.command,
                                      self.entries, True)

            Button(f, text='Ввод', command=action_with_arg).pack(side=TOP)

        elif 'special_insert' in self.options['is_input']:
            self.show = False
            c_f = Frame(f)
            l = Label(c_f, text='Заказы')
            l.pack(side=TOP)
            querry = """SELECT orders.id, cars.name, cars.car_number 
                        FROM orders, cars
                        WHERE orders.car_id = cars.id;"""
            h, res = self.DB.execute(querry)
            self.o = StringVar(c_f, "1")
            for row in res:
                row = list(map(str, row))
                Radiobutton(c_f,
                            text=' '.join(list(row)),
                            variable=self.o,
                            value=row[0]).pack(side=TOP)
            c_f.pack(side=LEFT)
            #Srvices
            c_f = Frame(f)
            l = Label(c_f, text='Услуги')
            l.pack(side=TOP)
            querry = """SELECT id, name, price 
                        FROM services
                    """
            h, res = self.DB.execute(querry)
            self.s = StringVar(c_f, "-1")
            self.m = ''
            for row in res:
                row = list(map(str, row))
                Radiobutton(c_f,
                            text=' '.join(list(row)),
                            variable=self.s,
                            value=row[0],
                            command=lambda: self.get_masters()).pack(side=TOP)
            c_f.pack(side=LEFT)

        f.pack(side=LEFT)

    def get_masters(self):
        #Masters
        if self.show:
            self.c_f.pack_forget()
            self.c_f.destroy()

        self.show = True

        self.c_f = Frame(self.f)
        l = Label(self.c_f, text='Мастера')
        l.pack(side=TOP)
        querry = """SELECT * FROM masters
                    WHERE id IN (SELECT master_id 
                        FROM types_masters 
                        WHERE type_id = (SELECT id 
								FROM services WHERE id = {}));
                    """.format(self.s.get())
        h, res = self.DB.execute(querry)
        self.m = StringVar(self.c_f, "0")
        for row in res:
            row = list(map(str, row))
            Radiobutton(self.c_f,
                        text=' '.join(list(row)),
                        variable=self.m,
                        value=row[0]).pack(side=TOP)
        self.entries = [self.o, self.s, self.m]
        action_with_arg = partial(self.run_formated_command, self.command,
                                  self.entries)

        self.b = Button(self.c_f, text='Ввод', command=action_with_arg).pack(
            fill=BOTH,
            expand=1,
            side=TOP,
        )
        self.c_f.pack(side=LEFT)

    def run_formated_command(self, command, inputs, ent=False):
        if 'special_insert' in self.options[
                'is_input'] or 'double_insert' in self.options['is_input']:
            self.inputs = inputs[:]

            f_command = command.format(*list(
                map(lambda x: "'" + x.get() + "'"
                    if x.get() != '' else 'NULL', self.inputs)))
            print(f_command)
        elif not ent:
            self.inputs = inputs[:]
            if self.checkboxes: self.inputs.append("'" + self.v.get() + "'")
            f_command = command.format(*self.inputs)
        else:
            self.inputs = inputs[:]
            f_command = command.format(*list(
                map(lambda x: "'" + x.get() + "'"
                    if x.get() != '' else 'NULL', self.inputs)))
            print(f_command)

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

        c_m_action_with_arg = partial(self.click_callback, 'c_m')
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
            login = 'admin'
            password = 'admin'
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
                                                                WHERE id = {})));""",
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
                'Добавить мастера': {
                    'command':
                    """INSERT INTO masters (name, second_name, last_name, phone_number)
                        VALUES
                        ({}, {}, {}, {});""",
                    'is_input': {
                        'insert': {
                            'label':
                            'Введите данные мастера',
                            'entity':
                            'clients',
                            'fields': [['name', 'имя'],
                                       ['second_name', 'фамилия'],
                                       ['last_name', 'отчество'],
                                       ['phone_number', 'номер телефона']],
                            'checkboxes': (()),
                        }
                    }
                },
                'Добавить заказ': {
                    'command':
                    """INSERT INTO orders (creation_date, final_date, car_id)
                        VALUES
                        ({}, {}, {});""",  #Даты без ковычек, подставить по ходу скрипта
                    'is_input': {
                        'insert': {
                            'label':
                            'Введите данные заказа',
                            'entity':
                            'orders',
                            'fields': [
                                ['creation_date', 'Дата создания'],
                                ['final_date', 'Дата завершения'],
                            ],
                            'checkboxes':
                            ('cars', 'машина', ['id', 'name', 'car_number'])
                        }
                    }
                },
                'Добавить машину': {
                    'command': """INSERT INTO cars (name, car_number, owner_id)
                        VALUES
                        ({}, {}, {});""",
                    'is_input': {
                        'insert': {
                            'label':
                            'Введите данные машины',
                            'entity':
                            'cars',
                            'fields': [
                                ['name', 'название машины'],
                                ['car_number', 'номер машины'],
                            ],
                            'checkboxes':
                            ('clients', 'клиент',
                             ['id', 'name', 'second_name', 'last_name'])
                        }
                    }
                },
                'Добавить клиента': {
                    'command':
                    """INSERT INTO clients (name, second_name, last_name, phone_number)
                        VALUES
                        ({}, {}, {}, {});""",
                    'is_input': {
                        'insert': {
                            'label':
                            'Введите данные клиента',
                            'entity':
                            'clients',
                            'fields': [['name', 'имя'],
                                       ['second_name', 'фамилия'],
                                       ['last_name', 'отчество'],
                                       ['phone_number', 'номер телефона']],
                            'checkboxes': (()),
                        }
                    }
                },
                'Добавить  тип услуги': {
                    'command': """INSERT INTO service_types (name)
                        VALUES
                        ({});""",
                    'is_input': {
                        'insert': {
                            'label': 'Введите название типа услуги',
                            'entity': 'service_types',
                            'fields': [
                                ['name', 'название'],
                            ],
                            'checkboxes': (()),
                        }
                    }
                },
                'Добавить мастеру тип услуги': {
                    'command': """
                        INSERT INTO types_masters (master_id, type_id)
                        VALUES
                        ({}, {});""",
                    'is_input': {
                        'double_insert': {
                            'label':
                            'Выберите название типа услуги и мастера',
                            'entity': ['types_masters'],
                            'checkboxes': (
                                ('services', 'id, name'),
                                ('masters', 'id', 'name', 'second_name',
                                 'last_name'),
                            ),
                        }
                    }
                },
                'Добавить услугу': {
                    'command': """INSERT INTO services (name, price, type_id)
                        VALUES
                        ({}, {}, {});""",
                    'is_input': {
                        'insert': {
                            'label':
                            'Введите название услуги',
                            'entity':
                            'services',
                            'fields': [['name', 'название'], ['price',
                                                              'цена']],
                            'checkboxes':
                            ('service_types', 'Типы услуг', ['id', 'name']),
                        }
                    }
                },
                'Добавить услугу к заказу': {
                    'command':
                    """INSERT INTO order_services (order_id, service_id, master_id)
                                    VALUES
                                        ({}, {}, {});""",
                    'is_input': {
                        'special_insert': {
                            'label':
                            'Введите название услуги',
                            'entity':
                            'services',
                            'radiobuttons': (
                                ('orders', 'Заказы', ['id']),
                                ('services', 'Услуги', ['id', 'name',
                                                        'price']),
                                ('masters', 'Мастер',
                                 ['id', 'name', 'second_name', 'last_name']),
                            )
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
                'Добавить мастера': {
                    'command':
                    """INSERT INTO masters (name, second_name, last_name, phone_number)
                        VALUES
                        ({}, {}, {}, {});""",
                    'is_input': {
                        'insert': {
                            'label':
                            'Введите данные мастера',
                            'entity':
                            'clients',
                            'fields': [['name', 'имя'],
                                       ['second_name', 'фамилия'],
                                       ['last_name', 'отчество'],
                                       ['phone_number', 'номер телефона']],
                            'checkboxes': (()),
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
                'Добавить мастеру тип услуги': {
                    'command': """
                        INSERT INTO types_masters (master_id, type_id)
                        VALUES
                        ({}, {});""",
                    'is_input': {
                        'double_insert': {
                            'label':
                            'Выберите название типа услуги и мастера',
                            'entity': ['types_masters'],
                            'checkboxes': (
                                ('services', 'id, name'),
                                ('masters', 'id', 'name', 'second_name',
                                 'last_name'),
                            ),
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
                                                                WHERE id = {})));""",
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
                'Добавить заказ': {
                    'command':
                    """INSERT INTO orders (creation_date, final_date, car_id)
                        VALUES
                        ({}, {}, {});""",  #Даты без ковычек, подставить по ходу скрипта
                    'is_input': {
                        'insert': {
                            'label':
                            'Введите данные заказа',
                            'entity':
                            'orders',
                            'fields': [
                                ['creation_date', 'Дата создания'],
                                ['final_date', 'Дата завершения'],
                            ],
                            'checkboxes':
                            ('cars', 'машина', ['id', 'name', 'car_number'])
                        }
                    }
                },
                'Добавить машину': {
                    'command': """INSERT INTO cars (name, car_number, owner_id)
                        VALUES
                        ({}, {}, {});""",
                    'is_input': {
                        'insert': {
                            'label':
                            'Введите данные машины',
                            'entity':
                            'cars',
                            'fields': [
                                ['name', 'название машины'],
                                ['car_number', 'номер машины'],
                            ],
                            'checkboxes':
                            ('clients', 'клиент',
                             ['id', 'name', 'second_name', 'last_name'])
                        }
                    }
                },
                'Добавить клиента': {
                    'command':
                    """INSERT INTO clients (name, second_name, last_name, phone_number)
                        VALUES
                        ({}, {}, {}, {});""",
                    'is_input': {
                        'insert': {
                            'label':
                            'Введите данные клиента',
                            'entity':
                            'clients',
                            'fields': [['name', 'имя'],
                                       ['second_name', 'фамилия'],
                                       ['last_name', 'отчество'],
                                       ['phone_number', 'номер телефона']],
                            'checkboxes': (()),
                        }
                    }
                },
                'Добавить услугу к заказу': {
                    'command':
                    """INSERT INTO order_services (order_id, service_id, master_id)
                                    VALUES
                                        ({}, {}, {});""",
                    'is_input': {
                        'special_insert': {
                            'label':
                            'Введите название услуги',
                            'entity':
                            'services',
                            'radiobuttons': (
                                ('orders', 'Заказы', ['id']),
                                ('services', 'Услуги', ['id', 'name',
                                                        'price']),
                                ('masters', 'Мастер',
                                 ['id', 'name', 'second_name', 'last_name']),
                            )
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
