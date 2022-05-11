from imports import *

#finish reservation: load in database and send email
def finish_reservation(mylist, manager_museums):
    cursor = manager_museums.cursor()
    for child in mylist.get_children():
        reservation_item = mylist.item(child)["values"]
        send_email(reservation_item[2], reservation_item)
        insert_reservation = "INSERT INTO `reservation`(`Name`, `Surname`, `Email`, `Museum`, `Phone`, `Age`, `Gender`, `Code`, `Date`, `Today`, `Time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_reservation, reservation_item)
        manager_museums.commit()
    cursor.close()
    mylist.delete(*mylist.get_children())

#function for statistics main
def stats(type, manager_museums):
    global museums
    cursor = manager_museums.cursor()
    if type == "Age":
        count_reservation = """select 
        sum(case when Age < 3 then 1 else 0 end) AS Over3,
        sum(case when Age >= 3 and Age < 8 then 1 else 0 end) AS Age3_8,
        sum(case when Age >= 8 and Age < 14 then 1 else 0 end) AS Age8_14,
        sum(case when Age >= 14 and Age < 18 then 1 else 0 end) AS Age14_18,
        sum(case when Age >= 18  then 1 else 0 end) AS Over18
        from reservation;"""
    elif type == "Gender":
        count_reservation = """select 
        sum(case when Gender = 'M' then 1 else 0 end) AS Male,
        sum(case when Gender = 'F' then 1 else 0 end) AS Female
        from reservation;"""
    elif type == "Interests":
        count_reservation = """select Museum from reservation;"""
        
    cursor.nextset()
    cursor.execute(count_reservation)
    result = cursor.fetchall()
    cursor.nextset()
    
    if type != "Interests":
        int_result = [str(result[0][i]) for i in range(len(result[0]))]
        values = [int(int_result[i]) for i in range(len(int_result))]
        percent = [round(values[i]/sum(values)*100, 2) for i in range(len(values))]
    else:
        list_result = [result[i][0].partition(' ')[0] for i in range(len(result))]
        
        values = [list_result.count(museums[i]) for i in range(len(museums))]
        percent = [round(values[i]/sum(values)*100, 2) for i in range(len(values))]
        
    manager_museums.commit()
    cursor.close()
    
    y = np.array(percent)
    if type == "Age":
        mylabel = ["Age < 3", "Age 3-8", "Age 8-14", "Age 14-18", "Age > 18"]
    elif type == "Gender":
        mylabel = ["Male", "Female"]
    else:
        mylabel = museums
        
    myexplode = [0 for i in range(len(y))]
    myexplode[list(y).index(max(list(y)))] = 0.2

    plt.pie(y, labels = mylabel, explode = myexplode, shadow = True, autopct = "%1.1f%%", center = (screensize[0]/2, screensize[1]/2))
    plt.show()

#function to connect to database application
def link_xampp(link_button, error_data_base):
    error_data_base.destroy()
    sleep(.5)
    pyautogui.press('win')
    sleep(.5)
    pyautogui.write('Xampp Control Panel')
    sleep(.5)
    pyautogui.press('enter')

#function to update entry fields any 500 ms
def update_entry(buy, entry_list):
    buy.after(500, update_entry)

#function to add reservation in database
def add_reservation(reservation_data, manager_museums, mylist):
    reservation_data_copy = reservation_data.copy()
    date_reservation = reservation_data_copy[8][0].get() + "-" + reservation_data_copy[8][1].get() + "-" + reservation_data_copy[8][2].get()
    reservation_data_copy[8] = date_reservation
    for i in range(8):
        if i != 2:
            reservation_data_copy[i] = reservation_data_copy[i].get()
        else:
            reservation_data_copy[i] = reservation_data_copy[i].get(1.0, "end-1c")
    if len(reservation_data_copy) == 10:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        reservation_data_copy.append(time)
    mylist.insert("", 'end', values = tuple(reservation_data_copy))

