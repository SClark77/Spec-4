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




#### Admin Functions ####
def admin():

	root = Tk()
	root.title("Repair Procedures")
	root.geometry("750x500")




	# create or connect to database
	con = sqlite3.connect("repair.db")

	# create curser
	c = con.cursor()

	# create table , only used for first run
	#c.execute("""CREATE TABLE repairs (
	#	unit text,
	#	problem text,
	#	repair_pro text
	#	)""")

	# create update function 
	def update():

		# create or connect to database
		con = sqlite3.connect("repair.db")
		# create curser
		c = con.cursor()



		record_id = select_box.get()

		c.execute("""UPDATE repairs SET
		unit = :unit,
		problem = :problem,
		repair_pro = :repair_pro

		WHERE oid = :oid""",

		{
		"unit": unit_edit.get(),
		"problem": fault_edit.get(),
		"repair_pro": fix_edit.get(),

		"oid": record_id

		}


		)


		# commit changes
		con.commit()


		# close connection
		con.close()

		editor.destroy()

	# create edit function to update a record
	def edit():

		global editor
		# create new window for edit
		editor = Tk()
		editor.title("Edit Record")
		editor.geometry("700x200")

		# create or connect to database
		con = sqlite3.connect("repair.db")
		# create curser
		c = con.cursor()

		record_id = select_box.get()
		# query the database
		c.execute("SELECT * FROM repairs WHERE oid = " + record_id)
		records = c.fetchall()

		# create global vaiable for text box names
		global unit_edit
		global fault_edit
		global fix_edit

		# entry fields
		unit_edit = Entry(editor, width=40)
		unit_edit.grid(row=0, column=1, sticky=W, padx=20, pady=10)

		fault_edit = Entry(editor, width=40)
		fault_edit.grid(row=1, column=1, sticky=W, padx=20, pady=10)

		fix_edit = Entry(editor, width=100)
		fix_edit.grid(row=2, column=1, padx=20)

		# create field labels
		unit_label_edit = Label(editor, text="Unit Type")
		unit_label_edit.grid(row=0, column=0, sticky=E, pady=10)

		fault_label_edit = Label(editor, text="Fault")
		fault_label_edit.grid(row=1, column=0, sticky=E, pady=10)

		fix_label_edit = Label(editor, text="Repair")
		fix_label_edit.grid(row=2, column=0, sticky=E)

		# loop through results
		for record in records:
			unit_edit.insert(0, record[0])
			fault_edit.insert(0, record[1])
			fix_edit.insert(0, record[2])

		# create a Save button
		save_btn = Button(editor, text="Save Record", command=update, bg="grey")
		save_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

	# create query function
	def query():
		global query
		# create new window for edit
		query = Tk()
		query.title("show Record")
		query.geometry("700x500")
		# create or connect to database
		con = sqlite3.connect("repair.db")
		# create curser
		c = con.cursor()

		record_id = select_box.get()
		# query the database
		c.execute("SELECT * FROM repairs oid = " + record_id)
		records = c.fetchall()

		# delete function
		def delete():
		# create or connect to database
			con = sqlite3.connect("repair.db")
			# create curser
			c = con.cursor()

			# delete record
			c.execute("DELETE from repairs WHERE oid = " + select_box.get())


			# commit changes
			con.commit()


			# close connection
			con.close()



	# submit function
	def submit():


		# create or connect to database
		con = sqlite3.connect("repair.db")
		# create curser
		c = con.cursor()
		# insert into table
		c.execute("INSERT INTO repairs VALUES (:unit, :fault, :fix)",
			{
			"unit": unit.get(),
			"fault": fault.get(),
			"fix": fix.get()
			})


		# commit changes
		con.commit()


		# close connection
		con.close()
		# clear text boxes
		unit.delete(0, END)
		fault.delete(0, END)
		fix.delete(0, END)

	# write to csv excel function
	def write_to_csv(records):
		with open("Repairs.csv","a", newline="") as f:
			w = csv.writer(f, dialect="excel")
			header = ["Unit Type", "Fault Type", "Possible Repairs", "Record #"]
			w.writerow(header)
			for record in records:
				
				w.writerow(record)



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
		sql = ""
		selected = drop.get()
		if selected == "Search by...":
			error = Label(search_records, text="Choose From List.")
			error.grid(row=1, column=2)

		if selected == "Unit":
			sql = "SELECT * FROM repairs WHERE unit = ?"

		if selected == "Fault":
			sql = "SELECT repair_pro FROM repairs WHERE problem = ?"



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
			searched_label = Label(search, text=result)
			searched_label.grid(row=3, column=0, sticky=W)	

		else:

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

			for index, x in enumerate(result):
					num = 0
					index +=2
					for y in x:
						searched_label = Label(second_frame, text=y)
						searched_label.grid(row=index, column=num, sticky=W)	

						num +=1

			
			button_quit = Button(second_frame, text="EXIT", command=search_now.destroy, fg="white", bg="blue")
			button_quit.grid(row=0, column=1)

			searched_label = Label(second_frame, text=result)
			searched_label.grid(row=2, column=1)

			con.commit()
			con.close()

	# search buttons

	global search_btn
	global button_quit

	search_btn = Button(search_records, text="Search", command=search_now)
	search_btn.grid(row=1, column=1, padx=10, pady=10)

	button_quit = Button(search_records, text="EXIT", command=search_records.destroy, fg="white", bg="blue")
	button_quit.grid(row=99, column=1)

	# create query function
	def query():
		# create new window for edit
		query = Tk()
		query.title("show Record")
		query.geometry("700x500")

		# create or connect to database
		con = sqlite3.connect("repair.db")
		# create curser
		c = con.cursor()
		# query the database
		c.execute('SELECT *, oid FROM repairs')
		records = c.fetchall()
		#print(records)

		# loop through results
		#print_records =""

		for index, record in enumerate(records):
			num = 0
			for y in record:
				query_label = Label(query, text=y)
				query_label.grid(row=index, column=num, sticky=W)	

				num +=1
			# export to excell button		
			csv_button = Button(query, text = "Save to Excel", command=lambda: write_to_csv(records))
			csv_button.grid(row=index+1, column=0)
			# commit changes
			con.commit()
			# close connection
			con.close()


	# entry fields
	unit = Entry(root, width=40)
	unit.grid(row=0, column=1, sticky=W, padx=20, pady=10)

	fault = Entry(root, width=40)
	fault.grid(row=1, column=1, sticky=W, padx=20, pady=10)

	fix = Entry(root, width=100)
	fix.grid(row=2, column=1, padx=20)

	select_box = Entry(root, width=10)
	select_box.grid(row=7, column=1)

	# create field labels
	unit_label = Label(root, text="Unit Type")
	unit_label.grid(row=0, column=0, sticky=E, pady=10, padx=10)

	fault_label = Label(root, text="Fault")
	fault_label.grid(row=1, column=0, sticky=E, pady=10)

	fix_label = Label(root, text="Repair")
	fix_label.grid(row=2, column=0, sticky=E,)

	select_label = Label(root, text="Select Record Number")
	select_label.grid(row=6, column=1)

	# create submit button
	submit_btn = Button(root, text="Submit Record", command=submit, bg="grey")
	submit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

	# create a query button
	query_btn = Button(root, text="Show Records", command=query, bg="grey")
	query_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

	# create a delete button
	delete_btn = Button(root, text="Delete Record", command=delete, bg="grey")
	delete_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

	# create a Update button
	update_btn = Button(root, text="Edit Record", command=edit, bg="grey")
	update_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

	# create search button
	search_btn = Button(root, text="Search", command=search)
	search_btn.grid(row=11, column=0, padx=10, pady=10, ipadx=30)

	button_quit = Button(root, text="EXIT", command=root.quit, fg="white", bg="blue")
	button_quit.grid(row=99, column=1)


	# commit changes
	con.commit()


	# close connection
	con.close()


	#### Buttons for main window ####
	# Admin button

	# search button
	search_btn = Button(main, text="Search", command = search, fg="white", bg="blue")
	search_btn.pack(padx=10, pady=10, ipadx=30)

	admin_btn = Button(main, text="Admin",command = admin, bg="grey")
	admin_btn.pack(pady=10, padx=10, ipadx=30)


	button_quit = Button(main, text="EXIT", command=main.quit, fg="white", bg="blue")
	button_quit.pack()



main.mainloop()
