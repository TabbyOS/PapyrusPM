import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, scrolledtext
import os
from utils import (
    init_logging, log_info, log_error,
    create_project, is_valid_project,
    get_log_file_path, read_log_content,
    load_settings, save_settings
)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates", "default_project_config.json")
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "papyruspm_config.json"))

# -------------------------------
# New Project Dialog
# -------------------------------
def create_new_project():
    def submit():
        project_name = name_entry.get().strip()
        target_dir = path_entry.get().strip()

        if not project_name:
            messagebox.showerror("Error", "Project name cannot be empty.")
            return
        if not os.path.isdir(target_dir):
            messagebox.showerror("Error", "Target directory is invalid.")
            return

        success = create_project(project_name, target_dir, TEMPLATE_DIR)
        if success:
            messagebox.showinfo("Success", f"Project '{project_name}' created.")
            log_info(f"Created new project: {os.path.join(target_dir, project_name)}")
            window.destroy()
        else:
            messagebox.showerror("Error", "Failed to create project. It may already exist.")

    def browse_path():
        selected = filedialog.askdirectory(title="Choose Project Folder")
        if selected:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, selected)

    window = tk.Toplevel()
    window.title("Create New Project")
    window.geometry("400x180")

    tk.Label(window, text="Project Name:").pack(pady=5)
    name_entry = tk.Entry(window, width=40)
    name_entry.pack(pady=5)

    tk.Label(window, text="Target Directory:").pack(pady=5)
    path_frame = tk.Frame(window)
    path_entry = tk.Entry(path_frame, width=30)
    path_entry.pack(side=tk.LEFT)
    tk.Button(path_frame, text="Browse", command=browse_path).pack(side=tk.LEFT, padx=5)
    path_frame.pack(pady=5)

    tk.Button(window, text="Create Project", command=submit).pack(pady=10)

# -------------------------------
# Build Project (Dummy)
# -------------------------------
def build_project():
    selected = filedialog.askdirectory(title="Select Project to Build")
    if not selected:
        return

    if not is_valid_project(selected):
        messagebox.showerror("Error", "Selected folder is not a valid project.")
        return

    # Hier könnte die echte Build-Logik integriert werden
    messagebox.showinfo("Build", f"Building project at:\n{selected}")
    log_info(f"Build triggered for project: {selected}")

# -------------------------------
# Settings Dialog (persistent)
# -------------------------------
def open_settings():
    settings = load_settings(CONFIG_PATH)
    current_path = settings.get("compiler_path", "")

    compiler_path = simpledialog.askstring("Settings", "Set path to Papyrus Compiler:", initialvalue=current_path)
    if compiler_path is not None:  # also allows empty string to clear path
        settings["compiler_path"] = compiler_path
        saved = save_settings(CONFIG_PATH, settings)
        if saved:
            messagebox.showinfo("Settings", f"Compiler path set to:\n{compiler_path}")
            log_info(f"Compiler path updated to: {compiler_path}")
        else:
            messagebox.showerror("Error", "Failed to save settings.")
    else:
        log_info("Settings dialog cancelled or empty input.")

# -------------------------------
# View Log Window
# -------------------------------
def view_log():
    log_path = get_log_file_path()
    if not os.path.isfile(log_path):
        messagebox.showwarning("Log Not Found", "No log file found.")
        return

    log_window = tk.Toplevel()
    log_window.title("Application Log")
    log_window.geometry("600x400")

    text_area = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=("Courier", 10))
    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    content = read_log_content(1000)
    text_area.insert(tk.END, content)
    text_area.config(state=tk.DISABLED)
    log_info("Log file viewed.")

# -------------------------------
# Main GUI
# -------------------------------
def launch_gui():
    init_logging()
    root = tk.Tk()
    root.title("Papyrus Project Manager")
    root.geometry("400x300")

    tk.Label(root, text="Papyrus Project Manager", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="New Project", width=30, command=create_new_project).pack(pady=5)
    tk.Button(root, text="Build Project", width=30, command=build_project).pack(pady=5)
    tk.Button(root, text="Settings", width=30, command=open_settings).pack(pady=5)
    tk.Button(root, text="View Log", width=30, command=view_log).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit, width=30).pack(pady=5)

    root.mainloop()
