# -*- coding: utf-8 -*-
import logging
import os
import re
import subprocess
import threading
import wx

from load_dialog import LoadDialog

logging.basicConfig(filename=__name__ + '.log',
                    format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.DEBUG, filemode='a',
                    datefmt='%Y-%m-%d%I:%M:%S %p')


def checkSub(types, callback, *subs):
    paths = []
    for index, sub in enumerate(subs):
        # if index == 0 or (index == len(subs) - 1 and isinstance(sub, bool)):
        if index == 0 or (isinstance(sub, bool)):
            paths.append(sub)
        elif types[index] == "text":
            if sub.GetValue() == '':
                showDialog("『" + sub.GetLabel() + "』を入力してください")
                return
            paths.append(sub.GetValue())
        else:
            if sub.GetPath() == '':
                showDialog("『" + sub.GetLabel() + "』を入力してください")
                return
            else:
                if not checkStyle(types[index], sub.GetPath()):
                    showDialog("『" + sub.GetLabel() + "』" + "ファイルの拡張子が正しくない")
                    return
                else:
                    paths.append(sub.GetPath())
    callback(paths)


def checkStyle(style, path):
    if style == 'db':
        return os.path.isfile(path) and path.endswith(".accdb")
    elif style == 'dir':
        return os.path.isdir(path)
    elif style == 'excel':
        return os.path.isfile(path) and (path.endswith(".xlsm") or path.endswith(".xlsx"))
    elif style == 'dore':
        return checkStyle('db', path) or checkStyle('excel', path)


def showDialog(message):
    stone = wx.MessageDialog(None, message, "提示", wx.YES_DEFAULT | wx.ICON_QUESTION)
    if stone.ShowModal() == wx.ID_YES:
        stone.Destroy()


def run_cmd(cmd_str='', echo_print=1, ld=None):
    if echo_print == 1:
        logging.info('\n run command="{}"'.format(cmd_str))
    result = subprocess.Popen('start cmd /k ' + cmd_str, shell=True, )
    # stdout=subprocess.PIPE,
    # stderr=subprocess.STDOUT, )
    # resultContent = result.communicate()[0].decode("UTF8")
    # logging.info('\n run command result content="{}"'.format(resultContent))
    # logging.info('\n run command result code="{}"'.format(result.returncode))

    ld.Destroy()

    # if result.returncode != 0 or re.search('error', resultContent, re.IGNORECASE):
    #     showDialog("エラーが発生しました。\nログファイルを確認ください。")


def show(cmd_str='', echo_print=1):
    ld = LoadDialog(None, size=(150, 150), style=wx.MINIMIZE_BOX)
    t = threading.Thread(target=run_cmd, args=(cmd_str, echo_print, ld))
    t.start()
    ld.ShowModal()
    # progressMax = 100
    # dialog = wx.ProgressDialog("お待ちください", "実行中．．．", progressMax,
    #                            style=wx.PD_AUTO_HIDE | wx.PD_APP_MODAL)
    # count = 0
    # while t.isAlive():
    #     count = count + 1
    #     wx.Sleep(1)
    #     dialog.Update(count)
    #     if count >= 99:
    #         count = 0
    # dialog.Update(progressMax)


def executeCmdStr(paths):
    cmd_str = "python"
    for p in paths:
        cmd_str = cmd_str + " " + str(p)
    show(cmd_str)


def executeJavaCmdStr(paths):
    cmd_str = "java -jar"
    for p in paths:
        cmd_str = cmd_str + " " + str(p)
    show(cmd_str)


def executeCmdStrFolder(paths):
    cmd_str = "python"
    for index, p in enumerate(paths):
        if index == len(paths) - 1:
            cmd_str = cmd_str + " " + os.path.dirname(str(p))
        else:
            cmd_str = cmd_str + " " + str(p)
    show(cmd_str)


def executeCmdStrFolder1(paths):
    cmd_str = "python"
    for index, p in enumerate(paths):
        if index == len(paths) - 2:
            cmd_str = cmd_str + " " + os.path.dirname(str(p))
        else:
            cmd_str = cmd_str + " " + str(p)
    show(cmd_str)
