from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkscrolledframe import ScrolledFrame
import csv
import re

class mainframe(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.option = 0
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
        self.stud_form = Frame(master, width = 420, height = 300, highlightthickness = 2)
        self.stud_form.grid(row = 2 , column = 8, sticky = 'Ew', rowspan = 8, padx = 10, pady = 10, columnspan = 5)
        self.stud_form.grid_propagate(False)
        self.stud_form.config(background = 'maroon', highlightbackground = 'gold')

    #Frame for options
        self.btn_frame = Frame(master, width = 250, height = 125, highlightthickness = 2)
        self.btn_frame.grid(row = 9 , column = 8, sticky = 'Ew', rowspan = 3, padx = 10, pady = 10, columnspan = 4)
        self.btn_frame.grid_propagate(False)
        self.btn_frame.config(background = 'maroon', highlightbackground = 'gold')
        option_lbl = Label(self.btn_frame, text = 'Options', font = 'Segoe 15', bg = 'maroon', fg = 'gold').grid(row = 0, column = 0, sticky = 'ew', columnspan = 4, pady = 10)
    #Options
        Button(self.btn_frame, text="Add", font="Segoe 15", relief=GROOVE, bd=0, command=self.add, fg="black", bg="gold",height = 1, width = 5).grid(row=3, column = 0,pady =7,padx =20,sticky="EW")      
        Button(self.btn_frame, text="Delete", font="Segoe 15", relief=GROOVE, bd=0, command=self.delete, fg="black", bg="gold",height = 1, width = 5).grid(row= 3, column = 1,pady =7,padx =20,sticky="EW")
        Button(self.btn_frame, text="Edit", font="Segoe 15", relief=GROOVE, bd=0, command=self.edit, fg="black", bg="gold",height = 1, width = 5).grid(row=3, column = 2,pady =7,padx =20,sticky="EW")
        Button(master, text="Search", font="Segoe 14", relief=GROOVE, bd=0, command=self.search, fg="black", bg="gold",height = 1, width = 5).grid(row=2, column = 4,pady =7,padx =7,sticky="W")
        Button(master, text='Reset', font = "Segoe 14", relief = GROOVE, bd = 0, command = self.update_list, fg ='black', height= 1, width = 5, bg= 'gold').grid(row = 5, column = 0, sticky = 'EW',pady = 7, padx = 3)
    # Automatic clear entry in search box
        def on_click(event):
            event.widget.delete(0, END)
        default_text = StringVar()
        default_text.set('Enter ID# here(0000-0000)')
    #search in treeview in every input
        def treesearch(event):
            self.tv_search()
    #Search bar
        self.search_bar = Entry(master, font="Segoe 15", fg="Gray", bg="white", bd=0, justify=RIGHT, textvariable= default_text, width = 25,)
        self.search_bar.bind("<Button-1>", on_click)
        self.search_bar.bind("<KeyRelease>",treesearch)
        self.search_bar.grid(row = 2, column = 3, sticky = 'e') 
    #Labels and title
        self.disp_label = Label(master, text = '-----Student Display-----', font= 'Segoe 14', bg = 'maroon', fg = 'gold').grid(row = 5, column = 2, columnspan = 3,padx = 5, pady =5, sticky ='ew')
        self.title_label = Label(master, text = 'Student Information System', font = 'Segoe 35', bg = 'maroon', fg = 'Gold').grid(row = 0, column = 1,sticky = 'ew', columnspan= 5, padx = 7, pady = 7)
    #Scroll frame for student display
        self.sf = ScrolledFrame(master, width=900, height=445)
        self.sf.grid(row = 6, rowspan = 6,column = 0, columnspan = 7, sticky = "s", padx = 7, pady = 7)
        self.sf.bind_arrow_keys(master)
        self.sf.bind_scroll_wheel(master)
        self.frame2 = self.sf.display_widget(Frame)
    #Treeview style
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=2, highlightbackground = 'Black', bd=0, font=('Segoe', 14))
        style.configure("mystyle.Treeview.Heading", font=('Segoe', 16,'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
    #Treeview for student display
        columns = ('ID number', 'Name', 'Course', 'Year level', 'Gender')
        self.tree = ttk.Treeview(self.frame2, style = "mystyle.Treeview",columns = columns, show = 'headings', height=445)
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
        
        self.update_list()
        self.main()

    def main(self):
        for widgets in self.stud_form.winfo_children():
            widgets.destroy()
        Yrlvl_op = ["1",'2','3','4','5', 'Irregular']

        Button(self.stud_form, text="Save", font="Segoe 11", relief=GROOVE, bd=0, command=self.save, fg="black", bg="gold",height = 1, width = 5).grid(row=7, column = 1, pady =7,padx =2, sticky = 'e')      
        Button(self.stud_form, text="Cancel", font="Segoe 11", relief=GROOVE, bd=0, command=self.cancel, fg="black", bg="gold",height = 1, width = 5).grid(row=7, column = 2, pady =7,padx =10)      
        #Labels and entry for Student Form
        self.label = Label(self.stud_form, text = 'Student Form', fg= 'gold' , font =('Segoe 18'), bg = 'maroon').grid(row= 0, column = 0, columnspan = 5, pady = 10)
        self.id_lbl = Label(self.stud_form,text = 'ID number :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 2, column = 0, sticky = 'ew', padx = 3, pady = 3)
        self.name_lbl = Label(self.stud_form,text = 'Name :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 3, column = 0, sticky = 'ew', padx = 3, pady = 3)
        self.course_lbl = Label(self.stud_form,text = 'Course :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 4, column = 0, sticky = 'ew', padx = 3, pady = 3) 
        self.year_lbl = Label(self.stud_form,text = 'Year :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 5, column = 0, sticky = 'ew', padx = 3, pady = 3)
        self.gender_lbl = Label(self.stud_form,text = 'Gender :', fg = 'gold', font = 'Segoe 15', bg = 'maroon').grid(row = 6, column = 0, sticky = 'ew', padx = 3, pady =3)
        
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
            self.id_bar.grid(row=2, column = 1 , pady =3, padx = 3, sticky = 'W')       
            self.name_bar.grid(row = 3, column= 1, pady= 3, padx = 3, sticky = 'w')       
            self.course_bar.grid(row = 4, column= 1, pady= 3, padx = 3, sticky = 'w') 
            self.year_bar.grid(row = 5, column= 1, pady= 3, padx = 3, sticky = 'w')
            self.gender_bar = Radiobutton(self.stud_form, text = 'Male', variable = self.gender_choice, value =1,font = 'Segoe 13', bg = 'maroon', fg = 'gold').grid(row=6, column =1, sticky = 'w')
            self.gender_bar = Radiobutton(self.stud_form, text = 'Female', variable = self.gender_choice, value =2,font = 'Segoe 13', bg= 'maroon', fg = 'gold').grid(row=6, column =1, sticky = 'E')

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
        self.tree.grid()

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
        for data in self.stud_data:
            if len(data)==0 or data == None:
                messagebox.showerror('Missing Fields', "One of the required field is empty; please check your input" )
                return
        file = open('Student Information.csv','r')
        reader = csv.reader(file)
        for element in reader:
            if (element[0] == self.stud_data[0] and self.stud_data[0] != self.id_num):
                messagebox.showerror("Inavlid Input", "ID number already exists")
                return 
        if self.option == 2: #edit option
            self.delete_in_csv()
        file = open('Student Information.csv', 'a', newline = '')
        writer = csv.writer(file)
        writer.writerow(self.stud_data)
        file.close()
        self.clear_entry()
        self.id_num = ''
        self.update_list()        

    #cancel function
    def cancel(self):
        self.id_num = ''
        self.clear_entry()
        self.update_list()
        self.search_bar.delete(0,END)

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

    #Search/Select Function
    def search(self):
        self.id_num = self.search_bar.get()
        self.tv_search()
        self.option = 3
        self.search_bar.delete(0,END)
        self.main()


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
                self.tree.grid()
                counter += 1
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
