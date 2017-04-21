# coding=utf-8
import Tkinter


class ConversationUI:

    def __init__(self, actionEnvoyer, actionRaccrocher, interlocuteur, tk, fromMainThread):
        #UI.UI.__init__(self)
        if fromMainThread:
            self.top = Tkinter.Toplevel(tk)
        else:
            self.top = Tkinter.Tk()
        self.actionEnvoyer = actionEnvoyer
        welcomeLabel = Tkinter.Label(self.top, text="Conversation avec "+str(interlocuteur.numTel))
        welcomeLabel.pack()

        self.conversation = ""

        self.conversationLabel = Tkinter.Label(self.top, text=self.conversation)
        self.conversationLabel.pack()

        L1 = Tkinter.Label(self.top, text="Entrez votre message")
        L1.pack()

        self.inputText = Tkinter.Entry(self.top, bd=5)
        self.inputText.pack()

        self.btnEnvoyer = Tkinter.Button(self.top, text="Parler", command=actionEnvoyer)
        self.btnEnvoyer.pack()

        self.btnRaccrocher = Tkinter.Button(self.top, text="Raccrocher", command=actionRaccrocher)
        self.btnRaccrocher.pack()

    def show(self):
        self.top.resizable(width=False, height=False)
        self.top.geometry('{}x{}'.format( 300, 200))
        self.top.mainloop()

    def ajouterMessage(self, message):
        self.conversation = self.conversation + "\n" + message
        self.conversationLabel.configure( text=self.conversation)

    def getMessage(self):
        return self.inputText.get()
