import sys
import tkinter as tk

import yaml

sys.path.append("../shared")

import grpc
import xee_pb2 as pb2
import xee_pb2_grpc as pb2_grpc

class Xeet:
    def __init__(self, parent, master, author, text, liked, likes, uuid):
        self.parent = parent
        self.liked = liked
        self.likes = likes
        self.uuid = uuid
        
        self.box = tk.Frame(master, bg='#000')
        
        self.author = tk.Label(self.box, text=author, font=("Arial", 16), justify="left", bg="#000", fg="#fff")

        self.text = tk.Text(self.box, width=40, height=10, bg="#000", fg="#fff")
        self.text.replace("1.0", "end", text)
        self.text.config(state='disabled')

        self.like = tk.Button(self.box, font=("Arial", 20), width=3, height=1, text=["♡", "♥"][self.liked], bg='#000', fg="#f00", command=self.like)

        self.likeIcon = tk.Label(self.box, text="♥", font=("Arial", 20), bg='#000', fg="#f00")
        self.likeCount = tk.Label(self.box, anchor="w", text=str(self.likes), font=("Arial", 20), bg='#000', fg="#fff")

        self.author.grid(row=0, column=0, sticky="W", columnspan=2)
        self.text.grid(row=1, column=0, sticky="we", columnspan=2)
        self.like.grid(row=1, column=2, padx=10)
        self.likeIcon.grid(row=2, column=0, padx=10, sticky="W")
        self.likeCount.grid(row=2, column=1, sticky="W")
        self.box.columnconfigure(1, weight=1)

        self.box.pack(pady=10, padx=10)

    def like(self):
        success, likes = self.parent.like(self.uuid, not self.liked)
        if not success:
            return
        
        self.liked = not self.liked
        self.like.configure(text=["♡", "♥"][self.liked])
        
        self.likes = likes
        self.likeCount.configure(text=str(self.likes))

    def clean(self):
        self.box.pack_forget()

class App:
    stubs = {}
    
    def __init__(self):
        self.window = tk.Tk()

        self.window.title("Xee - a social media service")

        self.window.configure(bg='#000')
        self.window.geometry("430x500")
        self.window.resizable(width=False, height=False)

        self.canvas = tk.Canvas(self.window, borderwidth=0, bg='#000')
        self.frame= tk.Frame(self.canvas, bg='#000')
        vsb = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.create_window((4, 5), window=self.frame, anchor="nw")

        self.canvas.update_idletasks() 
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.username = None
        self.token = None
        self.xeetdisplays = []

        self.gen_stubs()

        self.controlPanelLoggedIn = tk.Frame(self.window, bg='#000')

        post = tk.Button(self.controlPanelLoggedIn, text = "Post", command=self.post_xeet)
        self.xeet = tk.Text(self.controlPanelLoggedIn, width=40, height=10)
        logout = tk.Button(self.controlPanelLoggedIn, text = "Log Out", command=self.logout)
        update = tk.Button(self.controlPanelLoggedIn, text = "Refresh", command=self.update)

        post.grid(row=0, column=1, padx=10)
        update.grid(row=1, column=1, padx=10)
        logout.grid(row=2, column=1, padx=10)
        self.xeet.grid(row=0, column=0, padx=10, pady=10, rowspan=3)

        self.controlPanelUnauthorized = tk.Frame(self.window, bg='#000')
        self.name = tk.Entry(self.controlPanelUnauthorized)
        login = tk.Button(self.controlPanelUnauthorized, text="Log In", command=self.login)
        update = tk.Button(self.controlPanelUnauthorized, text="Refresh", command=self.update)

        self.name.grid(row=0, column=0, padx=10, rowspan=2)
        login.grid(row=0, column=1, padx=10, pady=10)
        update.grid(row=1, column=1, padx=10, pady=10)
        
        self.controlPanelUnauthorized.pack()

        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self.graceful_exit)
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            self.graceful_exit()

    def like(self, xeet_id, new_status):
        if self.token is None:
            return False, -1
        
        resp = self.stubs['like'].Like(pb2.LikeData(token=self.token, xeet_id=xeet_id, liked=new_status))
        return resp.success, resp.likes

    def post_xeet(self):
        text = self.xeet.get("1.0", 'end')
        if text == "" or self.token is None:
            return 
        
        self.stubs['post'].PostXeet(pb2.PostXeetData(token=self.token, text=text))
        self.update()
        
        self.xeet.delete("1.0", 'end')

    def logout(self):
        self.stubs['auth'].RevokeToken(pb2.UserData(token=self.token))
        
        self.username = None
        self.token = None
        
        self.update()

        self.controlPanelLoggedIn.pack_forget()
        self.controlPanelUnauthorized.pack()

    def login(self):
        self.username = self.name.get()
        if self.username == "":
            return
        
        self.token = self.stubs['auth'].AuthUser(pb2.AuthData(username = self.username)).token

        self.update()
        
        self.controlPanelLoggedIn.pack()
        self.controlPanelUnauthorized.pack_forget()

    def update(self):
        if self.token is not None:
            data = pb2.UserData(token=self.token)
        else:
            data = pb2.UserData()
        feed = self.stubs['get'].RetrieveFeed(data).feed

        for i in self.xeetdisplays:
            i.clean()
        self.xeetdisplays.clear()

        for i in feed:
            self.xeetdisplays.append(Xeet(self, self.frame, i.poster, i.text, i.liked, i.likes, i.id))

        self.canvas.update_idletasks() 
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def gen_stubs(self):
        config = yaml.safe_load(open("../shared/config.yaml"))['service-ips']
        
        channel = grpc.insecure_channel(config['post'])
        self.stubs['post'] = pb2_grpc.PosterStub(channel)

        channel = grpc.insecure_channel(config['auth'])
        self.stubs['auth'] = pb2_grpc.AuthenticatorStub(channel)
        
        channel = grpc.insecure_channel(config['get'])
        self.stubs['get'] = pb2_grpc.RetrieverStub(channel)
        
        channel = grpc.insecure_channel(config['like'])
        self.stubs['like'] = pb2_grpc.LikerStub(channel)

    def graceful_exit(self):
        if self.token is not None:
            self.logout()
        self.window.destroy()


if __name__ == "__main__":
    App()
