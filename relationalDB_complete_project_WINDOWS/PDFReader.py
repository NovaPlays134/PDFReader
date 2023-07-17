import tkinter as tk
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfilename
import pyperclip

# root
root = tk.Tk()
root.title("PDF Reader")
root.resizable(False, False)

# geometry
window_width = 800
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# header
header = tk.Frame(root, bg = "#1f1f1f")
header.place(relwidth = 1, relheight = 1)

# logo
logo = Image.open("resources/logo.png")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(header, image = logo, bg = "#1f1f1f")
logo_label.pack(side = tk.LEFT, padx = 25, pady = 10, anchor= tk.NW)
logo_label.pack(pady=10)
logo_label.image = logo


contents = {}

# button functions
def openFile():
    browse_text.set("Loading...")
    file = askopenfile(parent = root, mode = "rb", title = "Choose a file", filetype = [("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfReader(file)

        # text box settings
        text_box.configure(state = "normal")
        text_box.delete("1.0", "end")

        for i, page in enumerate(read_pdf.pages):
            page_string = "Page " + str(i + 1) + "\n"
            text_box.insert("end", page_string)

            page_content = page.extract_text()
            text_box.insert("end", page_content + "\n\n")
            browse_text.set("Browse")
            text_box.tag_configure("center", justify = "center")
            text_box.tag_add("center", 1.0, "end")

            contents["page" + str(i + 1)] = page_string
            contents["content" + str(i + 1)] = page_content + "\n"

        text_box.configure(state = "disabled")

def deleteText():
    if len(contents) != 0:
        text_box.configure(state = "normal")
        text_box.delete("1.0", "end")
        text_box.configure(state = "disabled")
        contents.clear()


def downloadFile():
    if len(contents) != 0:
        file_path = asksaveasfilename()
        if file_path :
            for k, text in contents.items():
                with open(file_path + ".txt", "a") as file:
                    file.write(text + "\n")

def copyText(*text):
    if len(contents) != 0:
        string = ""
        for k, text in contents.items():
            string = string + text + "\n"\
            
        pyperclip.copy(string)

# textbox
textbox_frame = tk.Frame(header, bg = "#1f1f1f")
textbox_frame.place(relx = 0.6, rely = 0.6, anchor = tk.CENTER)
text_box = tk.Text(textbox_frame, height = 10, width = 50, padx = 15, pady = 15, bg = "#1f1f1f", fg = "#b3b3b3", font = ("Segoe UI", 14))
text_box.configure(state = "disabled")
text_box.pack()

textbox_button_frame = tk.Frame(header, bg = "#1f1f1f")
textbox_button_frame.place(relx = 0.9, rely = 0.388, anchor = tk.CENTER)
copy_text = tk.Button(textbox_button_frame, text = "Copy", font = ("Segoe UI", 10), command = lambda: copyText(contents),
                    bg = "#1f1f1f", fg = "#b3b3b3", bd = 0, highlightbackground = "#1f1f1f", highlightcolor = "#1f1f1f", activebackground = "#1f1f1f", activeforeground = "white")
copy_text.pack()
copy_text.bind("<Enter>", lambda event: copy_text.config(fg = "white"))
copy_text.bind("<Leave>", lambda event: copy_text.config(fg = "#b3b3b3"))


# buttons
button_frame = tk.Frame(header, bg = "#1f1f1f")
button_frame.place(relx = 0.6, rely = 0.18, anchor = tk.CENTER)

browse_text = tk.StringVar()
open_file = tk.Button(button_frame, textvariable = browse_text, font = ("Segoe UI", 20), command = openFile,
                    bg = "#1f1f1f", fg = "#b3b3b3", bd = 0, highlightbackground = "#1f1f1f", highlightcolor = "#1f1f1f", activebackground = "#1f1f1f", activeforeground = "white")
open_file.pack(side = tk.LEFT, padx = 30)

browse_text.set("Browse")

open_file.bind("<Enter>", lambda event: open_file.config(fg = "white"))
open_file.bind("<Leave>", lambda event: open_file.config(fg = "#b3b3b3"))

delete_text = tk.Button(button_frame, text = "Delete", font = ("Segoe UI", 20), command = deleteText,
                    bg = "#1f1f1f", fg = "#b3b3b3", bd = 0, highlightbackground = "#1f1f1f", highlightcolor = "#1f1f1f", activebackground = "#1f1f1f", activeforeground = "white")
delete_text.pack(side = tk.LEFT, padx = 30)
delete_text.bind("<Enter>", lambda event: delete_text.config(fg = "white"))
delete_text.bind("<Leave>", lambda event: delete_text.config(fg = "#b3b3b3"))

download_text = tk.Button(button_frame, text = "Download", font = ("Segoe UI", 20), command = lambda: downloadFile(),
                    bg = "#1f1f1f", fg = "#b3b3b3", bd = 0, highlightbackground = "#1f1f1f", highlightcolor = "#1f1f1f", activebackground = "#1f1f1f", activeforeground = "white")
download_text.pack(side = tk.LEFT, padx = 30)
download_text.bind("<Enter>", lambda event: download_text.config(fg = "white"))
download_text.bind("<Leave>", lambda event: download_text.config(fg = "#b3b3b3"))


root.mainloop()