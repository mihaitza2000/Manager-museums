#import functions and imports file
from imports import *
from functions import *

def delete_function(mylist, manager_museums):
    selected_items = mylist.selection()
    for selected_item in selected_items:
        deleted_item = mylist.item(selected_item)['values']
        mylist.delete(selected_item)
    cursor = manager_museums.cursor()
    delete_reservation = "DELETE FROM `reservation` where Name = %s and Surname = %s and Email = %s and Museum = %s and Phone = %s and Age = %s and Gender = %s and Code = %s and Date = %s and Today = %s and Time = %s"
    cursor.nextset()
    cursor.execute(delete_reservation, deleted_item)
    manager_museums.commit()

def searchData(results, manager_museums, name_entry, surname_entry, email_entry, mylist):
    data_info = [name_entry.get(), surname_entry.get(), email_entry.get()]
    cursor = manager_museums.cursor()
    search_reservation = "SELECT * FROM `reservation` where Name = %s or Surname = %s or Email = %s"
    cursor.nextset()
    cursor.execute(search_reservation, data_info)
    result = cursor.fetchall()
    manager_museums.commit()
    mylist.delete(*mylist.get_children())
    for i in range(len(result)):
        mylist.insert('', 'end', values = tuple(result[i]))
    cursor.close()

def check_reservation(manager_museums):
    name_var, surname_var, email_var = StringVar(), StringVar(), StringVar()
    check = Toplevel()
    results = Toplevel()
    
    style = ttk.Style(results)
    style.theme_use('clam')
    scrollbar = Scrollbar(results)
    scrollbar.pack(side = RIGHT, fill = Y)
    mylist = ttk.Treeview(results, column=("Name", "Surname", "Email", "Museum", "Phone", "Age", "Gender", "Code", "Date", "Today", "Time"), show='headings', height = 50)
    
    mylist.column("# 1", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 1", text="Name")
    
    mylist.column("# 2", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 2", text="Surname")
    
    mylist.column("# 3", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 3", text="Mail")
    
    mylist.column("# 4", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 4", text="Museum")
    
    mylist.column("# 5", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 5", text="Phone")
    
    mylist.column("# 6", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 6", text="Age")
    
    mylist.column("# 7", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 7", text="Gender")
    
    mylist.column("# 8", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 8", text="Code")
    
    mylist.column("# 9", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 9", text="Date")
    
    mylist.column("# 10", anchor=CENTER, width = screensize[0]//24)
    mylist.heading("# 10", text="Today")
    
    mylist.column("# 11", anchor=CENTER, width = screensize[0]//22)
    mylist.heading("# 11", text="Time")
    
    mylist.pack(fill = 'both')
    
    myFont = font.Font(family='', size = screensize[1]//40)
    w, h, posX1, posY1 = screensize[0]//2, screensize[1], -screensize[1]//80, -screensize[1]//80
    posX2, posY2 = w+posX1, posY1
    check.geometry(f"{w}x{h}+{posX1}+{posY1}")
    results.geometry(f"{w}x{h}+{posX2}+{posY2}")
    title1 = Label(check, text = "Check Reservation", font = ("", 30))
    title1.place(x = w/2, y = h/16, anchor = "center")
    
    name = Label(check, text = "Name: ", font = ("", 25))
    name.place(x = w/8, y = h/4+2*h/16, anchor = "w")
    surname = Label(check, text = "Surname: ", font = ("", 25))
    surname.place(x = w/8, y = h/4+4*h/16, anchor = "w")
    email = Label(check, text = "E-mail: ", font = ("", 25))
    email.place(x = w/8, y = h/4+6*h/16, anchor = "w")
    
    name_entry = Entry(check, textvariable = name_var, font = ("", 22))
    surname_entry = Entry(check, textvariable = surname_var, font = ("", 22))
    email_entry = Entry(check, textvariable = email_var, font = ("", 22))
    name_entry.place(x = 2*w/5, y = h/4+2*h/16, anchor = "w")
    surname_entry.place(x = 2*w/5, y = h/4+4*h/16, anchor = "w")
    email_entry.place(x = 2*w/5, y = h/4+6*h/16, anchor = "w")
    
    search = Button(check, text = "Search", command = lambda: searchData(results, manager_museums, name_entry, surname_entry, email_entry, mylist))
    search.place(x = w/2, y = h/4+8*h/16, anchor = "center", width = h/6, height = h/15)
    
    delete = Button(check, text = "Delete", command = lambda: delete_function(mylist, manager_museums))
    delete.place(x = w/2, y = h/4+10*h/16, anchor = "center", width = h/6, height = h/15)
    search['font'] = myFont
    delete['font'] = myFont
    
    check.mainloop()
    results.mainloop()

#login function
def login(add_reservation):
    data = Tk()
    data.attributes("-fullscreen", True)
    user_input, password_input = StringVar(), StringVar()
    
    image1 = Image.open("./wallpapers/login_wallpaper.png")
    image2 = Image.open("./buttons/close.jpg")
    image3 = Image.open("./buttons/submit.jpg")
    image4 = Image.open("./buttons/eye_closed.jpg")
    
    resized1 = image1.resize(screensize)
    resized2 = image2.resize((screensize[0]//25, screensize[0]//25))
    resized3 = image3.resize((2*screensize[0]//25,screensize[0]//25))
    resized4 = image4.resize((screensize[0]//40, screensize[0]//40))
    
    wallpaper_image = ImageTk.PhotoImage(resized1)
    close_button_image = ImageTk.PhotoImage(resized2)
    submit_button_image = ImageTk.PhotoImage(resized3)
    eye_image = ImageTk.PhotoImage(resized4)
    
    wallpaper_label = Label(data, image = wallpaper_image)
    wallpaper_label.pack()
    eye_button = Button(data, image = eye_image, bg = "#285a41", command = lambda: change_eye(eye_button, password_entry), height = screensize[0]//40, width = screensize[0]//40)
    eye_button.place(x = 0.58*screensize[0] + 160, y = 3*
    screensize[1]/4 - screensize[0]//50 , anchor = "center")
    
    user_entry = Entry(data, textvariable = user_input, font = ("Arial", 20))
    user_entry.place(x = 0.58*screensize[0], y = 13*screensize[1]/20 - screensize[0]//60, height = screensize[0]//30, width = 250, anchor = "center")
    user_entry.focus_set()
    password_entry = Entry(data, show = "*", textvariable = password_input, font = ("Arial", 20))
    password_entry.place(x = 0.58*screensize[0], y = 3*
    screensize[1]/4 - screensize[0]//50, height = screensize[0]//30, width = 250, anchor = "center")
    
    close_button = Button(data, image = close_button_image, bg = "#003c3c", command = lambda *args:stop(submit_button, data))
    close_button.place(x = 0, y = 0)
    submit_button = Button(data, image = submit_button_image, bg = "#285a41", command = lambda *args:verification_login(submit_button, user_entry, password_entry, data))
    submit_button.place(x = screensize[0]/2, y = 7*screensize[1]/8, anchor = "center")
    
    user_input.trace("w", lambda *args: character_limit(user_input, 12, "characters", user_entry))
    password_input.trace("w", lambda *args: character_limit(password_input, 12, "characters", password_entry))
    
    data.mainloop()

#create Window class
class Window(Frame):
    #define constructor
    def __init__(self, master, manager_museums):
        Frame.__init__(self, master)
        self.master = master
        self.manager_museums = manager_museums
        self.index = randint(0, len(museum_types)-1)
        img = Image.open("./museums/"+museum_types[self.index])
        resized = img.resize(screensize)
        wallpaper = ImageTk.PhotoImage(resized)
        self.label = Label(self.master, image = wallpaper)
        self.label.pack()
        self.update()
    
    #update method to change wallpaper images any 2.5 s     
    def update(self):
        global list_index, museum_types
        if list_index == []:
            list_index = [i for i in range(len(museum_types))]
        self.index = choice(list_index)
        list_index.remove(self.index)
        img2 = Image.open("./museums/"+museum_types[self.index])
        resized2 = img2.resize(screensize, Image.ANTIALIAS)
        wallpaper2 = ImageTk.PhotoImage(resized2)
        self.label.configure(image=wallpaper2)
        self.label.image = wallpaper2
        self.label.after(2500, self.update)
    
    #menu funtion to deal with menus and theier options
    def menu_function(self):
        #create main menu
        menu = Menu(self.master)
        self.master.config(menu = menu)
        booking       = Menu(menu)
        file          = Menu(menu)
        statistics    = Menu(menu)
        font_size = 10
        file.add_command(label = "Exit", font = ("", font_size), command = ask_exit)
        statistics.add_command(label = "Age", font = ("", font_size), command = lambda: stats("Age", self.manager_museums))
        statistics.add_command(label = "Gender", font = ("", font_size), command = lambda: stats("Gender", self.manager_museums))
        statistics.add_command(label = "Interests", font = ("", font_size), command = lambda: stats("Interests", self.manager_museums))
        booking.add_cascade(label = "Buy ticket", font = ("", font_size), command = lambda: buy_ticket(manager_museums))
        booking.add_cascade(label = "Check/Cancel reservation", font = ("", font_size), command = lambda: check_reservation(self.manager_museums))
        menu.add_cascade(label = "Booking", menu = booking, font = ("", font_size))
        menu.add_cascade(label = "File", menu = file, font = ("", font_size))
        menu.add_cascade(label = "Statistics", menu = statistics, font = ("", font_size))
    
#main function
if __name__ == "__main__":
    #try to connect to database
    try:
        manager_museums = mysql.connector.connect(
            user = "root",
            password = "",
            host="localhost",
            database = "manager_museums"
        )
        login(manager_museums)
        exception = False
        if True:
            toggle2 = 1
            root = Tk()
            root.attributes("-fullscreen", True)
            app = Window(root, manager_museums)
            app.menu_function()
            root.mainloop()
        exit()
        
    #if can't connect to database a window will pop up
    #to direct to database app needed
    except:
        if exception:
            error_data_base = Tk()
            width1, height1 = 800, 800
            image1 = PIL.Image.open("./wallpapers/data_base_wallpaper.png")
            resized1 = image1.resize((width1, height1))
            wallpaper_image = ImageTk.PhotoImage(resized1)
            label_wallpaper = Label(error_data_base, image = wallpaper_image)
            label_wallpaper.pack()
            
            image2 = PIL.Image.open("./buttons/arrow_button.png")
            resized2 = image2.resize((100, 80))
            arrow_image = ImageTk.PhotoImage(resized2)
            
            link_button = Button(error_data_base, image = arrow_image, text = "Go to Xampp \nControl Panel", compound = "bottom")
            link_button.place(x = width1-130, y = 10, width = 120, height = 140)
            link_button.configure(command = lambda: link_xampp(link_button, error_data_base))
            posX, posY = screensize[0]//2-width1//2, screensize[1]//2-height1//2
            error_data_base.geometry(f"{width1}x{height1}+{posX}+{posY}")
            error_data_base.resizable(False, False)
            error_data_base.mainloop()