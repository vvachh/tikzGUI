#!/usr/bin/env python

import Tkinter as tk
import ttk
import math

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()
		self.activeTool = 'line'
		self.activeLine = 'reg'
		self.activePattern = 'empty'
		self.activeWeight = 'thin'

		self.linestrings = {'reg': '', 'dot': 'dotted', 'rarrow': '->', 'larrow': '<-'}
		self.fillstrings = {'empty': '', 'solid': 'fill=black', 'ne': 'pattern=north east lines', 'nw': 'pattern = north west lines', 'dots': 'pattern = dots'}
		self.weightstrings = {'thin': '', 'thick': 'thick', 'vt': 'very thick', 'ut': 'ultra thick'}

		self.codeOn = False
		self.drawingIndex = 0
		self.points = []
		self.objects = {'line':[], 'circle':[], 'rectangle': [], 'text':[]}


	def createWidgets(self):
		#self.quitButton = tk.Button(self, text='quit', command=self.quit)
		#self.quitButton.grid(0,0)
		
		# Code buttons
		self.codebuttons = tk.Frame(self)
		self.codebuttons.grid(row=0,column=0)

		self.codeButton = tk.Button(self.codebuttons, text='Show tikz', command=self.tikz)
		self.codeButton.grid(row=0, column=0)

		self.compileButton = tk.Button(self.codebuttons, text='Compile tikz', command = self.compile)
		self.compileButton.grid(row=0, column=1)

		def clear():
			self.canvas.delete('all')
			self.objects = {'line':[], 'circle':[], 'rectangle':[], 'text':[]}
		self.clearButton = tk.Button(self.codebuttons, text='Clear', command=clear )
		self.clearButton.grid(row=0,column=2)

		# Tool buttons
		self.toolbuttons = tk.Frame(self)
		self.toolbuttons.grid(row=1, column=0)

		self.lineButton = tk.Button(self.toolbuttons, text='/', relief = tk.SUNKEN, command = self.pickLine)
		self.lineButton.grid(row=0, column=0)

		self.rectButton = tk.Button(self.toolbuttons, text='[]', command = self.pickRect)
		self.rectButton.grid(row=0, column=1)

		self.circButton = tk.Button(self.toolbuttons, text='o', command = self.pickCirc)
		self.circButton.grid(row=0, column=2)

		self.textButton = tk.Button(self.toolbuttons, text='T', command = self.pickText)
		self.textButton.grid(row=0, column=3)

		# Line style buttons
		self.linestylebuttons = tk.Frame(self)
		self.linestylebuttons.grid(row=2)

		self.reglineButton = tk.Button(self.linestylebuttons, text='--', relief = tk.SUNKEN, command = self.pickRegLine)
		self.reglineButton.grid(row=0, column=0)

		self.dotlineButton = tk.Button(self.linestylebuttons, text='..', command = self.pickDotLine)
		self.dotlineButton.grid(row=0, column=1)

		self.rarrowButton = tk.Button(self.linestylebuttons, text='->', command = self.pickRArrow)
		self.rarrowButton.grid(row=0, column=2)

		self.larrowButton = tk.Button(self.linestylebuttons, text='<-', command = self.pickLArrow)
		self.larrowButton.grid(row=0, column=3)

		# Fill style buttons
		self.fillbuttons = tk.Frame(self)
		self.fillbuttons.grid(row=3)

		self.whiteButton = tk.Button(self.fillbuttons, relief=tk.SUNKEN, text='empty', command=self.pickEmpty)
		self.whiteButton.grid(row=0,column=0)

		self.blackButton = tk.Button(self.fillbuttons, text='solid', command=self.pickSolid)
		self.blackButton.grid(row=0,column=1)

		self.neButton = tk.Button(self.fillbuttons, text='//', command=self.pickNE)
		self.neButton.grid(row=0, column=2)

		self.nwButton = tk.Button(self.fillbuttons, text='\\\\', command=self.pickNW)
		self.nwButton.grid(row=0, column=3)

		self.dotsButton = tk.Button(self.fillbuttons, text='::', command=self.pickDots)
		self.dotsButton.grid(row=0, column=4)

		# Line weight buttons
		self.weightbuttons = tk.Frame(self)
		self.weightbuttons.grid()

		self.thinButton = tk.Button(self.weightbuttons, relief=tk.SUNKEN, text='thin', command=self.pickThin)
		self.thinButton.grid(row=0,column=0)

		self.thickButton = tk.Button(self.weightbuttons,  text='thick', command=self.pickThick)
		self.thickButton.grid(row=0,column=1)

		self.vtButton = tk.Button(self.weightbuttons, text='very thick', command=self.pickVT)
		self.vtButton.grid(row=0,column=2)

		self.utButton = tk.Button(self.weightbuttons, text='ultra thick', command=self.pickUT)
		self.utButton.grid(row=0,column=3)

		self.sep = ttk.Separator(self)
		self.sep.grid(pady=10, sticky=tk.E+tk.W)

		self.canvas = tk.Canvas(self, height='3i', width='5i')
		self.canvas.grid()

		self.codeWindow = tk.Text(self)
		self.codeWindow.grid()


		self.drawingProgram()

	def drawingProgram(self):
		canvas = self.canvas
		canvas.bind('<ButtonPress-1>', self.onPress)
		canvas.bind('<ButtonRelease-1>', self.onRelease)

	def tikz(self):
		self.codeWindow.delete('1.0','end')
		code = self.parseTikz()
		self.codeWindow.insert('1.0',code)

	# Selecting tool

	def disableAll(self):
		self.lineButton.config(relief = tk.RAISED)
		self.rectButton.config(relief = tk.RAISED)
		self.circButton.config(relief = tk.RAISED)
		self.textButton.config(relief = tk.RAISED)
	def pickLine(self):
		self.disableAll()
		self.lineButton.config(relief = tk.SUNKEN)
		self.activeTool='line'
	def pickRect(self):
		self.disableAll()
		self.rectButton.config(relief = tk.SUNKEN)
		self.activeTool='rectangle'
	def pickCirc(self):
		self.disableAll()
		self.circButton.config(relief = tk.SUNKEN)
		self.activeTool='circle'
	def pickText(self):
		self.disableAll()
		self.textButton.config(relief = tk.SUNKEN)
		self.activeTool='text'

	# Selecting line style
	def disableLines(self):
		self.reglineButton.config(relief = tk.RAISED)
		self.dotlineButton.config(relief = tk.RAISED)
		self.rarrowButton.config(relief = tk.RAISED)
		self.larrowButton.config(relief = tk.RAISED)
	def pickRegLine(self):
		self.disableLines()
		self.reglineButton.config(relief = tk.SUNKEN)
		self.activeLine='reg'
	def pickDotLine(self):
		self.disableLines()
		self.dotlineButton.config(relief = tk.SUNKEN)
		self.activeLine='dot'
	def pickRArrow(self):
		self.disableLines()
		self.rarrowButton.config(relief = tk.SUNKEN)
		self.activeLine='rarrow'
	def pickLArrow(self):
		self.disableLines()
		self.larrowButton.config(relief = tk.SUNKEN)
		self.activeLine='larrow'

	# Selecting pattern style
	def disablePatterns(self):
		self.blackButton.config(relief = tk.RAISED)
		self.neButton.config(relief = tk.RAISED)
		self.nwButton.config(relief = tk.RAISED)
		self.dotsButton.config(relief = tk.RAISED)
		self.whiteButton.config(relief = tk.RAISED)
	def pickSolid(self):
		self.disablePatterns()
		self.blackButton.config(relief = tk.SUNKEN)
		self.activePattern = 'solid'
	def pickNE(self):
		self.disablePatterns()
		self.neButton.config(relief = tk.SUNKEN)
		self.activePattern = 'ne'
	def pickNW(self):
		self.disablePatterns()
		self.nwButton.config(relief = tk.SUNKEN)
		self.activePattern = 'nw'
	def pickDots(self):
		self.disablePatterns()
		self.dotsButton.config(relief = tk.SUNKEN)
		self.activePattern = 'dots'
	def pickEmpty(self):
		self.disablePatterns()
		self.whiteButton.config(relief = tk.SUNKEN)
		self.activePattern = 'empty'    	

	# Selecting thickness
	def disableWeights(self):
		self.thinButton.config(relief = tk.RAISED)
		self.thickButton.config(relief = tk.RAISED)
		self.vtButton.config(relief = tk.RAISED)
		self.utButton.config(relief = tk.RAISED)
	def pickThin(self):
		self.disableWeights()
		self.thinButton.config(relief = tk.SUNKEN)
		self.activeWeight = 'thin'
	def pickThick(self):
		self.disableWeights()
		self.thickButton.config(relief = tk.SUNKEN)
		self.activeWeight = 'thick'
	def pickVT(self):
		self.disableWeights()
		self.vtButton.config(relief = tk.SUNKEN)
		self.activeWeight = 'vt'
	def pickUT(self):
		self.disableWeights()
		self.utButton.config(relief = tk.SUNKEN)
		self.activeWeight = 'ut'

	# What to do upon pressing canvas
	def onPress(self, event):
		if self.activeTool == 'line':
			self.line('press', event)
		elif self.activeTool == 'rectangle':
			self.rectangle('press', event)
		elif self.activeTool == 'circle':
			self.circle('press', event)
		elif self.activeTool == 'text':
			self.text(event)
		else:
			pass
	def onRelease(self, event):
		if self.activeTool == 'line':
			self.line('release', event)
		elif self.activeTool == 'rectangle':
			self.rectangle('release', event)
		elif self.activeTool == 'circle':
			self.circle('release', event)
		else:
			pass

	# Drawing tools
	def line(self, state, event):
		if state=='press':
			self.points = [event.x, event.y]
		elif state == 'release':
			self.points += [event.x, event.y]
			event.widget.create_line(self.points[0], self.points[1], self.points[2], self.points[3], smooth=True)
			self.objects['line']+= [self.points[:] + [self.weightstrings[self.activeWeight]]+['']+[self.linestrings[self.activeLine]]]

	def rectangle(self, state, event):
		if state=='press':
			self.points = [event.x, event.y]
		elif state == 'release':
			self.points += [event.x, event.y]
			event.widget.create_rectangle(self.points[0], self.points[1], self.points[2], self.points[3])
			self.objects['rectangle']+= [self.points[:] + [self.weightstrings[self.activeWeight]]+ [self.fillstrings[self.activePattern]]+[self.linestrings[self.activeLine]]]

	def circle(self, state, event):
		if state=='press':
			self.points = [event.x, event.y]
		elif state == 'release':
			center = self.points[:]
			radius = math.sqrt((event.x - self.points[0])**2 +  (event.y - self.points[1])**2)
			self.points = [self.points[0] - radius, self.points[1] - radius, self.points[0] + radius, self.points[1]+radius]
			event.widget.create_oval(self.points[0], self.points[1], self.points[2], self.points[3])
			self.objects['circle']+= [[center[0], center[1], radius] + [self.weightstrings[self.activeWeight]]+ [self.fillstrings[self.activePattern]]+ [self.linestrings[self.activeLine]]]

	def text(self, event):
		popup = tk.Toplevel()
		popup.title('enter text!')
		popup.transient()
		def putText(*args):
			txt = field.get()
			self.objects['text']+= [[event.x, event.y, txt]]
			self.canvas.create_text(event.x, event.y, text=txt)  
			popup.destroy()
		submitButton = tk.Button(popup, text='OK', command = putText)
		field = tk.Entry(popup)
		field.grid()
		submitButton.grid()
		field.focus_set()
		field.bind('<Return>', putText)

	# Tikz parser
	def parseTikz(self):
		code = '\\begin{tikzpicture}[scale=0.02]\n'

		code += self.parseLines()
		code += self.parseRectangles()
		code += self.parseCircles()
		code += self.parseText()

		code += '\\end{tikzpicture}'
		return code

	def parseLines(self):
		output = ''
		for line in self.objects['line']:
			thisline = '\t\\draw['+line[-3]+ ','+line[-2]+','+line[-1]+']( '+str(line[0])+' , '+str(-line[1])+' ) -- ( '+str(line[2])+' , '+str(-line[3])+' );\n'
			output += thisline
		return output
	def parseRectangles(self):
		output = ''
		for line in self.objects['rectangle']:
			thisrect = '\t\\draw[' +line[-3]+','+line[-2]+',' + line[-1]+'] ( '+str(line[0])+' , '+str(-line[1])+' ) rectangle ( '+str(line[2])+' , '+str(-line[3])+' );\n'
			output += thisrect
		return output
	def parseCircles(self):
		output = ''
		for line in self.objects['circle']:
			thiscirc = '\t\\draw[' +line[-3]+','+line[-2]+',' + line[-1]+'] ( '+str(line[0])+' , '+str(-line[1])+' ) circle ( '+str(line[2])+' );\n'
			output += thiscirc
		return output
	def parseText(self):
		output = ''
		for line in self.objects['text']:
			thistext = '\t\\draw ( '+ str(line[0]) + ' , ' + str(-line[1]) + ' ) node {' +line[2] + '};\n'
			output += thistext
		return output

	# Tikz compiler
	def compile(self):
		code = self.codeWindow.get('1.0','end')
		self.canvas.delete('all')
		lines = code.split('\n')
		self.objects = {'line':[], 'circle':[], 'rectangle':[], 'text':[]}
		for line in lines:
			options = line.split('[')[-1].split(']')[0].split(',');
			numbers = [float(s) for s in line.split(' ') if isanumber(s)]
			if '\\draw' in line:
				if 'rectangle' in line:
					coords = [numbers[0], -numbers[1], numbers[2], -numbers[3]] + options
					self.canvas.create_rectangle(numbers[0], -numbers[1], numbers[2], -numbers[3])
					self.objects['rectangle']+= [coords]
				elif 'circle' in line:
					coords = [numbers[0], -numbers[1], numbers[2]] + options
					tlc = [numbers[0] - numbers[2], -numbers[1] - numbers[2]]
					brc = [numbers[0] + numbers[2], -numbers[1] + numbers[2]]

					self.canvas.create_oval(tlc[0], tlc[1], brc[0], brc[1])
					self.objects['circle'] += [coords]
				elif 'node' in line:
					text = line.split('{')[1].split('}')[0]
					coords = [numbers[0], -numbers[1], text]
					self.canvas.create_text(coords[0], coords[1], text=text)
					self.objects['text'] += [coords]
				else:
					coords = [numbers[0], -numbers[1], numbers[2], -numbers[3]] + options
					self.canvas.create_line(numbers[0], -numbers[1], numbers[2], -numbers[3])
					self.objects['line']+= [coords]

  #   def parseLines(self, lines):
  #   	#for line in lines:#thisline = '\t\\draw ('+str(line[0])+' , '+str(line[1])+') -- ('+str(line[2])+' , '+str(line[3])+');'
		# #	print thisline
		# #	output += thisline
		# return output

def isanumber(num):
	try:
		float(num)
		return True
	except ValueError:
		return False
app = Application()
app.master.title('Super Minimal tikz GUI!')
app.mainloop()