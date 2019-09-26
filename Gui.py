from tkinter import ttk
from tkinter import Tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import Label, Listbox, Button, Toplevel
from netmiko import ConnectHandler
import time
import os


class Main_window():
    def __init__ (self):
        self.window = Tk()
        self.window.title("Backup Cisco device")
        self.window.geometry('900x600')

        self.txt = Listbox(self.window,width=100,height=10)
        self.txt.grid(column=0,row=2)
        
        self.device_list_backup1 = []
        n=0
        exec(open("Device_list.txt").read())
        for items in self.device_list_backup1:
                self.txt.insert(n,items)
                n+=1
        self.btn = Button(self.window, text="Добавить устройство",command=self.add_devices)
        self.btn.grid(column=0, row=4)

        self.lbl = Label(self.window, text="Известные устройства", font=("Arial Bold", 12))
        self.lbl.grid(column=0, row=0)

        self.dlt_btn = Button(self.window, text="Удалить устройство",command=self.remove_device_from_list)
        self.dlt_btn.grid(column=0, row=5)

        self.backup_all_btn = Button(self.window, text="Сохранить резервную копию всех устройств",command=self.back_all_devices)
        self.backup_all_btn.grid(column=0, row=6)

        self.backup_one_btn = Button(self.window, text="Сохранить резервную выбранного устройства",command=self.remove_device_from_list)
        self.backup_one_btn.grid(column=0, row=7)

        self.window.mainloop()
    def add_devices(self):
        self.add_devices_window = Toplevel(self.window)
        self.add_devices_window.title("Добавление устройств")
        self.add_devices_window.geometry ("300x600")

        IP_text = Label(self.add_devices_window,text="IP адрес", font=("Arial Bold", 12))
        IP_text.grid(column=0, row=0)

        self.IP_entry = ttk.Entry(self.add_devices_window, width=7)
        self.IP_entry.grid(column=1, row=0)
        
        username_text = Label(self.add_devices_window, text="Имя пользователя", font=("Arial Bold", 12))
        username_text.grid(column=0, row=1)

        self.username_entry = ttk.Entry(self.add_devices_window, width=7)
        self.username_entry.grid(column=1, row=1)

        password_text = Label(self.add_devices_window, text="Пароль", font=("Arial Bold", 12))
        password_text.grid(column=0, row=2)

        self.password_entry = ttk.Entry(self.add_devices_window, width=7)
        self.password_entry.grid(column=1, row=2)

    
        enable_password_text = Label(self.add_devices_window, text="Enable Пароль", font=("Arial Bold", 12))
        enable_password_text.grid(column=0, row=3)

        self.enable_password_entry = ttk.Entry(self.add_devices_window, width=7)
        self.enable_password_entry.grid(column=1, row=3)

        add_devices_button = Button(self.add_devices_window, text="Добавить устройство",
        command=self.add_devices_to_list)
        add_devices_button.grid(column=0, row=4)


    def add_devices_to_list(self):
        empty_dict = {}
        empty_dict["IP"] = self.IP_entry.get()
        empty_dict["Имя пользователя"] = self.username_entry.get()
        empty_dict["Пароль"] = self.password_entry.get()
        empty_dict["Enable Пароль"] = self.enable_password_entry.get()
        devices_list = [empty_dict]
        device_string = open ('Device_list.txt').read()
        device_string1 =device_string
        
        if "{" in device_string:
            device_string1 = device_string1[:-1]+","+str(devices_list[0])+"]"
        else:
            device_string1 = device_string1[:-1]+str(devices_list[0])+"]"
        with open ('Device_list.txt',"w"):
            pass
       
        with open ("Device_list.txt","w") as f:
                #if "self.device_list_backup1 = [" not in device_string1:
                   # f.write ("self.device_list_backup1 = ["+device_string1)
                
                f.write (device_string1)
        self.file = open('Device_list.txt')
        self.txt.delete(0,'end')
        #Update txt widget
        n=0
        exec(open("Device_list.txt").read())
        for items in self.device_list_backup1:
                self.txt.insert(n,items)
                n+=1
        messagebox.showinfo('Добавление устройства', 'Успешно!')
    def remove_device_from_list(self):
        item_for_dlt = self.txt.curselection()
        del_line = item_for_dlt[0]
        exec(open("Device_list.txt").read())
        del self.device_list_backup1[del_line]
        #add update for widget
        n = len (self.device_list_backup1)
        i = 0
        with open('Device_list.txt', 'w') as f:
            for item in self.device_list_backup1:
                if i ==0:
                    f.write("self.device_list_backup1 = [")
                f.write(str(item))
                i+=1
                if i == n:
                    f.write("]")
                else:
                    f.write(",")
        self.txt.delete(0,'end')
        for items in self.device_list_backup1:
                self.txt.insert(n,items)
                n+=1
        """
        with open("Device_list.txt","r") as self.textobj:
            line_list = list(self.textobj)    #puts all lines in a list
        del line_list[del_line]    #delete regarding element
        #rewrite the textfile from list contents/elements:
        with open("Device_list.txt","w") as textobj:
            for n in line_list:
                textobj.write(n)
        self.file = open('Device_list.txt')
        self.txt.delete(0,'end')
        n=0
        with open ('Device_list.txt') as f:
            for lines in f:
                self.txt.insert(n,lines)
                n+=1
            """
    def back_all_devices(self):
        dirname = time.strftime("%d,%B,%Y")
        try:
            os.mkdir(dirname)
        except FileExistsError:
            print ("directory with this name already exist")
        for item in self.device_list_backup1:
            ssh_connection = ConnectHandler(
            device_type = "cisco_ios",
            ip = item["IP"],
            username = item["Имя пользователя"],
            password = item["Пароль"],
            secret  = item["Enable Пароль"],
            )
            ssh_connection.enable()
            result = ssh_connection.find_prompt() + "\n"
            result += ssh_connection.send_command("terminal length 0", delay_factor=2)
            running_config = ssh_connection.send_command("show run", delay_factor = 2)
            ssh_connection.send_command("terminal length 24", delay_factor=2)
            ssh_connection.disconnect()
            name_of_the_file = item["IP"]+"_"+time.strftime("%d,%B,%Y")
            path = dirname
            path_create = os.path.join(path,name_of_the_file +".txt")
            with open (path_create,"a+") as text_file:
                text_file.write (running_config)
                text_file.close()
    def backup_one_device(self):
        dirname = time.strftime("%d,%B,%Y")
        try:
            os.mkdir(dirname)
        except FileExistsError:
            print ("directory with this name already exist")
        backup_tuple = self.txt.curselection()
        backup_item = backup_tuple[0]
        ssh_connection = ConnectHandler(
            device_type = "cisco_ios",
            ip = self.device_list_backup1[backup_item-1]["IP"],
            username = self.device_list_backup1[backup_item-1]["Имя пользователя"],
            password = self.device_list_backup1[backup_item-1]["Пароль"],
            secret  = self.device_list_backup1[backup_item-1]["Enable Пароль"],
        )
        ssh_connection.enable()
        result = ssh_connection.find_prompt() + "\n"
        result += ssh_connection.send_command("terminal length 0", delay_factor=2)
        running_config = ssh_connection.send_command("show run", delay_factor = 2)
        ssh_connection.send_command("terminal length 24", delay_factor=2)
        ssh_connection.disconnect()
        name_of_the_file = self.device_list_backup1[backup_item-1]["IP"]+"_"+time.strftime("%d,%B,%Y")
        path = dirname
        path_create = os.path.join(path,name_of_the_file +".txt")
        with open (path_create,"a+") as text_file:
            text_file.write (running_config)
            text_file.close()

a= Main_window()    