#function to send e-mail confirmation to client
def send_email(recipient, reservation_item):
    sender_email = "managermuseums@gmail.com"
    receiver_email = recipient
    password = "MuS3uMs22"

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email 
    price, discount = 100, 1
    if reservation_item[6] == 'M':
        polite = "Mr"
    else:
        polite = "Mrs"
    
    if reservation_item[5] < 3:
        discount = 0
    elif reservation_item[5] >= 3 and reservation_item[5] < 8:
        discount = 0.25
    elif reservation_item[5] >= 8 and reservation_item[5] < 14:
        discount = 0.5
    elif reservation_item[5] >= 14 and reservation_item[5] < 18:
        discount = 0.75
    elif reservation_item[7] != '':
        discount = 0.9
    
    price *= discount
    
    text = ""
    html = f"""\
    <html>
      <body>
        <p>Hello {polite} {reservation_item[0]} {reservation_item[1]}, <br><br>
           Your reservation at {reservation_item[3]} for {reservation_item[8]} is ready. The price is {price}<br>
           Please confirm at 
           <a href="https://sites.google.com/view/managermuseumscom/pagina-de-pornire">managermuseums.com</a> <br><br>
           Sincerly,<br>
           ManagerMuseums TM.
        </p>
      </body>
    </html>
    """
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

#funtion for exit window
def ask_exit(): 
    ask = Toplevel()
    
    width, height = 500, 400
    posX, posY = screensize[0]//2-width//2, screensize[1]//2-height//2
    ask.geometry(f"{width}x{height}+{posX}+{posY}")
    ask.resizable(False, False)
    
    img = Image.open("./wallpapers/exit.jpg")
    
    resized = img.resize((width, height))
    
    exit_image = ImageTk.PhotoImage(resized)
    ask_label = Label(ask, image = exit_image, text = "Are you sure\n you want to exit ?")
    ask_label.pack()
    
    yes_button = Button(ask, text="Yes",  command = exit)
    yes_button.place(x = width/3, y = 7*height/8, anchor = "center")
    
    no_button = Button(ask, text="No", command = ask.destroy)
    no_button.place(x = 2*width/3, y = 7*height/8, anchor = "center")
    
    ask.mainloop()  

#function for login verification
def verification_login(submit_button, user_entry, password_entry, data):
    if user_entry.get() == user_key and password_entry.get() == password_key:
        data.destroy()

#function for close button in the login page
def stop(submit_button, data):
    data.destroy()
    exit()

#function for limit input length in booking's fields entries
def character_limit(entry_text, limit, type, entry):
    global toggle2
    if toggle2 == 0:
        limit = 0
    if type == "digits" and entry_text.get()[-1] not in "0123456789":
        entry_text.set(entry_text.get()[:-1])
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[:limit])       

