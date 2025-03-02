from tkinter import *
import string
import random
import json
import threading
import subprocess
from itertools import chain
from tkinter import messagebox
from data_quotes import quotes

#CONSTANTS
BACKGROUND_COLOR = "#002F5D"
FOREGROUND_COLOR = "#F23005"
HIGHLIGHTCOLOR = "#73020C"
BUTTON_COLOR = "#260101"
FONT_STYLE = "Satoshi"
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
HEADER_DEFAULT = "No more password problems!"
PASSWORD_FILE = "my_passwords.json"
HEADER_UPDATE_INTERVAL = 8  # Seconds

# ---------------------------- UPDATE HEADER ------------------------------- #
def update_header(text=None):
	"""Updates the header text."""
	header.config(text=text if text else random.choice(quotes))
	threading.Timer(HEADER_UPDATE_INTERVAL, update_header).start()
# ---------------------------- COPY TO CLIPBOARD - FOR LINUX AND WINDOWS USERS ------------------------------- #
def copy_to_clipboard(text):
	"""Copies text to clipboard using xclip (Linux/macOS) or pyperclip (Windows)."""
	try:
		subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), check=True)
	except FileNotFoundError:
		import pyperclip
		pyperclip.copy(text)
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
	try:
		num_input = int(numeric_chars_entry.get().strip())
		spec_input = int(spec_chars_entry.get().strip())
	except ValueError:
		update_header("Type in valid numbers...")
		return

	update_header(f"Password generated with {num_input} numbers and {spec_input} special chars...")

	chosen_letters = random.choices(string.ascii_letters, k=6)
	chosen_digits = random.choices(string.digits, k=num_input)
	chosen_spec_chars = random.choices(string.punctuation, k=spec_input)

	password = "".join(random.sample(list(chain(chosen_letters, chosen_digits, chosen_spec_chars)),
									 len(chosen_letters) + num_input + spec_input))
	copy_to_clipboard(password)
	generate_button.config(state="disabled")
	password_entry.insert(0, password)
# ---------------------------- RESETTING THE APP ------------------------------- #
def reset():
	for entry in [password_entry, email_entry, website_entry, spec_chars_entry, numeric_chars_entry]:
		entry.delete(0, END)
	generate_button.config(state="normal")
	update_header(HEADER_DEFAULT)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
	"""Saves password info to a JSON file."""
	website_data = website_entry.get().strip()
	email_data = email_entry.get().strip()
	password = password_entry.get().strip()

	if not website_data or not email_data:
		messagebox.showerror("Empty fields!", "Check and fill in all the fields!")
		return
	else:
		messagebox.askokcancel("Save confirm", f"You want to save website as {website_data}\n"
															   f"email as {email_data}\n and password as {password}?")

	#modeled patern of data for JSON
	new_data = {website_data : {"email" : email_data,
								"password" : password}}
		#IMPORTANT
	try:
		with open("my_passwords.json", mode="r") as file:
			try:
				data_dict = json.load(file)
			except json.JSONDecodeError:
				data_dict = {}
	except FileNotFoundError:
		with open("my_passwords.json", mode="w") as file:
			json.dump(new_data, file, indent=5)
	else: #Else block continues if 1st try succeeded IMPORTANT
		data_dict.update(new_data)

		with open("my_passwords.json", mode="w") as file:
			json.dump(data_dict, file, indent=5)

	messagebox.showinfo("Data saved!", "You saved data successfully!")

#---------------------------- SEARCH ------------------------------  #
def search():
	"""Searches for saved password information"""
	website_data = website_entry.get().strip()

	try:
		with open("my_passwords.json", mode="r") as file:
			dict_data = json.load(file)
	except (FileNotFoundError, json.JSONDecodeError):
		messagebox.showerror("No such a file", "...thus, no data that you are looking for!")
		return
	else:
		if any(website_data in key for key in dict_data.keys()):
			matching_key = [key for key in dict_data.keys() if website_data in key][0]
			website_entry.delete(0,END)
			website_entry.insert(0,matching_key)
			email_data, password = dict_data[matching_key]["email"], dict_data[matching_key]["password"]
			email_entry.insert(0, email_data)
			password_entry.insert(0, password)
			messagebox.showinfo("Success!", "Data successfully retrieved!")
		else:
			messagebox.showerror("No data for search term!", "There is no such data!")
			return
# ---------------------------- UI SETUP ------------------------------- #

#APP BODY
window = Tk()
window.title("Personal password generator")
window.config(width= CANVAS_WIDTH, height=CANVAS_HEIGHT, pady=50, padx=50, bg=BACKGROUND_COLOR)

header = Label(text=HEADER_DEFAULT,
			   wraplength=700,
			   font=(FONT_STYLE, 16, "italic"),
			   background=BACKGROUND_COLOR,
			   foreground=FOREGROUND_COLOR)
header.grid(column=1, row=1, columnspan=4, padx=10, pady=10)

foto = Canvas(window, background=BACKGROUND_COLOR, highlightthickness=0)
photo_image = PhotoImage(file="logo.png")
image = foto.create_image(150, 120,image=photo_image, anchor="center")
foto.grid(column=1, row=2, columnspan=2, rowspan=2)

spec_chars_label = Label(text="Number of special chars: ",
						 wraplength=170,
						 justify="left",
						 font=(FONT_STYLE, 14, "bold"),
						 foreground=FOREGROUND_COLOR,
						 background=BACKGROUND_COLOR,
						 padx=10, pady=10)
spec_chars_label.grid(column=3, row=2)

spec_chars_entry = Entry(highlightcolor=HIGHLIGHTCOLOR,
						 font=(FONT_STYLE, 16, "bold"),
						 width= 10,
						 highlightthickness=3,
						 relief="raised",
						 justify="center",
						 borderwidth=1,
						 foreground=FOREGROUND_COLOR)
