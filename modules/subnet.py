from oci.core import VirtualNetworkClient
from oci.core.models import CreateSubnetDetails

from modules.vcn import Vcn
from modules.utils import Text, default_name

class Subnet:
    def __init__(self, config):
        self.client = VirtualNetworkClient(config)
        self.compartment_id = config["tenancy"]

    def create(self, vcn, auto = False):
        if auto:
            name = default_name("subnet")
            print(f"Creating new subnet... [{Text(name, "BRIGHT_YELLOW")}]")
        else:
            name = input("Enter the name of the subnet to be created: " + Text.codes["BRIGHT_YELLOW"])
            print(Text.codes["RESET"], end = '')
        
        try:
            details = CreateSubnetDetails(
                cidr_block = "10.0.0.0/24", 
                compartment_id = self.compartment_id, 
                display_name = name, 
                vcn_id = vcn.id
            )

            subnet = self.client.create_subnet(details).data
            print(Text("Success!", "BOLD", "BRIGHT_GREEN"))
            
            return subnet
        except:
            raise Exception("Failed to create a subnet!")

    def get(self, auto = False):
        subnets = self.client.list_subnets(self.compartment_id).data

        if not subnets:
            try:
                vcn = Vcn(self.client, self.compartment_id).get(auto)

                print('\n' + Text("No subnets detected!", "BRIGHT_RED"), end = "\n\n")
                return self.create(vcn, auto)
            except Exception as e:
                raise e
        
        print(f"{len(subnets)} subnet{'s'[:len(subnets) > 1]} detected:")

        if auto or len(subnets) == 1:
            print(f"  * {Text(subnets[0].display_name, "BRIGHT_YELLOW")} [{Text("auto-selected", "CYAN")}]")

            for i in range(1, len(subnets)):
                print(f"  * {Text(subnets[i].display_name, "BRIGHT_YELLOW")}")

            return subnets[0]
        else:
            for index, subnet in enumerate(subnets):
                print(f"  * {Text(subnet.display_name, "BRIGHT_YELLOW")} [{Text(index + 1, "CYAN")}]")

            print('\n')

            while True:
                index = input('\033[F' + "Enter the ID of the subnet to be selected: " + '\033[K' + Text.codes["CYAN"])
                print(Text.codes["RESET"], end = '')

                try:
                    index = int(index) - 1
                    if 0 <= index < len(subnets):
                        print("Selected subnet: " + Text(subnets[index].display_name, "BRIGHT_YELLOW"))
                        return subnets[index]
                except ValueError:
                    pass