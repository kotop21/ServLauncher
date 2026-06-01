import os


def accept_eula(server_path: str):
    eula_path = os.path.join(server_path, "eula.txt")
    with open(eula_path, "w", encoding="utf-8") as f:
        f.write(
            "#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n"
        )
        f.write("eula=true\n")
    print(f"[Core-util] EULA automatically accepted in {eula_path}")
