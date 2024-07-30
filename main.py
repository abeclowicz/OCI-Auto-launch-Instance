from argparse import ArgumentParser

parser = ArgumentParser(
    prog = "python main.py",
    description = "Python script that automates launching an OCI virtual machine instance.")

parser.add_argument(
    "-a", "--auto", 
    action = "store_true", 
    help = "\"auto\" mode, runs without user input (it will be set automatically)"
)

args = parser.parse_args()

# ======== ======== ======== ======== ======== ======== ======== ========

from oci.config import from_file
from oci.identity import IdentityClient
from modules.utils import Text

try:
    config = from_file(
        file_location = "~/.oci/config", 
        profile_name = "DEFAULT"
    )

    try:
        identity_client = IdentityClient(config)
        user = identity_client.get_user(config["user"]).data

        print("Authentication successful", f"[{Text(user.name, "BRIGHT_YELLOW")}]")
    except Exception as e:
        raise Exception(e.message)
        
except Exception as e:
    print(Text("Error:", "BOLD", "BRIGHT_RED"), Text(e, "RED"))
    exit()

# ======== ======== ======== ======== ======== ======== ======== ========

from modules.availability_domains import AvailabilityDomains
from modules.subnet import Subnet
from modules.image import Image
from modules.utils import ssh_keygen

try:
    print()
    availability_domains = AvailabilityDomains(config).get()

    print()
    subnet = Subnet(config).get(args.auto)

    print()
    image = Image(config).get(args.auto)

    private_key, public_key = ssh_keygen()

except Exception as e:
    print(Text("Error:", "BOLD", "BRIGHT_RED"), Text(e, "RED"))
    exit()

# ======== ======== ======== ======== ======== ======== ======== ========

from modules.utils import default_name

if args.auto:
    name = default_name("instance")
    print('\n' + "Name of the instance:", Text(name, "BRIGHT_YELLOW"), f"[{Text("auto-generated", "CYAN")}]")
else:
    name = input('\n' + "Enter the name of the instance: " + Text.codes["BRIGHT_YELLOW"])
    print(Text.codes["RESET"], end = '')

print("Creating new instance...")

# ======== ======== ======== ======== ======== ======== ======== ========

from modules.instance import Instance
from time import sleep
from pathlib import Path

attempt = 0

while True:
    for availability_domain in availability_domains:
        attempt += 1
        print('\n' + f"{Text(attempt, "CYAN")}:{availability_domain.name}")

        def launch_instance() -> None:
            try:
                Instance(config).launch(
                    availability_domain = availability_domain.name, 
                    display_name = name, 
                    image_id = image.id, 
                    ssh_authorized_keys = public_key, 
                    subnet_id = subnet.id
                )

                print(Text("Success:", "BOLD", "BRIGHT_GREEN"), "Instance created successfully.", end = "\n\n")

                try:
                    key_file = Path(f"{name}-key.pem")

                    if key_file.is_file():
                        raise FileExistsError
                    
                    key_file.write_text(private_key)

                    print(f"Saved private key file for authentication to {Text(f"'{str(key_file)}'", "CYAN")}.")
                except:
                    print(Text("Error:", "BOLD", "BRIGHT_RED"), Text("Failed to save private key file, printing it instead:", "RED"))
                    print('\n' + private_key)

                exit()
            except Exception as e:
                if str(e) == "Too many requests for the user":
                    print(f"{Text("Error:", "BOLD", "BRIGHT_YELLOW")} {str(e)}, waiting...")

                    sleep(2)
                    launch_instance()
                else:
                    print(f"{Text("Failed:", "BOLD", "BRIGHT_RED")} {str(e)}")

        launch_instance()

        sleep(1)