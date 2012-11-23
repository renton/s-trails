import wx
import wx.grid

class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        self.CreateGrid(9, 2)
        self.SetColLabelValue(0, "First")
        self.SetColLabelValue(1, "Last")
        self.SetRowLabelValue(0, "1")
        self.SetCellValue(0, 0, "A")
        self.SetCellValue(0, 1, "A")
        self.SetRowLabelValue(1, "2")
        self.SetCellValue(1, 0, "B")
        self.SetCellValue(1, 1, "B")
        self.SetRowLabelValue(2, "3")
        self.SetCellValue(2, 0, "C")
        self.SetCellValue(2, 1, "C")
        self.SetRowLabelValue(3, "4")
        self.SetCellValue(3, 0, "D")
        self.SetCellValue(3, 1, "D")
        self.SetRowLabelValue(4, "5")
        self.SetCellValue(4, 0, "E")
        self.SetCellValue(4, 1, "E")
        self.SetRowLabelValue(5, "6")
        self.SetCellValue(5, 0, "F")
        self.SetCellValue(5, 1, "F")
        self.SetRowLabelValue(6, "7")
        self.SetCellValue(6, 0, "G")
        self.SetCellValue(6, 1, "G")
        self.SetRowLabelValue(7, "8")
        self.SetCellValue(7, 0, "K")
        self.SetCellValue(7, 1, "K")
        self.SetRowLabelValue(8, "9")
        self.SetCellValue(8, 0, "L")
        self.SetCellValue(8, 1, "L")

class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "A Grid",
                size=(275, 275))
        grid = SimpleGrid(self)

app = wx.PySimpleApp()
frame = TestFrame(None)
frame.Show(True)
app.MainLoop()
