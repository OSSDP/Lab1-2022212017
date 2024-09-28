import ctypes
import inspect
from tkinter import *
import socket
import threading
from udpserver import udpserver

class TalkServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('交流软件服务器端')
        self.root.geometry('600x250')

        self.udp = udpserver('127.0.0.1', 52106)
        self.thread_stop = False

        self.frm = Frame(root)
        self.frm.pack()

        self.frm_M = Frame(self.frm)
        self.frm_M.pack(side=TOP)

        self.scrollbar = Scrollbar(self.frm_M, orient='vertical')
        self.scrollbar.pack(side=RIGHT, fill='both')

        self.t_show = Text(self.frm_M, width=45, height=6, font=('Verdana', 15), yscrollcommand=self.scrollbar.set)
        self.t_show.insert('1.0', '服务器已启动\n')
        self.t_show.pack()

        self.frm_L = Frame(self.frm)
        self.frm_LL = Frame(self.frm_L)
        self.frm_LL.pack(side=LEFT)

        Label(self.frm_LL, text='输入信息', font=('Fangsong', 18)).pack(side=TOP)
        Label(self.frm_LL, text='输入地址', font=('Fangsong', 18)).pack(side=TOP)

        self.smsg = StringVar()
        self.saddr = StringVar()

        self.frm_RL = Frame(self.frm_L)
        Entry(self.frm_RL, textvariable=self.smsg, width=30, font=('Fangsong', 18)).pack()
        Entry(self.frm_RL, textvariable=self.saddr, width=30, font=('Fangsong', 18)).pack()
        self.frm_RL.pack(side=RIGHT)

        self.frm_L.pack(side=TOP)
        self.frm_T = Frame(self.frm)
        self.frm_T.pack(side=TOP)

        Button(self.frm_T, text="发送", command=self.send, width=8, height=1).pack(side=RIGHT)
        Button(self.frm_T, text="停止", command=self.stop, width=8, height=1).pack(side=LEFT)
        Button(self.frm_T, text="启动", command=self.start_udp_server, width=8, height=1).pack(side=LEFT)

        self.p_list = []

    def udp_server_thread(self):
        try:
            self.udp.start()
            while not self.thread_stop:
                msg, addr = self.udp.recmsg()
                if msg:
                    self.t_show.insert('1.0', f'[{addr}] {msg.decode("utf-8")}\n')
        except Exception as e:
            self.t_show.insert('1.0', f"Error: {e}\n")
        finally:
            self.udp.stop()
            self.t_show.insert('1.0', "Server stopped.\n")

    def start_udp_server(self):
        self.thread_stop = False
        self.udp_thread = threading.Thread(target=self.udp_server_thread)
        try:
            self.udp_thread.start()
            self.p_list.insert(0, self.udp_thread)
        except Exception as e:
            self.t_show.insert('1.0', f"Failed to start server: {e}\n")

    def stop(self):
        self.thread_stop = True
        if self.p_list and self.p_list[0].is_alive():
            self._stop_thread(self.p_list[0])
            self.p_list.pop(0)
        self.t_show.insert('1.0', "Server stopped.\n")

    def send(self):
        msg = self.smsg.get().encode("utf-8")
        addr = eval(self.saddr.get())
        self.udp.sendmsg(addr, msg)
        self.t_show.insert('1.0', f"Server: {self.smsg.get()}\n")
        self.smsg.set('')

    def _async_raise(self, tid, exctype):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def _stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

if __name__ == "__main__":
    root = Tk()
    app = TalkServerApp(root)
    root.mainloop()