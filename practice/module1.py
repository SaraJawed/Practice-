import tkinter as tk
from tkinter import messagebox


class TodoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("To-Do List")

        # Theming (dark-ish)
        self.bg = "#0f172a"          # slate-900
        self.bg_alt = "#111827"      # gray-900
        self.surface = "#1f2937"     # gray-800
        self.accent = "#22c55e"      # green-500
        self.accent_hover = "#16a34a" # green-600
        self.text_primary = "#e5e7eb" # gray-200
        self.text_muted = "#9ca3af"   # gray-400

        self.root.configure(bg=self.bg)
        try:
            self.root.iconbitmap('')
        except Exception:
            pass

        self.tasks = []

        # Root layout container for screens
        self.container = tk.Frame(self.root, bg=self.bg)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Screens registry
        self.frames = {}
        for FrameClass in (WelcomeScreen, ViewScreen, AddScreen, DeleteScreen, UpdateScreen):
            frame = FrameClass(self)
            self.frames[FrameClass.__name__] = frame
            frame.frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeScreen")

    def show_frame(self, name: str) -> None:
        frame = self.frames[name]
        # Allow screens to refresh their content when shown
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.frame.tkraise()

    def refresh_all_lists(self) -> None:
        for frame in self.frames.values():
            if hasattr(frame, "refresh"):
                frame.refresh()

    def add_task(self) -> None:
        # Add screen holds its own entry
        add_screen = self.frames["AddScreen"]
        text = add_screen.entry.get().strip()
        if not text:
            messagebox.showinfo("Empty Task", "Please enter a task before adding.")
            return
        self.tasks.append(text)
        add_screen.entry.delete(0, tk.END)
        self.refresh_all_lists()
        add_screen.entry.focus_set()

    def remove_selected(self) -> None:
        delete_screen = self.frames["DeleteScreen"]
        selection = delete_screen.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a task to remove.")
            return
        for index in sorted(selection, reverse=True):
            self.tasks.pop(index)
        self.refresh_all_lists()

    def clear_all(self) -> None:
        if not self.tasks:
            return
        if messagebox.askyesno("Clear All", "Remove all tasks?"):
            self.tasks.clear()
            self.refresh_all_lists()

    # Helpers: styling and placeholder
    def _add_hover(self, button: tk.Button, base: str, hover: str) -> None:
        def on_enter(_):
            button.configure(bg=hover)
        def on_leave(_):
            button.configure(bg=base)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def _update_status_text(self) -> str:
        count = len(self.tasks)
        return f"{count} task" if count == 1 else f"{count} tasks"


class BaseScreen:
    def __init__(self, app: TodoApp):
        self.app = app
        self.frame = tk.Frame(self.app.container, bg=self.app.bg)

    def nav_button(self, parent: tk.Widget, text: str, command, bg: str) -> tk.Button:
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            activebackground=bg,
            fg="#06110a",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=14,
            pady=10
        )
        self.app._add_hover(btn, bg, bg)
        return btn


class WelcomeScreen(BaseScreen):
    def __init__(self, app: TodoApp):
        super().__init__(app)
        title = tk.Label(self.frame, text="Welcome", bg=self.app.bg, fg=self.app.text_primary, font=("Segoe UI", 20, "bold"))
        subtitle = tk.Label(self.frame, text="What would you like to do?", bg=self.app.bg, fg=self.app.text_muted, font=("Segoe UI", 12))
        title.grid(row=0, column=0, padx=16, pady=(16, 4), sticky="w")
        subtitle.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="w")

        grid = tk.Frame(self.frame, bg=self.app.bg)
        grid.grid(row=2, column=0, padx=16, pady=16, sticky="nsew")

        buttons = [
            ("View tasks", lambda: self.app.show_frame("ViewScreen"), self.app.accent),
            ("Add a task", lambda: self.app.show_frame("AddScreen"), "#60a5fa"),
            ("Delete a task", lambda: self.app.show_frame("DeleteScreen"), "#f87171"),
            ("Update a task", lambda: self.app.show_frame("UpdateScreen"), "#fbbf24"),
        ]
        for i, (label, cmd, color) in enumerate(buttons):
            btn = self.nav_button(grid, label, cmd, color)
            btn.grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="ew")

        self.frame.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)


