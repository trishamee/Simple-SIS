from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import csv
import re

class mainframe(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.option = 3
        self.gender_choice = StringVar()
        self.stud_num = StringVar()
        self.stud_name = StringVar()
        self.stud_course = StringVar()
        self.stud_year = StringVar()
        self.stud_gender = StringVar()
        self.stud_data = []
        self.id_num = ''
        self.year_lvl = StringVar()
        self.substring = ''

    #Frame For student frame and options
        self.stud_form = Frame(master, width = 420, height = 485, highlightthickness = 2)
        self.stud_form.grid(row = 3 , column = 8, sticky = 'nEw', padx = 10, pady = 10, columnspan = 4)
        self.stud_form.grid_propagate(False)
        self.stud_form.config(background = 'maroon', highlightbackground = 'gold')

    #Frame for options
        self.btn_frame = Frame(master, width = 700, height = 55, highlightthickness = 2)
        self.btn_frame.grid(row = 1, column = 4, sticky = 'Ew', padx = 30, pady = 10)
        self.btn_frame.grid_propagate(False)
        self.btn_frame.config(background = 'maroon', highlightbackground = 'gold')

    #Options
        Button(self.btn_frame, text="Add", font="Segoe 15", relief=GROOVE, bd=0, command=self.add, fg="black", bg="gold",height = 1, width = 5).grid(row=0, column = 5,pady =7,padx =7,sticky="e")      
        Button(self.btn_frame, text="Delete", font="Segoe 15", relief=GROOVE, bd=0, command=self.delete, fg="black", bg="gold",height = 1, width = 5).grid(row= 0, column = 7,pady =7,padx =7,sticky="e")
        Button(self.btn_frame, text="Edit", font="Segoe 15", relief=GROOVE, bd=0, command=self.edit, fg="black", bg="gold",height = 1, width = 5).grid(row=0, column = 8,pady =7,padx =7,sticky="E")
        Button(self.btn_frame, text='Reset Search', font = "Segoe 13", relief = GROOVE, bd = 0, command = self.reset, fg ='black', height= 1, bg= 'grey85').grid(row = 0, column = 3,pady =7,padx =7,sticky="W")

    # Automatic clear entry in search box
        def on_click(event):
            event.widget.delete(0, END)
        default_text = StringVar()
        default_text.set('Enter ID# here(0000-0000)')
    #search in treeview in every input
        def treesearch(event):
            self.tv_search()
    #Search bar
        self.search_bar = Entry(self.btn_frame, font="Segoe 15", fg="Gray", bg="white", bd=0, justify=RIGHT, textvariable= default_text, width = 25,)
        self.search_bar.bind("<Button-1>", on_click)
        self.search_bar.bind("<KeyRelease>",treesearch)
        self.search_bar.grid(row = 0, column = 1, sticky = 'w',columnspan = 2) 
    #Labels and title
        self.disp_label = Label(self.btn_frame, text = 'Search:', font= 'Segoe 16', bg = 'maroon', fg = 'gold').grid(row = 0, column = 0,padx = 1, pady =5, sticky ='e')
        self.title_label = Label(master, text = 'Student Information System', font = 'Segoe 35', bg = 'maroon', fg = 'Gold').grid(row = 0, column = 0,sticky = 'ew', padx = 7, pady = 25, columnspan = 12)
    #Scroll frame for student display

        self.sf = Frame(master, width=1200, height=480, bg = 'yellow')
        self.sf.grid(row = 3, rowspan = 6,column = 0, columnspan = 8, sticky = "nsew", padx = 7, pady = 7)
        self.sf.columnconfigure(0, weight = 1)


    #Treeview style
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=2, highlightbackground = 'Black', bd=0, font=('Segoe', 14))
        style.configure("mystyle.Treeview.Heading", font=('Segoe', 16,'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
    #Treeview for student display
        columns = ('ID number', 'Name', 'Course', 'Year level', 'Gender')
        self.tree = ttk.Treeview(self.sf, style = "mystyle.Treeview",columns = columns, show = 'headings')

        treescroll = Scrollbar(self.sf, orient = "vertical", command = self.tree.yview)
        treescroll.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = treescroll.set)

        self.tree.heading('ID number', text = 'ID number')
        self.tree.column('ID number', width = 130 )
        self.tree.heading('Name', text = 'Name')
        self.tree.column('Name', width = 390)
        self.tree.heading('Course', text = 'Course')
        self.tree.column('Course', width = 190)
        self.tree.heading('Year level', text = 'Year level')
        self.tree.column('Year level', width = 85)
        self.tree.heading('Gender', text = 'Gender')
        self.tree.column('Gender', width = 100)
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree.pack(side = LEFT, fill = BOTH)
        self.update_list()
        self.main()

    def main(self):
        for widgets in self.stud_form.winfo_children():
            widgets.destroy()
        Yrlvl_op = ["1",'2','3','4','5', 'Irregular']

        if self.option != 3:
            Button(self.stud_form, text="Save", font="Segoe 11", relief=GROOVE, bd=0, command=self.save, fg="black", bg="gold",height = 1, width = 5).grid(row=7, column = 1, pady =7,padx =2, sticky = 'e')      
            Button(self.stud_form, text="Cancel", font="Segoe 11", relief=GROOVE, bd=0, command=self.cancel, fg="black", bg="gold",height = 1, width = 5).grid(row=7, column = 2, pady =7,padx =10)      
        
        #Labels and entry for Student Form
        self.label = Label(self.stud_form, text = '------------', fg= 'maroon' , font =('Segoe 18'), bg = 'maroon').grid(row= 0, column = 0, columnspan = 5, pady = 30, sticky = 'nsew')
        self.label = Label(self.stud_form, text = 'Student Form', fg= 'gold' , font =('Segoe 18'), bg = 'maroon').grid(row= 0, column = 1, columnspan = 5, pady = 30, sticky = 'nsw')
        self.id_lbl = Label(self.stud_form,text = 'ID number :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 2, column = 0, sticky = 'sew', padx = 3, pady = 13)
        self.name_lbl = Label(self.stud_form,text = 'Name :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 3, column = 0, sticky = 'sew', padx = 3, pady = 13)
        self.course_lbl = Label(self.stud_form,text = 'Course :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 4, column = 0, sticky = 'sew', padx = 3, pady = 13) 
        self.year_lbl = Label(self.stud_form,text = 'Year :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 5, column = 0, sticky = 'sew', padx = 3, pady = 13)
        self.gender_lbl = Label(self.stud_form,text = 'Gender :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 6, column = 0, sticky = 'sew', padx = 3, pady =13)
        
        if self.option != 3: #For adding entry widgets students
            self.id_bar = Entry (self.stud_form, textvariable = self.stud_num, font = 'Segoe 15', bg = 'white', justify = LEFT)       
            self.name_bar = Entry (self.stud_form,textvariable = self.stud_name, font = 'Segoe 15', bg = 'white', justify = LEFT)
            self.course_bar = Entry (self.stud_form,textvariable = self.stud_course, font = 'Segoe 15', bg = 'white', justify = LEFT)
            self.year_bar = OptionMenu(self.stud_form, self.year_lvl, *Yrlvl_op)

        
        #For editing new students
        if self.option == 2: 
            file = open('Student Information.csv','r')
            stud_file = csv.reader(file)
            for element in stud_file:
                if element[0] == self.id_num:
                    self.id_bar.insert(0,element[0])
                    self.name_bar.insert(0,element[1])
                    self.course_bar.insert(0, element[2])
                    self.year_lvl.set(element[3])
                    self.gender_choice.set(element[4])

        #For searching/Selecting a student
        if self.option == 3:
            file = open('Student Information.csv','r')
            stud_file = csv.reader(file)
            for element in stud_file:
                if element[0] == self.id_num:
                    for i in range(0,5):
                        temp_var = element[i]
                        data = Label( self.stud_form,text = temp_var, fg= 'gold', font = 'Segoe 15', bg = 'maroon')
                        data.grid(row= i+2 ,column = 2)


        if (self.option!= 3):
            self.id_bar.grid(row=2, column = 1 , pady =13, padx = 3, sticky = 'sW')       
            self.name_bar.grid(row = 3, column= 1, pady= 13, padx = 3, sticky = 'sw')       
            self.course_bar.grid(row = 4, column= 1, pady= 13, padx = 3, sticky = 'sw') 
            self.year_bar.grid(row = 5, column= 1, pady= 13, padx = 3, sticky = 'sw')
            self.gender_bar = Radiobutton(self.stud_form, text = 'Male', variable = self.gender_choice, value =1,font = 'Segoe 13', bg = 'maroon', fg = 'gold').grid(row=6, column =1, sticky = 'sw', pady = 13)
            self.gender_bar = Radiobutton(self.stud_form, text = 'Female', variable = self.gender_choice, value =2,font = 'Segoe 13', bg= 'maroon', fg = 'gold').grid(row=6, column =1, sticky = 'sE', pady =13)
   
    # If reset-- list back unfiltered; search bar clear
    def reset(self):
        self.update_list()
        self.search_bar.delete(0, END)
        self.search_bar.insert(0,'Enter ID# here(0000-0000)')
   
    #For selecting students in the displayed list
    def item_selected(self,event):
        for selected_item in self.tree.selection():
            self.id_num = self.tree.item(selected_item)['values'][0]
            self.option = 3
            self.main()

    #updating displayed list of students
    def update_list(self):
        file = open ('Student Information.csv', newline = '')
        reader = csv.reader(file)
        for item in self.tree.get_children():
           self.tree.delete(item)
        for element in reader:
            self.tree.insert('',END, values = element)
        self.tree.pack()

    #Add in csv file
    def add_csv(self):
        file = open('Student Information.csv', 'a', newline = '')
        writer = csv.writer(file)
        writer.writerow(self.stud_data)
        file.close()
        self.update_list()

    #delete in csv file
    def delete_in_csv(self):
        temp_list =[]
        file = open('Student Information.csv', 'r')
        reader = csv.reader(file)
        for element in reader:
            if element[0] != self.id_num:
                temp_list.append(element)
        file.close()
        file = open('Student Information.csv' , 'w+' , newline = '')
        writer = csv.writer(file)
        writer.writerows(temp_list)
        file.close()
        self.update_list()
        self.clear_entry()

    #collect input
    def retrieve_input(self):
        self.num = self.stud_num.get()
        self.name = self.stud_name.get()
        self.course = self.stud_course.get()
        self.year = self.year_lvl.get()
        self.gender = self.gender_choice.get()
        if self.gender == '1':
            self.gender = 'Male'
        if self.gender == '2':
            self.gender ='Female'
        self.stud_data = [self.num, self.name, self.course, self.year, self.gender]

    #clear entry wiget after use
    def clear_entry(self):
        if self.option == 3:
            self.option =1
            self.main()
        else:
            self.id_bar.delete(0,END)
            self.name_bar.delete(0,END)
            self.course_bar.delete(0,END)
            self.gender_choice.set(None)
            self.year_lvl.set(None)

    #save input in csv
    def save(self):
        self.retrieve_input()
        if self.option == 3:
            messagebox.showerror("No changes were made", 'If you want to make changes in the selected student please click EDIT in the options below')
            return
        if not re.match('^[0-9]{4}-[0-9]{4}$', self.stud_data[0]):
            print ('huhuhu')
            messagebox.showerror('Invalid Input','ID number is invalid. Must be in format 0000-0000')
            return
        for data in self.stud_data:
            if len(data)==0 or data == None:
                messagebox.showerror('Missing Fields', "One of the required field is empty; please check your input" )
                return
        file = open('Student Information.csv','r')
        reader = csv.reader(file)
        for element in reader:
            if ((element[0] == self.stud_data[0] and self.stud_data[0] != self.id_num) or ()):
                messagebox.showerror("Inavlid Input", "ID number already exists")
                return 
        if self.option == 2: #edit option
            self.delete_in_csv()
        file = open('Student Information.csv', 'a', newline = '')
        writer = csv.writer(file)
        writer.writerow(self.stud_data)
        file.close()
        self.clear_entry()
        self.update_list()  
        self.selected = self.tree.get_children()[-1]
        self.tree.selection_set(self.selected) 
        self.tree.yview_moveto(1)
        

    #cancel function
    def cancel(self):
        self.id_num = ''
        self.clear_entry()
        self.update_list()
        self.search_bar.delete(0,END)
        for widgets in self.stud_form.winfo_children():
            widgets.destroy()
        self.option = 3
        self.main()

    #Add function
    def add(self):
        self.id_num = ''
        self.option = 1
        self.main()

    #Edit Function
    def edit(self):
        if self.option == 2:
            return
        if self.id_num == "":
            messagebox.showerror("Invalid action","Please select a student first")
            return
        self.option = 2
        self.main()

    #Delete function
    def delete(self):
        if self.id_num == "":
            messagebox.showerror("Invalid action","Please select a student first")
            return
        answer = messagebox.askquestion("delete?", "Are you sure you want to remove student from list?")
        if answer == 'yes':
            self.delete_in_csv()
        else:
            pass

    #display only items containing searh key
    def tv_search(self):
        counter =0
        self.substring = self.search_bar.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        file = open('Student Information.csv','r')
        reader = csv.reader(file)
        for element in reader:
            if element[0].find(self.substring) != -1:
                self.tree.insert('',END, values = element)
                self.tree.pack()
                counter += 1
        self.selected = self.tree.get_children()[0]
        self.tree.selection_set(self.selected) 
        self.tree.yview_moveto(0)
        if counter == 0:
            messagebox.showerror("Search Error", "Student does not exist.")


class SIS(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the window properties
        self.title("Student Information System")
        self.state('zoomed')
        self.configure(bg = 'maroon')
        mainframe(self).grid()


if __name__ == '__main__':
    app = SIS()
    app.mainloop()
