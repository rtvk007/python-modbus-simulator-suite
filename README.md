# 🔌 Python Modbus Simulator Suite

> A comprehensive asynchronous Python desktop application featuring GUI (Tkinter) and CLI interfaces for simulating and testing **Modbus TCP/IP** and **Modbus RTU (Serial)** Master/Slave communication networks.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![pymodbus](https://img.shields.io/badge/pymodbus-3.5.4-orange.svg)](https://pymodbus.readthedocs.io/)

---

## 📋 Overview

This project provides a complete testing and simulation environment for Modbus communication protocols commonly used in industrial automation, IoT devices, SCADA systems, and building management systems. It includes both **CLI** and **GUI** applications for easy testing and debugging of Modbus networks.

### ✨ Key Features

- ✅ **Dual Protocol Support**: Modbus TCP/IP and Modbus RTU (Serial RS-485/RS-232)
- ✅ **GUI & CLI Interfaces**: User-friendly Tkinter GUI + Command-line tools
- ✅ **Full Function Code Coverage**: FC1-FC6, FC15, FC16 (Read/Write Coils, Registers)
- ✅ **Asynchronous Architecture**: Built with `asyncio` for high performance
- ✅ **Real-time Monitoring**: Live data visualization and activity logging
- ✅ **Production-Ready**: Clean code, modular design, and comprehensive documentation

---

## 🎯 Use Cases

- **Industrial Automation Testing**: Simulate PLCs, sensors, and actuators
- **Protocol Development**: Test Modbus client/server implementations
- **Educational Tool**: Learn Modbus protocol hands-on
- **Network Debugging**: Troubleshoot communication issues
- **Integration Testing**: Validate SCADA/HMI system integrations

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- For RTU (Serial): COM port access or virtual serial ports

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/python-modbus-simulator-suite.git
   cd python-modbus-simulator-suite
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Run GUI Applications

**Modbus TCP/IP:**
```bash
# Start TCP Slave (Server)
python modbus_app/modbus_slave_gui.py

# Start TCP Master (Client)
python modbus_app/modbus_master_gui.py
```

**Modbus RTU (Serial):**
```bash
# Start RTU Slave (Server)
python modbus_rtu_app/modbus_rtu_slave_gui.py

# Start RTU Master (Client)
python modbus_rtu_app/modbus_rtu_master_gui.py
```

### Run CLI Applications

**Modbus TCP/IP:**
```bash
python modbus_app/modbus_slave.py
python modbus_app/modbus_master.py
```

**Modbus RTU:**
```bash
python modbus_rtu_app/modbus_rtu_slave.py
python modbus_rtu_app/modbus_rtu_master.py
```

---

## 🛠️ Technical Architecture

### Technology Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.8+ |
| **Protocol Library** | pymodbus 3.5.4 |
| **GUI Framework** | Tkinter (Standard Library) |
| **Async Runtime** | asyncio |
| **Serial Communication** | pyserial 3.5+ |

### Supported Modbus Functions

| Function Code | Operation | Type |
|--------------|-----------|------|
| **FC1** | Read Coils | Read |
| **FC2** | Read Discrete Inputs | Read |
| **FC3** | Read Holding Registers | Read |
| **FC4** | Read Input Registers | Read |
| **FC5** | Write Single Coil | Write |
| **FC6** | Write Single Register | Write |
| **FC15** | Write Multiple Coils | Write |
| **FC16** | Write Multiple Registers | Write |

---

## 📦 Project Structure

```
python-modbus-simulator-suite/
│
├── modbus_app/                  # Modbus TCP/IP Package
│   ├── modbus_slave.py          # CLI Slave
│   ├── modbus_slave_gui.py      # GUI Slave
│   ├── modbus_master.py         # CLI Master
│   ├── modbus_master_gui.py     # GUI Master
│   └── README.md                # TCP/IP Documentation
│
├── modbus_rtu_app/              # Modbus RTU (Serial) Package
│   ├── modbus_rtu_slave.py      # CLI Slave
│   ├── modbus_rtu_slave_gui.py  # GUI Slave
│   ├── modbus_rtu_master.py     # CLI Master
│   ├── modbus_rtu_master_gui.py # GUI Master
│   └── README.md                # RTU Documentation
│
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

---

## 🔧 Configuration

### Modbus TCP/IP Settings

- **Default Host**: `127.0.0.1`
- **Default Port**: `5020`
- **Slave ID**: `1` (configurable)

### Modbus RTU Settings

- **Default Port**: `COM3` (Windows) or `/dev/ttyUSB0` (Linux)
- **Baudrate**: `9600` (configurable: 9600, 19200, 38400, 57600, 115200)
- **Parity**: `None` (configurable: None, Even, Odd)
- **Stop Bits**: `1`
- **Byte Size**: `8`

For RTU testing without hardware, use virtual serial port software:
- **Windows**: [com0com](https://sourceforge.net/projects/com0com/)
- **Linux**: `socat -d -d pty,raw,echo=0 pty,raw,echo=0`

---

## 💡 Development

### Code Quality

- **Clean Architecture**: Modular, object-oriented design
- **Type Safety**: Clear function signatures and docstrings
- **Error Handling**: Comprehensive exception handling with user feedback
- **Async-First**: Non-blocking I/O for responsive UIs

### Extending the Project

To add new features:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

 ## Related Projects
  - [STM32 Modbus RTU Slave]([https://github.com/rtvk007/stm32-modbus-rtu-slave.git]) - Embedded implementation

## 📚 Resources

- [Modbus Protocol Specification](https://www.modbus.org/)
- [pymodbus Documentation](https://pymodbus.readthedocs.io/)
- [Python asyncio Guide](https://docs.python.org/3/library/asyncio.html)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Rutvik Kajavadra 
- GitHub: [rtvk007](https://github.com/rtvk007)
- LinkedIn: [Rutvik Kajavadra](https://www.linkedin.com/in/rutvikembeddedcoder/)
- Email: rkk0412@yahoo.com

---

## ⭐ Show Your Support

If this project helped you, please give it a ⭐️!

---

## 🔮 Future Roadmap

- [ ] Web-based dashboard (Flask/FastAPI)
- [ ] Database logging for historical data
- [ ] Docker containerization
- [ ] Unit test coverage
- [ ] CI/CD pipeline integration
- [ ] Multi-language support

---

**Built with ❤️ for the Industrial Automation Community**
