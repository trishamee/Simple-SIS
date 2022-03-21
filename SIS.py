from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkscrolledframe import ScrolledFrame
import csv

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
        self.id_num = StringVar()
    #Options
        Button(master, text="Add", font="Segoe 15", relief=GROOVE, bd=0, command=self.add, fg="black", bg="gold",height = 1, width = 5).grid(row=0, column = 0,pady =7,padx =7,sticky="W")      
        Button(master, text="Delete", font="Segoe 15", relief=GROOVE, bd=0, command=self.delete, fg="black", bg="gold",height = 1, width = 5).grid(row= 2, column = 0,pady =7,padx =7,sticky="W")
        Button(master, text="Edit", font="Segoe 15", relief=GROOVE, bd=0, command=self.edit, fg="black", bg="gold",height = 1, width = 5).grid(row=1, column = 0,pady =7,padx =7,sticky="W")
        Button(master, text="Search", font="Segoe 14", relief=GROOVE, bd=0, command=self.search, fg="black", bg="gold",height = 1, width = 5).grid(row=2, column = 4,pady =7,padx =7,sticky="W")
        Button(master, text = "Display student List", font = "Segoe 14", relief = GROOVE, command =self.update_list,fg= "black", bg= 'gold', bd=0).grid(row = 3, column = 0, sticky = 'ew', columnspan= 7, padx = 7, pady = 7)
    # Automatic clear entry in search box
        def on_click(event):
            event.widget.delete(0, END)
        default_text = StringVar()
        default_text.set('Enter ID# here(0000-0000)')
    #Search bar
        self.search_bar = Entry(master, font="Segoe 13", fg="Gray", bg="white", bd=0, justify=RIGHT, textvariable= default_text, width = 23)
        self.search_bar.bind("<Button-1>", on_click)
        self.search_bar.grid(row = 2, column = 3, sticky = 'e') 
    #Labels and title
        self.title_label = Label(master, text = 'Student Information', font = 'Segeo 25', bg = 'maroon', fg = 'Gold').grid(row = 0, column = 1, sticky = 'ew', columnspan= 5, padx = 7, pady = 7)
        self.title_label = Label(master, text = 'System', font = 'Segeo 25', bg = 'maroon', fg = 'Gold').grid(row = 1, column = 1, sticky = 'ew', columnspan= 5, padx = 7, pady = 7)
    #Scroll frame for student display
        self.sf = ScrolledFrame(master, width=415, height=250)
        self.sf.grid(row = 5, rowspan = 6,column = 0, columnspan = 7, sticky = "EW", padx = 7, pady = 7)
        self.sf.bind_arrow_keys(master)
        self.sf.bind_scroll_wheel(master)
        self.frame2 = self.sf.display_widget(Frame)
    #Treeview for student display
        columns = ('ID number', 'Name', 'Course', 'Year level', 'Gender')
        self.tree = ttk.Treeview(self.frame2, columns = columns, show = 'headings', height = 250)
        self.tree.heading('ID number', text = 'ID number')
        self.tree.column('ID number', width = 80)
        self.tree.heading('Name', text = 'Name')
        self.tree.column('Name', width = 150)
        self.tree.heading('Course', text = 'Course')
        self.tree.column('Course', width = 120)
        self.tree.heading('Year level', text = 'Year level')
        self.tree.column('Year level', width = 30)
        self.tree.heading('Gender', text = 'Gender')
        self.tree.column('Gender', width = 50)
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

    #For selecting students in the displayed list
    def item_selected(self,event):
        for selected_item in self.tree.selection():
            self.id_num = self.tree.item(selected_item)['values'][0]

    #updating displayed list of students
    def update_list(self):
        file = open ('Student Information.csv', newline = '')
        reader = csv.reader(file)
        for element in reader:
            self.tree.insert('',END, values = element)
        self.tree.grid()

    #Add in csv file
    def add_csv(self):
        file = open('Student Information.csv', 'a', newline = '')
        writer = csv.writer(file)
        writer.writerow(self.stud_data)
        file.close()
        for item in self.tree.get_children():
           self.tree.delete(item)
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
        for item in self.tree.get_children():
           self.tree.delete(item)
        self.update_list()

    # Student Form Function (For add and edit)
    def form(self, option):
        stud_form = Toplevel(bg = 'maroon')
        stud_form.geometry("380x200")
        stud_form.title("Student Information Form")
        stud_form.resizable(width=False, height=False)

        #collect input
        def retrieve_input():
            self.num = self.stud_num.get()
            self.name = self.stud_name.get()
            self.course = self.stud_course.get()
            self.year = self.stud_year.get()
            self.gender = self.gender_choice.get()
            if self.gender == '1':
                self.gender = 'Male'
            if self.gender == '2':
                self.gender ='Female'
            self.stud_data = [self.num, self.name, self.course, self.year, self.gender]

        #clear entry wiget after use
        def clear_entry():
            id_bar.delete(0,END)
            name_bar.delete(0,END)
            course_bar.delete(0,END)
            year_bar.delete(0,END)
            self.gender_choice.set(None)

        #save input in csv
        def save():
            retrieve_input()
            if self.option == 2: #edit option
                self.delete_in_csv()
            self.add_csv()
            clear_entry()
            stud_form.destroy()

        #cancel function
        def cancel():
            clear_entry()
            stud_form.destroy()

        id_lbl = Label(stud_form,text = 'ID number :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 0, column = 0, sticky = 'ew', padx = 3, pady = 3)
        name_lbl = Label(stud_form,text = 'Name :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 1, column = 0, sticky = 'ew', padx = 3, pady = 3)
        course_lbl = Label(stud_form,text = 'Course :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 2, column = 0, sticky = 'ew', padx = 3, pady = 3) 
        year_lbl = Label(stud_form,text = 'Year :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 3, column = 0, sticky = 'ew', padx = 3, pady = 3)
        gender_lbl = Label(stud_form,text = 'Gender :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 4, column = 0, sticky = 'ew', padx = 3, pady =3)
        
        Button(stud_form, text="Save", font="Segoe 11", relief=GROOVE, bd=0, command=save, fg="black", bg="gold",height = 1, width = 5).grid(row=5, column = 1, pady =7,padx =7, sticky = 'e')      
        Button(stud_form, text="Cancel", font="Segoe 11", relief=GROOVE, bd=0, command=cancel, fg="black", bg="gold",height = 1, width = 5).grid(row=5, column = 2, pady =7,padx =7)      
       
        id_bar = Entry (stud_form, textvariable = self.stud_num, font = 'Segoe 13', bg = 'white', justify = LEFT)       
        name_bar = Entry (stud_form,textvariable = self.stud_name, font = 'Segoe 13', bg = 'white', justify = LEFT)
        course_bar = Entry (stud_form,textvariable = self.stud_course, font = 'Segoe 13', bg = 'white', justify = LEFT)
        year_bar = Entry (stud_form,textvariable = self.stud_year, font = 'Segoe 13', bg = 'white', justify = LEFT)
       
        if self.option == 2:
            file = open('Student Information.csv','r')
            stud_file = csv.reader(file)
            for element in stud_file:
                if element[0] == self.id_num:
                    id_bar.insert(0,element[0])
                    name_bar.insert(0,element[1])
                    course_bar.insert(0, element[2])
                    year_bar.insert(0, element[3])
                    self.gender_choice.set(element[4])


        id_bar.grid(row=0, column = 1 , pady =3, padx = 3, sticky = 'W')       
        name_bar.grid(row = 1, column= 1, pady= 3, padx = 3, sticky = 'w')       
        course_bar.grid(row = 2, column= 1, pady= 3, padx = 3, sticky = 'w') 
        year_bar.grid(row = 3, column= 1, pady= 3, padx = 3, sticky = 'w')
        gender_bar = Radiobutton(stud_form, text = 'Male', variable = self.gender_choice, value =1,font = 'Segoe 13', bg = 'maroon', fg = 'gold').grid(row=4, column =1, sticky = 'w')
        gender_bar = Radiobutton(stud_form, text = 'Female', variable = self.gender_choice, value =2,font = 'Segoe 13', bg= 'maroon', fg = 'gold').grid(row=4, column =1, sticky = 'E')
    

    #Add function
    def add(self):
        self.option = 1
        self.form(self.option)

    #Delete function
    def delete(self):
        answer = messagebox.askquestion("delete?", "Are you sure you want to remove student from list?")
        if answer == 'yes':
            self.delete_in_csv()
        else:
            pass

    #Edit Function
    def edit(self):
        self.option = 2
        self.form(self.option)

    #Enter Function
    def search(self):
        stud_inf = Toplevel(bg = 'maroon')
        stud_inf.geometry("350x200")
        stud_inf.title("Student Information Form")
        stud_inf.resizable(width=False, height=False)
       
        def re_edit():
            stud_inf.destroy()
            self.edit()

        def re_delete():
            stud_inf.destroy()
            self.delete()

        self.id_num = self.search_bar.get()
        file = open('Student Information.csv','r')
        stud_file = csv.reader(file)
        counter = 0
        for element in stud_file:
            if element[0] == self.id_num:
                for i in range(0,5):
                    temp_var = element[i]
                    data = Label( stud_inf,text = temp_var, fg= 'gold', font = 'Segoe 13', bg = 'maroon')
                    data.grid(column = 2)
                counter += 1
        if counter == 0:
            messagebox.showerror("Search Error", "Student does not exist.")
            stud_inf.destroy()

        id_lbl = Label(stud_inf,text = 'ID number :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 0, column = 0, sticky = 'ew', padx = 3, pady = 3)
        name_lbl = Label(stud_inf,text = 'Name :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 1, column = 0, sticky = 'ew', padx = 3, pady = 3)
        course_lbl = Label(stud_inf,text = 'Course :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 2, column = 0, sticky = 'ew', padx = 3, pady = 3)
        year_lbl = Label(stud_inf,text = 'Year :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 3, column = 0, sticky = 'ew', padx = 3, pady = 3)
        gender_lbl = Label(stud_inf,text = 'Gender :', fg = 'gold', font = 'Segeo 13', bg = 'maroon').grid(row = 4, column = 0, sticky = 'ew', padx = 3, pady =3)

        Button(stud_inf, text="Edit", font="Segoe 11", relief=GROOVE, bd=0, command=re_edit, fg="black", bg="gold",height = 1, width = 5).grid(row=5, column = 1, pady =7,padx =7, sticky = 'e')      
        Button(stud_inf, text="Delete", font="Segoe 11", relief=GROOVE, bd=0, command=re_delete, fg="black", bg="gold",height = 1, width = 5).grid(row=5, column = 2, pady =7,padx =7)      


class SIS(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the window properties
        self.title("Student Information System")
        self.resizable(width=False, height=False)
        self.geometry("450x500") 
        self.configure(bg = 'maroon')
        mainframe(self).grid()


if __name__ == '__main__':
    app = SIS()
    app.mainloop()
