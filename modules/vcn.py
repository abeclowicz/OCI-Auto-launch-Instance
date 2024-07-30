from oci.core import VirtualNetworkClient
from oci.core.models import CreateVcnDetails

from modules.utils import Text, default_name

class Vcn:
    def __init__(self, client, compartment_id):
        self.client = client
        self.compartment_id = compartment_id

    def create(self, auto = False):
        if auto:
            name = default_name("vcn")
            print(f"Creating new virtual cloud network... [{Text(name, "BRIGHT_YELLOW")}]")
        else:
            name = input("Enter the name of the virtual cloud network to be created: " + Text.codes["BRIGHT_YELLOW"])
            print(Text.codes["RESET"], end = '')
        
        try:
            details = CreateVcnDetails(
                compartment_id = self.compartment_id, 
                display_name = name
            )

            vcn = self.client.create_vcn(details).data
            print(Text("Success!", "BOLD", "BRIGHT_GREEN"))
            
            return vcn
        except:
            raise Exception("Failed to create a virtual cloud network!")

    def get(self, auto = False):
        vcns = self.client.list_vcns(self.compartment_id).data * 0

        if not vcns:
            try:
                print(Text("No virtual cloud networks detected!", "BRIGHT_RED"), end = "\n\n")
                return self.create(auto)
            except Exception as e:
                raise e
        
        print(f"{len(vcns)} virtual cloud network{'s'[:len(vcns) > 1]} detected:")

        if auto or len(vcns) == 1:
            print(f"  * {Text(vcns[0].display_name, "BRIGHT_YELLOW")} [{Text("auto-selected", "CYAN")}]")

            for i in range(1, len(vcns)):
                print(f"  * {Text(vcns[i].display_name, "BRIGHT_YELLOW")}")

            return vcns[0]
        else:
            for index, vcn in enumerate(vcns):
                print(f"  * {Text(vcn.display_name, "BRIGHT_YELLOW")} [{Text(index + 1, "CYAN")}]")

            print('\n')

            while True:
                index = input('\033[F' + "Enter the ID of the virtual cloud network to be selected: " + '\033[K' + Text.codes["CYAN"])
                print(Text.codes["RESET"], end = '')

                try:
                    index = int(index) - 1
                    if 0 <= index < len(vcns):
                        print("Selected virtual cloud network: " + Text(vcns[index].display_name, "BRIGHT_YELLOW"))
                        return vcns[index]
                except ValueError:
                    pass