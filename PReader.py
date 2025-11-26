import struct
import os

image_filename = "CW Image.dd" 

def analyze_mbr():
    print(f"[*] Analyzing Partition Table for: {image_filename}")
    
    if not os.path.exists(image_filename):
        print(f"[!] ERROR: The file '{image_filename}' was not found.")
        return

    print("-" * 65)
    print(f"{'Part':<5} {'Status':<10} {'Type':<10} {'Start Sector':<15} {'Size (Sectors)':<15}")
    print("-" * 65)

    try:
        with open(image_filename, "rb") as f:

            mbr_data = f.read(512)
            
            
            partition_table_offset = 446
            
            for i in range(4):
                entry_start = partition_table_offset + (i * 16)
                entry = mbr_data[entry_start : entry_start + 16]
                
                
                status, type_code, start_sector, size_sectors = struct.unpack("<B 3x B 3x I I", entry)
                
                if type_code != 0:
                    status_str = "Bootable" if status == 0x80 else "Non-Boot"
                    print(f"{i+1:<5} {status_str:<10} {hex(type_code):<10} {start_sector:<15} {size_sectors:<15}")
                    
                    if i == 1: 
                        print(f"    [!] NOTE: Task requires focus on Partition 2 (Start: {start_sector})")

    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    analyze_mbr()
    input("\nPress Enter to close...")