#method applied to eye button login page        
def change_eye(eye_button, password_entry):
    global toggle
    if toggle == 0:
        password_entry.configure(show = "")
        toggle = 1
        image = Image.open("./buttons/eye_open.jpg")
    else:
        password_entry.configure(show = "*")
        toggle = 0
        image = Image.open("./buttons/eye_closed.jpg")
    
    resized = image.resize((screensize[0]//40, screensize[0]//40))
    changed_image = ImageTk.PhotoImage(resized)
    
    eye_button.configure(image = changed_image)
    eye_button.image = changed_image

#buy ticket function for Booking menu    
def buy_ticket(manager_museums):
    global museums_list
    buy = Toplevel()
    registrations = Toplevel()
    
    w, h, posX1, posY1 = screensize[0]//2, screensize[1], -10, 15
    posX2, posY2 = w + posX1, posY1
    
    registrations.geometry(f"{w}x{h}+{posX2}+{posY2}")
    buy.geometry(f"{w}x{h}+{posX1}+{posY1}")
    buy.resizable(False, False)
    registrations.resizable(False, False)
    
    mylist = ttk.Treeview(registrations, column=("Name", "Surname", "Email", "Museum", "Phone", "Age", "Gender", "Code", "Date", "Today", "Time"), show='headings', height = 50)
    
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
    
    img = Image.open("./wallpapers/buy_ticket.jpg")
    resized = img.resize((w, h))
    buy_image = ImageTk.PhotoImage(resized)
    buy_label = Label(buy, image = buy_image)
    buy_label.pack()
    
    #input variables for entries
    name_input, surname_input, cnp_input, phone_input, date_input_day, date_input_month, date_input_year, museum_input, code_input, mail_input, separator_input, gender_input, age_input = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
    
    #labels
    name_label = Label(buy, text = "Name: ", font = ("", 15))
    name_label.place(x = w/12, y = h/2-2*screensize[0]//30)
    surname_label = Label(buy, text = "Surname: ", font = ("", 15))
    surname_label.place(x = w/12, y = h/2-screensize[0]//30)
    gender_label = Label(buy, text = "Gender: ", font = ("", 15))
    gender_label.place(x = 5*w/8, y = h/2-2*screensize[0]//30)
    age_label = Label(buy, text = "Age: ", font = ("", 15))
    age_label.place(x = 5*w/8+0.22*w, y = h/2-2*screensize[0]//30)
    phone_label = Label(buy, text = "Phone: ", font = ("", 15))
    phone_label.place(x = 5*w/8, y = h/2)
    museum_label = Label(buy, text = "Museum: ", font = ("", 15))
    museum_label.place(x = w/12, y = h/2)
    code_label = Label(buy, text = "Code: ", font = ("", 15))
    code_label.place(x = 5*w/8, y = h/2+screensize[0]//30)
    mail_label = Label(buy, text = "Mail: ", font = ("", 15))
    mail_label.place(x = w/12, y = h/2+screensize[0]//30)
    date_label = Label(buy, text = "Date: ", font = ("", 15))
    date_label.place(x = 5*w/8, y = h/2+2*screensize[0]//30)
    
    #entries definitions and place
    name_entry = Entry(buy, textvariable = name_input, font = ("Arial", 14))
    name_entry.place(x = w/12+screensize[0]//12, y = h/2-2*screensize[0]//30, height = h/25, width = h/4)
    name_entry.focus_set()
    surname_entry = Entry(buy, textvariable = surname_input, font = ("Arial", 14))
    surname_entry.place(x = w/12+screensize[0]//12, y = h/2-screensize[0]//30, height = h/25, width = h/4)
    gender_entry = ttk.Combobox(buy, textvariable = gender_input, font = ("Arial", 14))
    gender_entry.place(x = 0.77*w, y = h/2-2*screensize[0]//30, height = h/25, width = w/18)
    gender_entry["values"] = ("M", "F")
    #gender_entry["state"] = "readonly"
    age_entry = Entry(buy, textvariable = age_input, font = ("Arial", 14))
    age_entry.place(x = 0.77*w+w/6, y = h/2-2*screensize[0]//30, height = h/25, width = w/18)
    phone_entry = Entry(buy, textvariable = phone_input, font = ("Arial", 14))
    phone_entry.place(x = 0.77*w, y = h/2, height = h/25, width = 0.18*w)
    museum_entry = AutocompleteEntry(buy, textvariable = museum_input, font = ("Arial", 14), completevalues = museums_list)
    museum_entry.place(x = w/12+screensize[0]//12, y = h/2, height = h/25, width = h/4)
    code_entry = Entry(buy, textvariable = code_input, font = ("Arial", 14))
    code_entry.place(x = 0.77*w, y = h/2 + screensize[0]//30, height = h/25, width = w/7)
    mail_entry = Text(buy, font = ("Arial", 14))
    mail_entry.place(x = w/12+screensize[0]//12, y = h/2+screensize[0]//30, height = h/14, width = h/4)
    date_entry_day = Entry(buy, textvariable = date_input_day, font = ("Arial", 14))
    date_entry_month = Entry(buy, textvariable = date_input_month, font = ("Arial", 14))
    date_entry_year = Entry(buy, textvariable = date_input_year, font = ("Arial", 14))
    date_entry_day.place(x = 0.77*w, y = h/2+2*screensize[0]//30, height = h/25, width = w/25)
    date_entry_month.place(x = 0.77*w+w/14, y = h/2+2*screensize[0]//30, height = h/25, width = w/25)
    date_entry_year.place(x = 0.77*w+2*w/14, y = h/2+2*screensize[0]//30, height = h/25, width = 2*w/25)
    separator1 = Entry(buy, textvariable = separator_input, font = ("Arial", 14))
    separator2 = Entry(buy, textvariable = separator_input, font = ("Arial", 14))
    separator1.place(x = 0.77*w+w/22, y = h/2+2*screensize[0]//30, height = h/25, width = w/50)
    separator2.place(x = 0.77*w+17*w/144, y = h/2+2*screensize[0]//30, height = h/25, width = w/50)
    today = datetime.today().strftime("%Y-%m-%d")
    

    ###uncomment this to register randomly when booking
    '''
    for i in range(20):
        dict = {1:[31,31], 2:[28, 29], 3:[31,31], 4:[30,30], 5:[31,31], 6:[30,30], 7:[31,31], 8:[31,31], 9:[30,30], 10:[31,31], 11:[30,30], 12:[31,31]}
        name_entry.insert(0, choice(names_list))
        surname_entry.insert(0, choice(surnames_list))
        age_entry.insert(0, choice(ages_list))
        museum_entry.insert(0, choice(museums_list))
        mail_entry.insert(INSERT, name_entry.get() + "_" + surname_entry.get() + ".gmail.com")
        gender_entry.insert(0, choice(genders_list))
        phone_entry.insert(0, choice(phones_list))
        prob = randint(1, 100)
        prob2 = randint(1, 100)
        if(prob < prob2):
            code_entry.insert(0, choice(codes_list))
        date_entry_year.insert(0, randint(datetime.now().year, 2023))
        if datetime.now().year == date_entry_year.get():
            date_entry_month.insert(0, randint(datetime.now().month, 12))
        else:
            date_entry_month.insert(0, randint(1, 12))
        if int(date_entry_year.get()) % 4 != 0:
            date_entry_day.insert(0, randint(1, dict[int(date_entry_month.get())][0]))
        else:
            date_entry_day.insert(0, randint(1, dict[int(date_entry_month.get())][1]))
    '''
        ###
    
    
    #trace inputs entries to limitate size
    separator_input.set("/")
    name_input.trace("w", lambda *args: character_limit(name_input, 15, "characters", name_entry))
    surname_input.trace("w", lambda *args: character_limit(surname_input, 15, "characters", surname_entry))
    phone_input.trace("w", lambda *args: character_limit(phone_input, 10, "digits", phone_entry))
    cnp_input.trace("w", lambda *args: character_limit(cnp_input, 13, "digits", cnp_entry))
    museum_input.trace("w", lambda *args: character_limit(museum_input, 30, "characters", museum_entry))
    code_input.trace("w", lambda *args: character_limit(code_input, 8, "digits", code_entry))
    date_input_day.trace("w", lambda *args: character_limit(date_input_day, 2, "digits", date_entry_day))
    date_input_month.trace("w", lambda *args: character_limit(date_input_month, 2, "digits", date_entry_month))
    date_input_year.trace("w", lambda *args: character_limit(date_input_year, 4, "digits", date_entry_year))
    separator_input.trace("w", lambda *args: character_limit(separator_input, 1, "characters", separator1))
    separator_input.trace("w", lambda *args: character_limit(separator_input, 1, "characters", separator2))
    age_input.trace("w", lambda *args: character_limit(age_input, 3, "digits", age_input))
    
    #store reservation data in a list
    reservation_data = [name_entry, surname_entry, mail_entry, museum_entry, phone_entry, age_entry, gender_entry, code_entry, [date_entry_year, date_entry_month, date_entry_day], today]
    
    #buy button
    ###add to window not load in database
    buy_button = Button(buy, text = "Buy", command = lambda: add_reservation(reservation_data, manager_museums, mylist))
    buy_button.place(x = w/2 - w/10, y = 4*h/5, anchor = "center", width = w/10, height = h/20)
    
    finish_button = Button(buy, text = "Finish", command = lambda: finish_reservation(mylist, manager_museums))
    finish_button.place(x = w/2 + w/10, y = 4*h/5, anchor = "center", width = w/8, height = h/20)
    
    myFont = font.Font(family='', size = 20)
    buy_button['font'] = myFont
    finish_button['font'] = myFont
      
        ###uncomment this to invoke button automatically
    '''    
        buy_button.invoke()        
        name_entry.delete(0, END)
        surname_entry.delete(0, END)
        age_entry.delete(0, END)
        museum_entry.delete(0, END)
        mail_entry.delete('1.0', END)
        gender_entry.delete(0, END)
        phone_entry.delete(0, END)
        gender_entry.delete(0, END)
        date_entry_day.delete(0, END)
        date_entry_month.delete(0, END)
        date_entry_year.delete(0, END)
    '''  
        ###
    
    buy.mainloop() 