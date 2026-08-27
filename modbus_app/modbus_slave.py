"""
Modbus Slave (Server) Application
Simulates a Modbus device with coils, discrete inputs, holding registers, and input registers
"""
import asyncio
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


class ModbusSlave:
    def __init__(self, host='0.0.0.0', port=5020):
        self.host = host
        self.port = port
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
        print("✅ Modbus Slave datastore initialized")
        print("   - Coils: 100 (addresses 0-99)")
        print("   - Discrete Inputs: 100 (addresses 0-99)")
        print("   - Holding Registers: 100 (addresses 0-99)")
        print("   - Input Registers: 100 (addresses 0-99)")

    async def run(self):
        """Start the Modbus TCP server"""
        self.setup_datastore()
        print(f"\n🚀 Starting Modbus Slave on {self.host}:{self.port}")
        print("   Press Ctrl+C to stop\n")

        await StartAsyncTcpServer(
            context=self.context,
            address=(self.host, self.port),
        )


if __name__ == "__main__":
    slave = ModbusSlave(host='127.0.0.1', port=5020)

    try:
        asyncio.run(slave.run())
    except KeyboardInterrupt:
        print("\n\n⛔ Modbus Slave stopped by user")
