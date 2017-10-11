"""
Author: TRUONG Van Thanh
Program: Simple Text Editor
Date: 10 Oct 2017
More information about tkinter: http://tkdocs.com
How to use:
    -open command line(terminal)
    -python /path/to/simple_editor.py
Make sure you run this program with python 3(recommended version 3.4 or newer)
"""
from tkinter import *

def quit():
    """
    quit callback function: simply exit the program.
    """
    exit()
def cut_callback(context_text):
    """
    cut_callback: implement cut function(I just used built-in cut function of Text object)
    context_text: Text object
    """
    context_text.event_generate('<<Cut>>')
def copy_callback(context_text):
    """
    copy callback: implement copy function
    context_text: Text object
    """
    context_text.event_generate('<<Copy>>')
def paste_callback(context_text):
    """
    paster callback: implement paste function
    context_text: Text object
    """
    context_text.event_generate('<<Paste>>')
def undo_callback(context_text):
    """
    undo callback: implement undo function
    context_text: Text object
    """
    context_text.event_generate('<<Undo>>')
def redo_callback(context_text):
    """
    redo callback: implement redo fucntion
    context_text: Text object
    """
    context_text.event_generate('<<Redo>>')

def select_all_callback(context_text, event=None):
    """
    select all callback: implement select all function
    context_text: Text object
    """
    #just mark tag sel("selected") from beginning to the end of Text object 
    context_text.tag_add('sel', '1.0', 'end')
def find_text_callback(master, context_text, event=None):
    """
    find text callback: implement find text function
    master: the root frame(or toplevel window)
    context_text: Text object
    """
    def close_search_window():
        """
        close_search_window: remove all tag and close the search window
        """
        context_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
        return "break"
    search_toplevel = Toplevel(master)
    search_toplevel.title('Find text')
    search_toplevel.transient(master)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text='Find All:').grid(row=0, column=0,
        sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2,
        sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', 
        variable=ignore_case_value).grid(row=1, column=0, sticky='e')
    Button(search_toplevel, text="Find All", underline=0, 
        command=lambda: search_output(search_entry_widget.get(), ignore_case_value.get(),
        context_text, search_toplevel, search_entry_widget)).grid(row=0, column=0,
                sticky='e' + 'w', padx=2, pady=2)
    #we replace the close button of the find window by close_search_window function
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)

def search_output(search_string, if_ignore_case, context_text, search_toplevel, search_box):
    context_text.tag_remove('match', '1.0', END)
    """
    search_output: find search_string and add match tag to the matching text
    """
    matches_found = 0
    if search_string:
        start_pos = '1.0'
        while True:
            start_pos = context_text.search(search_string, start_pos, 
                nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(search_string))
            context_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
            context_text.tag_config('match', foreground='red', background='yellow')
            search_box.focus_set()
            search_toplevel.title('{} matches found'.format(matches_found))
    
class Editor(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
    def init_window(self):
        """
        Just define the menu of program.
        """
        self.master.title('Simple Text Editor')
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)
        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='View', menu=self.view_menu)
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)
        self.shortcut_bar = Frame(self.master, height = 25)
        self.shortcut_bar.pack(expand='no', fill='x')
        self.line_number_bar = Text(self.master, width=4, padx=3, takefocus=0, border=0,
            state='disabled', wrap='none')
        self.line_number_bar.pack(expand='no', fill='y', side='left')
        self.context_text = Text(self.master, wrap='word', undo=1)
        self.context_text.pack(expand='yes', fill='both')
        self.scroll_bar = Scrollbar(self.context_text)
        self.context_text.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.context_text.yview)
        self.scroll_bar.pack(side='right', fill='y')

        #File menu
        self.file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left', command=quit)
        self.file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left', command=quit)
        self.file_menu.add_command(label='Save', accelerator='Ctrl+S', compound='left', command=quit)
        self.file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+N', 
            compound='left', command=quit)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', accelerator='Alt+F4', compound='left', command=quit)
        #edit menu
        self.edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', compound='left', 
            command=lambda : undo_callback(self.context_text))
        self.edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound='left', 
            command=lambda : redo_callback(self.context_text))
        self.edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left', 
            command=lambda : cut_callback(self.context_text))
        self.edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left', 
            command=lambda :copy_callback(self.context_text))
        self.edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left', 
            command=lambda : paste_callback(self.context_text))
        self.edit_menu.add_command(label='Select All', accelerator='Ctrl+A', 
            compound='left', command=lambda: select_all_callback(self.context_text))
        self.edit_menu.add_command(label='Find', accelerator='Ctrl+F',
            compound='left', command=lambda: find_text_callback(self.master, self.context_text))
        
        #We bind shortcut with the function correspondence
        self.context_text.bind('<Control-x>', cut_callback(self.context_text))
        self.context_text.bind('<Control-X>', cut_callback(self.context_text))
        self.context_text.bind('<Control-c>', copy_callback(self.context_text))
        self.context_text.bind('<Control-C>', copy_callback(self.context_text))
        self.context_text.bind('<Control-v>', paste_callback(self.context_text))
        self.context_text.bind('<Control-V>', paste_callback(self.context_text))
        self.context_text.bind('<Control-z>', undo_callback(self.context_text))
        self.context_text.bind('<Control-Z>', undo_callback(self.context_text))
        self.context_text.bind('<Control-Y>', redo_callback(self.context_text))
        self.context_text.bind('<Control-Y>', redo_callback(self.context_text))
        self.context_text.bind('<Control-A>', 
            lambda:select_all_callback(self.context_text))
        self.context_text.bind('<Control-a>', 
            lambda:select_all_callback(self.context_text))
        self.context_text.bind('<Control-F>',
            lambda x: find_text_callback(self.master, self.context_text))
        self.context_text.bind('<Control-f>',
            lambda x: find_text_callback(self.master, self.context_text))

if __name__ == '__main__':
    root = Tk()
    window = Editor(root)
    root.mainloop()