class ViewScreen(BaseScreen):
    def __init__(self, app: TodoApp):
        super().__init__(app)
        header = tk.Label(self.frame, text="View Tasks", bg=self.app.bg, fg=self.app.text_primary, font=("Segoe UI", 18, "bold"))
        header.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")

        list_frame = tk.Frame(self.frame, bg=self.app.bg)
        list_frame.grid(row=1, column=0, padx=12, pady=(0, 8), sticky="nsew")
        self.listbox = tk.Listbox(list_frame, height=16, activestyle="dotbox", bg=self.app.surface, fg=self.app.text_primary, selectbackground="#334155", selectforeground=self.app.text_primary, highlightthickness=0, relief="flat", font=("Segoe UI", 11))
        self.listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview, bg=self.app.bg)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        footer = tk.Frame(self.frame, bg=self.app.bg_alt)
        self.status = tk.Label(footer, text="", anchor="w", bg=self.app.bg_alt, fg=self.app.text_muted, font=("Segoe UI", 9))
        self.status.pack(fill="x", padx=8, pady=4)
        footer.grid(row=2, column=0, sticky="ew")

        nav = tk.Frame(self.frame, bg=self.app.bg)
        back = self.nav_button(nav, "Back", lambda: self.app.show_frame("WelcomeScreen"), "#94a3b8")
        back.pack(side="left", padx=8, pady=8)
        nav.grid(row=3, column=0, sticky="w")

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def refresh(self) -> None:
        self.listbox.delete(0, tk.END)
        for task in self.app.tasks:
            self.listbox.insert(tk.END, task)
        self.status.configure(text=self.app._update_status_text())

    def on_show(self) -> None:
        self.refresh()


class AddScreen(BaseScreen):
    def __init__(self, app: TodoApp):
        super().__init__(app)
        header = tk.Label(self.frame, text="Add Task", bg=self.app.bg, fg=self.app.text_primary, font=("Segoe UI", 18, "bold"))
        header.grid(row=0, column=0, columnspan=2, padx=12, pady=(12, 8), sticky="w")

        input_frame = tk.Frame(self.frame, bg=self.app.bg)
        input_frame.grid(row=1, column=0, columnspan=2, padx=12, pady=(0, 8), sticky="ew")
        self.entry = tk.Entry(input_frame, width=60, bg=self.app.surface, fg=self.app.text_primary, insertbackground=self.app.text_primary, relief="flat", font=("Segoe UI", 11))
        self.entry.grid(row=0, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        placeholder = "Describe your task..."
        self.placeholder = placeholder
        self.entry.insert(0, placeholder)
        self.entry.configure(fg=self.app.text_muted)
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._apply_placeholder)

        add_btn = tk.Button(input_frame, text="Add", command=self.app.add_task, bg=self.app.accent, activebackground=self.app.accent_hover, fg="#06110a", relief="flat", font=("Segoe UI", 10, "bold"), padx=12, pady=6)
        add_btn.grid(row=0, column=1, padx=(8, 0))
        self.app._add_hover(add_btn, self.app.accent, self.app.accent_hover)

        nav = tk.Frame(self.frame, bg=self.app.bg)
        back = self.nav_button(nav, "Back", lambda: self.app.show_frame("WelcomeScreen"), "#94a3b8")
        back.pack(side="left", padx=8, pady=8)
        nav.grid(row=2, column=0, sticky="w")

        self.frame.grid_columnconfigure(0, weight=1)

        self.entry.bind("<Return>", lambda _: self.app.add_task())

    def _apply_placeholder(self, _event=None) -> None:
        if not self.entry.get().strip():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.placeholder)
            self.entry.configure(fg=self.app.text_muted)

    def _clear_placeholder(self, _event=None) -> None:
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=self.app.text_primary)

    def on_show(self) -> None:
        self.entry.focus_set()


