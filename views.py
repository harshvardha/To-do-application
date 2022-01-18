import tkinter
from task import Task
from databaseManager import DatabaseManager
class TaskCard(tkinter.Frame):

    # This class represents the structure of the information card of the task

    def __init__(self, parent, cardInformationObject: Task, rootWindowObject, **kwargs):
        super().__init__(master = parent, **kwargs)
        self.parent = parent
        self.rootWindowObject = rootWindowObject
        self.cardInformationObject = cardInformationObject
        self.columnconfigure(0, weight = 1)
        self._labels = {}
        self._buttons = {}
        self.createCard()
    
    def createCard(self):

        # This function assembles the labels showing information about the task on the card

        # This is the dictionary of label properties
        labelProperties = {
            "font" : ("Comic Sans MS", 13, "bold"),
            "bg" : "#ffffff"
        }

        # This is the dictionary of button properties
        buttonProperties = {
            "width" : 20,
            "bg" : "#ECECEC",
            "fg" : "#707070",
            "bd" : 0,
            "font" : ("Comic Sans MS", 13, "bold")
        }

        # Now creating the labels dictionary
        self._labels = {
            "task name" : tkinter.Label(master = self, text = "Task name : " + self.cardInformationObject.getTaskName(), **labelProperties),
            "starting date" : tkinter.Label(master = self, text = "Starting date : " + self.cardInformationObject.getTaskStartingDate(), **labelProperties),
            "ending date" : tkinter.Label(master = self, text = "Ending date : " + self.cardInformationObject.getTaskEndingDate(), **labelProperties),
            "task description" : tkinter.Label(master = self, text = "Task description : " + self.cardInformationObject.getTaskDescription(), wraplength = 800, justify = tkinter.LEFT, **labelProperties)
        }

        # Now creating the buttons dictionary
        buttonsFrame = tkinter.Frame(master = self, bg = "#FFFFFF")
        buttonsFrame.columnconfigure(0, weight = 1)
        buttonsFrame.grid(column = 0, row = 4)
        self._buttons = {
            "update task" : tkinter.Button(master = buttonsFrame, text = "Update Task", command = self._updateLabels, **buttonProperties),
            "task completed" : tkinter.Button(master = buttonsFrame, text = "Task Completed", command = self._deleteTask, **buttonProperties)
        }

        # This row variable represents the row number and will be incremented after placement of every label widget
        rowNumber = 0
        
        # This column variable represents the column number of the buttonsFrame
        columnNumber = 0

        # Now assembling the labels
        for key in self._labels.keys():
            self._labels[key].grid(column = 0, row = rowNumber, sticky = tkinter.W)
            rowNumber += 1
        rowNumber = 0
        
        # Now assembling the buttons
        for key in self._buttons.keys():
            self._buttons[key].grid(column = columnNumber, row = rowNumber, padx = 20, pady = 20)
            columnNumber += 1
    
    def _updateLabels(self):
        TaskInformationDialogBox(self.parent, "#ffffff", "Update task", self.cardInformationObject, "UPDATE TASK")
        update = ""
        for key in self._labels.keys():
            if(key == "task name"):
                update = self.cardInformationObject.getTaskName()
            elif(key == "starting date"):
                update = self.cardInformationObject.getTaskStartingDate()
            elif(key == "ending date"):
                update = self.cardInformationObject.getTaskEndingDate()
            elif(key == "task description"):
                update = self.cardInformationObject.getTaskDescription()
            self._labels[key].configure(text = key.title() + " : " + update)
            
    
    def _deleteTask(self):
        self.rootWindowObject.deleteTaskObject(self.cardInformationObject.getTaskIdentityNumber())
        del self.cardInformationObject
        self.destroy()

