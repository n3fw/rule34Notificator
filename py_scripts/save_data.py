import configparser as cg
import configparser
import os.path

class DataSave():
    def __init__(self) -> None:
        self.config = cg.ConfigParser()
    
    def is_first_launch(self) -> bool:
        """
        checks if the config.ini file exists (if not -> first launch)
        """
        if os.path.isfile('config.ini') == False:
            return True
        else:
            return False
    
    def create_config(self):
        """
        creates the config.ini file

        :section a -> fav tags
        :section b -> number of posts per tag
        :section c -> settings per tag
        """
        self.config.add_section('tags')
        self.config.add_section("save_posts")
        self.config.add_section("settings")

        with open("config.ini", "w") as file:
            self.config.write(file)

    def how_many_tags(self) -> int:
        """
        checks how many tags are saved as fav

        :return the next integrer after the last saved tag
        :example : tag saved = {tag1, tag2} -> return 3
        """
        self.config.read("config.ini")
        compt = 1
        while True:
            try:
                self.config.get('tags', ('tag' + f"{compt}"))
            except configparser.NoOptionError:
                break
            compt += 1
        return compt

    def add_fav_tag(self, tag: str, sett: str, post_amount: str):
        """
        adds a favorite tag in the config.ini
        """
        nb_tag = self.how_many_tags()
        new_entry = "tag" + f"{nb_tag}"
        new_amount = "val" + f"{nb_tag}"
        new_sett = "sett" + f"{nb_tag}"
        self.config.read("config.ini")
        self.config.set("tags", new_entry, tag)
        self.config.set("save_posts", new_amount, post_amount)
        self.config.set("settings", new_sett, sett)
        with open("config.ini", "w") as file:
            self.config.write(file)
    
    def remove_fav_tag(self, tag: str):
        """
        removes a favorite tag in the config.ini
        """
        self.config.read("config.ini")
        tag_list = self.config.items("tags")
        index = 0
        for i in range(len(tag_list)):
            if tag_list[i][1] == tag:
                index = i + 1
                break
        tag_to_remove = self.config.get("tags", "tag"+f"{index}")
        value_to_remove = self.config.get("save_posts", "val"+f"{index}")
        sett_to_remove = self.config.get("settings", "sett"+f"{index}")

        last_tag = self.how_many_tags() - 1
        self.config.set("tags", "tag"+f"{index}", self.config.get("tags", "tag"+f"{last_tag}"))
        self.config.set("save_posts", "val"+f"{index}", self.config.get("save_posts", "val"+f"{last_tag}"))
        self.config.set("settings","sett"+f"{index}", self.config.get("settings", "sett"+f"{last_tag}"))

        self.config.set("tags", "tag"+f"{last_tag}", tag_to_remove)
        self.config.set("save_posts", "val"+f"{last_tag}", value_to_remove)
        self.config.set("settings", "sett"+f"{last_tag}", sett_to_remove)

        self.config.remove_option("tags", "tag"+f"{last_tag}")
        self.config.remove_option("save_posts", "val"+f"{last_tag}")
        self.config.remove_option("settings", "sett"+f"{last_tag}")
        with open("config.ini", "w") as file:
            self.config.write(file)
    
    def exist_or_not(self, tag: str) -> bool:
        """
        checks if a tag already exists

        :return True if it exists, else False
        """
        self.config.read("config.ini")
        tag_list = self.config.items("tags")

        for i in range(len(tag_list)):
            if tag_list[i][1] == tag:
                return True
        return False