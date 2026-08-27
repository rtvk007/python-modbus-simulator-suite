"""
Modbus RTU Slave (Server) - GUI Application for Serial Communication
Simulates a Modbus RTU device with a graphical interface
"""
import asyncio
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pymodbus.server import StartAsyncSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.framer import ModbusRtuFramer
from datetime import datetime


class ModbusRtuSlaveGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modbus RTU Slave (Server)")
        self.root.geometry("700x650")
        self.root.resizable(True, True)

        self.server_running = False
        self.server_task = None
        self.context = None
        self.loop = None

        self.setup_ui()

    def setup_ui(self):
        # Configuration Frame
        config_frame = ttk.LabelFrame(self.root, text="Serial Setup", padding=10)
        config_frame.pack(fill="x", padx=10, pady=10)

        # Port
        ttk.Label(config_frame, text="Port:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.port_entry = ttk.Entry(config_frame, width=12)
        self.port_entry.insert(0, "COM3")
        self.port_entry.grid(row=0, column=1, padx=5, pady=5)

        # Baudrate
        ttk.Label(config_frame, text="Baudrate:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.baud_combo = ttk.Combobox(config_frame, values=["9600", "19200", "38400", "57600", "115200"], width=10)
        self.baud_combo.set("9600")
        self.baud_combo.grid(row=0, column=3, padx=5, pady=5)

        # Parity
        ttk.Label(config_frame, text="Parity:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.parity_combo = ttk.Combobox(config_frame, values=["N (None)", "E (Even)", "O (Odd)"], width=10)
        self.parity_combo.set("N (None)")
        self.parity_combo.grid(row=0, column=5, padx=5, pady=5)

        # Stopbits
        ttk.Label(config_frame, text="Stopbits:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.stop_combo = ttk.Combobox(config_frame, values=["1", "2"], width=10)
        self.stop_combo.set("1")
        self.stop_combo.grid(row=1, column=1, padx=5, pady=5)

        # Slave ID
        ttk.Label(config_frame, text="Slave ID:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.slave_entry = ttk.Entry(config_frame, width=12)
        self.slave_entry.insert(0, "1")
        self.slave_entry.grid(row=1, column=3, padx=5, pady=5)

        # Control Frame
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill="x", padx=10)

        self.start_btn = ttk.Button(control_frame, text="▶ Start Server", command=self.start_server, width=15)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ttk.Button(control_frame, text="⏹ Stop Server", command=self.stop_server, state="disabled", width=15)
        self.stop_btn.pack(side="left", padx=5)

        self.status_label = ttk.Label(control_frame, text="⚫ Server Stopped", foreground="red")
        self.status_label.pack(side="left", padx=20)

        # Data View Frame
        data_frame = ttk.LabelFrame(self.root, text="Datastore Values", padding=10)
        data_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs for different data types
        self.notebook = ttk.Notebook(data_frame)
        self.notebook.pack(fill="both", expand=True)

        # Holding Registers Tab
        hr_frame = ttk.Frame(self.notebook)
        self.notebook.add(hr_frame, text="Holding Registers")
        self.hr_text = scrolledtext.ScrolledText(hr_frame, height=10, wrap=tk.WORD)
        self.hr_text.pack(fill="both", expand=True)

        # Input Registers Tab
        ir_frame = ttk.Frame(self.notebook)
        self.notebook.add(ir_frame, text="Input Registers")
        self.ir_text = scrolledtext.ScrolledText(ir_frame, height=10, wrap=tk.WORD)
        self.ir_text.pack(fill="both", expand=True)

        # Coils Tab
        co_frame = ttk.Frame(self.notebook)
        self.notebook.add(co_frame, text="Coils")
        self.co_text = scrolledtext.ScrolledText(co_frame, height=10, wrap=tk.WORD)
        self.co_text.pack(fill="both", expand=True)

        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Server Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD, state="disabled")
        self.log_text.pack(fill="both", expand=True)

        # Refresh button
        refresh_btn = ttk.Button(self.root, text="🔄 Refresh Data", command=self.refresh_data)
        refresh_btn.pack(pady=5)

    def log(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def setup_datastore(self):
        """Initialize Modbus datastore with default values"""
        store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0]*100),
            co=ModbusSequentialDataBlock(0, [0]*100),
            hr=ModbusSequentialDataBlock(0, [0]*100),
            ir=ModbusSequentialDataBlock(0, [0]*100),
        )

        # Set initial values
        store.setValues(3, 0, [100, 200, 300, 400, 500])  # Holding registers
        store.setValues(4, 0, [10, 20, 30, 40, 50])       # Input registers
        store.setValues(1, 0, [1, 0, 1, 0, 1])            # Coils

        self.context = ModbusServerContext(slaves=store, single=True)
        self.log("✅ Datastore initialized with default values")
        self.refresh_data()

    def refresh_data(self):
        """Refresh the displayed data from datastore"""
        if not self.context:
            return

        slave = self.context[0]

        # Holding Registers
        self.hr_text.delete(1.0, tk.END)
        hr_values = slave.getValues(3, 0, 20)
        self.hr_text.insert(tk.END, "Address | Value\n")
        self.hr_text.insert(tk.END, "-" * 30 + "\n")
        for i, val in enumerate(hr_values):
            if val != 0:
                self.hr_text.insert(tk.END, f"  {i:4d}  |  {val}\n")

        # Input Registers
        self.ir_text.delete(1.0, tk.END)
        ir_values = slave.getValues(4, 0, 20)
        self.ir_text.insert(tk.END, "Address | Value\n")
        self.ir_text.insert(tk.END, "-" * 30 + "\n")
        for i, val in enumerate(ir_values):
            if val != 0:
                self.ir_text.insert(tk.END, f"  {i:4d}  |  {val}\n")

        # Coils
        self.co_text.delete(1.0, tk.END)
        co_values = slave.getValues(1, 0, 20)
        self.co_text.insert(tk.END, "Address | Value\n")
        self.co_text.insert(tk.END, "-" * 30 + "\n")
        for i, val in enumerate(co_values):
            if val != 0:
                self.co_text.insert(tk.END, f"  {i:4d}  |  {'ON' if val else 'OFF'}\n")

    def start_server(self):
        """Start the Modbus RTU server in a background thread"""
        port = self.port_entry.get()
        baudrate = int(self.baud_combo.get())
        parity_val = self.parity_combo.get()[0]  # Take 'N', 'E', or 'O'
        stopbits = int(self.stop_combo.get())
        slave_id = int(self.slave_entry.get())

        self.setup_datastore()

        def run_server():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            async def server_coro():
                await StartAsyncSerialServer(
                    context=self.context,
                    framer=ModbusRtuFramer,
                    port=port,
                    baudrate=baudrate,
                    bytesize=8,
                    parity=parity_val,
                    stopbits=stopbits,
                )

            try:
                self.loop.run_until_complete(server_coro())
            except Exception as e:
                self.root.after(0, lambda: self.log(f"❌ Server error: {e}"))
                self.root.after(0, lambda: messagebox.showerror("Server Error", f"Could not start server:\n{e}"))
                self.root.after(0, self.stop_server)

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

        self.server_running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.port_entry.config(state="disabled")
        self.baud_combo.config(state="disabled")
        self.parity_combo.config(state="disabled")
        self.stop_combo.config(state="disabled")
        self.slave_entry.config(state="disabled")
        self.status_label.config(text="🟢 Server Running", foreground="green")
        self.log(f"🚀 Server started on {port} @ {baudrate}")

        # Auto-refresh data every 2 seconds
        self.auto_refresh()

    def auto_refresh(self):
        """Auto-refresh data while server is running"""
        if self.server_running:
            self.refresh_data()
            self.root.after(2000, self.auto_refresh)

    def stop_server(self):
        """Stop the Modbus RTU server"""
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

        self.server_running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.port_entry.config(state="normal")
        self.baud_combo.config(state="normal")
        self.parity_combo.config(state="normal")
        self.stop_combo.config(state="normal")
        self.slave_entry.config(state="normal")
        self.status_label.config(text="⚫ Server Stopped", foreground="red")
        self.log("⏹ Server stopped")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModbusRtuSlaveGUI(root)
    root.mainloop()
