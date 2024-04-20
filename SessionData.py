import os
import pickle

class SessionData:
    def __init__(self):
        self.recent_files = []
        # SensoryData object (sensory data of self.recent_files[-1])
        self.sensory_data = None
        self.view = {}
        self.view["grid"] = False
        self.view["legend"] = True
        self.view["selection"] = True
        self.image_save_path = ""
        self.export_active_plots = []

    def store_session_file(self, filename="session.dat"):
        """
        Save session data
        Note: overwrites file given by filename
        pickle.HIGHEST_PROTOCOL will be used
        """
        try:
            f = open(filename, "wb")
            pickle.dump(self, f, -1)
            f.close()
        except BaseException:
            print("Could not write file.")

    def update(self, **kwargs):

        limit = 15

        if "new_recent" in kwargs:
            temp = []
            for recent in self.recent_files:
                if recent[0] != kwargs["new_recent"][0]:
                    temp.append(recent)
            temp.append(kwargs["new_recent"])
            if len(temp) > limit:
                del temp[0]
            self.recent_files = temp

        if "sensory_data" in kwargs:
            self.sensory_data = kwargs["sensory_data"]

        if "view" in kwargs:
            self.update_view(kwargs["view"])

        if "image_save_path" in kwargs:
            self.image_save_path = kwargs["image_save_path"]

        if "export_active_plots" in kwargs:
            self.export_active_plots = kwargs["export_active_plots"]

    def update_view(self, v):
        self.view["grid"] = v["grid"]
        self.view["legend"] = v["legend"]
        self.view["selection"] = v["selection"]

    def check_recent_files(self):
        temp = []
        for recent_file in self.recent_files:
            if os.path.isfile(recent_file[0]):
                temp.append(recent_file)
        self.recent_files = temp

def load_session_data(filename="session.dat"):
    """

    Loads SessionData object

    """
    print(filename)
    session = {}

    file_exists = os.path.exists(filename)
    if file_exists:
        try:
            f = open(filename, "rb")
            session = pickle.load(f)  # class/object is reconstructed and returned
            session.check_recent_files()
            f.close()
            return session
        except Exception as e:
            print(e)
            print("Could not load session file.")
            return None
    else:
        print("No previous session file.")