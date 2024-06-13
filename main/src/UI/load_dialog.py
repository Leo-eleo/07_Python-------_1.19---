import os

from wx.adv import AnimationCtrl
import wx


class LoadDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(LoadDialog, self).__init__(*args, **kwargs)
        self.SetBackgroundColour(wx.Colour(255, 255, 255, 0))
        self.animation = AnimationCtrl(self)
        fileName = os.path.join(os.path.abspath('.'), "loading.gif")
        self.animation.LoadFile(fileName)
        self.animation.Play()

        self.Centre()
        self.Show()
