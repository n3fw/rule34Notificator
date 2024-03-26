import page_get as pg
import save_data as sd
import ui as ui

class RunApp():
    def __init__(self) -> None:
        self.page = pg.PageGet()
        self.data = sd.DataSave()
        self.ui = ui.UI()
        self.for_notif = []
        self.notifs = []
    
    def get_for_notif(self):
        return self.for_notif
    
    def get_notifs(self):
        return self.notifs

    def run(self):
        if self.data.is_first_launch():
            self.data.create_config()
        if self.page.net_check() == False:
            self.ui.print_message("Couldn't connect to rule34 ! Try again", "Error")
            exit()
        self.ui.main_window()
        WhatToDo = self.ui.get_action_id()
        if WhatToDo == 0:
            if self.ui.get_tag_to_add() != None: 
                tag = self.page.add_tag(self.ui.get_tag_to_add())
                if self.page.is_tag_none() or tag == False:
                    self.ui.print_message("This tag doesn't exist or uses invalid caracters", "TagNotFound")
                else:
                    self.page.page_amount()
                    self.page.number_post_by_tag()
                    setting = self.ui.get_settings()
                    posts = str(self.page.get_tag_amount())

                    self.data.add_fav_tag(self.page.get_tag(), setting, posts)
                    self.ui.print_message("Tag succesfully added !", "Success")
        
        elif WhatToDo == 1:
            tag = self.ui.get_tag_to_remove()
            if self.data.exist_or_not(tag):
                self.data.remove_fav_tag(tag)
                self.ui.print_message("Tag succesfully removed.", "Success")
            else:
                self.ui.print_message("Tag is not saved as favorite !", "TagNotFound")

        elif WhatToDo == 2:
            self.data.config.read("config.ini")
            if self.data.config.items("tags") == [] or self.data.config.items("tags") == None:
                self.ui.print_message("No tags saved as favorites !", "TagNotFound")
            else:
                self.ui.button_notif_clicked(self.notifs)

    def update(self):
        """
        changes the values of posts saved to the current amount

        :changes the config.ini file
        """
        self.data.config.read("config.ini")
        list_tag = self.data.config.items("tags")
        for i in range (len(list_tag)):
            self.page.add_tag(list_tag[i][1])
            self.page.page_amount()
            self.page.number_post_by_tag()
            self.for_notif[i][2] = self.page.get_tag_amount()
            self.data.config.set("save_posts", "val"+f"{i + 1}", str(self.page.get_tag_amount()))
        with open("config.ini", "w") as file:
            self.data.config.write(file)

    def list_for_notif(self):
        """
        creates a 2dim list with tag, old save of posts and 0

        :0 value is changed in update(self)
        :changes self.for_notif
        """
        self.data.config.read("config.ini")
        list_tag = self.data.config.items("tags")
        list_val = self.data.config.items("save_posts")
        for i in range (len(list_tag)):
            group = [list_tag[i][1], list_val[i][1], 0]
            self.for_notif.append(group)
    
    def create_notifs(self):
        """
        creates a list of tuple with tag, and number of new posts

        :changes self.notifs
        """
        self.notifs = []
        self.data.config.read("config.ini")
        list_tag = self.data.config.items("tags")
        for i in range (len(list_tag)):
            self.page.add_tag(list_tag[i][1])
            self.page.calc_new_posts(int(self.for_notif[i][1]), self.for_notif[i][2])
            self.notifs.append((list_tag[i][1], self.page.get_newposts()))

    def reset_action(self):
        """
        resets the flag for action on the main window to None
        """
        self.ui.action_id = None
    
    def is_no_action(self):
        """
        checks if any action has been performed on the main window
        """
        return self.ui.action_id == None
    
    def launch(self):
        if self.data.is_first_launch():
            self.data.create_config()
        if self.page.net_check() == False:
            self.ui.print_message("Couldn't connect to rule34 ! Try again", "Error")
            exit()