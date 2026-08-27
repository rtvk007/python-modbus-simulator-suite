"""
Modbus TCP Master (Client) - GUI Application
Connects to Modbus TCP slaves and performs read/write operations
"""
import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pymodbus.client import AsyncModbusTcpClient
from datetime import datetime


class ModbusTcpMasterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modbus TCP Master (Client)")
        self.root.geometry("750x700")
        self.root.resizable(True, True)

        self.client = None
        self.connected = False

        self.setup_ui()

    def setup_ui(self):
        # Connection Frame
        conn_frame = ttk.LabelFrame(self.root, text="Connection Settings", padding=10)
        conn_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(conn_frame, text="Host:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.host_entry = ttk.Entry(conn_frame, width=15)
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(conn_frame, text="Port:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.port_entry = ttk.Entry(conn_frame, width=10)
        self.port_entry.insert(0, "5020")
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(conn_frame, text="Slave ID:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.slave_entry = ttk.Entry(conn_frame, width=10)
        self.slave_entry.insert(0, "1")
        self.slave_entry.grid(row=0, column=5, padx=5, pady=5)

        self.connect_btn = ttk.Button(conn_frame, text="🔌 Connect", command=self.connect, width=12)
        self.connect_btn.grid(row=0, column=6, padx=5, pady=5)

        self.disconnect_btn = ttk.Button(conn_frame, text="⏏ Disconnect", command=self.disconnect, state="disabled", width=12)
        self.disconnect_btn.grid(row=0, column=7, padx=5, pady=5)

        self.status_label = ttk.Label(conn_frame, text="⚫ Disconnected", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=8, pady=5)

        # Operations Frame
        ops_frame = ttk.LabelFrame(self.root, text="Modbus Operations", padding=10)
        ops_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Read Operations
        read_frame = ttk.LabelFrame(ops_frame, text="Read Operations", padding=10)
        read_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(read_frame, text="Address:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.read_addr = ttk.Entry(read_frame, width=10)
        self.read_addr.insert(0, "0")
        self.read_addr.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(read_frame, text="Count:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.read_count = ttk.Entry(read_frame, width=10)
        self.read_count.insert(0, "5")
        self.read_count.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(read_frame, text="Read Coils (FC1)", command=lambda: self.read_operation("coils"), width=18).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(read_frame, text="Read Discrete Inputs (FC2)", command=lambda: self.read_operation("discrete"), width=22).grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        ttk.Button(read_frame, text="Read Holding Regs (FC3)", command=lambda: self.read_operation("holding"), width=22).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(read_frame, text="Read Input Regs (FC4)", command=lambda: self.read_operation("input"), width=18).grid(row=2, column=2, padx=5, pady=5)

        # Write Operations
        write_frame = ttk.LabelFrame(ops_frame, text="Write Operations", padding=10)
        write_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(write_frame, text="Address:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.write_addr = ttk.Entry(write_frame, width=10)
        self.write_addr.insert(0, "10")
        self.write_addr.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(write_frame, text="Value(s):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.write_value = ttk.Entry(write_frame, width=30)
        self.write_value.insert(0, "999")
        self.write_value.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(write_frame, text="(For multiple: use comma, e.g., 100,200,300)", font=("", 8)).grid(row=1, column=0, columnspan=4, sticky="w", padx=5)

        ttk.Button(write_frame, text="Write Single Coil (FC5)", command=lambda: self.write_operation("single_coil"), width=22).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(write_frame, text="Write Single Reg (FC6)", command=lambda: self.write_operation("single_register"), width=20).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(write_frame, text="Write Multiple Coils (FC15)", command=lambda: self.write_operation("multiple_coils"), width=25).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(write_frame, text="Write Multiple Regs (FC16)", command=lambda: self.write_operation("multiple_registers"), width=25).grid(row=3, column=2, columnspan=2, padx=5, pady=5)

        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Activity Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, wrap=tk.WORD, state="disabled")
        self.log_text.pack(fill="both", expand=True)

        clear_btn = ttk.Button(log_frame, text="Clear Log", command=self.clear_log)
        clear_btn.pack(pady=5)

    def log(self, message, color="black"):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def clear_log(self):
        """Clear the log"""
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")

    def connect(self):
        """Connect to Modbus TCP server"""
        host = self.host_entry.get()
        port = int(self.port_entry.get())

        async def do_connect():
            self.client = AsyncModbusTcpClient(host, port=port)
            await self.client.connect()
            return self.client.connected

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            connected = loop.run_until_complete(do_connect())

            if connected:
                self.connected = True
                self.status_label.config(text=f"🟢 Connected to {host}:{port}", foreground="green")
                self.connect_btn.config(state="disabled")
                self.disconnect_btn.config(state="normal")
                self.log(f"✅ Connected to {host}:{port}")
            else:
                messagebox.showerror("Connection Error", "Failed to connect to server")
                self.log(f"❌ Failed to connect to {host}:{port}")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Error: {e}")
            self.log(f"❌ Connection error: {e}")

    def disconnect(self):
        """Disconnect from Modbus TCP server"""
        if self.client:
            self.client.close()
            self.connected = False
            self.status_label.config(text="⚫ Disconnected", foreground="red")
            self.connect_btn.config(state="normal")
            self.disconnect_btn.config(state="disabled")
            self.log("🔌 Disconnected from server")

    def read_operation(self, operation_type):
        """Perform read operation"""
        if not self.connected:
            messagebox.showwarning("Not Connected", "Please connect to server first")
            return

        address = int(self.read_addr.get())
        count = int(self.read_count.get())
        slave_id = int(self.slave_entry.get())

        async def do_read():
            if operation_type == "coils":
                result = await self.client.read_coils(address, count, slave=slave_id)
                return "Coils", result.bits[:count] if not result.isError() else None
            elif operation_type == "discrete":
                result = await self.client.read_discrete_inputs(address, count, slave=slave_id)
                return "Discrete Inputs", result.bits[:count] if not result.isError() else None
            elif operation_type == "holding":
                result = await self.client.read_holding_registers(address, count, slave=slave_id)
                return "Holding Registers", result.registers if not result.isError() else None
            elif operation_type == "input":
                result = await self.client.read_input_registers(address, count, slave=slave_id)
                return "Input Registers", result.registers if not result.isError() else None

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            name, values = loop.run_until_complete(do_read())

            if values is not None:
                self.log(f"📖 Read {name} [Addr: {address}, Count: {count}]: {values}")
            else:
                self.log(f"❌ Error reading {name}")
                messagebox.showerror("Read Error", f"Failed to read {name}")
        except Exception as e:
            self.log(f"❌ Read error: {e}")
            messagebox.showerror("Read Error", str(e))

    def write_operation(self, operation_type):
        """Perform write operation"""
        if not self.connected:
            messagebox.showwarning("Not Connected", "Please connect to server first")
            return

        address = int(self.write_addr.get())
        slave_id = int(self.slave_entry.get())
        value_str = self.write_value.get()

        async def do_write():
            if operation_type == "single_coil":
                value = bool(int(value_str))
                result = await self.client.write_coil(address, value, slave=slave_id)
                return "Single Coil", value, not result.isError()
            elif operation_type == "single_register":
                value = int(value_str)
                result = await self.client.write_register(address, value, slave=slave_id)
                return "Single Register", value, not result.isError()
            elif operation_type == "multiple_coils":
                values = [bool(int(v.strip())) for v in value_str.split(",")]
                result = await self.client.write_coils(address, values, slave=slave_id)
                return "Multiple Coils", values, not result.isError()
            elif operation_type == "multiple_registers":
                values = [int(v.strip()) for v in value_str.split(",")]
                result = await self.client.write_registers(address, values, slave=slave_id)
                return "Multiple Registers", values, not result.isError()

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            name, value, success = loop.run_until_complete(do_write())

            if success:
                self.log(f"✏️ Wrote {name} [Addr: {address}]: {value}")
            else:
                self.log(f"❌ Error writing {name}")
                messagebox.showerror("Write Error", f"Failed to write {name}")
        except Exception as e:
            self.log(f"❌ Write error: {e}")
            messagebox.showerror("Write Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ModbusTcpMasterGUI(root)
    root.mainloop()