class ScrollingFrame(tkinter.Frame):
    
    # This creates a scrollable frame
    def __init__(self, parent, background: str):
        super().__init__(master = parent, bg = background, bd = 0)
        self.parent = parent
        self.background = background
        self.widgetContainerFrame: tkinter.Frame
        self.canvas: tkinter.Canvas
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0,weight = 1)
        self.buildScrollingFrame()
    
    def buildScrollingFrame(self):
        # creating a canvas which will be scrolled
        self.canvas = tkinter.Canvas(master = self, bg = self.background, bd = 0)
        self.canvas.columnconfigure(0, weight = 1)
        self.canvas.grid(column = 0, row = 0, sticky = (tkinter.N, tkinter.S, tkinter.W, tkinter.E))

        # creating a scrollbar which will be used to scroll the canvas
        scrollBar = tkinter.Scrollbar(master = self, orient = tkinter.VERTICAL, command = self.canvas.yview)
        scrollBar.grid(column = 1, row = 0, sticky = (tkinter.E, tkinter.S, tkinter.N))

        # configuring the canvas so that it can scroll when it is scrolled
        self.canvas.configure(yscrollcommand = scrollBar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        self.canvas.bind("<MouseWheel>", self.onMouseWheel)

        # creating another frame inside the canvas which will contain the widgets which are not scrollable
        # to make them scrollable
        self.widgetContainerFrame = tkinter.Frame(master = self.canvas, bg = self.background)
        self.widgetContainerFrame.columnconfigure(0, weight = 1)
        # Now adding the widgetContainerFrame to a new window in canvas
        self.canvas.create_window((0, 0), window = self.widgetContainerFrame, anchor = "nw")
    
    def getWidgetContainerFrame(self) -> tkinter.Frame:
        return self.widgetContainerFrame
    
    def onMouseWheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120),"units")

class MainWindow(tkinter.Tk):

    # This class represents the main ui window where all the tasks will be displayed in their respective cards

    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        self.title("To do App")
        self.configure(bg = "#FAFAFA")
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self._taskRowNumber = 0
        self._rowNumber = 0
        self._labelsDictionary = {}
        self._buttonsDictionary = {}
        self._taskObjects = {}
        self.scrollableFrame = ScrollingFrame(self, "#FAFAFA")
        self.scrollableFrame.grid(column = 0, row = 0, sticky = (tkinter.N, tkinter.S, tkinter.W, tkinter.E))
        if(not self.checkDatabase()):
            self.assembleTaskCards()
            self._rowNumber = 1
        else:
            self._createLabels()
        self._createButtons()
    
    def checkDatabase(self):

        # This function will check whether the database is empty or not
        # if the database is empty then the welcome label will be created
        # otherwise all the taskcards will be assembled
        dbObject = DatabaseManager("todo_list_database.db")
        isEmpty: bool
        if(not dbObject.isEmpty()):
            isEmpty = False
        else:
            isEmpty = True
        dbObject.closeDatabaseConnection()
        return isEmpty
    
    def assembleTaskCards(self):
        dbObject = DatabaseManager("todo_list_database.db")
        taskList = dbObject.readFromTable()
        cardProperties = {
            "bg" : "#ffffff"
        }
        for task in taskList:
            taskObject = Task(
                identityNumber = task[0],
                taskName = task[1],
                taskStartingDate = task[2],
                taskEndingDate = task[3],
                taskDescription = task[4]
            )
            self._taskObjects[taskObject.getTaskIdentityNumber()] = taskObject
            taskCardObject = TaskCard(
                parent = self.scrollableFrame.getWidgetContainerFrame(),
                cardInformationObject = taskObject,
                rootWindowObject = self,
                **cardProperties
            )
            taskCardObject.grid(column = 0, row = self._taskRowNumber, sticky = (tkinter.N, tkinter.W, tkinter.E), padx = 20, pady = 20)
            self._taskRowNumber += 1
        dbObject.closeDatabaseConnection()
    
    def _createLabels(self):
        labelsProperties = {
            "font" : ("Comic Sans MS", 15, "bold"),
            "fg" : "#ACACAC",
            "bg" : "#FAFAFA",
            "bd" : 0
        }

        # creating the labels
        self._labelsDictionary = {
            "welcome label" : tkinter.Label(master = self, text = "Welcome to your task planner", **labelsProperties)
        }

        # assembling the labels
        for key in self._labelsDictionary.keys():
            self._labelsDictionary[key].grid(column = 0, row = self._rowNumber)
            self._rowNumber += 1
        
    def _createButtons(self):
        buttonsProperties = {
            "width" : 10,
            "bg" : "#ECECEC",
            "fg" : "#ACACAC",
            "bd" : 0,
            "font" : ("Comic Sans MS", 13, "bold")
        }

        # creating the buttons
        self._buttonsDictionary = {
            "add task" : tkinter.Button(master = self, text = "Add Task", command = self.createCard,**buttonsProperties)
        }

        # assembling the buttons
        for key in self._buttonsDictionary.keys():
            self._buttonsDictionary[key].grid(column = 0, row = self._rowNumber, sticky = tkinter.N, pady = 15)
            self._rowNumber += 1
    
    def createCard(self):
        taskObject = Task()
        TaskInformationDialogBox(self, "#ffffff", "Fill task details", taskObject, "SAVE TASK")
        cardProperties = {
            "bg" : "#ffffff"
        }
        if(not taskObject.isEmpty()):
            self._taskObjects[taskObject.getTaskIdentityNumber()] = taskObject
            task = TaskCard(parent = self.scrollableFrame.getWidgetContainerFrame(), cardInformationObject = taskObject, rootWindowObject = self, **cardProperties)
            if(len(self._labelsDictionary) > 0):
                self._labelsDictionary["welcome label"].destroy()
            task.grid(column = 0, row = self._taskRowNumber, sticky = (tkinter.N, tkinter.W, tkinter.E), padx = 20, pady = 20)
            self._taskRowNumber += 1
        else:
            del taskObject
    
    def deleteTaskObject(self, taskId):
        if(taskId in self._taskObjects):
            del self._taskObjects[taskId]
            dbObject = DatabaseManager("todo_list_database.db")
            dbObject.deleteTask(taskId)
            dbObject.closeDatabaseConnection()

