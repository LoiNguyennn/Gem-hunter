import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.font as tkFont
import os

class GameMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File and Level Selector")
        self.method = None
        self.file_name = None
        self.exit = False
        self.create_widgets()
        self.run_menu()
    
    def create_widgets(self):
        self.title('Hide And Seek')
        self.geometry('580x350+380+150')
        self.resizable(width=False, height=False)
        # Frame to hold the label and button
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        element_font = tkFont.Font(family="Helvetica", size=11)
        main_font = tkFont.Font(family="Helvetica", size = 12, weight= 'bold')
        font_color = ('#%02x%02x%02x' % (36, 56, 105))
        button_color = ('#%02x%02x%02x' % (69, 102, 120))
        button_font_color = ('#%02x%02x%02x' % (255, 255, 255))
        # Main label
        self.main_label = tk.Label(top_frame, text="\nGAME MENU\n", fg=font_color, font=("Helvetica", 22, "bold"))
        self.main_label.pack(side=tk.LEFT, padx=180)
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(fill=tk.X)
        
        # Label for the entry box
        self.input_label = tk.Label(self.entry_frame, text=" Input puzzle:        ", width=15, font= main_font, fg = font_color)
        self.input_label.pack(side=tk.LEFT)

        # Create an entry box for file name display and input
        self.file_name_entry = tk.Entry(self.entry_frame, width=37, font = element_font)
        self.file_name_entry.insert(0, "  file's directory path")
        self.file_name_entry.pack(side=tk.LEFT, ipadx=15)

        #Space
        self.space_label = tk.Label(text = "\n")
        self.space_label.pack()

        # Create a button to browse for files
        self.browse_button = tk.Button(self.entry_frame, text="Browse", command=self.browse_file, width = 7, font = ("Helvetica", 10, 'bold'), bg = button_color, fg= button_font_color)
        self.browse_button.pack(side=tk.LEFT)

        # Frame for the file and method selection comboboxes and their labels
        self.selection_frame = tk.Frame(self)
        self.selection_frame.pack(fill=tk.X)

        self.space_label1 = tk.Label(text = "\n")
        self.space_label1.pack()
        
        # Label for the file selection combobox
        self.file_label = tk.Label(self.selection_frame, text=" Available puzzle:", width=14, font= main_font, fg = font_color)
        self.file_label.pack(side=tk.LEFT)

        # Create a combobox for file selection
        self.file_combobox = ttk.Combobox(self.selection_frame, width=12, font = element_font)
        self.file_combobox.bind('<<ComboboxSelected>>', self.update_entry_from_combobox)
        self.file_combobox.pack(side=tk.LEFT, padx=(5, 20))

        
        # Label for the method selection combobox
        self.level_label = tk.Label(self.selection_frame, text="Choose method:", width=13, font= main_font, fg = font_color)
        self.level_label.pack(side=tk.LEFT)

        # Create a combobox for method selection
        self.level_combobox = ttk.Combobox(self.selection_frame, values=["Optimal", "Backtracking", "Brute-force"], state="readonly", width=12, font = element_font)
        self.level_combobox.pack(side=tk.LEFT, padx=(5, 20))

        
        # Create an enter button to submit the selections
        self.enter_button = tk.Button(self, text="Enter", command=self.submit, width = 10, font=("Helvetica", 10, "bold"), bg = button_color, fg= button_font_color)
        self.enter_button.pack()
        
        self.message_label = tk.Label(self, text="", fg="red", font = element_font)
        self.message_label.pack()

        # Initialize the file combobox
        self.update_file_combobox('input')

    def update_file_combobox(self, initial_dir):
        files = self.read_files(initial_dir)
        self.file_combobox['values'] = files

    def read_files(self, initial_dir):
        list_file = []
        for root, dirs, files in os.walk(initial_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_name = file[:-4]
                    list_file.append(file_name)
        return list_file

    # Function to update the entry box with the selected file name from the combobox
    def update_entry_from_combobox(self, event):
        selected_file = self.file_combobox.get()
        self.file_name_entry.delete(0, tk.END)
        self.file_name_entry.insert(0, selected_file)

    # Function to browse for a file and update the entry box with the file path
    def browse_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            self.file_name_entry.delete(0, tk.END)
            self.file_name_entry.insert(0, filepath)

    def check_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                return False
        except FileNotFoundError:
            try:
                with open('input/' + file_name + '.txt', 'r') as file:
                    return False
            except FileNotFoundError:
                return True
    # Function to submit the selected file name and method
    def submit(self):
        selected_file_name = self.file_name_entry.get()
        selected_level = self.level_combobox.get()
        foul = 0
        message = "\n"
        
        # Check if a method is selected
        if not selected_level:
            message += "You haven't chosen any method!\n"
            foul += 1
        # Check if the file name is not 'map' and the file exists
        if selected_file_name == 'map' or self.check_file(selected_file_name):
            message += "You choose the wrong directory path, please enter again.\n"
            foul += 1
        
        # If no errors, proceed with setting the values and destroying the window
        if foul == 0:
            self.file_name = selected_file_name
            self.method = selected_level
            self.destroy()
        else:
            self.message_label.config(text=message)
        
    def run_menu(self):
        self.mainloop()