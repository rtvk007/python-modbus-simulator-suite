"""
Modbus Master (Poll) Application
Connects to a Modbus slave and performs read/write operations
"""
from pymodbus.client import ModbusTcpClient
import time
import sys


class ModbusMaster:
    def __init__(self, host='127.0.0.1', port=5020):
        self.host = host
        self.port = port
        self.client = None

    def connect(self):
        """Connect to Modbus slave"""
        print(f"🔌 Connecting to Modbus Slave at {self.host}:{self.port}...")
        self.client = ModbusTcpClient(self.host, port=self.port)

        if self.client.connect():
            print("✅ Connected successfully!\n")
            return True
        else:
            print("❌ Connection failed!")
            return False

    def disconnect(self):
        """Disconnect from Modbus slave"""
        if self.client:
            self.client.close()
            print("\n🔌 Disconnected from Modbus Slave")

    # READ OPERATIONS

    def read_coils(self, address, count=1):
        """Read Coils (Function Code 1)"""
        print(f"📖 Reading {count} coil(s) from address {address}...")
        result = self.client.read_coils(address, count)

        if not result.isError():
            print(f"✅ Coils: {result.bits[:count]}")
            return result.bits[:count]
        else:
            print(f"❌ Error: {result}")
            return None

    def read_discrete_inputs(self, address, count=1):
        """Read Discrete Inputs (Function Code 2)"""
        print(f"📖 Reading {count} discrete input(s) from address {address}...")
        result = self.client.read_discrete_inputs(address, count)

        if not result.isError():
            print(f"✅ Discrete Inputs: {result.bits[:count]}")
            return result.bits[:count]
        else:
            print(f"❌ Error: {result}")
            return None

    def read_holding_registers(self, address, count=1):
        """Read Holding Registers (Function Code 3)"""
        print(f"📖 Reading {count} holding register(s) from address {address}...")
        result = self.client.read_holding_registers(address, count)

        if not result.isError():
            print(f"✅ Holding Registers: {result.registers}")
            return result.registers
        else:
            print(f"❌ Error: {result}")
            return None

    def read_input_registers(self, address, count=1):
        """Read Input Registers (Function Code 4)"""
        print(f"📖 Reading {count} input register(s) from address {address}...")
        result = self.client.read_input_registers(address, count)

        if not result.isError():
            print(f"✅ Input Registers: {result.registers}")
            return result.registers
        else:
            print(f"❌ Error: {result}")
            return None

    # WRITE OPERATIONS

    def write_single_coil(self, address, value):
        """Write Single Coil (Function Code 5)"""
        print(f"✏️  Writing coil at address {address} = {value}...")
        result = self.client.write_coil(address, value)

        if not result.isError():
            print(f"✅ Coil written successfully")
            return True
        else:
            print(f"❌ Error: {result}")
            return False

    def write_single_register(self, address, value):
        """Write Single Register (Function Code 6)"""
        print(f"✏️  Writing register at address {address} = {value}...")
        result = self.client.write_register(address, value)

        if not result.isError():
            print(f"✅ Register written successfully")
            return True
        else:
            print(f"❌ Error: {result}")
            return False

    def write_multiple_coils(self, address, values):
        """Write Multiple Coils (Function Code 15)"""
        print(f"✏️  Writing {len(values)} coils starting at address {address}...")
        result = self.client.write_coils(address, values)

        if not result.isError():
            print(f"✅ Coils written successfully")
            return True
        else:
            print(f"❌ Error: {result}")
            return False

    def write_multiple_registers(self, address, values):
        """Write Multiple Registers (Function Code 16)"""
        print(f"✏️  Writing {len(values)} registers starting at address {address}...")
        result = self.client.write_registers(address, values)

        if not result.isError():
            print(f"✅ Registers written successfully")
            return True
        else:
            print(f"❌ Error: {result}")
            return False

    def run_demo(self):
        """Run a demonstration of all Modbus functions"""
        print("\n" + "="*60)
        print("🔄 MODBUS MASTER DEMO - Testing All Functions")
        print("="*60 + "\n")

        # READ OPERATIONS
        print("\n--- READ OPERATIONS ---\n")
        self.read_holding_registers(0, 5)
        time.sleep(0.5)

        self.read_input_registers(0, 5)
        time.sleep(0.5)

        self.read_coils(0, 5)
        time.sleep(0.5)

        self.read_discrete_inputs(0, 5)
        time.sleep(0.5)

        # WRITE OPERATIONS
        print("\n--- WRITE OPERATIONS ---\n")
        self.write_single_register(10, 999)
        time.sleep(0.5)

        self.write_multiple_registers(20, [111, 222, 333])
        time.sleep(0.5)

        self.write_single_coil(10, True)
        time.sleep(0.5)

        self.write_multiple_coils(20, [True, False, True, False])
        time.sleep(0.5)

        # VERIFY WRITES
        print("\n--- VERIFY WRITES ---\n")
        self.read_holding_registers(10, 1)
        time.sleep(0.5)

        self.read_holding_registers(20, 3)
        time.sleep(0.5)

        self.read_coils(10, 1)
        time.sleep(0.5)

        self.read_coils(20, 4)

        print("\n" + "="*60)
        print("✅ Demo Complete!")
        print("="*60 + "\n")


