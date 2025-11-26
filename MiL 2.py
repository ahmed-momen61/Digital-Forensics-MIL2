import sys
import codecs
import os
from Registry import Registry


def rot13(s):
    return codecs.decode(s, 'rot_13') if s else ""

def ask_path(name):
    path = input(f"\n[?] Please enter path to {name} (or drag the file here): ").strip().replace('"', '')
    return path if os.path.exists(path) else None


def get_usb_name(serial_key):
    possible_keys = ["FriendlyName", "DeviceDesc", "USB", "ContainerID"]
    for k in possible_keys:
        try:
            return serial_key.value(k).value()
        except:
            pass
    return "Unknown USB Name"


def show_user_accounts(sam_hive):
    print("\n" + "="*50)
    print("   [1] USER ACCOUNTS (From SAM)")
    print("="*50)

    try:
        reg = Registry.Registry(sam_hive)
        users_key = reg.open("SAM\\Domains\\Account\\Users\\Names")

        print(f"{'Username':<30} | Status")
        print("-"*45)

        for user in users_key.subkeys():
            print(f"{user.name():<30} | OK")

    except Exception as e:
        print(f"[!] Error reading SAM: {e}")



def show_installed_apps(software_hive):
    print("\n" + "="*50)
    print("   [2] INSTALLED PROGRAMS (From SOFTWARE)")
    print("="*50)

    try:
        reg = Registry.Registry(software_hive)
        apps = reg.open("Microsoft\\Windows\\CurrentVersion\\Uninstall")

        print(f"{'Application':<50} | Version")
        print("-"*70)

        for app in apps.subkeys():
            try:
                name = app.value("DisplayName").value()
                ver = app.value("DisplayVersion").value() if "DisplayVersion" in [v.name() for v in app.values()] else "N/A"
                print(f"{name:<50} | {ver}")
            except:
                pass

    except Exception as e:
        print(f"[!] Error reading Installed Apps: {e}")



def show_usb_history(system_hive):
    print("\n" + "="*50)
    print("   [3] USB HISTORY (From SYSTEM)")
    print("="*50)

    try:
        reg = Registry.Registry(system_hive)
        usb_root = reg.open("ControlSet001\\Enum\\USBSTOR")

        for device in usb_root.subkeys():
            print(f"\nDevice Type: {device.name()}")

            for serial in device.subkeys():
                print(f"  -> Device ID: {serial.name()}")

                # NEW FIX: Get a friendly name
                usb_label = get_usb_name(serial)
                print(f"  -> USB Name: {usb_label}")

                # Last connected timestamp
                print(f"  -> Last Connected: {serial.timestamp()}")

            print("-"*40)

    except Exception as e:
        print(f"[!] Error reading USB history: {e}")



def show_user_activity(ntuser_hive):
    print("\n" + "="*50)
    print("   [4] USER ACTIVITY (From NTUSER.DAT)")
    print("="*50)

    try:
        reg = Registry.Registry(ntuser_hive)


        print("\n--- RunMRU Commands (RUN box history) ---")
        try:
            run_mru = reg.open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU")
            for val in run_mru.values():
                if val.name() != "MRUList":
                    print(f"  > {val.value()}")
        except:
            print("  No RunMRU data found.")


        print("\n--- UserAssist (Apps user opened) ---")
        ua_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"
        ua_root = reg.open(ua_path)

        for guid in ua_root.subkeys():
            try:
                count_key = reg.open(f"{ua_path}\\{guid.name()}\\Count")
                for entry in count_key.values():
                    decoded = rot13(entry.name())
                    if any(x in decoded.lower() for x in ["cmd", "ftp", "rar", "zip", "powershell"]):
                        print(f"  Suspicious Program: {decoded}")
            except:
                pass

    except Exception as e:
        print(f"[!] Error reading NTUSER.DAT: {e}")


if __name__ == "__main__":
    print("=== Simple Forensic Script ===")
    print("Make sure you have SAM, SOFTWARE, SYSTEM, and NTUSER.DAT ready.\n")

    sam = "SAM" if os.path.exists("SAM") else ask_path("SAM Hive")
    soft = "SOFTWARE" if os.path.exists("SOFTWARE") else ask_path("SOFTWARE Hive")
    syst = "SYSTEM" if os.path.exists("SYSTEM") else ask_path("SYSTEM Hive")
    nt = "NTUSER.DAT" if os.path.exists("NTUSER.DAT") else ask_path("NTUSER.DAT Hive")

    if sam: show_user_accounts(sam)
    if soft: show_installed_apps(soft)
    if syst: show_usb_history(syst)
    if nt: show_user_activity(nt)

    input("\nDone! Press Enter to exit...")
