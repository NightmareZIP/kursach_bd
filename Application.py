from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Text_window(ttk.Frame):
    def __init__(self, master, *args, is_input=False, func=None, **kwargs):
        super().__init__(master, *args, **kwargs)
        if True or is_input:
            message = StringVar()
            inp = Entry(self, textvariable=message)
            inp.pack()
        l_res = Text(self)
        l_res.insert(END, 'AAAAAAAAAAA')
        l_res.pack()

    # def run_mod(self):
    #     self.mod.pack_forget()
    #     self.mod.destroy()#уничтожаем старый фрейм
    #     self.mod = Frame(self, width = 300)
    #     conf = modules[t.get()][m.get()] #Первый элемент - текст, который будет выведен, второй - модуль, который будет запущен
    #     func = conf[1]
    #     l_name = Label(self.mod, text = m.get())
    #     l_describe = Label(self.mod, text = conf[0])
    #     ent = Text(self.mod, height = 10)
    #     l_res = Text(self.mod)
    #     b = Button(self.mod, text = "Get result", command = lambda : self.run_func(func, ent.get(1.0, END), l_res))
    #     #r = Label(self.mod, text = "reuslt")
    #     self.mod.pack(fill = BOTH, side = LEFT, expand =1)

    #     l_name.pack()
    #     l_describe.pack()
    #     ent.pack()
    #     b.pack()
    #     l_res.pack(anchor = W)

    # def run_func(self, func, ent, l_res):
    #     ent = re.sub('[\s\s+]|,', ' ', ent)
    #     #ent = re.sub('[/]', ' ', ent)
    #     ent = ent.split()
    #     print(ent)
    #     res = -1
    #     try :res = func(*ent)
    #     except:
    #         l_res.delete(1.0, END)

    #         l_res.insert(END, "ERROR! CHECK YOUR INPUT!")
    #     else:
    #         l_res.delete(1.0, END)

    #         l_res.insert(END, "Ответ: " + res)
    #         print(res)


class Types(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.mod_f = Frame(master)

        #style = ttk.Style(self)
        #style.configure('lefttab.TNotebook', tabposition='wn')
        #notebook = ttk.Notebook(master, style='lefttab.TNotebook')
        #maximum = max([len(i) for i in modules.keys()])
        l_f = Frame(self)

        r = Button(l_f, text="Машинки", command=lambda: messagebox.showinfo(
            "Hello Python", "НАЖАЛЪ"))
        # r = Radiobutton(l_f, text = 'AAA', variable = t, value = i, indicatoron=0, command = self.new_list )
        r.pack(fill=BOTH, side=TOP, expand=1, anchor=W)

        l_f.pack(fill=BOTH, side=LEFT, expand=1, )

    # def new_list(self):
    #     print("called")
    #     self.mod_f.pack_forget()
    #     self.mod_f.destroy()#уничтожаем старый фрейм
    #     self.mod_f = Mods(self)
    #     self.mod_f.pack(fill = Y, side = LEFT, expand = 1, anchor = W)


class Main_application(ttk.Frame):

    def __init__(self, master, *args, **kwargs):

        super().__init__(master, *args, **kwargs)

        self.master = master

        f = Types(self)
        f.pack(fill=BOTH, side=LEFT, anchor=W)
        w = Text_window(self)
        w.pack(fill=BOTH, side=RIGHT, anchor=W)


root = Tk()
root.title("Автосервис")
#root.attributes('-fullscreen', True)
t = StringVar()
m = StringVar()

# root.geometry('400x400')
root.minsize(800, 400)

app = Main_application(root)
app.pack(fill=BOTH, expand=1)
root.mainloop()
