import ctypes
import inspect
import threading
from tkinter import *
from udpclient import udpclient

class TalkClientApp:
    def __init__(self, root, client):
        self.root = root
        self.client = client
        self.thread_stop = False

        self.setup_ui()
        self.start_udp_client()

    def setup_ui(self):
        self.root.title('交流软件客户端')
        self.root.geometry('600x250')

        # Main frame
        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True)

        # Message display frame
        message_frame = Frame(main_frame)
        message_frame.pack(side=TOP, fill=BOTH, expand=True)

        scrollbar = Scrollbar(message_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.message_text = Text(message_frame, width=45, height=6, font=('Verdana', 15), yscrollcommand=scrollbar.set)
        self.message_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.message_text.yview)

        # Input frame
        input_frame = Frame(main_frame)
        input_frame.pack(side=BOTTOM, fill=X)

        Label(input_frame, text='输入信息', font=('Fangsong', 18)).pack(side=LEFT)

        self.input_entry = Entry(input_frame, width=30, font=('Fangsong', 18))
        self.input_entry.pack(side=LEFT, fill=X, expand=True)

        send_button = Button(input_frame, text="发送", command=self.send, width=8, height=1)
        send_button.pack(side=RIGHT)

    def udp_client_thread(self):
        self.client.start()
        try:
            while not self.thread_stop:
                msg, addr = self.client.recmsg()
                if msg:
                    decoded_msg = msg.decode("utf-8")
                    self.message_text.insert(END, f'[{addr}] {decoded_msg}\n')
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client.stop()
            print("Client stopped.")

    def start_udp_client(self):
        self.udp_thread = threading.Thread(target=self.udp_client_thread)
        self.udp_thread.start()

    def stop(self):
        self.thread_stop = True
        if self.udp_thread.is_alive():
            self._stop_thread(self.udp_thread)
        print("Client stopped.")

    def send(self):
        msg = self.input_entry.get().encode("utf-8")
        self.client.sendmsg(msg)
        self.message_text.insert(END, f"Client: {self.input_entry.get()}\n")
        self.input_entry.delete(0, END)

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
    client = udpclient('127.0.0.1', 52106)
    root = Tk()
    app = TalkClientApp(root, client)
    root.protocol("WM_DELETE_WINDOW", app.stop)  # Add cleanup on window close
    root.mainloop()