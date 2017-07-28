import wx
import wx.xrc
import re
import time
from tzlocal import get_localzone
from datetime import datetime
from jira import JIRA, JIRAError
import threading
from confg import *
from wx.lib.embeddedimage import PyEmbeddedImage
icon_32 = PyEmbeddedImage(
    "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"
    "gZGcaQAAAABJRU5ErkJggg==")

CFG = read_config()

EVT_LOGIN = wx.NewEventType()
EVT_LOGIN_DONE = wx.PyEventBinder(EVT_LOGIN, 1)
EVT_LOGWORK = wx.NewEventType()
EVT_LOGWORK_DONE = wx.PyEventBinder(EVT_LOGWORK, 1)

# Converters
def started2str(startedTime):
    """Takes started time in seconds since the epoch and returns string in "%H:%M %d.%m.%Y" format"""
    if startedTime == -1:
        return u"--:-- --.--.----"
    else:
        return time.strftime("%H:%M  %d.%m.%Y", time.localtime(startedTime))
def time_spent2str(timeSpentS):
    """Takes time spent in seconds and returns string in "HH:MM:SS" format"""
    return "{0:0>2}:{1:0>2}:{2:0>2}".format(timeSpentS / 3600, (timeSpentS%3600) / 60, timeSpentS % 60)

class AddIssueEvent(wx.PyCommandEvent):
    """Event to signal that login is done"""
    def __init__(self, etype, eid):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)

class AddIssueThread(threading.Thread):
    def __init__(self, parent, issueID):
        threading.Thread.__init__(self)
        self._parent = parent
        self._issueID = issueID

    def run(self):
        if self._parent.jira is None:
            self._parent.m_statusBar.SetStatusText("Connecting to JIRA...", 0)
            self._parent.m_statusBar.SetStatusText("", 1)
            self._parent.m_statusBar.SetStatusText("", 2)
            try:
                self._parent.jira = JIRA(server="https://jira.wargaming.net", basic_auth=(CFG["login"], self._parent.password))
            except UnicodeEncodeError, e:
                self._parent.password = None
                self._parent.m_statusBar.SetStatusText("Connection failed.", 0)
                wx.MessageBox('Check keyboard layout. And try again.', 'Error!', style=wx.ICON_EXCLAMATION)
            except JIRAError, e:
                if 'HTTP 401' in str(e):
                    self._parent.password = None
                    self._parent.m_statusBar.SetStatusText("Connection failed.", 0)
                    wx.MessageBox('Wrong login or password. Try again.', 'Error!', style=wx.ICON_EXCLAMATION)
                else:
                    #print e
                    wx.MessageBox(str(e), 'Error!', style=wx.ICON_ERROR)
            else:
                self._parent.m_statusBar.SetStatusText("JIRA connected!", 0)

        if self._parent.jira is not None:
            self._parent.m_statusBar.SetStatusText("Searching issue summary...", 1)
            self._parent.m_statusBar.SetStatusText("", 2)
            try:
                issue = self._parent.jira.issue(self._issueID, fields='summary')
            except JIRAError, e:
                self._parent.m_statusBar.SetStatusText("Searching failed.", 1)
                wx.MessageBox(str(e), 'Error!', style=wx.ICON_ERROR)
            else:
                CFG["issue"][self._issueID] = {"Summary": issue.fields.summary, "Started": -1,
                                         "Comment": u"", "TimeSpentS": 0}
                self._parent.currentIssueID = self._issueID
                self._parent.m_comboBoxIssue.AppendItems([u"{0} | {1}".format(self._issueID, CFG["issue"][self._issueID]["Summary"])])
                self._parent.m_comboBoxIssue.SetSelection(
                    self._parent.m_comboBoxIssue.FindString(u"{0} | {1}".format(self._issueID, CFG["issue"][self._issueID]["Summary"])))

                self._parent.m_staticTextWhen.SetLabel(started2str(-1))
                self._parent.m_staticTextHowMuch.SetLabel(time_spent2str(0))
                self._parent.m_textCtrlComment.Clear()

                self._parent.m_statusBar.SetStatusText('Current issue - ' + self._issueID, 2)

                write_config(CFG)

        evt = AddIssueEvent(EVT_LOGIN, -1)
        wx.PostEvent(self._parent, evt)

