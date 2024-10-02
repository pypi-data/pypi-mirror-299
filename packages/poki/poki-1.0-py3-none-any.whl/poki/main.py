import os
import sys
import time
import json
import psutil
import argparse
from tabulate import tabulate
from colorama import init, Fore, Style

init(autoreset=True)

class AdvancedCLIPortManager:
    def __init__(self):
        self.ports = []
        self.favorites = self.load_favorites()
        self.history = self.load_history()
        self.config_dir = os.path.join(os.path.expanduser("~"), ".poki")
        os.makedirs(self.config_dir, exist_ok=True)
        self.favorites_file = os.path.join(self.config_dir, 'favorites.json')
        self.history_file = os.path.join(self.config_dir, 'history.json')

    def load_favorites(self):
        try:
            if os.path.exists(self.favorites_file):
                with open(self.favorites_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading favorites: {e}")
            return []

    def save_favorites(self):
        try:
            with open(self.favorites_file, 'w') as f:
                json.dump(self.favorites, f, indent=4)
        except Exception as e:
            print(f"Error saving favorites: {e}")

    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading history: {e}")
            return []

    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_to_history(self, action):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.history.append(f"{timestamp} - {action}")
        if len(self.history) > 100:
            self.history = self.history[-100:]
        self.save_history()

    def update_port_list(self):
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

    def display_ports(self):
        headers = ["Port", "PID", "Process", "Status"]
        table_data = [[p['port'], p['pid'], p['process'], p['status']] for p in self.ports]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def kill_process(self, port):
        for p in self.ports:
            if p['port'] == port:
                try:
                    if p['pid'] == 'N/A':
                        print(f"{Fore.YELLOW}No PID found for port {port}.")
                        return
                    process = psutil.Process(p['pid'])
                    process.terminate()
                    process.wait(timeout=3)
                    self.add_to_history(f"Killed process on port {port} (PID: {p['pid']})")
                    print(f"{Fore.GREEN}Process on port {port} (PID: {p['pid']}) has been terminated.")
                    return
                except psutil.NoSuchProcess:
                    print(f"{Fore.RED}Error: Process on port {port} no longer exists.")
                except psutil.AccessDenied:
                    print(f"{Fore.RED}Error: Insufficient permissions to kill process on port {port}.")
                except psutil.TimeoutExpired:
                    print(f"{Fore.RED}Error: Failed to terminate process on port {port} within timeout.")
        print(f"{Fore.YELLOW}No process found using port {port}.")

    def add_favorite(self, port):
        if port not in self.favorites:
            self.favorites.append(port)
            self.save_favorites()
            self.add_to_history(f"Added port {port} to favorites")
            print(f"{Fore.GREEN}Added port {port} to favorites.")
        else:
            print(f"{Fore.YELLOW}Port {port} is already in favorites.")

    def remove_favorite(self, port):
        if port in self.favorites:
            self.favorites.remove(port)
            self.save_favorites()
            self.add_to_history(f"Removed port {port} from favorites")
            print(f"{Fore.GREEN}Removed port {port} from favorites.")
        else:
            print(f"{Fore.YELLOW}Port {port} is not in favorites.")

    def display_favorites(self):
        if self.favorites:
            print(f"{Fore.CYAN}Favorite ports: {', '.join(self.favorites)}")
        else:
            print(f"{Fore.YELLOW}No favorite ports.")

    def display_history(self):
        if self.history:
            print(f"{Fore.CYAN}History:")
            for action in reversed(self.history):
                print(action)
        else:
            print(f"{Fore.YELLOW}No history available.")

    def search_ports(self, query):
        results = [p for p in self.ports if query.lower() in str(p['port']).lower() or query.lower() in p['process'].lower()]
        if results:
            headers = ["Port", "PID", "Process", "Status"]
            table_data = [[p['port'], p['pid'], p['process'], p['status']] for p in results]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print(f"{Fore.YELLOW}No matching ports found.")

    def run(self):
        while True:
            self.update_port_list()
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Poki - Advanced Port Killer CLI")
            print(f"{Fore.CYAN}{'=' * 40}")
            print(f"{Fore.WHITE}1. Show used ports")
            print("2. Kill a process by port")
            print("3. Add favorite port")
            print("4. Remove favorite port")
            print("5. Show favorites")
            print("6. Show history")
            print("7. Search ports")
            print("8. Exit")
            choice = input(f"{Fore.GREEN}Enter your choice: {Style.RESET_ALL}").strip()

            if choice == '1':
                self.display_ports()
            elif choice == '2':
                port = input("Enter port number to kill: ").strip()
                if port.isdigit():
                    self.kill_process(int(port))
                else:
                    print(f"{Fore.RED}Invalid port number. Please enter a numeric value.")
            elif choice == '3':
                port = input("Enter port number to add to favorites: ").strip()
                if port.isdigit():
                    self.add_favorite(port)
                else:
                    print(f"{Fore.RED}Invalid port number. Please enter a numeric value.")
            elif choice == '4':
                port = input("Enter port number to remove from favorites: ").strip()
                self.remove_favorite(port)
            elif choice == '5':
                self.display_favorites()
            elif choice == '6':
                self.display_history()
            elif choice == '7':
                query = input("Enter search query (port or process name): ").strip()
                self.search_ports(query)
            elif choice == '8':
                print(f"{Fore.YELLOW}Exiting...")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.")

            input(f"\n{Fore.CYAN}Press Enter to continue...")

def main():
    parser = argparse.ArgumentParser(description="Poki - Advanced Port Killer CLI")
    args = parser.parse_args()

    manager = AdvancedCLIPortManager()
    manager.run()

if __name__ == "__main__":
    main()