import tkinter as tk
import easygui as g


window = tk.Tk()
window.title('my window')
window.geometry('500x500')

l=tk.Label(window,text='请选择要使用的功能',bg='white')
l1=tk.Label(window,text='功能1：支持本地上传csv/xlsx文件，批量输入新闻，并输出新闻分类')
l2=tk.Label(window,text='功能2：输入单条新闻，输出新闻的分类')
l.pack()
l1.pack()
l2.pack()
counter=0


def start_job_1():
    # fileopenbox()函数的返回值是你选择的那个文件的具体路径
    str1 = g.fileopenbox('open file', 'C:/User/Administrator/Desktop/__pycache__')
    # msgbox()是测试用的，可以不用写
    g.msgbox(str1)
    global t1
    b1 = tk.Button(window, text='1：使用该文件进行分析', width=17, height=2, command=insert_1)
    b1.pack()
    t1 = tk.Text(window, height=100)
    t1.pack()

def insert_1():
    t1 = tk.Text(window, height=100)
    t1.pack()

def start_job_2():
    global e2
    global t2
    e2=tk.Entry(window,show='',width=100)
    e2.pack()
    b2=tk.Button(window,text='2：开始分析',width=15,height=2,command=insert_2)
    b2.pack()
    t2=tk.Text(window,height=100)
    t2.pack()


def insert_2():
    var=e2.get()
    t2.insert('insert',var)

menubar=tk.Menu(window)
filemenu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='功能',menu=filemenu)
filemenu.add_command(label='功能1',command=start_job_1)
filemenu.add_command(label='功能2',command=start_job_2)

window.config(menu=menubar)

window.mainloop()