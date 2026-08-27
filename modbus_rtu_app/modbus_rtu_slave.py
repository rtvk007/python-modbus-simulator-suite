"""
Modbus RTU Slave (Server) Application for Serial Communication
Simulates a Modbus RTU device with coils, discrete inputs, holding registers, and input registers
"""
import asyncio
from pymodbus.server import StartAsyncSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.framer import ModbusRtuFramer
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


class ModbusRtuSlave:
    def __init__(self, port='COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1, slave_id=1):
        """
        Initialize Modbus RTU Slave

        Args:
            port: Serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate: Communication speed (9600, 19200, 38400, 57600, 115200)
            bytesize: Number of data bits (7 or 8)
            parity: Parity checking ('N'=None, 'E'=Even, 'O'=Odd)
            stopbits: Number of stop bits (1 or 2)
            slave_id: Modbus slave ID (1-247)
        """
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.slave_id = slave_id
        self.context = None

    def setup_datastore(self):
        """Initialize Modbus datastore with default values"""
        # Create data blocks for all function codes
        # di = Discrete Inputs (FC2), co = Coils (FC1, FC5, FC15)
        # hr = Holding Registers (FC3, FC6, FC16), ir = Input Registers (FC4)

        store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs (100 bits)
            co=ModbusSequentialDataBlock(0, [0]*100),  # Coils (100 bits)
            hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers (100 registers)
            ir=ModbusSequentialDataBlock(0, [0]*100),  # Input Registers (100 registers)
        )

        # Set some initial values
        store.setValues(3, 0, [100, 200, 300, 400, 500])  # Holding registers
        store.setValues(4, 0, [10, 20, 30, 40, 50])       # Input registers
        store.setValues(1, 0, [1, 0, 1, 0, 1])            # Coils

        self.context = ModbusServerContext(slaves=store, single=True)
        print("✅ Modbus RTU Slave datastore initialized")
        print("   - Coils: 100 (addresses 0-99)")
        print("   - Discrete Inputs: 100 (addresses 0-99)")
        print("   - Holding Registers: 100 (addresses 0-99)")
        print("   - Input Registers: 100 (addresses 0-99)")

    async def run(self):
        """Start the Modbus RTU server"""
        self.setup_datastore()
        print(f"\n🚀 Starting Modbus RTU Slave")
        print(f"   Port: {self.port}")
        print(f"   Baudrate: {self.baudrate}")
        print(f"   Parity: {self.parity}")
        print(f"   Stopbits: {self.stopbits}")
        print(f"   Slave ID: {self.slave_id}")
        print("   Press Ctrl+C to stop\n")

        await StartAsyncSerialServer(
            context=self.context,
            framer=ModbusRtuFramer,
            port=self.port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
        )


if __name__ == "__main__":
    # Configure your serial port settings here
    # Windows: COM1, COM2, COM3, etc.
    # Linux: /dev/ttyUSB0, /dev/ttyS0, etc.
    slave = ModbusRtuSlave(
        port='COM3',        # Change to your serial port
        baudrate=9600,      # Common: 9600, 19200, 38400, 115200
        bytesize=8,
        parity='N',         # N=None, E=Even, O=Odd
        stopbits=1,
        slave_id=1
    )

    try:
        asyncio.run(slave.run())
    except KeyboardInterrupt:
        print("\n\n⛔ Modbus RTU Slave stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure the serial port is available and not in use by another application")
