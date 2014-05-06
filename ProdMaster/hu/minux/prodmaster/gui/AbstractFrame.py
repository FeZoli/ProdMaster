'''
Created on 2014.03.05.

@author: fekete
'''

import tkinter.messagebox as mbox
from tkinter import END
from tkinter.constants import *
from tkinter import TclError
from tkinter.ttk import *
from builtins import NotImplemented

from hu.minux.prodmaster.tools.World import World
from hu.minux.prodmaster.gui.QuestionDialog import QuestionDialog


class AbstractFrame(Frame):

    _instance = None
    _myTabId = 0
    _myElementId = 0
    _myEntity = None
    _myType = 'Not Implemented'
    _myApplication = None
    _myListBox = None
    _myStoredListItems = None
    _myState = None
    answer = None


    def __init__(self, master, appFrame, elementId=0):
        Frame.__init__(self, master, padding= World.padSize())
        World().LOG().info("Frame called: " + self._myType)
        self._myApplication = appFrame
        self._myElementId = elementId
        self._myListBox = self._myApplication.getListBox()
        self._myListBox.bind('<<ListboxSelect>>', self.refreshDetails)
        self._createWidgets()
        self._fillListWithElements()
        self._displayElement(elementId) 
        self._setControls()
       
        
    def _cancel(self):
        self._myApplication.saveButtonEnabled(False)
        self._myApplication.cancelButtonEnabled(False)
        self._displayElement(self._myElementId)

    
    def _close(self):
        self._myListBox.delete(0, END)
        self.master.forget('current')
        if self.master.index('end') > 0:
            self.master.select('end')
        else:
            self._myApplication.closeButtonEnabled(False)

    def _createWidgets(self):
        raise NotImplemented

    
    def _displayElement(self, elementId):
        self.answer = ''
        if self._getState() == 'normal' and elementId != self._myElementId:
            self._handleChangeWhileInEditMode()
            
        if self.answer != 'ABORT':
            self._myElementId = elementId

        idx = 0    
        if self._myElementId == 0:
            idx = 0
        else:
            for item in self._myStoredListItems:
                if item.id == self._myElementId:
                    break
                idx += 1
    
        if self.answer != 'ABORT':
            self._setState(self, 'normal')
            self.showItem(self._myStoredListItems[idx].id)
            self._setState(self, 'disabled')

        self._myListBox.selection_clear(0, END)        
        self._myListBox.selection_set(idx)
        
        
    def _edit(self):
        self._setState(self, 'normal')
        self._myApplication.saveButtonEnabled(True)
        self._myApplication.cancelButtonEnabled(True)
        
        
    def _getState(self):
        return self._myState
        
    
    def _setState(self, widget, state='disabled'):
        if widget.winfo_class() == 'TLabel':
            return
        try:
            widget.configure(state=state)
            print(widget.winfo_class())
        except TclError:
            pass
        for child in widget.winfo_children():
            if child.winfo_class() == 'TEntry' or child.winfo_class() == 'Text':
                child.configure(state=state)
                if  child.winfo_class() == 'Text':
                    if state == 'disabled':
                        child.configure(background=World.getDisabledBackgroundColor())
                        child.configure(foreground=World.getDisabledForegroundColor())
                    else:
                        child.configure(background=World.getNormalBackgroundColor())
                        child.configure(foreground=World.getNormalForegroundColor())
                        
        self._myState = state

    
    def _fillListWithElements(self):
        self._myStoredListItems = self._myEntity.getListItems()
        for e in self._myStoredListItems:
            self._myListBox.insert(END, e.name)        
        
        self._myApplication.editButtonEnabled(True)
        self._myApplication.closeButtonEnabled(True)
        
        
    def _handleChangeWhileInEditMode(self):
        QuestionDialog(self,
                           title=World.L('QUESTION'),
                           message=World.L('AbstractFrame.ARC'),
                           cancelLabel=World.L('PROCEED_NO_SAVE'))
        if self.answer == 'SAVE':
            self._save()
        
        
    def _save(self):
        raise NotImplemented
        
        
    def _setControls(self):
        self._myApplication.closeButton.config(command=self._close)
        self._myApplication.cancelButton.config(command=self._cancel)
        self._myApplication.saveButton.config(command=self._save)
        self._myApplication.editButton.config(command=self._edit)        
        
            
    def refreshDetails(self, params):
        selectedIdx = int(self._myListBox.curselection()[0])
        self._displayElement(self._myStoredListItems[selectedIdx].id)
    
        
    def showItem(self, elementId):
        raise NotImplemented
        
        
    @staticmethod    
    def getInstance(master):
        raise NotImplemented
            