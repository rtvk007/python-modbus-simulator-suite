# Modbus Master/Slave Application

A complete Modbus TCP implementation for Windows with Python backend supporting all standard Modbus functions.

## Features

### Modbus Slave (Server)
- ✅ Modbus TCP Server
- ✅ 100 Coils (Read/Write)
- ✅ 100 Discrete Inputs (Read Only)
- ✅ 100 Holding Registers (Read/Write)
- ✅ 100 Input Registers (Read Only)
- ✅ Supports all standard function codes (1, 2, 3, 4, 5, 6, 15, 16)

### Modbus Master (Client/Poll)
- ✅ Read Coils (FC1)
- ✅ Read Discrete Inputs (FC2)
- ✅ Read Holding Registers (FC3)
- ✅ Read Input Registers (FC4)
- ✅ Write Single Coil (FC5)
- ✅ Write Single Register (FC6)
- ✅ Write Multiple Coils (FC15)
- ✅ Write Multiple Registers (FC16)
- ✅ Interactive CLI mode
- ✅ Demo mode

## Installation

1. Install Python (3.8 or higher)
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Start the Modbus Slave

Open a terminal and run:

```bash
python modbus_slave.py
```

You should see:
```
✅ Modbus Slave datastore initialized
🚀 Starting Modbus Slave on 127.0.0.1:5020
   Press Ctrl+C to stop
```

### Step 2: Run the Modbus Master

Open a **second terminal** and run:

#### Option A: Interactive Mode
```bash
python modbus_master.py
```

Then use commands like:
```
modbus> rhr 0 5          # Read 5 holding registers from address 0
modbus> wr 10 999        # Write value 999 to register 10
modbus> wc 5 1           # Write coil at address 5 = ON
modbus> demo             # Run full demo
modbus> quit             # Exit
```

#### Option B: Demo Mode
```bash
python modbus_master.py demo
```

This will automatically test all Modbus functions.

## Command Reference (Interactive Mode)

| Command | Description | Example |
|---------|-------------|---------|
| `rc <addr> <count>` | Read Coils | `rc 0 5` |
| `rdi <addr> <count>` | Read Discrete Inputs | `rdi 0 5` |
| `rhr <addr> <count>` | Read Holding Registers | `rhr 0 10` |
| `rir <addr> <count>` | Read Input Registers | `rir 0 5` |
| `wc <addr> <value>` | Write Single Coil | `wc 10 1` |
| `wr <addr> <value>` | Write Single Register | `wr 20 500` |
| `wmc <addr> <values>` | Write Multiple Coils | `wmc 10 1,0,1,0` |
| `wmr <addr> <values>` | Write Multiple Registers | `wmr 20 100,200,300` |
| `demo` | Run demonstration | `demo` |
| `quit` or `exit` | Exit program | `quit` |

## Configuration

Edit the connection settings in the code:

```python
# modbus_slave.py
slave = ModbusSlave(host='127.0.0.1', port=5020)

# modbus_master.py
master = ModbusMaster(host='127.0.0.1', port=5020)
```

## Modbus Function Codes

| Function Code | Function Name | Type |
|---------------|---------------|------|
| 1 | Read Coils | Read |
| 2 | Read Discrete Inputs | Read |
| 3 | Read Holding Registers | Read |
| 4 | Read Input Registers | Read |
| 5 | Write Single Coil | Write |
| 6 | Write Single Register | Write |
| 15 | Write Multiple Coils | Write |
| 16 | Write Multiple Registers | Write |

## Troubleshooting

### "Connection failed"
- Make sure the slave is running first
- Check if port 5020 is available
- Verify firewall settings

### "Module not found: pymodbus"
```bash
pip install pymodbus
```

## Architecture

```
┌─────────────────┐         TCP/IP         ┌─────────────────┐
│  Modbus Master  │◄──────────────────────►│  Modbus Slave   │
│   (Client)      │      Port 5020         │   (Server)      │
│                 │                         │                 │
│ - Read/Write    │                         │ - 100 Coils     │
│ - Poll data     │                         │ - 100 DI        │
│ - Interactive   │                         │ - 100 HR        │
│ - CLI/Demo      │                         │ - 100 IR        │
└─────────────────┘                         └─────────────────┘
```

## License

Free to use for educational and commercial purposes.