def interactive_mode(master):
    """Interactive CLI for Modbus operations"""
    print("\n" + "="*60)
    print("🎮 INTERACTIVE MODE")
    print("="*60)
    print("\nCommands:")
    print("  rc <addr> <count>       - Read Coils")
    print("  rdi <addr> <count>      - Read Discrete Inputs")
    print("  rhr <addr> <count>      - Read Holding Registers")
    print("  rir <addr> <count>      - Read Input Registers")
    print("  wc <addr> <value>       - Write Single Coil (0/1)")
    print("  wr <addr> <value>       - Write Single Register")
    print("  wmc <addr> <v1,v2,...>  - Write Multiple Coils")
    print("  wmr <addr> <v1,v2,...>  - Write Multiple Registers")
    print("  demo                    - Run demo")
    print("  quit / exit             - Exit")
    print("="*60 + "\n")

    while True:
        try:
            cmd = input("modbus> ").strip().lower()

            if not cmd:
                continue

            if cmd in ['quit', 'exit', 'q']:
                break

            if cmd == 'demo':
                master.run_demo()
                continue

            parts = cmd.split()
            operation = parts[0]

            if operation == 'rc' and len(parts) == 3:
                master.read_coils(int(parts[1]), int(parts[2]))
            elif operation == 'rdi' and len(parts) == 3:
                master.read_discrete_inputs(int(parts[1]), int(parts[2]))
            elif operation == 'rhr' and len(parts) == 3:
                master.read_holding_registers(int(parts[1]), int(parts[2]))
            elif operation == 'rir' and len(parts) == 3:
                master.read_input_registers(int(parts[1]), int(parts[2]))
            elif operation == 'wc' and len(parts) == 3:
                master.write_single_coil(int(parts[1]), bool(int(parts[2])))
            elif operation == 'wr' and len(parts) == 3:
                master.write_single_register(int(parts[1]), int(parts[2]))
            elif operation == 'wmc' and len(parts) == 3:
                values = [bool(int(v)) for v in parts[2].split(',')]
                master.write_multiple_coils(int(parts[1]), values)
            elif operation == 'wmr' and len(parts) == 3:
                values = [int(v) for v in parts[2].split(',')]
                master.write_multiple_registers(int(parts[1]), values)
            else:
                print("❌ Invalid command. Type 'help' to see available commands.")

            print()  # blank line after each operation

        except KeyboardInterrupt:
            print("\n")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    master = ModbusMaster(host='127.0.0.1', port=5020)

    if master.connect():
        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == 'demo':
            master.run_demo()
        else:
            interactive_mode(master)

        master.disconnect()
    else:
        print("\n⚠️  Make sure the Modbus Slave is running first!")
        print("   Run: python modbus_slave.py")
