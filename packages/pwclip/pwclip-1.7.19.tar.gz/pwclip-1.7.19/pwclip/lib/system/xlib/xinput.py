"""xinput window"""
# -*- encoding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
#
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
from os import name as osname

try:
	from tkinter import StringVar, Button, Entry, Frame, Label, Tk, TclError
except ImportError:
	try:
		from Tkinter import StringVar, Button, Entry, Frame, Label, Tk, TclError
	except ModuleNotFoundError:
		class StringVar(object): pass
		class TclError(object): pass
		class Button(object): pass
		class Entry(object): pass
		class Frame(object): pass
		class Label(object): pass
		class Tk(object): pass
try:
	import readline
except ImportError:
	pass

from colortext import abort


class XInput(Frame):
	"""password clipping class for tkinter.Frame"""
	inp = None
	def __init__(self, root, message, exchange='', noop=None, noin=None):
		self.noop = noop
		self.noin = noin
		self.exchg = exchange
		self.message = message
		self.root = root
		self.input = None
		#self.root.after(1, lambda: self.root.focus_force())
		#self.root.after(1, lambda: self.root.
		Frame.__init__(self, root)
		self.pack()
		self.inputwindow()
	@staticmethod
	def setfocus(root, noop=None, noin=None):
		if osname == 'nt':
			root.after(1, lambda: root.focus_force())
	def _enterexit(self, _=None):
		"""exit by saving challenge-response for input"""
		self.inp = True if not self.input else self.input.get()
		self.quit()
	def _okexit(self, _=None):
		"""exit by saving challenge-response for input"""
		self.inp = True
		self.quit()
	def _exit(self, _=None):
		"""just exit (for ESC mainly)"""
		self.inp = False
		self.quit()
	def inputwindow(self):
		"""password input window creator"""
		self.lbl = Label(self, text=self.message)
		self.lbl.pack()
		okside = {}
		clside = {}
		self.root.bind("<Control-c>", self._exit)
		self.root.bind("<Escape>", self._exit)
		self.root.bind("<Return>", self._enterexit)
		self.ok = Button(self)
		self.ok.bind("<Control-c>", self._exit)
		self.ok.bind("<Escape>", self._exit)
		self.ok.bind("<Return>", self._enterexit)
		self.ok["text"] = "OK"
		self.ok["command"] =  self._okexit
		okside = {'side': 'bottom'}
		if not self.noin:
			self.input = StringVar()
			self.entry = Entry(self, show=self.exchg)
			self.entry.bind("<Return>", self._enterexit)
			self.entry.bind("<Control-c>", self._exit)
			self.entry.bind("<Escape>", self._exit)
			self.entry["textvariable"] = self.input
			self.entry.pack()
			okside = {'side': 'left'}
		if not self.noop:
			self.cl = Button(self)
			self.cl.bind("<Return>", self._exit)
			self.cl.bind("<Control-c>", self._exit)
			self.cl.bind("<Escape>", self._exit)
			self.cl["text"] = "Cancel"
			self.cl["command"] = self._exit
			self.cl.pack({'side': 'right'})
			okside = {'side': 'left'}
		self.ok.pack(okside)
		self.setfocus(self.root)
		if self.noin or self.noop:
			self.ok.focus_set()
		else:
			self.entry.focus_set()


def xinput(message='enter input'):
	"""x screen input window"""
	try:
		root = Tk()
		pwc = XInput(root, message, None)
		pwc.lift()
		pwc.mainloop()
	except KeyboardInterrupt:
		root.destroy()
		raise KeyboardInterrupt
	try:
		root.destroy()
	except:
		pass
	finally:
		return pwc.inp

def xgetpass(message="input will not be displayed"):
	"""gui representing function"""
	try:
		root = Tk()
		pwc = XInput(root, message, exchange='*')
		pwc.setfocus(root)
		pwc.lift()
		pwc.mainloop()
	except KeyboardInterrupt:
		root.destroy()
		raise KeyboardInterrupt
	try:
		root.destroy()
	except:
		pass
	finally:
		return pwc.inp

def xmsgok(message='press ok to continue'):
	"""gui representing function"""
	try:
		root = Tk()
		pwc = XInput(root, message, noop=True, noin=True)
		pwc.setfocus(root)
		pwc.lift()
		pwc.mainloop()
	except KeyboardInterrupt:
		root.destroy()
		raise KeyboardInterrupt
	try:
		root.destroy()
	except:
		pass

def xyesno(message='press ok to continue'):
	"""gui representing function"""
	try:
		root = Tk()
		pwc = XInput(root, message, noin=True)
		pwc.setfocus(root)
		pwc.lift()
		pwc.mainloop()
	except KeyboardInterrupt:
		root.destroy()
		raise KeyboardInterrupt
	try:
		root.destroy()
	except:
		pass
	finally:
		return pwc.inp


if __name__ == '__main__':
	exit(1)
