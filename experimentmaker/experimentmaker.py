import tkinter as tk
import sys

from promptdesigner.PromptDesigner import LunchPromptDesigner
from pipelinemaker.experimentmaker import LunchExperiment
from PIL import Image, ImageTk
import os
from pathlib import Path


IMG_X = 75

# for stand-alone
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)

# for pip
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = os.path.dirname(os.path.abspath(__file__)) # getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


app = tk.Tk()
app.title('Experiment Maker')

menu = tk.Frame(app)
menu.pack()

icon_folder = Path(__file__).parent
images = {'promptdesigner': ImageTk.PhotoImage(
        Image.open(icon_folder.joinpath('promptdesignerlogo.png')).resize((IMG_X, IMG_X)),
                                                                 master=menu),
         'pipelinemaker': ImageTk.PhotoImage(
        Image.open(icon_folder.joinpath('pipelinemakerlogo.ico')).resize((IMG_X, IMG_X)),
                                                                 master=menu)}

promptdesigner = tk.Button(menu,
                           text='Prompt Designer',
                           command=LunchPromptDesigner,
                           image=images['promptdesigner'],
                           compound='top',
                           ).pack(side='left')

pipelinemaker = tk.Button(menu,
                          text='Pipeline Maker',
                          command=LunchExperiment,
                          image=images['pipelinemaker'],
                           compound='top',
                          ).pack(side='right')

menu.mainloop()
sys.exit(0)