class DeleteScreen(BaseScreen):
    def __init__(self, app: TodoApp):
        super().__init__(app)
        header = tk.Label(self.frame, text="Delete Tasks", bg=self.app.bg, fg=self.app.text_primary, font=("Segoe UI", 18, "bold"))
        header.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")

        list_frame = tk.Frame(self.frame, bg=self.app.bg)
        list_frame.grid(row=1, column=0, padx=12, pady=(0, 8), sticky="nsew")
        self.listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, height=16, activestyle="dotbox", bg=self.app.surface, fg=self.app.text_primary, selectbackground="#7c2d12", selectforeground=self.app.text_primary, highlightthickness=0, relief="flat", font=("Segoe UI", 11))
        self.listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview, bg=self.app.bg)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        buttons = tk.Frame(self.frame, bg=self.app.bg)
        delete_btn = self.nav_button(buttons, "Remove Selected", self.app.remove_selected, "#ef4444")
        delete_btn.pack(side="left", padx=8, pady=8)
        back = self.nav_button(buttons, "Back", lambda: self.app.show_frame("WelcomeScreen"), "#94a3b8")
        back.pack(side="left", padx=8, pady=8)
        buttons.grid(row=2, column=0, sticky="w")

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.listbox.bind("<Delete>", lambda _: self.app.remove_selected())

    def refresh(self) -> None:
        self.listbox.delete(0, tk.END)
        for task in self.app.tasks:
            self.listbox.insert(tk.END, task)

    def on_show(self) -> None:
        self.refresh()


class UpdateScreen(BaseScreen):
    def __init__(self, app: TodoApp):
        super().__init__(app)
        header = tk.Label(self.frame, text="Update Task", bg=self.app.bg, fg=self.app.text_primary, font=("Segoe UI", 18, "bold"))
        header.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")

        content = tk.Frame(self.frame, bg=self.app.bg)
        content.grid(row=1, column=0, padx=12, pady=(0, 8), sticky="nsew")

        # List on the left
        left = tk.Frame(content, bg=self.app.bg)
        left.grid(row=0, column=0, sticky="nsew")
        self.listbox = tk.Listbox(left, height=14, activestyle="dotbox", bg=self.app.surface, fg=self.app.text_primary, selectbackground="#334155", selectforeground=self.app.text_primary, highlightthickness=0, relief="flat", font=("Segoe UI", 11))
        self.listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(left, orient="vertical", command=self.listbox.yview, bg=self.app.bg)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=scrollbar.set)
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        # Editor on the right
        right = tk.Frame(content, bg=self.app.bg)
        right.grid(row=0, column=1, padx=(12, 0), sticky="nsew")
        label = tk.Label(right, text="New text", bg=self.app.bg, fg=self.app.text_muted, font=("Segoe UI", 10))
        label.grid(row=0, column=0, sticky="w")
        self.entry = tk.Entry(right, width=40, bg=self.app.surface, fg=self.app.text_primary, insertbackground=self.app.text_primary, relief="flat", font=("Segoe UI", 11))
        self.entry.grid(row=1, column=0, sticky="ew", pady=(4, 8))
        save = tk.Button(right, text="Save", command=self._save_update, bg=self.app.accent, activebackground=self.app.accent_hover, fg="#06110a", relief="flat", font=("Segoe UI", 10, "bold"), padx=12, pady=6)
        save.grid(row=2, column=0, sticky="w")
        self.app._add_hover(save, self.app.accent, self.app.accent_hover)

        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        nav = tk.Frame(self.frame, bg=self.app.bg)
        back = self.nav_button(nav, "Back", lambda: self.app.show_frame("WelcomeScreen"), "#94a3b8")
        back.pack(side="left", padx=8, pady=8)
        nav.grid(row=2, column=0, sticky="w")

        self.listbox.bind("<<ListboxSelect>>", self._load_selected)

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def _load_selected(self, _event=None) -> None:
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.app.tasks[index])

    def _save_update(self) -> None:
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a task to update.")
            return
        index = selection[0]
        new_text = self.entry.get().strip()
        if not new_text:
            messagebox.showinfo("Empty Text", "Please enter new text for the task.")
            return
        self.app.tasks[index] = new_text
        self.app.refresh_all_lists()
        self.listbox.selection_clear(0, tk.END)
        self.entry.delete(0, tk.END)

    def refresh(self) -> None:
        self.listbox.delete(0, tk.END)
        for task in self.app.tasks:
            self.listbox.insert(tk.END, task)

    def on_show(self) -> None:
        self.refresh()


def main() -> None:
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
