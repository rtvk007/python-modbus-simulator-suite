"""
Modbus RTU Master (Client/Poll) Application for Serial Communication
Connects to Modbus RTU slaves and performs read/write operations
"""
import asyncio
from pymodbus.client import AsyncModbusSerialClient
from pymodbus.framer import ModbusRtuFramer
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


class ModbusRtuMaster:
    def __init__(self, port='COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=3):
        """
        Initialize Modbus RTU Master

        Args:
            port: Serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate: Communication speed (9600, 19200, 38400, 57600, 115200)
            bytesize: Number of data bits (7 or 8)
            parity: Parity checking ('N'=None, 'E'=Even, 'O'=Odd)
            stopbits: Number of stop bits (1 or 2)
            timeout: Response timeout in seconds
        """
        self.client = AsyncModbusSerialClient(
            port=port,
            framer=ModbusRtuFramer,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout,
        )
        self.port = port
        self.baudrate = baudrate

    async def connect(self):
        """Connect to the Modbus RTU slave"""
        await self.client.connect()
        print(f"✅ Connected to Modbus RTU Slave on {self.port} @ {self.baudrate} baud")

    async def disconnect(self):
        """Disconnect from the Modbus RTU slave"""
        self.client.close()
        print("🔌 Disconnected from Modbus RTU Slave")

    async def read_coils(self, address, count, slave_id=1):
        """Read Coils (Function Code 1)"""
        result = await self.client.read_coils(address, count, slave=slave_id)
        if result.isError():
            print(f"❌ Error reading coils: {result}")
            return None
        print(f"📖 Read Coils [Address {address}, Count {count}]: {result.bits[:count]}")
        return result.bits[:count]

    async def read_discrete_inputs(self, address, count, slave_id=1):
        """Read Discrete Inputs (Function Code 2)"""
        result = await self.client.read_discrete_inputs(address, count, slave=slave_id)
        if result.isError():
            print(f"❌ Error reading discrete inputs: {result}")
            return None
        print(f"📖 Read Discrete Inputs [Address {address}, Count {count}]: {result.bits[:count]}")
        return result.bits[:count]

    async def read_holding_registers(self, address, count, slave_id=1):
        """Read Holding Registers (Function Code 3)"""
        result = await self.client.read_holding_registers(address, count, slave=slave_id)
        if result.isError():
            print(f"❌ Error reading holding registers: {result}")
            return None
        print(f"📖 Read Holding Registers [Address {address}, Count {count}]: {result.registers}")
        return result.registers

    async def read_input_registers(self, address, count, slave_id=1):
        """Read Input Registers (Function Code 4)"""
        result = await self.client.read_input_registers(address, count, slave=slave_id)
        if result.isError():
            print(f"❌ Error reading input registers: {result}")
            return None
        print(f"📖 Read Input Registers [Address {address}, Count {count}]: {result.registers}")
        return result.registers

    async def write_single_coil(self, address, value, slave_id=1):
        """Write Single Coil (Function Code 5)"""
        result = await self.client.write_coil(address, value, slave=slave_id)
        if result.isError():
            print(f"❌ Error writing coil: {result}")
            return False
        print(f"✏️ Wrote Single Coil [Address {address}]: {value}")
        return True

    async def write_single_register(self, address, value, slave_id=1):
        """Write Single Register (Function Code 6)"""
        result = await self.client.write_register(address, value, slave=slave_id)
        if result.isError():
            print(f"❌ Error writing register: {result}")
            return False
        print(f"✏️ Wrote Single Register [Address {address}]: {value}")
        return True

    async def write_multiple_coils(self, address, values, slave_id=1):
        """Write Multiple Coils (Function Code 15)"""
        result = await self.client.write_coils(address, values, slave=slave_id)
        if result.isError():
            print(f"❌ Error writing multiple coils: {result}")
            return False
        print(f"✏️ Wrote Multiple Coils [Address {address}, Count {len(values)}]: {values}")
        return True

    async def write_multiple_registers(self, address, values, slave_id=1):
        """Write Multiple Registers (Function Code 16)"""
        result = await self.client.write_registers(address, values, slave=slave_id)
        if result.isError():
            print(f"❌ Error writing multiple registers: {result}")
            return False
        print(f"✏️ Wrote Multiple Registers [Address {address}, Count {len(values)}]: {values}")
        return True


async def demo():
    """Demonstration of all Modbus RTU Master operations"""
    # Configure your serial port settings here
    master = ModbusRtuMaster(
        port='COM3',        # Change to your serial port
        baudrate=9600,      # Common: 9600, 19200, 38400, 115200
        bytesize=8,
        parity='N',         # N=None, E=Even, O=Odd
        stopbits=1,
        timeout=3
    )

    await master.connect()

    print("\n" + "="*60)
    print("🔍 MODBUS RTU MASTER - POLLING DEMO")
    print("="*60 + "\n")

    slave_id = 1  # Modbus slave ID to communicate with

    try:
        # READ OPERATIONS
        print("--- READ OPERATIONS ---\n")
        await master.read_coils(0, 5, slave_id)
        await asyncio.sleep(0.5)

        await master.read_discrete_inputs(0, 5, slave_id)
        await asyncio.sleep(0.5)

        await master.read_holding_registers(0, 5, slave_id)
        await asyncio.sleep(0.5)

        await master.read_input_registers(0, 5, slave_id)
        await asyncio.sleep(0.5)

        # WRITE OPERATIONS
        print("\n--- WRITE OPERATIONS ---\n")
        await master.write_single_coil(10, True, slave_id)
        await asyncio.sleep(0.5)

        await master.write_single_register(10, 999, slave_id)
        await asyncio.sleep(0.5)

        await master.write_multiple_coils(20, [True, False, True, False, True], slave_id)
        await asyncio.sleep(0.5)

        await master.write_multiple_registers(20, [111, 222, 333, 444, 555], slave_id)
        await asyncio.sleep(0.5)

        # VERIFY WRITES
        print("\n--- VERIFY WRITTEN VALUES ---\n")
        await master.read_coils(10, 1, slave_id)
        await asyncio.sleep(0.5)

        await master.read_holding_registers(10, 1, slave_id)
        await asyncio.sleep(0.5)

        await master.read_coils(20, 5, slave_id)
        await asyncio.sleep(0.5)

        await master.read_holding_registers(20, 5, slave_id)

        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error during operations: {e}")
    finally:
        await master.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        print("\n\n⛔ Modbus RTU Master stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure:")
        print("   1. The serial port is correct and available")
        print("   2. The Modbus RTU Slave is running on the same/connected serial port")
        print("   3. Baudrate and serial settings match between master and slave")
