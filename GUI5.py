from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

days = {'Mon':'จันทร์', 'Tues':'อังคาร', 'Wed':'พุธ', 'Thur':'พฤหัส', 'Fri': 'ศุกร์', 'Sat': 'เสาร์', 'Sun':'อาทิตย์'}

def csv_file(expense, PPI, quantity, price, dt):
    with open('savedata.csv','a', encoding = 'utf=8', newline = '') as f:
        fw = csv.writer(f)
        data = [expense, PPI, quantity, price, dt]
        fw.writerow(data)

def read_csv():
    with open('savedata.csv', newline = '', encoding = 'utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
        return data

def update_data(data):
    text2 = ''
    for record in tv.get_children():
        tv.delete(record)
    for i in range(len(data)):
        tv.insert(parent = '', index = 'end', iid = i, value = data[i])
        for j in range(len(data[i])):
            if j == 0 :
                text2 = f'{text2}{data[i][j]}'
            text2 = f'{text2}---{data[i][j]}'
            v2_result.set(text2)
        text2 = text2 + '\n'

def Save(event = None):
    expense = v_expense.get()
    PPI = v_PPI.get()
    quantity = v_quantity.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('ERROR','Please input Expense !')
        E1.focus()
        return

    elif PPI == '':
        messagebox.showwarning('ERROR','Please input Price per item !')
        E2.focus()
        return
        
    elif quantity == '':
        messagebox.showwarning('ERROR','Please input Quantity !')
        E3.focus()
        return    
 
    try:
        price = float(PPI) * int(quantity)
        today = datetime.now().strftime('%a')
        dt = datetime.now().strftime('{}-%Y-%m-%d %H:%M:%S'.format(days[today]))
        print(f'Expense: {expense}\nPrice per item: {PPI}\nQuantity: {quantity}\nTotal price: {price}\nLog time: {dt}')
        text = f'Expense: {expense}\nPrice per item: {PPI}\nQuantity: {quantity}\nTotal price: {price}\nLog time: {dt}'
        v_result.set(text)
        v_expense.set('')
        v_PPI.set('')
        v_quantity.set('')
        csv_file(dt, expense, PPI, quantity, price)
        data = read_csv()
        update_table()
        E1.focus()
    except:
        print('ERROR')
        #messagebox.showerror('ERROR','Please Reinform !!!')
        messagebox.showwarning('ERROR','Please Reinform !!!')
        #messagebox.showinfo('ERROR','Please Reinform !!!')
        v_expense.set('')
        v_PPI.set('')
        v_quantity.set('')
        E1.focus()


GUI = Tk()
GUI.title('Expense calculation program By Hapuria ver 0.1')
GUI.geometry('1000x650+100+0')

##################MENU##################
menubar = Menu(GUI)
GUI.config(menu = menubar)

#FileMenu
filemenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'File', menu = filemenu)
filemenu.add_command(label = 'Import CSV')
filemenu.add_command(label = 'Export to')
filemenu.add_command(label = 'Close')

#Help
def About():
    messagebox.showinfo('About', 'Hello! my name is Tee.\nNice to meet you.')

helpmenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'Help', menu = helpmenu)
helpmenu.add_command(label = 'About', command = About)

#Donate
donatemenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'Donate', menu = donatemenu)
donatemenu.add_command(label = 'Membership')


########################################


Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill = BOTH, expand = 1)

icon_t1 = PhotoImage(file = 'Add_Expense.png')
icon_t2 = PhotoImage(file = 'Expense_List.png')
icon_save = PhotoImage(file = 'Save.png')
icon_bag = PhotoImage(file = 'Bag.png')

Tab.add(T1, text = f'{"Add Expense":^{20}}', image = icon_t1, compound = 'top')
Tab.add(T2, text = f'{"Expense List":^{20}}', image = icon_t2, compound = 'top')

#Frame Add Expense#

F1 = ttk.Frame(T1)
F1.pack() #Create Frame

Main_icon = Label(F1, image = icon_bag)
Main_icon.pack()

FONT1 = (None, 10) #Font setting apply on all text

L1 = ttk.Label(F1, text = 'Expense', font = FONT1)
L1.pack()
v_expense = StringVar()

E1 = ttk.Entry(F1, textvariable = v_expense, font = FONT1)
E1.pack()

L2 = ttk.Label(F1, text = 'Price per item', font = FONT1)
L2.pack()
v_PPI = StringVar()

E2 = ttk.Entry(F1, textvariable = v_PPI, font = FONT1)
E2.pack()

L3 = ttk.Label(F1, text = 'Quantity', font = FONT1)
L3.pack()
v_quantity = StringVar()

E3 = ttk.Entry(F1, textvariable = v_quantity, font = FONT1)
E3.pack()


B = ttk.Button(F1, text = 'Save', command = Save, image = icon_save, compound = 'left')
B.pack(ipadx = 10, ipady = 7)

v_result = StringVar()
v_result.set('-------------- RESULT --------------')
result = ttk.Label(F1, textvariable = v_result, font = FONT1, foreground = "green")
result.pack(pady = 30)

#Frame Expense List#

F2 = ttk.Frame(T2)
F2.pack() #Create Frame

v2_result = StringVar()
v2_result.set('-------------- Empty Expense List --------------')

L4 = ttk.Label(F2, textvariable = v2_result, font = FONT1, foreground = "red")
L4.pack()

header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2, columns = header, show = 'headings', height = 10)
resulttable.pack()
for i in header:
    resulttable.heading(i, text = i)

headerwidth = [150,170,80,80,80]

for h,w in zip(header, headerwidth):
    resulttable.column(h,width = w)

def update_table():
    resulttable.delete(*resulttable.get_children())
    data = read_csv()
    for d in data:
        resulttable.insert('',0, value = d)

update_table()


# tv = ttk.Treeview(F2)

# tv['columns'] = ('Datetime','Expense','Price per item','Quantity','Total price')
# tv.column('#0', width = 0)
# tv.column('Datetime', width = 150, minwidth = 150)
# tv.column('Expense',anchor = W, width = 150, minwidth = 100)
# tv.column('Price per item',anchor = CENTER, width = 150, minwidth = 100)
# tv.column('Quantity',anchor = CENTER, width = 150, minwidth = 100)
# tv.column('Total price',anchor = CENTER, width = 150, minwidth = 100)

# tv.heading("Datetime", text = 'Datetime')
# tv.heading('Expense', text = 'Expense')
# tv.heading('Price per item', text = 'Price per item')
# tv.heading('Quantity', text = 'Quantity')
# tv.heading('Total price', text = 'Total price')

# tv.pack()
# try:
#     data = read_csv()
#     update_data(data)
# except:
#     pass
GUI.mainloop()