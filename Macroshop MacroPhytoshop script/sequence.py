import os
import re

class Sequence:
    def __init__(self, image=None):
        self.images = {}
        if image:
            self.set_base(self.parse_base(image))
            self.add_image(image)
            self.set_folder(self.get_base())
        self.set_crop_bounds("")
        self.power_of_two_size = [0,0]
        self.part_params = []
        
    @staticmethod
    def parse_base(image):
        image = os.path.basename(image)
        res = image.replace(".png", "").split(".")
        res2 = res[0].split("_")
        return res2[0]

    @staticmethod
    def index(image):
        pattern = '\.[0-9]+\.'
        res = re.compile(pattern).search(image)
        if res:
            index = int(res.group().replace(".", ""))
            return index
        return None

    @staticmethod
    def gloss(image):
        image = os.path.basename(image)
        return "gloss" in image.lower()

    def get_power_of_two_size(self):
        return self.power_of_two_size
    
    def set_power_of_two_size(self, value):
        self.power_of_two_size = value
        
    def set_part_params(self, values):
        self.part_params = values

        # Part params is a list of values
        # 0. 1stEmpty
        # 1. sortorder
        # 2. Tmenuorder
        # 3. TmenuFrame
    def get_part_params(self):
        return self.part_params
    
    def set_crop_bounds(self, value):
        self.crop_bounds = value
        
    def get_crop_bounds(self):
        return self.crop_bounds
        
    def add_image(self, item):
        # Discard duplicate adding
        index = self.parse_index(item)
        if index in self.get_images():
            print("Index {} exists".format(index))
            return
        self.get_images()[index] = item

    def get_images(self):
        return self.images

    def get_folder(self):
        return self.folder
    
    def set_folder(self, folder):
        self.folder = folder

        
    def parse_index(self, image):
        #image = os.path.basename(image)
        #print(self.get_base())
        #res = image.replace(".png", "").replace(self.get_base(),"").replace(".","")
        #return int(res)

        pattern = '\.[0-9]+\.'
        res = re.compile(pattern).search(image)
        if res:
            index = int(res.group().replace(".", ""))
            return index
        return None
        

        
    def is_member_of(self, image):
        return self.get_base() == self.parse_base(image)

    def set_base(self, base):
        self.base = base
        
    def get_base(self):
        return self.base