class TaskInformationDialogBox(tkinter.Toplevel):

    def __init__(self, parent, background, dialogTitle, taskObj, buttonText):
        super().__init__(parent, width = 50, height = 50, bg = background)
        self.taskObject = taskObj
        self.parent = parent
        self.buttonText = buttonText
        self.title(dialogTitle)
        self.geometry("449x473")
        self.transient(parent)
        self.resizable(width = False, height = False)
        self.grab_set()
        self.columnconfigure(0, weight = 1)
        self._widgets = {}
        for i in range(5):
            self.rowconfigure(i, weight = 1)
        self._createUI()
        self.focus_set()
        self.wait_window()
    
    def _createUI(self):

        # creating dictionaries of properties of different widgets used
        frameProperties = {
            "bg" : "#ffffff"
        }
        labelWidgetsProperties = {
            "bg" : "#ffffff",
            "fg" : "#4E4343",
            "font" : ("Comic Sans MS", 15, "bold"),
        }
        textWidgetsProperties = {
            "width" : 40,
            "bg" : "#ffffff",
            "fg" : "#3A3333",
            "font" : ("Comic Sans MS", 14, "bold"),
            "bd" : 1,
            "highlightbackground" : "#707070"
        }
        buttonWidgetProperties = {
            "text" : self.buttonText,
            "bg" : "#ECECEC",
            "fg" : "#4E4343",
            "bd" : 0,
            "font" : ("Comic Sans MS", 15, "bold")
        }

        # creating frames dictionary for the container frames
        frames = {
            "taskName" : tkinter.Frame(master = self, **frameProperties),
            "startingDate" : tkinter.Frame(master = self, **frameProperties),
            "endingDate" : tkinter.Frame(master = self, **frameProperties),
            "taskDescription" : tkinter.Frame(master = self, **frameProperties)
        }

        # creating label and edit text widgets for respective frames
        self._widgets = {
            "taskNameWidgets" : {
                "Label" : tkinter.Label(master = frames["taskName"], text = "Task Name", **labelWidgetsProperties),
                "EditText" : tkinter.Entry(master = frames["taskName"], **textWidgetsProperties)
            },
            "startingDateWidgets" : {
                "Label" : tkinter.Label(master = frames["startingDate"], text = "Starting Date", **labelWidgetsProperties),
                "EditText" : tkinter.Entry(master = frames["startingDate"], **textWidgetsProperties)
            },
            "endingDateWidgets" : {
                "Label" : tkinter.Label(master = frames["endingDate"], text = "Ending Date", **labelWidgetsProperties),
                "EditText" : tkinter.Entry(master = frames["endingDate"], **textWidgetsProperties)
            },
            "taskDescriptionWidgets" : {
                "Label" : tkinter.Label(master = frames["taskDescription"], text = "Task Description", **labelWidgetsProperties),
                "EditText" : tkinter.Text(master = frames["taskDescription"], height = 5, **textWidgetsProperties)
            },
            "saveAndUpdateWidget" : {
                "Button" : tkinter.Button(master = self, **buttonWidgetProperties)
            }
        }

        # binding the dialog box to the events of escape key and return key and giving command option to button widget
        self.bind("<Escape>", self._cancel)
        if(self.buttonText == "SAVE TASK"):
            self._widgets["saveAndUpdateWidget"]["Button"].configure(command = self._collectTaskInformation)
            self.bind("<Return>", self._collectTaskInformation)
        elif(self.buttonText == "UPDATE TASK"):
            for key in self._widgets.keys():
                if("Button" not in self._widgets[key]):
                    if(key == "taskNameWidgets"):
                        self._widgets[key]["EditText"].insert(tkinter.END, self.taskObject.getTaskName())
                    elif(key == "startingDateWidgets"):
                        self._widgets[key]["EditText"].insert(tkinter.END, self.taskObject.getTaskStartingDate())
                    elif(key == "endingDateWidgets"):
                        self._widgets[key]["EditText"].insert(tkinter.END, self.taskObject.getTaskEndingDate())
                    elif(key == "taskDescriptionWidgets"):
                        self._widgets[key]["EditText"].insert(tkinter.END, self.taskObject.getTaskDescription())
            self._widgets["saveAndUpdateWidget"]["Button"].configure(command = self._collectUpdatedTaskInformation)
            self.bind("<Return>", self._collectUpdatedTaskInformation)

        # Now assembling each frame and their widgets
        for i, key in enumerate(frames.keys()):
            frames[key].columnconfigure(0, weight = 1)
            frames[key].rowconfigure(0, weight = 1)
            frames[key].rowconfigure(1, weight = 1)
            frames[key].grid(column = 0, row = i, sticky = (tkinter.W, tkinter.S), padx = 20)

        for key in self._widgets.keys():
            if("Button" not in self._widgets[key]):
                self._widgets[key]["Label"].grid(column = 0, row = 0, sticky = (tkinter.W, tkinter.S))
                self._widgets[key]["EditText"].grid(column = 0, row = 1, sticky = (tkinter.W, tkinter.S))
            else:
                self._widgets[key]["Button"].grid(column = 0, row = 4, sticky = tkinter.E, padx = 20)
    
    # function for save task dialog box which will be invoked when save task button will be clicked
    def _collectTaskInformation(self, event = None):
        taskInformation = {}
        for key in self._widgets.keys():
            if("Button" not in self._widgets[key]):
                if(key != "taskDescriptionWidgets"):
                    info = self._widgets[key]["EditText"].get()
                else:
                    info = self._widgets[key]["EditText"].get("1.0", "end-2c")
                if(len(info) > 0):
                    taskInformation[self._widgets[key]["Label"].cget("text")] = info
                else:
                    break
        if(len(taskInformation) == 4):
            dbObject = DatabaseManager("todo_list_database.db")
            dbObject.insertIntoTable(taskInformation)
            self.taskObject.setTaskIdentityNumber(dbObject.getRecentlyAddedTaskId())
            self.taskObject.setTaskName(taskInformation["Task Name"])
            self.taskObject.setTaskStartingDate(taskInformation["Starting Date"])
            self.taskObject.setTaskEndingDate(taskInformation["Ending Date"])
            self.taskObject.setTaskDescription(taskInformation["Task Description"])
            dbObject.closeDatabaseConnection()
            self._cancel(event)

    # function for update task dialog box which will be invoked when update task button will be clicked
    def _collectUpdatedTaskInformation(self, event = None):
        update = ""
        updatedFields = {}
        for key in self._widgets.keys():
            if("Button" not in self._widgets[key]):
                if(key != "taskDescriptionWidgets"):
                    update = self._widgets[key]["EditText"].get()
                else:
                    update = self._widgets[key]["EditText"].get("1.0", "end-1c")
                if(len(update) > 0):
                    if(key == "taskNameWidgets" and self.taskObject.getTaskName() != update):
                        self.taskObject.setTaskName(update)
                        updatedFields["taskName"] = update
                    elif(key == "startingDateWidgets" and self.taskObject.getTaskStartingDate() != update):
                        self.taskObject.setTaskStartingDate(update)
                        updatedFields["taskStartingDate"] = update
                    elif(key == "endingDateWidgets" and self.taskObject.getTaskEndingDate() != update):
                        self.taskObject.setTaskEndingDate(update)
                        updatedFields["taskEndingDate"] = update
                    elif(key == "taskDescriptionWidgets" and self.taskObject.getTaskDescription() != update):
                        self.taskObject.setTaskDescription(update)
                        updatedFields["taskDescription"] = update
                else:
                    break
        if(len(update) > 0):
            updatedFields["id"] = self.taskObject.getTaskIdentityNumber()
            dbObject = DatabaseManager("todo_list_database.db")
            dbObject.updateTable(updatedFields)
            dbObject.closeDatabaseConnection()
            self._cancel(event)

    # This function is invoked whenver the dialog box has to be destroyed
    def _cancel(self, event):
        self.withdraw()
        self.update_idletasks()
        self.parent.focus_set()
        self.destroy()

if __name__ == "__main__":
    MainWindow().mainloop()