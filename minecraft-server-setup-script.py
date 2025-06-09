from urllib import request
import os
from time import sleep

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

def check_if_folder_exists():
    if not os.path.exists(f"{SCRIPT_PATH}/minecraft-server"):
        print("Server folder not present, creating...")
        sleep(1)
        os.makedirs(f"{SCRIPT_PATH}/minecraft-server")
        print("Folder created successfully.")
        return
    print("Server folder present, continuing...")
    sleep(1)

def accept_eula(eula_path):
    if not os.path.exists(eula_path):
        print("EULA file not found, creating...")
        with open(eula_path, 'w') as eula_file:
            eula_file.write("eula=true\n")
        print("EULA file created successfully.")
    else:
        with open(eula_path, 'r') as eula_file:
            content = eula_file.read()
            if "eula=true" not in content:
                print("EULA file found but not accepted, updating...")
                with open(eula_path, 'w') as eula_file:
                    eula_file.write("eula=true\n")
                print("EULA file updated successfully.")
            else:
                print("EULA file already accepted, skipping modification...")
    return

def create_bat():
    bat_path = f"{SCRIPT_PATH}/minecraft-server/start.bat"
    if os.path.exists(bat_path):
        print("Start server batch file already exists, skipping creation.")
        return
    ram_amount = input("Enter the amount of RAM to allocate to the server (in GB, default is 6): ")
    if not ram_amount.isdigit() or int(ram_amount) <= 0:
        print("Invalid RAM amount, using default value of 6GB.")
        print("You can change this in the start.bat file with the -Xmx_G flag.")
        ram_amount = 6
        soft_heap = 5
    soft_heap = max(int(ram_amount) - 1, 1)
    if not os.path.exists(bat_path):
        print("Creating start server batch file...")
        with open(bat_path, 'w') as bat_file:
            bat_file.write(
                "@echo off\n"
                f"java -Xmx{ram_amount}G -Xms1G -XX:SoftMaxHeapSize={soft_heap}G -XX:+UnlockExperimentalVMOptions "
                "-XX:+UseZGC -jar server.jar --nogui\n"
                "pause\n"
            )
        print("Start file created successfully.")
    else:
        print("Start file already exists, skipping creation.")

def download_server_file():
    server_path = f"{SCRIPT_PATH}/minecraft-server/server.jar"
    if os.path.exists(server_path):
        print("Server file already exists, skipping download.")
    else:
        print("Downloading server file...")
        request.urlretrieve("https://meta.fabricmc.net/v2/versions/loader/1.21.5/0.16.14/1.0.3/server/jar", 
                            f"{server_path}")
    return

def setup_server():
    check_if_folder_exists()
    print("Setting up Minecraft server...")
    sleep(0.2)
    print("Downloading server files...")
    sleep(0.2)
    download_server_file()
    print("Accepting eula...")
    sleep(0.2)
    accept_eula(f"{SCRIPT_PATH}/minecraft-server/eula.txt")
    print("Creating start file...")
    sleep(0.2)
    create_bat()
    sleep(0.2)
    print("Minecraft server setup completed successfully.")
    choice = input("Would you like to install optimization mods? (y/N): ")
    if choice.strip().lower() == 'y':
        install_optimization_mods()
    else:
        print("Skipping optimization mods installation.")
    choice = input("Would you like to apply recommended settings? (y/N): ")
    if choice.strip().lower() == 'y':
        apply_recommended_settings()
    else:
        print("Skipping recommended settings application.")
    print("You can now run the server by running the start.bat in the minecraft-server folder.")

def install_optimization_mods():
    if not os.path.exists(f"{SCRIPT_PATH}/minecraft-server/mods"):
        print("Mods folder not found, creating...")
        os.makedirs(f"{SCRIPT_PATH}/minecraft-server/mods")
        print("Mods folder created successfully.")
    print("Installing optimization mods...")
    sleep(0.2)
    print("Downloading Lithium...")
    request.urlretrieve("https://www.curseforge.com/api/v1/mods/360438/files/6401322/download",
                        f"{SCRIPT_PATH}/minecraft-server/mods/lithium.jar")
    print("Downloading Ferrite-Core...")
    request.urlretrieve("https://www.curseforge.com/api/v1/mods/459857/files/6365997/download",
                        f"{SCRIPT_PATH}/minecraft-server/mods/ferrite-core.jar")
    print("Downloading Sodium...")
    request.urlretrieve("https://www.curseforge.com/api/v1/mods/394468/files/6382664/download",
                        f"{SCRIPT_PATH}/minecraft-server/mods/sodium.jar")
    print("Downloading Fabric API...")
    request.urlretrieve("https://www.curseforge.com/api/v1/mods/306612/files/6614851/download",
                        f"{SCRIPT_PATH}/minecraft-server/mods/fabric-api.jar")
    sleep(0.2)
    print("Optimization mods installed successfully.")

def apply_recommended_settings():
    if not os.path.exists(f"{SCRIPT_PATH}/minecraft-server/server.properties"):
        print("Server properties file not found, downloading...")
        request.urlretrieve("https://raw.githubusercontent.com/Najfallik/minecraft-server-setup-script/main/server.properties",
                            f"{SCRIPT_PATH}/minecraft-server/server.properties")
    else:
        print("Server properties file found, applying recommended settings...")
        with open(f"{SCRIPT_PATH}/minecraft-server/server.properties", 'r') as server_properties:
            properties = server_properties.readlines()
        with open(f"{SCRIPT_PATH}/minecraft-server/server.properties", 'w') as server_properties:
            for line in properties:
                if line.startswith("difficulty="):
                    server_properties.write("difficulty=normal\n")
                elif line.startswith("motd="):
                    server_properties.write("motd=§l §7c        §a Sikkos Optimization script §4[1.21.5] §c§r\n§l  §c  §9§lHIGH PERFORMANCE §7- §5§lOPTIMIZED SERVER\n")
                elif line.startswith("view-distance="):
                    server_properties.write("view-distance=12\n")
                else:
                    server_properties.write(line)

def main_menu():
    while True:
        print("\nWelcome to the Minecraft Server Setup Script")
        print("1 - Setup Server")
        print("2 - Install optimization mods")
        print("3 - Apply recommended world settings")
        print("q - Exit")
        choice = input("Please select an option: ")

        if choice == '1':
            setup_server()
        elif choice == '2':
            install_optimization_mods()
        elif choice == '3':
            apply_recommended_settings()
        elif choice == 'q':
            print("Exiting...")
            exit(0)
        else:
            print("Invalid choice, please try again.")

def main():
    main_menu()

if __name__ == "__main__":
    main()