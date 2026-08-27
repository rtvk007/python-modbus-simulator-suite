# Modbus RTU Master & Slave Application

A complete **Modbus RTU (Serial)** Master and Slave application built with Python for Windows (also works on Linux).

## 📋 Features

### Modbus RTU Slave (Server)
- Simulates a Modbus RTU device
- Supports all standard Modbus data types:
  - Coils (Read/Write)
  - Discrete Inputs (Read-only)
  - Holding Registers (Read/Write)
  - Input Registers (Read-only)
- Configurable serial port settings (baudrate, parity, stopbits)
- Pre-populated with demo data

### Modbus RTU Master (Client/Poll)
- Connect to any Modbus RTU slave via serial port
- All standard Modbus function codes:
  - FC1: Read Coils
  - FC2: Read Discrete Inputs
  - FC3: Read Holding Registers
  - FC4: Read Input Registers
  - FC5: Write Single Coil
  - FC6: Write Single Register
  - FC15: Write Multiple Coils
  - FC16: Write Multiple Registers
- Includes complete demo with all operations

## 🚀 Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Serial Port Setup

#### **Option A: Physical Serial Port (Real RS-485/RS-232)**
If you have physical serial hardware:
- Connect RS-485 or RS-232 devices
- Use ports like `COM1`, `COM2`, `COM3` (Windows) or `/dev/ttyUSB0`, `/dev/ttyS0` (Linux)

#### **Option B: Virtual Serial Ports (For Testing)**

**Windows - Using com0com (Free):**
1. Download com0com: https://sourceforge.net/projects/com0com/
2. Install and create a virtual COM port pair (e.g., COM3 ↔ COM4)
3. Run the slave on COM3 and master on COM4

**Windows - Using Virtual Serial Port Driver (Eltima):**
1. Download: https://www.virtual-serial-port.org/
2. Create a pair of virtual ports

**Linux - Using socat:**
```bash
socat -d -d pty,raw,echo=0 pty,raw,echo=0
# This creates two virtual ports like /dev/pts/2 and /dev/pts/3
```

## 📖 Usage

### Running the Slave (Server)

Edit `modbus_rtu_slave.py` to configure your serial port:
```python
slave = ModbusRtuSlave(
    port='COM3',        # Change to your serial port
    baudrate=9600,      # 9600, 19200, 38400, 115200
    bytesize=8,
    parity='N',         # N=None, E=Even, O=Odd
    stopbits=1,
    slave_id=1
)
```

Run the slave:
```bash
python modbus_rtu_slave.py
```

### Running the Master (Client/Poll)

Edit `modbus_rtu_master.py` to configure your serial port:
```python
master = ModbusRtuMaster(
    port='COM4',        # Change to your serial port (different from slave if using virtual ports)
    baudrate=9600,      # Must match slave settings
    bytesize=8,
    parity='N',         # Must match slave settings
    stopbits=1,
    timeout=3
)
```

Run the master:
```bash
python modbus_rtu_master.py
```

## 🔧 Serial Port Configuration

### Common Baudrates
- 9600 (most common)
- 19200
- 38400
- 57600
- 115200

### Parity Options
- `'N'` - None (most common)
- `'E'` - Even
- `'O'` - Odd

### Important Notes
1. **Master and Slave must use identical serial settings** (baudrate, parity, stopbits, bytesize)
2. **For virtual ports**, use different ports for master and slave (e.g., COM3 for slave, COM4 for master)
3. **For physical ports**, connect TX to RX and RX to TX between devices
4. **RS-485** requires proper termination resistors (120Ω) at both ends

## 📊 Data Layout

The slave is initialized with:
- **Holding Registers (0-4)**: `[100, 200, 300, 400, 500]`
- **Input Registers (0-4)**: `[10, 20, 30, 40, 50]`
- **Coils (0-4)**: `[1, 0, 1, 0, 1]`
- All data types have 100 addresses available (0-99)

## 🛠️ Customization

### Custom Master Operations

```python
import asyncio
from modbus_rtu_master import ModbusRtuMaster

async def custom_operations():
    master = ModbusRtuMaster(port='COM4', baudrate=9600)
    await master.connect()
    
    # Read 10 holding registers starting at address 0
    values = await master.read_holding_registers(0, 10, slave_id=1)
    
    # Write a single register
    await master.write_single_register(50, 1234, slave_id=1)
    
    # Write multiple registers
    await master.write_multiple_registers(60, [100, 200, 300], slave_id=1)
    
    await master.disconnect()

asyncio.run(custom_operations())
```

## 🐛 Troubleshooting

### "Error: Port is already in use"
- Close any other application using the serial port
- Make sure you're not running multiple instances of slave/master on the same port

### "Error: Could not open port"
- Verify the port name is correct (`COM3`, `/dev/ttyUSB0`, etc.)
- On Linux, you may need permissions: `sudo chmod 666 /dev/ttyUSB0`
- Check if the port exists: `mode` (Windows) or `ls /dev/tty*` (Linux)

### "No response from slave"
- Verify master and slave serial settings match exactly
- Check physical connections (TX ↔ RX) or virtual port pairing
- Verify the slave is running before starting the master
- Ensure slave_id matches (default is 1)

### Virtual Port Not Working
- Windows: Make sure com0com is installed and ports are properly paired
- Linux: Verify socat is creating the port pair correctly

## 📦 Building Executables (Optional)

To create standalone `.exe` files:

```bash
pip install pyinstaller

# Build Slave
pyinstaller --onefile --name modbus_rtu_slave modbus_rtu_slave.py

# Build Master
pyinstaller --onefile --name modbus_rtu_master modbus_rtu_master.py
```

The executables will be in the `dist/` folder.

## 📚 Resources

- **pymodbus Documentation**: https://pymodbus.readthedocs.io/
- **Modbus Protocol**: https://www.modbus.org/
- **RS-485 Wiring Guide**: Search for "RS485 wiring guide" for hardware connections

## 🆚 Differences from TCP/IP Version

| Feature | TCP/IP | RTU (Serial) |
|---------|--------|--------------|
| **Transport** | Ethernet/Network | Serial (RS-485/RS-232) |
| **Connection** | IP Address + Port | COM Port + Baudrate |
| **Speed** | Fast (Mbps) | Slower (kbps) |
| **Distance** | Long (with routers) | Limited (meters) |
| **Setup** | Network configuration | Physical wiring or virtual ports |
| **Use Case** | Modern systems, IoT | Industrial legacy systems |

## 📄 License

Free to use and modify.
