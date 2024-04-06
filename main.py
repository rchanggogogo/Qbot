#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

import wx

from gui.mainframe import MainFrame

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, title="AI智能量化投研平台")
    frame.Show()

    # os.popen(
    #     "python /Users/changlei/opt/anaconda3/envs/qbot/bin/python /Users/changlei/Work/01-project/Qbot/auto_monitor.py"
    # )

    app.MainLoop()
