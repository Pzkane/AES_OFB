from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from aes import encrypt_decrypt

class App(Tk):
    def __init__(self):
        super().__init__()

        # assign on_closing method to window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("AES encryption in OFB mode")
        self.geometry("400x150")

        self.filename = StringVar(value="")

        self.tabControl = ttk.Notebook(self)

        # Encrypt menu
        self.tab_enc = ttk.Frame(self.tabControl)
        Label(self.tab_enc, text="Encryption Key").grid(row=0)
        Label(self.tab_enc, text="Initialization vector").grid(row=1)
        self.key_input = ttk.Entry(self.tab_enc)
        self.iv_input = ttk.Entry(self.tab_enc)
        self.key_input.grid(row=0, column=1)
        self.iv_input.grid(row=1, column=1)
        self.enc_button = Button(self.tab_enc, text='Encrypt', command=self.encryptAction)
        self.enc_button.grid(row=2, column=1)

        # Decrypt menu
        self.tab_dec = ttk.Frame(self.tabControl)
        Label(self.tab_dec, text="Decryption Key").grid(row=0)
        self.dec_key_input = ttk.Entry(self.tab_dec)
        self.dec_key_input.grid(row=0, column=1)
        self.dec_button = Button(self.tab_dec, text='Decrypt', command=self.decryptAction)
        self.dec_button.grid(row=1, column=1)

        self.tabControl.add(self.tab_enc, text ='Encrypt')
        self.tabControl.add(self.tab_dec, text ='Decrypt')
        self.tabControl.pack(expand = 1, fill ="both")

        button = Button(self, text='Choose file ...', command=self.UploadAction)
        button.pack()

    def showMsg(self, message):
        top = Toplevel(self)
        label = Label(top, text=message)
        label.pack(padx=20, pady=20)

        top.after(3000, top.destroy)

    def UploadAction(self, event=None):
        self.filename.set(filedialog.askopenfilename())
        print('Selected:', self.filename.get())

    def checkFile(self, action):
        if len(self.filename.get()) == 0:
            self.showMsg(f"Choose file to {action}")
            return False
        return True

    def encryptAction(self):
        if not self.checkFile("encrypt"):
            return
        key = self.key_input.get()
        iv = self.iv_input.get()
        if len(key) == 0:
            self.showMsg("Provide encryption key")
            return
        if len(iv) == 0:
            self.showMsg("Provide initialization vector")
            return
        encrypt_decrypt('E', self.filename.get(), str.encode(key), str.encode(iv))
        self.showMsg("File encrypted")

    def decryptAction(self):
        if not self.checkFile("decrypt"):
            return
        key = self.dec_key_input.get()
        if len(key) == 0:
            self.showMsg("Provide decryption key")
            return
        encrypt_decrypt('D', self.filename.get(), str.encode(key), str.encode('0'))
        self.showMsg("File decrypted")

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()