class LogWorkEvent(wx.PyCommandEvent):
    """Event to signal that login is done"""
    def __init__(self, etype, eid):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)

class LogWorkThread(threading.Thread):
    def __init__(self, parent):
        """
        @param parent: The gui object that should recieve the value
        @param issueID: value to 'calculate' to  """
        threading.Thread.__init__(self)
        self._parent = parent

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start()."""
        #time.sleep(10) our simulated calculation time
        if self._parent.jira is None:
            self._parent.m_statusBar.SetStatusText("Connecting to JIRA...", 0)
            try:
                self._parent.jira = JIRA(server="https://jira.wargaming.net", basic_auth=(CFG["login"], self._parent.password))
            except UnicodeEncodeError, e:
                self._parent.password = None
                self._parent.m_statusBar.SetStatusText("Connection failed.", 0)
                wx.MessageBox('Check keyboard layout. And try again.', 'Error!', style=wx.ICON_EXCLAMATION)
                self._parent.m_statusBar.SetStatusText("", 1)
                self._parent.m_buttonPlus.Enable(True)
                self._parent.m_buttonMinus.Enable(True)
                self._parent.m_textCtrlComment.Enable(True)
                self._parent.m_buttonStart.Enable(True)
                self._parent.m_buttonStart.SetDefault()
                self._parent.m_buttonReset.Enable(True)
                self._parent.m_buttonLogWork.Enable(True)
            except JIRAError, e:
                if 'HTTP 401' in str(e):
                    self._parent.password = None
                    self._parent.m_statusBar.SetStatusText("Connection failed.", 0)
                    wx.MessageBox('Wrong login or password. Try again.', 'Error!', style=wx.ICON_EXCLAMATION)
                    self._parent.jira = None
                else:
                    wx.MessageBox(str(e), 'Error!', style=wx.ICON_ERROR)
                    self._parent.jira = None
            else:
                self._parent.m_statusBar.SetStatusText(" JIRA connected!", 0)

        if self._parent.jira is not None:
            self._parent.m_statusBar.SetStatusText("Logging work...", 1)
            tz = get_localzone()
            A = CFG["issue"][self._parent.currentIssueID]["Started"]
            B = A + 3 * 60 * 60
            C = datetime.fromtimestamp(B)
            D = tz.localize(C)
            try:
                self._parent.jira.add_worklog(self._parent.currentIssueID,
                                      timeSpent="{0}m".format(1 + CFG["issue"][self._parent.currentIssueID]["TimeSpentS"] / 60),
                                      comment=self._parent.m_textCtrlComment.GetRange(0, -1), started=D)

            except JIRAError, e:
                #print e
                wx.MessageBox(str(e), 'Error!', style=wx.ICON_ERROR)
            else:
                #print "add_worklog() success!"
                wx.MessageBox("Started:  {0}               Time spent:  {1}m\nComment:\n".format(started2str(A),\
                            1 + CFG["issue"][self._parent.currentIssueID]["TimeSpentS"] / 60) +  \
                            self._parent.m_textCtrlComment.GetRange(0, -1),\
                            "Work logged successfully!", style=wx.ICON_INFORMATION)

                CFG["issue"][self._parent.currentIssueID]["Started"] = -1
                CFG["issue"][self._parent.currentIssueID]["Comment"] = u""
                CFG["issue"][self._parent.currentIssueID]["TimeSpentS"] = 0
                write_config(CFG)

                self._parent.m_staticTextWhen.SetLabel(started2str(-1))
                self._parent.m_staticTextHowMuch.SetLabel(time_spent2str(0))
                self._parent.m_textCtrlComment.Clear()



        #evt = AddIssueEvent(EVT_LOGIN, -1)
        evt = LogWorkEvent(EVT_LOGIN, -1)
        wx.PostEvent(self._parent, evt)

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"WorkLogger - 1.0a beta", pos=wx.DefaultPosition,
                          size=wx.Size(600, 300), style=(wx.DEFAULT_FRAME_STYLE ^(wx.MAXIMIZE_BOX | wx.RESIZE_BORDER))| wx.TAB_TRAVERSAL)
        self.SetIcon(icon_32.GetIcon())
        self.password = None # just 'login'
        self.jira = None # JIRA object

        #self.currentIssueID = CFG["currentIssue"]  # selected issue ID
        self.currentIssueID = None
        self.defaultIssue = {"Started": -1,
                             "TimeSpentS": 0,
                             "Comment": u""}
        #self.Tdelta = 0
        self.TimeSpentS = 0

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizerMain = wx.BoxSizer(wx.VERTICAL)

        sbSizerIssue = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Issue"), wx.HORIZONTAL)

        m_comboBoxIssueChoices = []
        for issue in sorted(CFG["issue"].keys()):
            m_comboBoxIssueChoices.append(u"{0} | {1}".format(issue, CFG["issue"][issue]["Summary"]))
        self.m_comboBoxIssue = wx.ComboBox(sbSizerIssue.GetStaticBox(), wx.ID_ANY, u"Enter issue URL or select existing task...",
                                           wx.DefaultPosition, wx.DefaultSize, m_comboBoxIssueChoices, 0)
        # if m_comboBoxIssueChoices != []:
        #    for item in range( self.m_comboBoxIssue.GetCount() ):
        #        if self.currentIssueID in self.m_comboBoxIssue.GetString(item):
        #            self.m_comboBoxIssue.SetSelection(item)

        sbSizerIssue.Add(self.m_comboBoxIssue, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_buttonPlus = wx.Button(sbSizerIssue.GetStaticBox(), wx.ID_ANY, u"+", wx.DefaultPosition,
                                      wx.Size(16, 22), 0)
        self.m_buttonPlus.SetDefault()
        sbSizerIssue.Add(self.m_buttonPlus, 0,
                         wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 5)

        self.m_buttonMinus = wx.Button(sbSizerIssue.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition,
                                      wx.Size(16, 22), 0)
        self.m_buttonMinus.Enable(False)
        sbSizerIssue.Add(self.m_buttonMinus, 0,
                         wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        bSizerMain.Add(sbSizerIssue, 0, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        bSizerTime = wx.BoxSizer(wx.HORIZONTAL)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.calculateT, self.timer)

        self.m_staticTextStarted = wx.StaticText(self, wx.ID_ANY, u"Started at:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticTextStarted.Wrap(-1)
        bSizerTime.Add(self.m_staticTextStarted, 0, wx.ALL, 5)

        self.m_staticTextWhen = wx.StaticText(self, wx.ID_ANY, started2str(self.defaultIssue["Started"]), wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.m_staticTextWhen.Wrap(-1)
        self.m_staticTextWhen.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        bSizerTime.Add(self.m_staticTextWhen, 0, wx.ALL, 5)

        bSizerTime.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        self.m_staticTextTimeSpent = wx.StaticText(self, wx.ID_ANY, u"Time Spent:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticTextTimeSpent.Wrap(-1)
        bSizerTime.Add(self.m_staticTextTimeSpent, 0, wx.ALL, 5)

        self.m_staticTextHowMuch = wx.StaticText(self, wx.ID_ANY, time_spent2str(self.defaultIssue["TimeSpentS"]),
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticTextHowMuch.Wrap(-1)
        self.m_staticTextHowMuch.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        bSizerTime.Add(self.m_staticTextHowMuch, 0, wx.ALL, 5)

        bSizerMain.Add(bSizerTime, 0, wx.EXPAND, 5)

        self.m_staticTextComment = wx.StaticText(self, wx.ID_ANY, u"Comment:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticTextComment.Wrap(-1)
        bSizerMain.Add(self.m_staticTextComment, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)

        self.m_textCtrlComment = wx.TextCtrl(self, wx.ID_ANY, self.defaultIssue["Comment"], wx.DefaultPosition, wx.DefaultSize,
                                             wx.TE_MULTILINE)
        self.m_textCtrlComment.Enable(False)
        bSizerMain.Add(self.m_textCtrlComment, 1, wx.ALL | wx.EXPAND, 5)

        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.m_buttonStart = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_buttonStart.Enable(False)
        bSizerButtons.Add(self.m_buttonStart, 0, wx.ALL, 5)

        self.m_buttonReset = wx.Button(self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_buttonReset.Enable(False)
        bSizerButtons.Add(self.m_buttonReset, 0, wx.ALL, 5)

        bSizerButtons.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        self.m_buttonLogWork = wx.Button(self, wx.ID_ANY, u"Log Work", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_buttonLogWork.Enable(False)
        bSizerButtons.Add(self.m_buttonLogWork, 0, wx.ALL, 5)

        bSizerMain.Add(bSizerButtons, 0, wx.EXPAND, 5)

        self.SetSizer(bSizerMain)
        self.Layout()

        self.m_statusBar = self.CreateStatusBar(3, wx.ST_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_comboBoxIssue.Bind(wx.EVT_COMBOBOX, self.onCombobox)
        self.m_buttonPlus.Bind(wx.EVT_BUTTON, self.addIssue)
        self.Bind(EVT_LOGIN_DONE, self.addIssueDone)
        self.m_buttonMinus.Bind(wx.EVT_BUTTON, self.removeIssue)
        self.m_buttonStart.Bind(wx.EVT_BUTTON, self.onStart)
        self.m_buttonReset.Bind(wx.EVT_BUTTON, self.onReset)
        self.m_buttonLogWork.Bind(wx.EVT_BUTTON, self.onLogWork)
        self.Bind(EVT_LOGWORK_DONE, self.addIssueDone)
        self.Bind(wx.EVT_CLOSE, self.onClose)


    def __del__(self):
        pass

    ################ functions ################
    def onClose(self, event):
        if self.m_buttonStart.GetLabelText() == u"Pause":
            self.timer.Stop()
            CFG["issue"][self.currentIssueID]["TimeSpentS"] = self.TimeSpentS + self.Tdelta
            self.m_buttonStart.SetLabel(u"Start")
            CFG["issue"][self.currentIssueID]["Comment"] = self.m_textCtrlComment.GetRange(0, -1)
        write_config(CFG)
        self.Destroy()


    def getPass(self):
        if self.password is None:
            dlg = MyDialog(CFG["login"])
            if dlg.ShowModal() == wx.ID_CANCEL:
                #print 'cancel'
                dlg.Destroy()
                return False
            else:
                CFG["login"] = dlg.login_t.GetRange(0, -1)
                self.password = dlg.pass_t.GetRange(0, -1)
                dlg.Destroy()
                return True
        else:
            return True

    def addIssue(self, event):
        text = self.m_comboBoxIssue.GetValue()
        results = re.findall("[A-z]+-\d+", text)
        if len(results) == 0:
            wx.MessageBox("Can't detect issue ID. Try again.", 'Error!', style = wx.ICON_EXCLAMATION)
        else:
            issueID = results[0].upper()

            if issueID in CFG["issue"].keys():
                wx.MessageBox("Issue already in list!", 'What?')

            else:
                if self.m_buttonStart.GetLabelText() == u"Pause":
                    self.timer.Stop()
                    # self.currentTimeSpent += self.Tdelta
                    CFG["issue"][self.currentIssueID]["TimeSpentS"] = self.TimeSpentS + self.Tdelta
                    self.m_buttonStart.SetLabel(u"Start")
                    CFG["issue"][self.currentIssueID]["Comment"] = self.m_textCtrlComment.GetRange(0, -1)
                    write_config(CFG)

                self.m_buttonPlus.Enable(False)
                self.m_buttonMinus.Enable(False)
                self.m_textCtrlComment.Enable(False)
                self.m_buttonStart.Enable(False)
                self.m_buttonStart.SetDefault()
                self.m_buttonReset.Enable(False)
                self.m_buttonLogWork.Enable(False)

                CHECK_PASS_OK = True
                if self.password is None:
                    CHECK_PASS_OK = self.getPass()
                ## start login tread
                if CHECK_PASS_OK == True:
                    worker = AddIssueThread(self, issueID)
                    worker.start()
                else:
                    self.m_buttonPlus.Enable(True)

    def addIssueDone(self, event):
        if self.jira is not None:
            self.m_statusBar.SetStatusText("", 1)
            self.m_buttonPlus.Enable(True)
            self.m_buttonMinus.Enable(True)
            self.m_textCtrlComment.Enable(True)
            self.m_buttonStart.Enable(True)
            self.m_buttonStart.SetDefault()
            self.m_buttonReset.Enable(True)
            self.m_buttonLogWork.Enable(True)
        else:
            self.m_buttonPlus.Enable(True)

    def removeIssue(self, event):
        text = self.m_comboBoxIssue.GetValue()
        results = re.findall("[A-z]+-\d+", text)
        if len(results) == 0:
            wx.MessageBox("Can't detect issue ID. Try again.", 'Error!', style=wx.ICON_EXCLAMATION)
        else:
            if self.m_buttonStart.GetLabelText() == u"Pause":
                self.timer.Stop()
                CFG["issue"][self.currentIssueID]["TimeSpentS"] = self.TimeSpentS + self.Tdelta
                self.m_buttonStart.SetLabel(u"Start")

            self.m_staticTextWhen.SetLabel(started2str(-1))
            self.m_staticTextHowMuch.SetLabel(time_spent2str(0))
            self.m_textCtrlComment.Clear()

            issueID = results[0].upper()

            self.m_comboBoxIssue.Delete(self.m_comboBoxIssue.FindString(text))
            self.m_comboBoxIssue.SetSelection(-1)
            #self.currentIssue = self.m_comboBoxIssue.GetValue().split("|")[0].strip()
            self.currentIssueID = None
            self.m_textCtrlComment.Clear()
            del CFG["issue"][issueID]
            write_config(CFG)

            self.m_buttonMinus.Enable(False)
            self.m_textCtrlComment.Enable(True)
            self.m_buttonStart.Enable(False)
            self.m_buttonPlus.SetDefault()
            self.m_buttonReset.Enable(False)
            self.m_buttonLogWork.Enable(False)
            self.m_statusBar.SetStatusText('', 2)

    def onCombobox(self, event):
        # print self.m_comboBoxIssue.GetValue()
        if self.m_buttonStart.GetLabelText() == u"Pause":
            self.timer.Stop()
            #self.currentTimeSpent += self.Tdelta
            CFG["issue"][self.currentIssueID]["TimeSpentS"] = self.TimeSpentS + self.Tdelta
            self.m_buttonStart.SetLabel(u"Start")
            CFG["issue"][self.currentIssueID]["Comment"] = self.m_textCtrlComment.GetRange(0, -1)
            write_config(CFG)

        if self.currentIssueID is not None:
            CFG["issue"][self.currentIssueID]["Comment"] = self.m_textCtrlComment.GetRange(0,-1)
        else:
            self.m_buttonMinus.Enable(True)
            self.m_textCtrlComment.Enable(True)
            self.m_buttonStart.Enable(True)
            self.m_buttonStart.SetDefault()
            self.m_buttonReset.Enable(True)
            self.m_buttonLogWork.Enable(True)

        text = self.m_comboBoxIssue.GetValue()
        self.currentIssueID = re.findall("[A-z]+-\d+", text)[0].upper()
        write_config(CFG)
        self.m_staticTextWhen.SetLabel(started2str(CFG["issue"][self.currentIssueID]["Started"]))
        self.m_staticTextHowMuch.SetLabel(time_spent2str(CFG["issue"][self.currentIssueID]["TimeSpentS"]))
        self.m_textCtrlComment.Clear()
        self.m_textCtrlComment.AppendText(CFG["issue"][self.currentIssueID]["Comment"])

        self.m_statusBar.SetStatusText('Current issue - ' + self.currentIssueID, 2)

    def calculateT(self, event):
        self.Tdelta = int(time.clock() - self.Tstart)
        #T = self.currentTimeSpent + self.Tdelta
        T = self.TimeSpentS + self.Tdelta
        self.m_staticTextHowMuch.SetLabel(time_spent2str(T))
        if T%60 == 0:
            CFG["issue"][self.currentIssueID]["TimeSpentS"] = T
            CFG["issue"][self.currentIssueID]["Comment"] = self.m_textCtrlComment.GetRange(0, -1)
            write_config(CFG)

    # Virtual event handlers, overide them in your derived class

    def onStart(self, event):
        #if self.currentStarted == -1:
        if CFG["issue"][self.currentIssueID]["Started"] == -1:
            CFG["issue"][self.currentIssueID]["Started"] = time.mktime(time.localtime())
            #print self.Started
            self.m_staticTextWhen.SetLabel(started2str(CFG["issue"][self.currentIssueID]["Started"]))

        if self.m_buttonStart.GetLabelText() == u"Start":
            self.Tstart = time.clock() - 1
            self.TimeSpentS = CFG["issue"][self.currentIssueID]["TimeSpentS"]
            #print "starting timer..."
            self.timer.Start(997)
            self.m_buttonStart.SetLabel(u"Pause")
        else:
            self.timer.Stop()
            CFG["issue"][self.currentIssueID]["TimeSpentS"] = self.TimeSpentS + self.Tdelta
            self.m_buttonStart.SetLabel(u"Start")
            CFG["issue"][self.currentIssueID]["Comment"] = self.m_textCtrlComment.GetRange(0, -1)

        write_config(CFG)

    def onReset(self, event):
        if self.m_buttonStart.GetLabelText() == u"Pause":
            self.timer.Stop()
            self.m_buttonStart.SetLabel(u"Start")
        CFG["issue"][self.currentIssueID]["Started"] = -1
        CFG["issue"][self.currentIssueID]["TimeSpentS"] = 0
        CFG["issue"][self.currentIssueID]["Comment"] = u""
        write_config(CFG)

        self.m_staticTextWhen.SetLabel(started2str(-1))
        self.m_staticTextHowMuch.SetLabel(time_spent2str(0))
        self.m_textCtrlComment.Clear()

    def onLogWork(self, event):
        if self.m_buttonStart.GetLabelText() == u"Pause":
            self.timer.Stop()
            #self.currentTimeSpent += self.Tdelta
            CFG["issue"][self.currentIssueID]["TimeSpentS"] = self.TimeSpentS + self.Tdelta
            self.m_buttonStart.SetLabel(u"Start")

        #issueID = self.currentIssueID
        self.m_buttonPlus.Enable(False)
        self.m_buttonMinus.Enable(False)
        self.m_textCtrlComment.Enable(False)
        self.m_buttonStart.Enable(False)
        self.m_buttonStart.SetDefault()
        self.m_buttonReset.Enable(False)
        self.m_buttonLogWork.Enable(False)

        CHECK_PASS_OK = True
        if self.password is None:
            CHECK_PASS_OK = self.getPass()
        ## start login tread
        if CHECK_PASS_OK == True:
            worker = LogWorkThread(self)
            worker.start()
        else:
            self.m_statusBar.SetStatusText("", 1)
            self.m_buttonPlus.Enable(True)
            self.m_buttonMinus.Enable(True)
            self.m_textCtrlComment.Enable(True)
            self.m_buttonStart.Enable(True)
            self.m_buttonStart.SetDefault()
            self.m_buttonReset.Enable(True)
            self.m_buttonLogWork.Enable(True)

    def onLogWorkDone(self):
            self.m_statusBar.SetStatusText("", 1)
            self.m_buttonPlus.Enable(True)
            self.m_buttonMinus.Enable(True)
            self.m_textCtrlComment.Enable(True)
            self.m_buttonStart.Enable(True)
            self.m_buttonStart.SetDefault()
            self.m_buttonReset.Enable(True)
            self.m_buttonLogWork.Enable(True)



class NotEmptyValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self):
        """
        Note that every validator must implement the Clone() method.
        """
        return NotEmptyValidator()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if len(text) == 0:
            wx.MessageBox("This field must contain some text!", "Error")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True


class MyDialog(wx.Dialog):
    def __init__(self, login):
        wx.Dialog.__init__(self, None, -1, "Enter login and password")

        # Create the text controls
        login_l = wx.StaticText(self, -1, "Login:")
        pass_l = wx.StaticText(self, -1, "Pass:")

        self.login_t = wx.TextCtrl(self, validator=NotEmptyValidator(), value=login)
        self.pass_t = wx.TextCtrl(self, validator=NotEmptyValidator(), style=wx.TE_PASSWORD)

        # Use standard button IDs
        okay = wx.Button(self, wx.ID_OK)
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        # Layout with sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        fgs = wx.FlexGridSizer(3, 2, 5, 5)
        fgs.Add(login_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.login_t, 0, wx.EXPAND)
        fgs.Add(pass_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.pass_t, 0, wx.EXPAND)
        fgs.AddGrowableCol(1)
        sizer.Add(fgs, 0, wx.EXPAND | wx.ALL, 5)

        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        sizer.Add(btns, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


class myApp(wx.App):
    """ app"""
    def __init__(self, redirect=True):
        wx.App.__init__(self, redirect)


    def OnInit(self):
        self.main_frame = MainFrame(parent=None)
        self.main_frame.Show()
        self.SetTopWindow(self.main_frame)
        return True


if __name__ == '__main__':
    myApp = myApp(redirect=True)
    myApp.MainLoop()