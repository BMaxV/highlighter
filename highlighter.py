import tkinter
import os
from tkinter.filedialog import askopenfilename, asksaveasfile, askdirectory

import hashlib
import json
import jinja2

class Highlighter:
    def __init__(self,width=600,height=400):
        self.root = tkinter.Tk()
        
        self.TextArea = tkinter.Text(self.root)
        self.MenuBar = tkinter.Menu(self.root)
        self.FileMenu = tkinter.Menu(self.MenuBar,tearoff=0)
        
        self.HelpMenu = tkinter.Menu(self.MenuBar,tearoff=0)
        self.ScrollBar = tkinter.Scrollbar(self.TextArea)
        self.filename = None
        
        self.highlights={}
        self.highlights_data={}
        
        #set the window text
        self.root.title("Untitled - Highlighter")

        #center the window
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        left = (screenWidth / 2) - (width / 2)
        top = (screenHeight / 2) - (height /2)

        self.root.geometry('%dx%d+%d+%d' % (width, height, left, top))

        #to make the textarea auto resizable
        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_columnconfigure(0,weight=1)

        #add controls (widget)

        self.TextArea.grid(sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)

        self.FileMenu.add_command(label="New",command=self.newFile)
        self.FileMenu.add_command(label="Open",command=self.openFile)
        self.FileMenu.add_command(label="SaveAs",command=self.saveasFile)
        self.FileMenu.add_command(label="Save",command=self.save)
        
        self.MenuBar.add_cascade(label="File",menu=self.FileMenu)
        
        self.MenuBar.add_command(label="mark selection", command=self.get_selected)
        self.MenuBar.add_command(label="make output", command=self.make_output)
        self.MenuBar.add_command(label="dump selection info", command=self.dump_info)
        self.MenuBar.add_command(label="load selection info", command=self.load_info)
        self.root.config(menu=self.MenuBar)
                
        self.ScrollBar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.ScrollBar.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=self.ScrollBar.set)
    
    def openFile(self):
        
        self.filename = askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        
        if self.filename == "":
            self.filename = None
        else:
            #try to open the file
            #set the window title
            self.root.title(os.path.basename(self.filename) + " - Highlighter")
            self.TextArea.delete(1.0,tkinter.END)
            with open(self.filename,"r") as f:
                text=f.read()
            self.TextArea.insert(1.0,text)   
            
            self.load_info() 
    
    def load_info(self):
        
        if self.filename==None:
            return
        
        fn=os.path.basename(self.filename)
        fn_x=fn.split(".")
        full_fn=fn_x[0]+"_selection_data_dump.txt"
        
        with open(full_fn,"r") as f:
            for line in f.readlines():
                loads=json.loads(line)
                loads=tuple(loads)
                self.highlights_data[loads]=None
        
        for key in self.highlights_data:
            hex_hash=self.hex_hash_tup(key)
            str1="1.0 + "+str(int(key[0]))+" chars"
            str2="1.0 + "+str(int(key[1]))+" chars"
            self.TextArea.tag_add(hex_hash,str1,str2)
            
            self.TextArea.tag_configure(hex_hash,background="red")
        
    def dump_info(self):
        fn=os.path.basename(self.filename)
        fn_x=fn.split(".")
        full_fn=fn_x[0]+"_selection_data_dump.txt"
        with open(full_fn,"w") as f:
            for key in self.highlights_data:
                dumps=json.dumps(key)
                f.write(dumps+"\n")
                
    def hex_hash_tup(self,tup):
        tup_json=json.dumps(tup)
        tup_json=tup_json.encode()
        the_hash=hashlib.sha256(tup_json)
        hex_hash=the_hash.hexdigest()
        return hex_hash
        
    def get_selected(self):
        """construct the selection tuple from the currently selected text"""
        selected_text=None
        try:
            full=self.TextArea.get("1.0","end-1c")
            #full=full.split("\n")
            self.full_text=full
            
            selected_text=self.TextArea.get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
            feh1=self.TextArea.get("1.0",tkinter.SEL_FIRST)
            guh3=self.TextArea.get("1.0",tkinter.SEL_LAST)
                        
            lines3=str(guh3)
            full_copy=str(full)
            
            #the line I'm in
            current_line=full_copy[0]
            lines3=lines3[0]
            
            start_index=len(guh3)-len(selected_text)
            end_index=len(guh3)
            
            tup=(start_index,end_index,selected_text)
            hex_hash=self.hex_hash_tup(tup)
            
            self.TextArea.tag_add(hex_hash,tkinter.SEL_FIRST,tkinter.SEL_LAST)
            self.TextArea.tag_configure(hex_hash,background="red")
            
            self.highlights.update({hex_hash:tup})
            self.highlights_data.update({tup:selected_text})
                        
        except tkinter.TclError:
            pass
        return selected_text,start_index,end_index
        
    def newFile(self):
        self.root.title("Untitled - Highlighter")
        self.filename = None
        self.TextArea.delete(1.0,tkinter.END)

    def saveasFile(self):
        #save as new file
        self.filename = asksaveasfile(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        self.filename = self.filename.name
        #print(self.filename)
        if self.filename == "":
            self.filename = None
        else:
            #try to save the file
            with open(self.filename,"w") as f:
                f.write(self.TextArea.get(1.0,tkinter.END))
            
            #change the window title
            self.root.title(os.path.basename(self.filename) + " - Notepad")
                
    def save(self):
        with open(self.filename,"w") as f:
            f.write(self.TextArea.get(1.0,tkinter.END))
            

    def run(self):
        self.root.mainloop()
    #def show_output(self):
        
    def make_output(self):
        
        full_text=self.TextArea.get("1.0","end-1c")
        keylist=list(self.highlights_data.keys())
        
        t=page("temp.html",full_text,keylist)
        fn=os.path.basename(self.filename)
        fn_x=fn.split(".")
        full_fn=fn_x[0]+"_highlights.html"
        with open(full_fn,"w") as f:
            f.write(t)
        
def page(template_filename,full_text,keylist,x="100%",y="100%"):
    with open(template_filename,"r") as f:
        t=f.read()
        
    T=jinja2.Template(t)
    
    segments=[]
    c=0
    
    add_full_text=True
    last_segment_end=0
    for key in keylist:
        
        if key[1]< last_segment_end:
            continue
        add_full_text=False
        #because of sorting this will never fail
        start=max(key[0],last_segment_end)
        seg1=full_text[last_segment_end:start]
        seg2=full_text[start:key[1]]
        
        segments.append((False,seg1))
        segments.append((True,seg2))
        last_segment_end=key[1]
        
    if last_segment_end!=0:
        segments.append((False,full_text[last_segment_end:]))
            
    if add_full_text:
        segments.append((False,full_text))
    
    html=T.render(x=x,y=y,segments=segments)
    
    return html

if __name__=="__main__":
    HL = Highlighter()
    HL.run()
