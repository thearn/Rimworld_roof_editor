import Tkinter, Tkconstants, tkFileDialog
#import zlib,base64
from rim_map_roof import RimMapRoof
#from PIL import Image, ImageTk

class TkFileDialogExample(Tkinter.Frame):

  def __init__(self, root):

    Tkinter.Frame.__init__(self, root)

    # options for buttons
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    self.b1 = Tkinter.Button(self, text='Load save game file', command=self.get_save_filename)
    self.b2 = Tkinter.Button(self, text='Generate map roof image', command=self.save_image)
    self.b3 = Tkinter.Button(self, text='Load edited map roof image', command=self.load_image)
    self.b4 = Tkinter.Button(self, text='Export to new game save file', command=self.write_savegame)

    self.l1 = Tkinter.Label(self,text="(No file loaded)")
    self.l2 = Tkinter.Label(self,text="")
    self.l3 = Tkinter.Label(self,text="")
    self.l4 = Tkinter.Label(self,text="")

    self.b1.grid(row=0, column=0)
    self.b2.grid(row=1, column=0)
    self.b3.grid(row=2, column=0)
    self.b4.grid(row=3, column=0)

    self.l1.grid(row=0, column=1)
    self.l2.grid(row=1, column=1)
    self.l3.grid(row=2, column=1)
    self.l4.grid(row=3, column=1)

    w = 25
    self.b1.config(width=w)
    self.b2.config(state='disabled', width=w)
    self.b3.config(state='disabled', width=w)
    self.b4.config(state='disabled', width=w)

    for b in [self.b1, self.b2, self.b3, self.b4]:
        pass#b.pack(**button_opt)


    # define options for opening a save game
    self.game_file_opt = options = {}
    options['defaultextension'] = '.rws'
    options['filetypes'] = [('all files', '.*'), ('text files', '.rws')]
    options['initialdir'] = '.'
    options['parent'] = root
    options['title'] = 'Save game file'

    self.im_file_opt = options = {}
    options['defaultextension'] = '.bmp'
    options['filetypes'] = [('all files', '.*'), ('text files', '.bmp')]
    options['initialdir'] = '.'
    options['parent'] = root
    options['title'] = 'Select image'

  def get_save_filename(self):

    # get filename
    filename = tkFileDialog.askopenfilename(**self.game_file_opt)

    self.map = RimMapRoof(filename)

    for b in [self.b2, self.b3, self.b4]:
        b.config(state='normal')

    self.l1.config(text='Loaded: ' + filename)

  def save_image(self):

    # get filename
    filename = tkFileDialog.asksaveasfilename(**self.im_file_opt)
    if filename == '':
        return
    self.map.write_image(filename)
    self.l2.config(text='Image saved: ' + filename)

  def load_image(self):

    # get filename
    filename = tkFileDialog.askopenfilename(**self.im_file_opt)
    if filename == '':
        return
    self.map.read_image(filename)
    self.l3.config(text='Image Loaded: ' + filename)

  def write_savegame(self):

    # get filename
    filename = tkFileDialog.asksaveasfilename(**self.game_file_opt)
    if filename == '':
        return
    self.map.save(filename)
    self.l4.config(text='Success!')

if __name__=='__main__':

  #icon=zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
  #'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
  
  root = Tkinter.Tk()
  #image=ImageTk.PhotoImage(data=icon)
  #root.tk.call('wm', 'iconphoto', root._w, image)
  root.wm_title("Rimworld roof editor")
  TkFileDialogExample(root).pack()
  root.mainloop()