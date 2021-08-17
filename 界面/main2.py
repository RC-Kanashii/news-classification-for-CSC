import tkinter as tk
import easygui as g
import ctypes
from tkinter import scrolledtext as st
import tkinter.font as tkFont



global e1,e2#定义全局变量，储存标题和文件
global t2,t1
window = tk.Tk()
window.title('my window')
window.geometry('600x600')

#尾号为1的是关于功能1的
#尾号为2的是关于功能2的



def insert_1():#功能1：输入单条新闻，输出新闻的分类

    t1.grid(row=7,column=0)#用于输出程序结果，处理后的结果需要编写）




def insert_2():#在进行点击功能2按钮后才会开始读取文件信息
    b9 = tk.Button(window, text='选择文件', width=10, height=2, command=start_job_2,font=f1)#在start_job_2中开始实现功能2
    b9.grid(row=10,column=0)#按钮重叠，点击同一处地方即可实现功能

def start_job_2():##功能2：支持本地上传csv/xlsx文件，批量输入新闻，并输出新闻分类
    # fileopenbox()函数的返回值是你选择的那个文件的具体路径
    str1 = g.fileopenbox('open file', 'C:/User/Administrator/Desktop/__pycache__')
    # msgbox()是测试用的，可以不用写
    #g.msgbox(str1)
    global t2
    l3=tk.Label(window,text=str1,font=f1)
    l3.grid(row=11,column=0)
    b2 = tk.Button(window, text='开始预测，预测结果如下', width=19, height=2, command=start_2,font=f1)#在start_2中具体实现功能2
    b2.grid(row=10,column=0)
    t2 = st.ScrolledText(window, height=10,font=f1)
    t2.grid(row=12,column=0)


def start_2():#功能2：支持本地上传csv/xlsx文件，批量输入新闻，并输出新闻分类
    t2.grid(row=12,column=0)#用于输出程序结果，处理后的结果（需要编写）


f1 = tkFont.Font(family='microsoft yahei', size=16) # 字体设定

l = tk.Label(window,text=' ')
l1 = tk.Label(window,text='功能1：输入单条新闻，输出新闻的分类',width=75,font=f1)
l2 = tk.Label(window,text='功能2：支持本地上传xlsx文件  ，批量输入新闻,并输出新闻分类',width=83,font=f1)
l3 = tk.Label(window,text=' ')


l.grid()
l1.grid()#功能1的简介

#功能1的板块
l4=tk.Label(window,text='标题:',width=60,anchor="w",font=f1)
l4.grid(row=4,column=0)
e1=st.ScrolledText(window,width=50,font=f1,height=2)#标题(输入的标题保存在e1中)在之前定义过全局变量，所以在函数中可以直接使用
e1.grid(row=4,column=0)
l4=tk.Label(window,text='文本:',width=60,anchor="w",font=f1)
l4.grid(row=5,column=0)
e2=st.ScrolledText(window,width=50,height=10,font=f1)#文本(输入的文本保存在e2中)
e2.grid(row=5,column=0)
b1 = tk.Button(window, text='执行功能1', width=10, height=2, command=insert_1,font=f1)#在insert_1中实现功能1
b1.grid(row=6,column=0)
t1=st.ScrolledText(window,height=10)


l3.grid()#空一行
l2.grid()#功能2的简介

#功能2的板块
l3=tk.Label(window,text=' ',font=f1)
l3.grid(row=8,column=0)
b2=tk.Button(window,text='执行功能2',width=10,height=2,command=insert_2,font=f1)#在insert_2中实现打开文件的操作
b2.grid(row=10,column=0)
t2=st.ScrolledText(window,font=f1,height=10)

# 适配dpi
try:  # >= win 8.1
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:  # win 8.0 or less
    ctypes.windll.user32.SetProcessDPIAware()
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
window.tk.call('tk', 'scaling', ScaleFactor/75)

window.mainloop()