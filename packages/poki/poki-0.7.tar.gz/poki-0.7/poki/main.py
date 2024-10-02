import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import re
import sys
import os
import argparse
import json
import time
from threading import Thread
import psutil

class PortManager:
    def __init__(self, use_gui=False):
        self.use_gui = use_gui
        self.ports = []
        self.favorites = self.load_favorites()
        self.history = self.load_history()

        # Define paths for favorites and history
        self.config_dir = os.path.join(os.path.expanduser("~"), ".poki")
        os.makedirs(self.config_dir, exist_ok=True)
        self.favorites_file = os.path.join(self.config_dir, 'favorites.json')
        self.history_file = os.path.join(self.config_dir, 'history.json')

        if self.use_gui:
            self.root = tk.Tk()
            self.root.title("Poki - Port Killer")
            self.root.geometry("800x600")
            self.create_widgets()

        self.update_port_list()

    def create_widgets(self):
        try:
            main_frame = ttk.Frame(self.root)
            main_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

            # Port List Frame
            list_frame = ttk.LabelFrame(main_frame, text="Port List")
            list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

            self.tree = ttk.Treeview(list_frame, columns=('Port', 'PID', 'Process', 'Status'), show='headings')
            self.tree.heading('Port', text='Port')
            self.tree.heading('PID', text='PID')
            self.tree.heading('Process', text='Process')
            self.tree.heading('Status', text='Status')
            self.tree.column('Port', width=80, anchor='center')
            self.tree.column('PID', width=80, anchor='center')
            self.tree.column('Process', width=200, anchor='w')
            self.tree.column('Status', width=100, anchor='center')
            self.tree.pack(fill=tk.BOTH, expand=1)

            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.tree.configure(yscrollcommand=scrollbar.set)

            # Control Frame
            control_frame = ttk.Frame(main_frame)
            control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

            # Refresh Button
            self.refresh_button = ttk.Button(control_frame, text="Refresh", command=self.update_port_list)
            self.refresh_button.pack(fill=tk.X, pady=2)

            # Port Entry and Kill Button
            port_frame = ttk.Frame(control_frame)
            port_frame.pack(fill=tk.X, pady=2)
            self.port_entry = ttk.Entry(port_frame, width=15)
            self.port_entry.pack(side=tk.LEFT, padx=2)
            self.kill_button = ttk.Button(port_frame, text="Kill Process", command=self.kill_process)
            self.kill_button.pack(side=tk.LEFT, padx=2)

            # Favorites Frame
            fav_frame = ttk.LabelFrame(control_frame, text="Favorites")
            fav_frame.pack(fill=tk.X, pady=2)
            self.fav_listbox = tk.Listbox(fav_frame, height=5)
            self.fav_listbox.pack(fill=tk.X)
            self.update_favorites_list()

            fav_button_frame = ttk.Frame(fav_frame)
            fav_button_frame.pack(fill=tk.X)
            ttk.Button(fav_button_frame, text="Add", command=self.add_favorite).pack(side=tk.LEFT, padx=2)
            ttk.Button(fav_button_frame, text="Remove", command=self.remove_favorite).pack(side=tk.LEFT, padx=2)

            # History Frame
            history_frame = ttk.LabelFrame(control_frame, text="History")
            history_frame.pack(fill=tk.X, pady=2)
            self.history_listbox = tk.Listbox(history_frame, height=5)
            self.history_listbox.pack(fill=tk.X)
            self.update_history_list()

            # Auto-refresh Checkbox
            self.auto_refresh_var = tk.BooleanVar()
            self.auto_refresh_checkbox = ttk.Checkbutton(
                control_frame, text="Auto-refresh", variable=self.auto_refresh_var,
                command=self.toggle_auto_refresh
            )
            self.auto_refresh_checkbox.pack(fill=tk.X, pady=2)

            # Start auto-refresh loop
            self.root.after(1000, self.auto_refresh_loop)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating widgets: {e}")

    def update_port_list(self):
        try:
            self.ports.clear()
            connections = psutil.net_connections()
            for conn in connections:
                if conn.status == 'LISTEN' and conn.laddr:
                    try:
                        process = psutil.Process(conn.pid) if conn.pid else None
                        self.ports.append({
                            'port': conn.laddr.port,
                            'pid': conn.pid if conn.pid else 'N/A',
                            'process': process.name() if process else 'Unknown',
                            'status': conn.status
                        })
                    except psutil.NoSuchProcess:
                        self.ports.append({
                            'port': conn.laddr.port,
                            'pid': 'N/A',
                            'process': 'Unknown',
                            'status': conn.status
                        })

            if self.use_gui:
                # Clear existing entries
                for item in self.tree.get_children():
                    self.tree.delete(item)
                # Insert updated port information
                for port in self.ports:
                    self.tree.insert('', 'end', values=(
                        port['port'],
                        port['pid'],
                        port['process'],
                        port['status']
                    ))
            else:
                # Command-line mode: print port information
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{'Port':<10}{'PID':<10}{'Process':<25}{'Status':<15}")
                print('-' * 60)
                for port in self.ports:
                    print(f"{port['port']:<10}{port['pid']:<10}{port['process']:<25}{port['status']:<15}")
        except Exception as e:
            if self.use_gui:
                messagebox.showerror("Error", f"An error occurred while updating port list: {e}")
            else:
                print(f"Error updating port list: {e}")

    def kill_process(self):
        try:
            if self.use_gui:
                port = self.port_entry.get().strip()
            else:
                port = input("Enter port number to kill: ").strip()

            if not port.isdigit():
                if self.use_gui:
                    messagebox.showerror("Invalid Input", "Please enter a valid port number.")
                else:
                    print("Invalid port number. Please enter a numeric value.")
                return

            port = int(port)
            for p in self.ports:
                if p['port'] == port:
                    try:
                        if p['pid'] == 'N/A':
                            if self.use_gui:
                                messagebox.showwarning("No PID", f"No PID found for port {port}.")
                            else:
                                print(f"No PID found for port {port}.")
                            return
                        process = psutil.Process(p['pid'])
                        process.terminate()
                        process.wait(timeout=3)
                        self.add_to_history(f"Killed process on port {port} (PID: {p['pid']})")
                        if self.use_gui:
                            messagebox.showinfo("Process Killed",
                                                f"Process on port {port} (PID: {p['pid']}) has been terminated.")
                        else:
                            print(f"Process on port {port} (PID: {p['pid']}) has been terminated.")
                        self.update_port_list()
                        return
                    except psutil.NoSuchProcess:
                        if self.use_gui:
                            messagebox.showerror("Error", f"Process on port {port} no longer exists.")
                        else:
                            print(f"Error: Process on port {port} no longer exists.")
                        return
                    except psutil.AccessDenied:
                        if self.use_gui:
                            messagebox.showerror("Access Denied", f"Insufficient permissions to kill process on port {port}.")
                        else:
                            print(f"Error: Insufficient permissions to kill process on port {port}.")
                        return
                    except psutil.TimeoutExpired:
                        if self.use_gui:
                            messagebox.showerror("Timeout", f"Failed to terminate process on port {port} within timeout.")
                        else:
                            print(f"Error: Failed to terminate process on port {port} within timeout.")
                        return

            # If port not found
            if self.use_gui:
                messagebox.showwarning("Port Not Found", f"No process found using port {port}.")
            else:
                print(f"No process found using port {port}.")
        except Exception as e:
            if self.use_gui:
                messagebox.showerror("Error", f"An error occurred while killing process: {e}")
            else:
                print(f"Error killing process: {e}")

    def load_favorites(self):
        try:
            config_dir = os.path.join(os.path.expanduser("~"), ".poki")
            os.makedirs(config_dir, exist_ok=True)
            favorites_path = os.path.join(config_dir, 'favorites.json')
            if os.path.exists(favorites_path):
                with open(favorites_path, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading favorites: {e}")
            return []
    def save_favorites(self):
        try:
            with open(self.favorites_file, 'w') as f:
                json.dump(self.favorites, f, indent=4)
        except Exception as e:
            if self.use_gui:
                messagebox.showerror("Error", f"Failed to save favorites: {e}")
            else:
                print(f"Error saving favorites: {e}")

    def update_favorites_list(self):
        try:
            self.fav_listbox.delete(0, tk.END)
            for fav in self.favorites:
                self.fav_listbox.insert(tk.END, fav)
        except Exception as e:
            if self.use_gui:
                messagebox.showerror("Error", f"Failed to update favorites list: {e}")
            else:
                print(f"Error updating favorites list: {e}")

    def add_favorite(self):
        try:
            port = simpledialog.askstring("Add Favorite", "Enter port number:")
            if port:
                port = port.strip()
                if not port.isdigit():
                    messagebox.showerror("Invalid Input", "Please enter a valid numeric port number.")
                    return
                if port not in self.favorites:
                    self.favorites.append(port)
                    self.save_favorites()
                    self.update_favorites_list()
                    self.add_to_history(f"Added port {port} to favorites")
                else:
                    messagebox.showinfo("Already Exists", f"Port {port} is already in favorites.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add favorite: {e}")

    def remove_favorite(self):
        try:
            selection = self.fav_listbox.curselection()
            if selection:
                port = self.fav_listbox.get(selection[0])
                self.favorites.remove(port)
                self.save_favorites()
                self.update_favorites_list()
                self.add_to_history(f"Removed port {port} from favorites")
            else:
                messagebox.showwarning("No Selection", "Please select a port to remove.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove favorite: {e}")

    def load_history(self):
        try:
            config_dir = os.path.join(os.path.expanduser("~"), ".ag_port_killer")
            os.makedirs(config_dir, exist_ok=True)
            history_path = os.path.join(config_dir, 'history.json')
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading history: {e}")
            return []

    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            if self.use_gui:
                messagebox.showerror("Error", f"Failed to save history: {e}")
            else:
                print(f"Error saving history: {e}")

    def add_to_history(self, action):
        try:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            self.history.append(f"{timestamp} - {action}")
            if len(self.history) > 100:  # Keep only last 100 actions
                self.history = self.history[-100:]
            self.save_history()
            if self.use_gui:
                self.update_history_list()
        except Exception as e:
            if self.use_gui:
                messagebox.showerror("Error", f"Failed to add to history: {e}")
            else:
                print(f"Error adding to history: {e}")

    def update_history_list(self):
        try:
            self.history_listbox.delete(0, tk.END)
            for action in reversed(self.history):
                self.history_listbox.insert(tk.END, action)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update history list: {e}")

    def toggle_auto_refresh(self):
        try:
            if self.auto_refresh_var.get():
                self.add_to_history("Enabled auto-refresh")
            else:
                self.add_to_history("Disabled auto-refresh")
        except Exception as e:
            if self.use_gui:
                messagebox.showerror("Error", f"Failed to toggle auto-refresh: {e}")
            else:
                print(f"Error toggling auto-refresh: {e}")

    def auto_refresh_loop(self):
        try:
            if self.use_gui:
                if self.auto_refresh_var.get():
                    self.update_port_list()
                self.root.after(5000, self.auto_refresh_loop)  # Schedule next check in 5 seconds
        except Exception as e:
            if self.use_gui:
                messagebox.showerror("Error", f"Auto-refresh error: {e}")
            else:
                print(f"Auto-refresh error: {e}")

    def run(self):
        if self.use_gui:
            self.root.mainloop()
        else:
            while True:
                try:
                    print("\nAG Port Killer Menu:")
                    print("1. Show used ports")
                    print("2. Kill a process by port")
                    print("3. Add favorite port")
                    print("4. Remove favorite port")
                    print("5. Show favorites")
                    print("6. Show history")
                    print("7. Exit")
                    choice = input("Enter your choice: ").strip()

                    if choice == '1':
                        self.update_port_list()
                        input("\nPress Enter to continue...")
                    elif choice == '2':
                        self.kill_process()
                        input("\nPress Enter to continue...")
                    elif choice == '3':
                        port = input("Enter port number to add to favorites: ").strip()
                        if port.isdigit():
                            if port not in self.favorites:
                                self.favorites.append(port)
                                self.save_favorites()
                                print(f"Added port {port} to favorites.")
                                self.add_to_history(f"Added port {port} to favorites")
                            else:
                                print(f"Port {port} is already in favorites.")
                        else:
                            print("Invalid port number. Please enter a numeric value.")
                        input("\nPress Enter to continue...")
                    elif choice == '4':
                        port = input("Enter port number to remove from favorites: ").strip()
                        if port in self.favorites:
                            self.favorites.remove(port)
                            self.save_favorites()
                            print(f"Removed port {port} from favorites.")
                            self.add_to_history(f"Removed port {port} from favorites")
                        else:
                            print(f"Port {port} is not in favorites.")
                        input("\nPress Enter to continue...")
                    elif choice == '5':
                        if self.favorites:
                            print("Favorite ports:", ', '.join(self.favorites))
                        else:
                            print("No favorite ports.")
                        input("\nPress Enter to continue...")
                    elif choice == '6':
                        if self.history:
                            print("History:")
                            for action in reversed(self.history):
                                print(action)
                        else:
                            print("No history available.")
                        input("\nPress Enter to continue...")
                    elif choice == '7':
                        print("Exiting...")
                        break
                    else:
                        print("Invalid choice. Please try again.")
                        input("\nPress Enter to continue...")
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except Exception as e:
                    print(f"An error occurred: {e}")
                    input("\nPress Enter to continue...")

def main():
    parser = argparse.ArgumentParser(description="AG Port Killer")
    parser.add_argument("--gui", action="store_true", help="Use GUI mode")
    args = parser.parse_args()

    manager = PortManager(use_gui=args.gui)
    manager.run()

if __name__ == "__main__":
    main()
