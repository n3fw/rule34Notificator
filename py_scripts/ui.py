import tkinter as tk

class UI():
    def __init__(self):
        self.window = None
        self.size = "600x500"
        self.color = "#b0e4a4"
        self.title = "Rule34 Notificator"
        self.ima = "0"
        self.gif = "0"
        self.vid = "0"
        self.settings = None
        self.tag_to_add = None
        self.tag_to_remove = None
        self.action_id = None
        self.icon = "ressources/main_icon.ico"

    def get_settings(self):
        return self.settings
    
    def get_tag_to_add(self):
        return self.tag_to_add
    
    def get_tag_to_remove(self):
        return self.tag_to_remove
    
    def get_action_id(self):
        return self.action_id

    def create_settings(self, category: int):
        """
        changes the self.ima, self.gif and self.vid attributes.
        takes an int as argument which indicates which attributes to change.

        0 -> change self.ima.
        1 -> change self.gif.
        2 -> change self.vid.

        :return None
        :used in button_add_clicked(self)
        :"0" means content_type not saved, "1" means saved
        """
        if category == 0:
            if self.ima == "0":
                self.ima = "1"
            elif self.ima == "1":
                self.ima = "0"
        if category == 1:
            if self.gif == "0":
                self.gif = "1"
            elif self.gif == "1":
                self.gif = "0"
        if category == 2:
            if self.vid == "0":
                self.vid = "1"
            elif self.vid == "1":
                self.vid = "0" 

    def button_add_clicked(self):
        """
        creates a window that allow the user to enter a new fav tag

        :changes both self.tag_to_addn self.action_id and self.settings
        """
        self.window.destroy()
        self.ima, self.gif, self.vid = "0", "0", "0"
        add_window = tk.Tk()
        add_window.geometry("300x250")
        add_window.title("Add Tag")
        add_window.iconbitmap(self.icon)
        add_window.configure(bg = self.color)

        text = tk.Label(add_window, text="Enter a tag to add to favorite here :", bg= self.color)
        text.pack(padx=10, pady=10, side="top", anchor= "nw")
        ima_var = tk.IntVar()
        ima_check = tk.Checkbutton(add_window, text="Check for new images", variable=ima_var, command=lambda: self.create_settings(0), bg= self.color)
        ima_check.place_configure(relx=0.02, rely=0.25)
        gif_var = tk.IntVar()
        gif_check = tk.Checkbutton(add_window, text="Check for new gifs", variable=gif_var, command=lambda: self.create_settings(1), bg= self.color)
        gif_check.place_configure(relx=0.02, rely=0.35)
        vid_var = tk.IntVar()
        vid_check = tk.Checkbutton(add_window, text="Check for new videos", variable=vid_var, command=lambda: self.create_settings(2), bg= self.color)
        vid_check.place_configure(relx=0.02, rely=0.45)
        entry_var = tk.StringVar()
        entry_tag = tk.Entry(add_window, textvariable=entry_var, font=("Arial", 10))
        entry_tag.place_configure(relx= 0.04, rely=0.15, relheight=0.08, relwidth=0.4)
        button_save = tk.Button(add_window, text="Save", command=add_window.destroy, font=("Arial", 15))
        button_save.place_configure(relx = 0.65, rely = 0.75, relheight=0.16, relwidth=0.2)

        add_window.mainloop()
        if entry_var.get() != "" or entry_var.get() != None:
            self.tag_to_add = self.tag_to_add = entry_var.get()
            self.settings = self.ima + self.gif + self.vid
        self.action_id = 0

    def button_remove_clicked(self):
        """
        creates a window to remove a tag from favs

        :changes self.tag_to_remove
        """
        self.window.destroy()
        remove_window = tk.Tk()
        remove_window.geometry("250x100")
        remove_window.title("Remove Tag")
        remove_window.iconbitmap(self.icon)
        remove_window.configure(bg= self.color)

        text = tk.Label(remove_window, text="Select a tag to remove :", bg= self.color)
        text.pack(padx = 10, pady = 10, side="top", anchor = "nw")
        rem_var = tk.StringVar()
        rem_tag = tk.Entry(remove_window, textvariable=rem_var, font=("Arial", 10))
        rem_tag.place_configure(relx = 0.05, rely = 0.35, relheight= 0.18, relwidth= 0.4)
        button_remove = tk.Button(remove_window, text="Remove", command=remove_window.destroy, font= ("Arial", 15))
        button_remove.place_configure(relx = 0.55, rely = 0.60, relheight=0.30, relwidth=0.34)

        remove_window.mainloop()
        self.tag_to_remove = rem_var.get()
        self.action_id = 1
    
    def button_notif_clicked(self, notifs: list[tuple: (str, list)]):
        """
        handles the windows displaying notifications

        :return None
        :takes a list of tuple : ("tag", int("new posts"))
        """
        notif_window = tk.Tk()
        notif_window.geometry("500x" + str(len(notifs) * 20 + 25))
        notif_window.title("Notifications")
        notif_window.iconbitmap(self.icon)
        notif_window.configure(bg = self.color)

        text_notif = ""
        for i in range (1, len(notifs) + 1):
            if notifs[i-1][1] != [None, None, None]:
                text_notif += f"{notifs[i-1][0]}" + " : " + ( (f"{notifs[i-1][1][0]}" + " new images, ") if notifs[i-1][1][0] != None else "") + ( (f"{notifs[i-1][1][1]}" + " new gifs, ") if notifs[i-1][1][1] != None else "") + ( (f"{notifs[i-1][1][2]}" + " new videos, ") if notifs[i-1][1][2] != None else "") + "\n"
            else:
                text_notif += f"{notifs[i-1][0]}" + " : 0 new posts" + "\n"
        notif_label = tk.Label(notif_window, padx=10, text=text_notif, background=self.color)
        notif_label.pack(side="top")
        quit_button = tk.Button(notif_window, pady=5, text="Ok", command=notif_window.destroy)
        quit_button.pack(side="bottom")

        notif_window.mainloop()

    def set_action_to_notif(self):
        """
        used to set self.action_id to 2, so the RunApp class knows to call self.button_notif_cliked()

        :used in main_window(self)
        """
        self.window.destroy()
        self.action_id = 2

    def main_window(self):
        """
        creates the main window of the app
        """
        self.window = tk.Tk()
        self.window.geometry(self.size)
        self.window.title(self.title)
        self.window.configure(bg= self.color)
        self.window.iconbitmap(self.icon)
        button_add = tk.Button(self.window, text="Add favorite tag", command=self.button_add_clicked, font=("Arial", 10))
        button_add.place_configure(relx= 0.15, rely= 0.75, relheight=0.05, relwidth=0.2)

        button_remove = tk.Button(self.window, text="Remove favorite tag", command=self.button_remove_clicked, font=("Arial", 10))
        button_remove.place_configure(relx=0.65, rely=0.75, relheight=0.05, relwidth=0.2)

        button_notif = tk.Button(self.window, text="See notifications", command=self.set_action_to_notif, font=("Arial", 10))
        button_notif.place_configure(relx=0.40, rely=0.75, relheight=0.05, relwidth=0.2)

        try:
            image_logo = tk.PhotoImage(file="ressources/logo.png")
            image_logo = image_logo.subsample(2, 2)
            logo_label = tk.Label(self.window, image=image_logo)
            logo_label.place_configure(relx = 0.15, rely = 0.15)
        except:
            self.print_message("Couldn't load logo image !", "Error")

        self.window.mainloop()
    
    def print_message(self, mess: str, wind_title: str):
        window = tk.Tk()
        window.title(wind_title)
        window.iconbitmap("ressources/error_icon.ico")
        label = tk.Label(window, text=mess, font=("Arial", 12))
        label.pack(padx=20, pady=20)
        close_button = tk.Button(window, text="Close", command=window.destroy, font=("Arial", 12))
        close_button.pack(pady=10)

        window.mainloop()
    
    def action_id_reset(self):
        """
        resets the value of self.action_id to None

        :changes the self.action_id attributes
        """
        self.action_id = None