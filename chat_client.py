#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: 人海中的海盗
# 在线聊天客户端
import tkinter
import tkinter.font as tkFont
import time
import requests
global clientSock


class ClientUI:
    # 初始化类的相关属性的构造函数
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Python客户端-deepseek咨询')
        # 窗口  4个frame面板布局
        self.frame = [tkinter.Frame(), tkinter.Frame(), tkinter.Frame(), tkinter.Frame()]
        # 滚动条
        self.chatTextScrollBar = tkinter.Scrollbar(self.frame[0])
        self.chatTextScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # 显示Text，绑定滚动条
        ft = tkFont.Font(family='Fixdsys', size=11)
        self.chatText = tkinter.Listbox(self.frame[0], width=70, height=18, font=ft)
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set
        self.chatText.pack(expand=1, fill=tkinter.BOTH)
        self.chatTextScrollBar['command'] = self.chatText.yview()
        self.frame[0].pack(expand=1, fill=tkinter.BOTH)
        # 分开消息显示和消息输入
        label = tkinter.Label(self.frame[1], height=2)
        label.pack(fill=tkinter.BOTH)
        self.frame[1].pack(expand=1, fill=tkinter.BOTH)
        # 输入消息的滚动条
        self.inputTextScrollBar = tkinter.Scrollbar(self.frame[2])
        self.inputTextScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        ft = tkFont.Font(family='Fixdsys', size=11)
        self.inputText = tkinter.Text(self.frame[2], width=70, height=8, font=ft)
        self.inputText['yscrollcommand'] = self.inputTextScrollBar.set
        self.inputText.pack(expand=1, fill=tkinter.BOTH)
        self.inputTextScrollBar['command'] = self.chatText.yview()
        self.frame[2].pack(expand=1, fill=tkinter.BOTH)
        # 发送按钮
        self.sendButton = tkinter.Button(self.frame[3], text='发送', width=10, command=self.receive_message)
        self.sendButton.pack(expand=1, side=tkinter.BOTTOM and tkinter.RIGHT, padx=25, pady=5)
        # 关闭按钮
        self.closeButton = tkinter.Button(self.frame[3], text='关闭', width=10, command=self.close)
        self.closeButton.pack(expand=1, side=tkinter.RIGHT, padx=25, pady=5)
        self.frame[3].pack(expand=1, fill=tkinter.BOTH)

        self.buffer = 1024

    def close(self):
        self.root.destroy()

    # 接收消息
    def receive_message(self):
        message = self.inputText.get('1.0', tkinter.END)
        if message.strip() == "":
            self.chatText.insert(tkinter.END, '请输入问题后再发送……\n')
            return -1
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chatText.insert(tkinter.END, '客观' + theTime + '问：\n' + message + '\n')
        json_q = {"question": message.strip()}
        try:
            response = requests.post(url="http://171.1.4.1:8080/chat/deepseek", json=json_q, timeout=300)
            result = response.json()
            if result["result"] == 0:
                self.flag = True
                self.server_msg = f'{result["answer"]} \n 所以经过我的思考，{result["answer"]}'
                the_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.chatText.insert(tkinter.END, f'deep seek {the_time} 回答：{self.server_msg}\n')
                self.chatText.see(tkinter.END)
            else:
                self.flag = False
                self.chatText.insert(tkinter.END, '服务器繁忙\n')
        except Exception as e:
            self.chatText.insert(tkinter.END, f'服务器发生异常：{str(e)}\n')


if __name__ == '__main__':
    client = ClientUI()
    client.root.mainloop()

