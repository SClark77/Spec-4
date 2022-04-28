# Common Repair Quick Reference Tool
# By Stephen Clark
# Created for Update, Triage and Technician Quick lookup of common faults and repairs.


import csv
import sqlite3
from tkinter import *
from tkinter import ttk
from subprocess import call

main = Tk()
main.title("Repair Procedures")
main.geometry("180x150")

# update function
def update():
	global update

	con = sqlite3.connect("repair.db")
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


	con.commit()

	con.close()

	editor.destroy()

# update record

def edit():

	global editor

	editor = Tk()
	editor.title("Edit Record")
	editor.geometry("700x200")

	con = sqlite3.connect("repair.db")

	c = con.cursor()

	record_id = select_box.get()

	c.execute("SELECT * FROM repairs WHERE oid = " + record_id)
	records = c.fetchall()


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

	# field labels
	unit_label_edit = Label(editor, text="Unit Type")
	unit_label_edit.grid(row=0, column=0, sticky=E, pady=10)

	fault_label_edit = Label(editor, text="Fault")
	fault_label_edit.grid(row=1, column=0, sticky=E, pady=10)

	fix_label_edit = Label(editor, text="Repair")
	fix_label_edit.grid(row=2, column=0, sticky=E)

	select_box = Entry(root, width=10)
	select_box.grid(row=7, column=1)
	# loop
	for record in records:
		unit_edit.insert(0, record[0])
		fault_edit.insert(0, record[1])
		fix_edit.insert(0, record[2])

	# Save button
	save_btn = Button(editor, text="Save Record", command=update, bg="grey")
	save_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# query function
def query():
	global query

	query = Tk()
	query.title("show Record")
	query.geometry("700x500")

	con = sqlite3.connect("repair.db")
	c = con.cursor()

	record_id = select_box.get()

	c.execute("SELECT * FROM repairs oid = " + record_id)
	records = c.fetchall()

# delete function
def delete():

	con = sqlite3.connect("repair.db")
	c = con.cursor()

	c.execute("DELETE from repairs WHERE oid = " + select_box.get())

	con.commit()
	con.close()



# submit function
def submit():

	con = sqlite3.connect("repair.db")
	c = con.cursor()

	c.execute("INSERT INTO repairs VALUES (:unit, :fault, :fix)",
			{
			"unit": unit.get(),
			"fault": fault.get(),
			"fix": fix.get()
			})

	con.commit()
	con.close()

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

# search records function

def search_records():
	search_records = Tk()
	search_records.title("Search")
	search_records.geometry("700x500")

	main_frame = Frame(search_records)
	main_frame.pack(fill=BOTH, expand=1)

	my_canvas = Canvas(main_frame)
	my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

	my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
	my_scrollbar.pack(side=RIGHT, fill=Y)

	my_canvas.configure(yscrollcommand=my_scrollbar.set)
	my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion = my_canvas.bbox("all")))

	second_frame = Frame(my_canvas)

	my_canvas.create_window((0,0), window=second_frame, anchor="nw")

	def search_now():

		con = sqlite3.connect("repair.db")
		c = con.cursor()

		searched = search_box.get()
		sql = "SELECT repair_pro FROM repairs WHERE problem = ?"
		name = (searched, )
		result = c.execute(sql, name)
		result = c.fetchall()

		if not result:
			result = "Record Not Found"

		searched_label = Label(second_frame, text=result)
		searched_label.grid(row=2, column=0,pady=10, padx=10)

		con.commit()
		con.close()

	# entry box search records
	search_box = Entry(second_frame)
	search_box.grid(row=0, column=1,pady=10, padx=10)

	search_box_label = Label(second_frame, text="Search ")
	search_box_label.grid(row=0, column=0,pady=10, padx=10)

	# buttons
	search_btn = Button(second_frame, text="Search", command=search_now)
	search_btn.grid(row=1, column=1, padx=10, pady=10)


# query function
def query():

	query = Tk()
	query.title("show Record")
	query.geometry("700x500")

	con = sqlite3.connect("repair.db")
	c = con.cursor()

	c.execute('SELECT *, oid FROM repairs')
	records = c.fetchall()

	for index, record in enumerate(records):
		num = 0
		for y in record:
			query_label = Label(query, text=y)
			query_label.grid(row=index, column=num, sticky=W)

			num +=1
	# export to excell button
	csv_button = Button(query, text = "Save to Excel", command=lambda: write_to_csv(records))
	csv_button.grid(row=index+1, column=0)

	con.commit()
	con.close()

def root():
	root = Tk()
	root.title("Repair Procedures")
	root.geometry("750x500")

	con = sqlite3.connect("repair.db")
	c = con.cursor()

    # entry fields
	unit = Entry(root, width=40)
	unit.grid(row=0, column=1, sticky=W, padx=20, pady=10)

	fault = Entry(root, width=40)
	fault.grid(row=1, column=1, sticky=W, padx=20, pady=10)

	fix = Entry(root, width=100)
	fix.grid(row=2, column=1, padx=20)

	select_box = Entry(root, width=10)
	select_box.grid(row=7, column=1)

    # field labels
	unit_label = Label(root, text="Unit Type")
	unit_label.grid(row=0, column=0, sticky=E, pady=10, padx=10)

	fault_label = Label(root, text="Fault")
	fault_label.grid(row=1, column=0, sticky=E, pady=10)

	fix_label = Label(root, text="Repair")
	fix_label.grid(row=2, column=0, sticky=E,)

	select_label = Label(root, text="Select Record Number")
	select_label.grid(row=6, column=1)

    # submit button
	submit_btn = Button(root, text="Submit Record", command=submit, bg="grey")
	submit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

    # query button
	query_btn = Button(root, text="Show Records", command=query, bg="grey")
	query_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

    # delete button
	delete_btn = Button(root, text="Delete Record", command=delete, bg="grey")
	delete_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

    # Update button
	update_btn = Button(root, text="Edit Record", command=edit, bg="grey")
	update_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

    # search button
	search_btn = Button(root, text="Search", command=search_records)
	search_btn.grid(row=11, column=0, padx=10, pady=10, ipadx=30)

	button_quit = Button(root, text="EXIT", command=root.quit, fg="white", bg="blue")
	button_quit.grid(row=99, column=1)

	con.commit()
	con.close()



# Admin button
admin_btn = Button(main, text="Admin Functions",command = root, bg="grey")
admin_btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=30)

# search button
search_btn = Button(main, text="Search", command = search_records)
search_btn.grid(row=0, column=0, padx=10, pady=10, ipadx=30, columnspan=1)

button_quit = Button(main, text="EXIT", command=main.quit, fg="white", bg="blue")
button_quit.grid(row=99, column=0, columnspan=1)

main.mainloop()
