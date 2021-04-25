import tkinter as tk
from tkinter import *
import random
import map_point
import map_gen
import stella_point
import gps_point

# class TestCreation(tk.Frame):
# 	def __init__(self, parent):
# 		tk.Frame.__init__(self, parent)

# 		self.canvas = tk.Canvas(self, width=1600, height=900, background="bisque")
# 		self.xbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
# 		self.ybar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
# 		# self.item_canvas = tk.Canvas(self, width=400, height=400, 
# 		# 	xscrollcommand=self.xbar.set, yscrollcommand=self.ybar.set)

# 		self.xbar.configure(command=self.canvas.xview)
# 		self.ybar.configure(command=self.canvas.yview)

# 		self.canvas.configure(scrollregion=(0,0,4999,4999))

# 		self.xbar.pack(side=BOTTOM, fill=X)
# 		self.ybar.pack(side=RIGHT, fill=Y)
# 		self.canvas.pack(side=LEFT, expand=TRUE, fill=BOTH)

# class that inherits from tk.Frame
class MapCreation(tk.Frame):
	# constructor for MapCreation
	def __init__(self, master=None):
		# call constructor for tk.Frame
		tk.Frame.__init__(self, master)

		# initialize the grid system
		self.grid()

		# set the title
		self.master.title("VIR-Atlas")

		# set the default display mode
		self.mode = 'tmp'


		# set up the rows and columns for the grid system
		for row in range(2):
			self.master.rowconfigure(row, weight=1)

		for col in range(2):
			self.master.columnconfigure(col, weight=1)

		self.update()

		# initialize the frames
		# self.menuFrame = tk.Frame(master, width=self.master.winfo_width(), height=100, bg='yellow')
		self.irFrame = tk.Frame(self.master, bg='blue')
		self.satFrame = tk.Frame(self.master, bg='red')
		self.notesFrame = tk.Frame(self.master, bg='green')

		# place the frames in the grid system
		# self.menuFrame.place(x=0, y=0)
		self.irFrame.grid(
			row=0, 
			column=0, 
			rowspan=1, 
			columnspan=1, 
			sticky=W+E+N+S)
		self.satFrame.grid(
			row=0, column=1, 
			rowspan=1, 
			columnspan=1, 
			sticky=W+E+N+S)
		self.notesFrame.grid(
			row=1, 
			column=0, 
			rowspan=1, 
			columnspan=2, 
			sticky=W+E+N+S)

		# fixes the frame in place so the canvas doesn't forcely expand it
		self.irFrame.grid_propagate(0)
		# self.menuFrame.grid_propagate(0)

		self.setCanvas(self.irFrame, self.stellaCanvas)
		self.setMenubar()


	def setMenubar(self):
		self.menu = tk.Menu(
			self.master,
			background='black',
			foreground='white',
			activebackground='grey',
			activeforeground='white')

		# file
		self.fileButton = tk.Menu(
			self.menu,
			tearoff=0,
			background='black',
			foreground='white')
		self.fileButton.add_command(
			label="Open",
			command=self.openFile)
		self.fileButton.add_command(
			label="Save",
			command=self.saveFile)
		self.menu.add_cascade(
			label="File",
			menu=self.fileButton)

		#view
		self.viewButton = tk.Menu(
			self.menu, 
			tearoff=0, 
			background='black', 
			foreground='white')
		self.viewButton.add_command(
			label="Visual Map", 
			command=self.getVis)
		self.viewButton.add_command(
			label="NIR Map", 
			command=self.getNir)
		self.viewButton.add_command(
			label="Temperature Map", 
			command=self.getTmp)
		self.menu.add_cascade(
			label="View", 
			menu=self.viewButton)

		# Annotate
		self.annotateButton = tk.Menu(
			self.menu, 
			tearoff=0, 
			background='black', 
			foreground='white')
		self.annotateButton.add_command(
			label="New Annotation", 
			command=self.newAnnotate)
		self.menu.add_cascade(
			label="Annotate", 
			menu=self.annotateButton)

		# Help
		self.helpButton = tk.Menu(
			self.menu, 
			tearoff=0, 
			background='black', 
			foreground='white')
		self.helpButton.add_command(
			label="About", 
			command=self.about)
		self.menu.add_cascade(
			label="Help", 
			menu=self.helpButton)

		self.master.config(menu=self.menu)

	def openFile():
		pass

	def saveFile():
		pass

	def newAnnotate():
		pass

	def getVis(self):
		print("vis called")
		self.mode = 'vis'
		self.getMapChange()

	def getNir(self):
		print("nir called")
		self.mode = 'nir'
		self.getMapChange()

	def getTmp(self):
		print("tmp called")
		self.mode = 'tmp'
		self.getMapChange()

	def getMapChange(self):
		self.irFrame.destroy()

		self.irFrame = tk.Frame(self.master, bg='blue')
		self.irFrame.grid(
			row=0, 
			column=0, 
			rowspan=1, 
			columnspan=1, 
			sticky=W+E+N+S)
		self.irFrame.grid_propagate(0)

		self.setCanvas(self.irFrame, self.stellaCanvas)

	def about():
		aboutWindow = Tk()
		aboutWindow.title("About")
		aboutWindow.geometry("400x300")

		Label(aboutWindow,
			text="Our team proposes to build an accurate visible and NIR (near-Infrared light) spectrum (or\n "
				"Color-Infrared) mapping software specifically for STELLA (Science and Technology Education for\n "
				"Land/Life Assessment), that will cartographically include and/or display STELLA’s other sensor\n "
				"readings in a user friendly and visually appealing GUI (Graphical User Interface).\n "
	          ).pack()

		aboutWindow.mainloop()

	def stellaCanvas(self, canvas):
		gps_file = r'vir-atlas-master\Data Files\Feb-26th-2021-05-57PM-Flight-Airdata.csv'
		stella_file = r'vir-atlas-master\Data Files\data.txt'

		canvas_size = 1200
		resolution = 10
		mode = 'vis'

		canvas = map_gen.get_map_alt(gps_file, stella_file, canvas_size, resolution, mode, canvas)

		# pull data from files
		# self.gpsPoints = gps_point.read_drone_csv(r'Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv')
		# self.stellaPoints = stella_point.make_stella_list(r'Data Files/data.txt')

		# parse data, get width and height
		# self.stellaPoints = stella_point.get_batch(self.stellaPoints, "1.X")
		# self.mapPoints,self.mapWidth,self.mapHeight, delta_lat = \
		# 	map_point.set_xy(self.gpsPoints, self.stellaPoints, 1200)

		# # preprocess width and height
		# self.mapWidth = round(self.mapWidth/10) * 10
		# self.mapHeight = round(self.mapHeight/10) * 10

		# # create image based on data
		# self.polyFill = map_gen.get_poly(self.mapHeight, self.mapWidth)
		# self.filled = map_gen.draw_data(self.mapPoints,
		# 	self.polyFill,
		# 	self.mode,
		# 	10,
		# 	self.mapWidth)
		# map_gen.fill_all(self.filled,
		# 	self.polyFill,
		# 	self.mapWidth,
		# 	self.mapHeight,
		# 	10)

		# # attach map imaging to the canvas
		# for t in self.polyFill:
		# 	t.draw(self.canvas)

		# # draw the drone's flight path
		# map_gen.draw_flight_path(self.mapPoints, self.canvas)

	def setCanvas(self, baseFrame, canvasMode):
		# tk.update() will allow retrieval of width and height
		self.update()
		self.windowWidth = baseFrame.winfo_width()
		self.windowHeight = baseFrame.winfo_height()

		# set up the canvas
		self.canvas = Canvas(baseFrame, 
			width=self.windowWidth*0.5, 
			height=self.windowHeight*0.5, 
			background='grey')

		# set up the scrollbars (unnecessary imo)
		self.xsb = tk.Scrollbar(baseFrame,
			orient="horizontal",
			command=self.canvas.xview)
		self.ysb = tk.Scrollbar(baseFrame,
			orient="vertical", 
			command=self.canvas.yview)

		# bound the scrolling region (needs work?)
		self.canvas.configure(scrollregion=(0,0,
			self.windowWidth*0.5,
			self.windowHeight*0.5))

		# set up the grid for the canvas
		self.xsb.grid(row=1, column=0, sticky="ew")
		self.ysb.grid(row=0, column=1, sticky="ns")

		# place the canvas on the frame
		self.canvas.grid(row=0, column=0, sticky="nsew")
		baseFrame.grid_rowconfigure(0, weight=1)
		baseFrame.grid_columnconfigure(0, weight=1)

		# set up the type of canvas you want
		canvasMode(self.canvas)

		# This is what enables using the mouse:
		self.canvas.bind("<ButtonPress-1>", self.move_start)
		self.canvas.bind("<B1-Motion>", self.move_move)

		#linux scroll
		self.canvas.bind("<Button-4>", self.zoomerP)
		self.canvas.bind("<Button-5>", self.zoomerM)

		#windows scroll
		self.canvas.bind("<MouseWheel>",self.zoomer)

	#move
	def move_start(self, event):
		self.canvas.scan_mark(event.x, event.y)

	def move_move(self, event):
		self.canvas.scan_dragto(event.x, event.y, gain=1)

	#windows zoom
	def zoomer(self,event):
		if (event.delta > 0):
			self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
		elif (event.delta < 0):
			self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
		self.canvas.configure(scrollregion = self.canvas.bbox("all"))

	#linux zoom
	def zoomerP(self,event):
		self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
		self.canvas.configure(scrollregion = self.canvas.bbox("all"))
	def zoomerM(self,event):
		self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
		self.canvas.configure(scrollregion = self.canvas.bbox("all"))


if __name__ == '__main__':
	master = tk.Tk()
	master.geometry('1600x900')
	MapCreation(master)
	master.mainloop()

# if __name__ == '__main__':
# 	root = tk.Tk()
# 	TestCreation(root)
# 	root.title("VIR-Atlas")
# 	root.mainloop()

# class Box(tk.Frame):
# 	def __init__(self, master, cardinal_direction):
# 		super().__init__(master)

# 		tk.Label(self, text=cardinal_direction, bg="gray", fg="black").pack()
# 		self.entry = tk.Entry(self, width=10,bg="white", fg="blue")
# 		self.entry.pack()

# if __name__ == '__main__':

#	root = tk.Tk()

#	canvas = tk.Canvas(root)

#	boxes = dict()

#	for card_dir in ['North', 'South', 'East', 'West']:
#		boxes[card_dir] = Box(canvas, card_dir)
#		boxes[card_dir].pack(side='left')

#	canvas.pack()

#	root.mainloop()