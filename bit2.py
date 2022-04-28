# Common Repair Quick Reference Tool
# By Stephen Clark
# Created for Update, Triage and Technician Quick lookup of common faults and repairs.


import csv
import sqlite3
from tkinter import *
from tkinter import ttk
from subprocess import call

main = Tk()
main.title("Repair Quick Reference Tool")
main.geometry("280x250")

##### Search Functions ####

def search():
	global search

	search_records = Tk()
	search_records.title("Search")
	search_records.geometry("350x250")

# entry box search records

	search_box = Entry(search_records)
	search_box.grid(row=0, column=1,pady=10, padx=10)

	search_box_label = Label(search_records, text="Search ")
	search_box_label.grid(row=0, column=0,pady=10, padx=10)

	drop = ttk.Combobox(search_records, value=["Search by...", "Unit", "Fault"])
	drop.current(0)
	drop.grid(row=0, column=2)

	def search_now():
		global search_now

		selected = drop.get()
		if selected == "Search by...":
			error = Label(search_records, text="Choose From List.")
			error.grid(row=1, column=2)

		if selected == "Unit":
			sql = "SELECT * FROM repairs WHERE unit = ?"

		if selected == "Fault":
			sql = "SELECT * FROM repairs WHERE problem = ?"



		search_now= Toplevel()
		search_now.title("Search Results")
		search_now.geometry("700x500")

		con = sqlite3.connect("repair.db")

		c = con.cursor()

		searched = search_box.get()
		#sql = "SELECT repair_pro FROM repairs WHERE problem = ?"
		name = (searched, )
		result = c.execute(sql, name)
		result = c.fetchall()

		if not result:
			result = "Record Not Found"

		main_frame = Frame(search_now)
		main_frame.pack(fill=BOTH, expand=1)

		my_canvas = Canvas(main_frame)
		my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

		my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
		my_scrollbar.pack(side=RIGHT, fill=Y)

		my_canvas.configure(yscrollcommand=my_scrollbar.set)
		my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion = my_canvas.bbox("all")))

		second_frame = Frame(my_canvas)

		my_canvas.create_window((0,0), window=second_frame, anchor="nw")

		searched_label = Label(second_frame, text=result)
		searched_label.grid(row=2, column=0,pady=10, padx=10)
		button_quit = Button(second_frame, text="EXIT", command=search_now.destroy, fg="white", bg="blue")
		button_quit.grid(row=99, column=1)

		con.commit()
		con.close()

	# search buttons

	global search_btn
	global button_quit

	search_btn = Button(search_records, text="Search", command=search_now)
	search_btn.grid(row=1, column=1, padx=10, pady=10)

	button_quit = Button(search_records, text="EXIT", command=search_records.destroy, fg="white", bg="blue")
	button_quit.grid(row=99, column=1)


#### Admin Functions ####



#### Buttons for main window ####
# Admin button

# search button
search_btn = Button(main, text="Search", command = search, fg="white", bg="blue")
search_btn.pack(padx=10, pady=10, ipadx=30)

admin_btn = Button(main, text="Admin",command = "root", bg="grey")
admin_btn.pack(pady=10, padx=10, ipadx=30)


button_quit = Button(main, text="EXIT", command=main.quit, fg="white", bg="blue")
button_quit.pack()



main.mainloop()
