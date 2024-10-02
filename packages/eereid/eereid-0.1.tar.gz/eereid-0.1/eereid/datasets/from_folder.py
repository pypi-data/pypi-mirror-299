from eereid.datasets.dataset import dataset
import numpy as np

import re
import os
from glob import glob

from PIL import Image

from tqdm import tqdm

class from_folder(dataset):
    def __init__(self,pth,label,include=None,reshape="median"):
        if include is None:
            include= lambda x: True
        self.pth = pth
        self.label = label
        self.include = include
        self.reshape = reshape
        super().__init__("from_folder")
        self.search_files()

    def search_files(self):
        if type(self.pth) is list:
            files = []
            for p in self.pth:
                files += glob(p)
        else:
            files=glob(self.pth)
        if callable(self.include):
            files = [f for f in files if self.include(f)]
        elif type(self.include) is str:
            files = [f for f in files if re.match(self.include,f)]
        else:
            raise ValueError("include must be a callable or a string")
        files.sort()
        self.files = files

        print("Found {} files".format(len(self.files)))

        
    def auto_size(self,reshape):
        itera=tqdm(self.files,desc="Determining Image Sizes")
        ims=[]
        wids,heis=[],[]
        for fn in itera:
            im=Image.open(fn)
            ims.append(im)
            wids.append(im.size[1])
            heis.append(im.size[0])
            im.close()
        if reshape=="max":
            reshape=(max(wids),max(heis))
        elif reshape=="min":
            reshape=(min(wids),min(heis))
        elif reshape=="mean":
            reshape=(int(np.mean(wids)),int(np.mean(heis)))
        elif reshape=="median":
            reshape=(int(np.median(wids)),int(np.median(heis)))
        else:
            raise ValueError("reshape must be 'max', 'min', 'mean', 'median' or an int tuple")
        print("Reshaping to {}".format(reshape))
        return reshape


    def load_raw(self):
        reshape=self.reshape
        if type(reshape) is str:
            reshape=self.auto_size(reshape)
        x,y=[],[]
        itera=tqdm(self.files)
        itera.set_description("Loading images")
        for fn in itera:
            im=Image.open(fn)
            if reshape is not None:
                im = im.resize(reshape)
            x.append(np.array(im))
        if callable(self.label):
            y = [self.label(f) for f in self.files]
        elif type(self.label) is str:
            y = [re.match(self.label,f).group(1) for f in self.files]
        else:
            raise ValueError("label must be a callable or a string")
        x = np.array(x)
        y = np.array(y)
        return x,y

    def input_shape(self):
        return np.array(Image.open(self.files[0])).shape
    
    def sample_count(self):
        return len(self.files)

    def save(self,pth):
        super().save(pth,pth=self.pth,label=self.label,include=self.include)

    def explain(self):
        return f"Loading images from {self.pth}"



