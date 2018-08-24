import tkinter as tk
from tkinter import filedialog
from pdf_to_image import *
from wand.image import Image
import math
import datetime


def change():
    global root
    filePath = filedialog.askopenfilename(initialdir=".", title="Select file",
                                                 filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
    root.var.set("处理中")
    root.update()
    bg = convert(filePath)
    bg.save(filename="bg.png")
    root.var.set("新背景处理完成")


def open():
    global root
    root.fileNames = filedialog.askopenfilenames(initialdir=".", title="Select file",
                                                 filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
    root.var.set("已选中"+str(len(root.fileNames))+"个证书")

def start():
    global root
    if root.fileNames=="":
        root.var.set("没有文件")
        return
    root.var.set("处理背景文件")
    root.update()
    with Image(filename="bg.png", resolution=RESOLUTION) as bg:
        file_count = len(root.fileNames)
        page_count = math.ceil(file_count/25)

        for j in range(page_count):
            output_page = bg.clone()
            for i in range(25):
                index = j*25 + i
                file_path = root.fileNames[index]
                root.var.set("处理文件" + str(index+1) + "/" + str(file_count))
                root.update()
                l = i%5
                t = math.floor(i/5)
                output_page = composite_fg_bg(output_page, convert_fg(file_path), l, t)
                if i==24 or index==file_count-1: #time to save the page
                    out_put_file_name = "output/"+str(j)+".png"
                    output_page.save(filename=out_put_file_name)
                    break
    root.var.set("处理完成")
    root.update()



        # for i in range(len(root.fileNames)):
        #     filePath = root.fileNames[i]
        #     root.var.set("处理文件"+str(i+1)+"/"+str(len(root.fileNames)))
        #     root.update()
        #     page = int(i/25)
        #     index = i%25
        #     if index==0: #new page
        #         if(page!=0): #save old page
        #             result.save(filename="output/output"+str(page)+".png")
        #         result = composite_fg_bg(bg,convert_fg(filePath),0,0)
        #     else:
        #         left = index%5
        #         top = int(index/5)
        #         result = composite_fg_bg(result,convert_fg(filePath),left,top)
        #     if i == len(root.fileNames)-1 :
        #         result.save(filename="output/output"+str(page)+".png")








if __name__ == '__main__':
    root = tk.Tk()
    root.title("证书排版工具")
    root.fileNames = ""

    root.var = tk.StringVar()
    l = tk.Label(root,
                 textvariable=root.var,
                 bg='green', font=('Arial', 12), width=15, height=2)
    l.pack()

    b = tk.Button(root,
                  text='打开待排版证书',
                  width=15, height=2,
                  command=open)
    b.pack()

    s = tk.Button(root,
                  text='开始排版',
                  width=15, height=2,
                  command=start)
    s.pack()

    a = tk.Button(root,
                  text='重新选择背景',
                  width=15, height=2,
                  command=change)
    a.pack()


    root.mainloop()