spec_chars_entry.grid(column=4, row=2)

numeric_label = Label(text="Number of numeric chars: ",
					  wraplength=170,
					  justify="left",
					  font=(FONT_STYLE, 14, "bold"),
					  foreground=FOREGROUND_COLOR,
					  background=BACKGROUND_COLOR,
					  padx=10, pady=10)
numeric_label.grid(column=3, row=3)

numeric_chars_entry = Entry(highlightcolor=HIGHLIGHTCOLOR,
						 font=(FONT_STYLE, 16, "bold"),
						 width= 10,
						 highlightthickness=3,
						 relief="raised",
						 justify="center",
						 borderwidth=1,
						 foreground=FOREGROUND_COLOR)
numeric_chars_entry.grid(column=4, row=3)

canvas_test = Canvas(width=500, height=500)
canvas_test.create_text(250, 30, text='No more forgotten passwords',
						anchor='center',
						font=('Fira Code', 18, "bold"),
						fill=BACKGROUND_COLOR)
locker_image = PhotoImage(file="logo.png")
my_image = canvas_test.create_image(250, 150, image=locker_image, anchor="center")

website = Label(text="Website:",
				wraplength=170,
				justify="right",
				font=(FONT_STYLE, 14, "bold"),
				foreground=FOREGROUND_COLOR,
				background=BACKGROUND_COLOR,
				padx=10, pady=10)
website.grid(column=1, row=4)

website_entry = Entry(highlightcolor=HIGHLIGHTCOLOR,
					  font=(FONT_STYLE, 16, "bold"),
					  width=30,
					  highlightthickness=3,
					  relief="raised",
					  justify="center",
					  borderwidth=1,
					  foreground=FOREGROUND_COLOR
					  )
website_entry.grid(column=2, row=4, columnspan=2)

email = Label(text="Email / username:",
				wraplength=170,
				justify="right",
				font=(FONT_STYLE, 14, "bold"),
				foreground=FOREGROUND_COLOR,
				background=BACKGROUND_COLOR,
				padx=10, pady=10)
email.grid(column=1, row=5)

email_entry = Entry(highlightcolor=HIGHLIGHTCOLOR,
					  font=(FONT_STYLE, 16, "bold"),
					  width=41,
					  highlightthickness=3,
					  relief="raised",
					  justify="center",
					  borderwidth=1,
					  foreground=FOREGROUND_COLOR)
email_entry.grid(column=2, row=5, columnspan=3)

password = Label(text="Password:",
				wraplength=170,
				justify="right",
				font=(FONT_STYLE, 14, "bold"),
				foreground=FOREGROUND_COLOR,
				background=BACKGROUND_COLOR,
				padx=10, pady=10)
password.grid(column=1, row=6)

password_entry = Entry(highlightcolor=HIGHLIGHTCOLOR,
					  font=(FONT_STYLE, 16, "bold"),
					  width=25,
					  highlightthickness=3,
					  relief="raised",
					  justify="center",
					  borderwidth=1,
					  foreground=FOREGROUND_COLOR)
password_entry.grid(column=2, row=6, columnspan=2)

generate_button = Button(padx=8, pady=12,
						 bg=BUTTON_COLOR,
						 width=16,
						 cursor="hand2",
						 height=1,
						 relief="raised",
						 borderwidth=2,
						 activebackground=HIGHLIGHTCOLOR,
						 text='Generate password',
						 font=(FONT_STYLE, 10, "bold"),
						 fg=FOREGROUND_COLOR,
						 command=generate_password
						 )
generate_button.grid(column=4, row=6)

reset_button = Button(padx=8, pady=12,
					  bg=BUTTON_COLOR,
					  width=12,
					  cursor="hand2",
					  height=1,
					  relief="raised",
					  borderwidth=2,
					  anchor="center",
					  activebackground=HIGHLIGHTCOLOR,
					  text='Reset',
					  font=(FONT_STYLE, 10, "bold"),
					  fg=FOREGROUND_COLOR,
					  command=reset
					  )
reset_button.grid(column=1, row=7)

search_button = Button(padx=8, pady=12,
						 bg=BUTTON_COLOR,
						 width=14,
						 cursor="hand2",
						 height=1,
						 relief="raised",
						 borderwidth=2,
						 activebackground=HIGHLIGHTCOLOR,
						 text='Search',
						 font=(FONT_STYLE, 10, "bold"),
						 fg=FOREGROUND_COLOR,
						 command=search
						 )
search_button.grid(column=4, row=4)


create_file = Button(padx=8, pady=12,
					 bg=BUTTON_COLOR,
					 cursor="hand2",
					 width=16,
					 height=1,
					 relief="raised",
					 borderwidth=2,
					 justify="left",
					 activebackground=HIGHLIGHTCOLOR,
					 text='Save file',
					 font=(FONT_STYLE, 10, "bold"),
					 command=save_password,
					 fg=FOREGROUND_COLOR)
create_file.grid(column=2, row=7, columnspan=2)

footer = Label(text="App is for local and personal use only\nCoded by Gruyanidas",
			   font=(FONT_STYLE, 10, "italic"),
			   background=BACKGROUND_COLOR,
			   foreground=FOREGROUND_COLOR)
footer.grid(column=1, row=8, columnspan=4, padx=10, pady=20)

#PLACEHOLDERS AND MISC FUNCTIONALITY
def clean_field(entry):
	entry.delete(0, END)

spec_chars_entry.bind("<FocusIn>", lambda event: clean_field(spec_chars_entry))
spec_chars_entry.focus()
numeric_chars_entry.bind("<FocusIn>", lambda event: clean_field(numeric_chars_entry))
update_header()
window.mainloop()