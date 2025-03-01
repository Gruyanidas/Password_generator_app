from tkinter import *
import string, random
from itertools import chain
from tkinter import messagebox
import subprocess
import json
from data_quotes import quotes
import threading

#CONSTANTS
BACKGROUND_COLOR = "#002F5D"
FOREGROUND_COLOR = "#F23005"
HIGHLIGHTCOLOR = "#73020C"
FONT_STYLE = "Satoshi"
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
SPACING = 20
BUTTON_COLOR = "#260101"
HEADER_DEFAULT = "No more passwords problems!"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
	try:
		num_input = int(numeric_chars_entry.get().strip())
		spec_input = int(spec_chars_entry.get().strip())

	except (ValueError, TypeError):
		header.config(text="Type in valid numbers...")
		return

	header.config(text=f"Password generated with {num_input}"
					   f" numbers and {spec_input} spec chars...")

	letters = string.ascii_letters
	digits = string.digits
	spec_chars = string.punctuation
	#PICKING RANDOMS
	chosen_letters = random.choices(letters, k=6)
	chosen_digits = random.choices(digits, k=num_input)
	chosen_spec_chars = random.choices(spec_chars, k=spec_input)

	final_sample = list(chain(chosen_letters, chosen_digits,chosen_spec_chars))
	random.shuffle(final_sample)
	gener_password = "".join(final_sample)
	#copying the password to a clipboard automatically
	subprocess.run(['xclip', '-selection', 'clipboard'], input=gener_password.encode(), check=True)
	# pyperclip.copy(gener_password) command for windows users
	#disabling button
	generate_button.config(state="disabled")
	#inserting values
	password_entry.insert(0, gener_password)
# ---------------------------- RESETTING THE APP ------------------------------- #
def reset():
	generate_button.config(state="normal")
	password_entry.delete(0, END)
	email_entry.delete(0, END)
	website_entry.delete(0, END)
	spec_chars_entry.delete(0, END)
	numeric_chars_entry.delete(0, END)
	header.config(text=HEADER_DEFAULT)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
	# getting data from entries
	website_data = website_entry.get()
	email_data = email_entry.get()
	password = password_entry.get()
	#dict prepared for json to be written
	new_data = {
		website_data : {
			"email" : email_data,
			"password" : password,
		}
	}

	if not website_data or not email_data:
		messagebox.showerror("Empty fields!", "Check and fill in all the fields!")
	else:
		messagebox.askokcancel("Are you fine with this info?", f"You want to save website as {website_data}\n"
															   f"email as {email_data}\n and password as {password}?")
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
		else: #Else je nastavak od try ako try uspe IMPORTANT
			data_dict.update(new_data)

			with open("my_passwords.json", mode="w") as file:
				json.dump(data_dict, file, indent=5)

		messagebox.showinfo("Data saved!", "You saved data for your new account!")

#---------------------------- SEARCH ------------------------------  #
def search():
	website_data = website_entry.get().strip()
	try:
		with open("my_passwords.json", mode="r") as file:
			dict_data = json.load(file)
	except FileNotFoundError:
		messagebox.showerror("No such a file", "...thus, no data that you are looking for!")
	else:
		if website_data not in dict_data:
			messagebox.showerror("No data for search term!", "There is no such data!")
			return
		email_data = dict_data[website_data]["email"]
		password = dict_data[website_data]["password"]
		email_entry.insert(0, email_data)
		password_entry.insert(0, password)
		messagebox.showinfo("Success!", "Data successfully retrieved!")

#---------------------------- CHANGE HEADER ------------------------------  #
def change_header():
	quote = random.choice(quotes)
	header.config(text=quote)
	threading.Timer(8, change_header).start()

# ---------------------------- UI SETUP ------------------------------- #

#APP BODY
window = Tk()
window.title("Personal password generator")
window.config(width= CANVAS_WIDTH, height=CANVAS_HEIGHT, pady=50, padx=50, bg=BACKGROUND_COLOR)

header = Label(text=HEADER_DEFAULT,
			   wraplength=400,
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
					 command=save,
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

spec_chars_entry.bind("<FocusIn>", lambda event: clean_field(spec_chars_entry)) #Event isto reaguje
spec_chars_entry.focus()
numeric_chars_entry.bind("<FocusIn>", lambda event: clean_field(numeric_chars_entry))
change_header()
window.mainloop()