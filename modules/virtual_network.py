from oci.core import VirtualNetworkClient
from oci.core.models import CreateSubnetDetails, CreateVcnDetails
from oci.vn_monitoring import models
from modules.utils import Text, default_name

class Subnet:
    def __init__(self, config: dict) -> None:
        self.client = VirtualNetworkClient(config)
        self.compartment_id = config["tenancy"]

    def build(self, **kwargs) -> CreateSubnetDetails:
        required_kwargs = [
            "compartment_id", 
            "vcn_id"
        ]

        missing_kwargs = [key for key in required_kwargs if key not in kwargs]
        if missing_kwargs:
            raise ValueError(f"Subnet.build() has missing kwargs: {missing_kwargs}")

        optional_kwargs = [
            "cidr_block", 
            "display_name"
        ]

        extra_kwargs = [key for key in kwargs if key not in required_kwargs + optional_kwargs]
        if extra_kwargs:
            raise ValueError(f"Subnet.build() has extra kwargs: {extra_kwargs}")
        
        return CreateSubnetDetails(
            cidr_block = kwargs.get("cidr_block", "10.0.0.0/24"), 
            compartment_id = kwargs["compartment_id"], 
            display_name = kwargs.get("display_name", default_name("subnet")), 
            vcn_id = kwargs["vcn_id"]
        )

    def create(self, auto = False) -> models.Subnet:
        try:
            vcn = Vcn(self.client, self.compartment_id).get(auto)
        except Exception as e:
            raise e

        print('\n' + "No subnets detected:")

        if auto:
            name = default_name("subnet")
            print(f"  - Creating new subnet... [{Text(name, "BRIGHT_YELLOW")}]")
        else:
            name = input("  - Enter the name of the subnet to be created: " + Text.codes["BRIGHT_YELLOW"])
            print(Text.codes["RESET"], end = '')
        
        try:
            details = self.build(
                compartment_id = self.compartment_id, 
                display_name = name, 
                vcn_id = vcn.id
            )

            subnet = self.client.create_subnet(details).data
            print("  - " + Text("Subnet successfully created!", "BOLD", "BRIGHT_GREEN"))
            
            return subnet
        except:
            raise Exception("Failed to create a subnet!")
        
    def print(self, subnets: list, is_first_selected = False, with_ids = False) -> None:
        print(f"{len(subnets)} subnet{'s'[:len(subnets) > 1]} detected:")
        
        for index, subnet in enumerate(subnets):
            print(
                f"  - {Text(subnet.display_name, "BRIGHT_YELLOW")}", 
                f" [{Text("auto-selected", "CYAN")}]" if index == 0 and is_first_selected else '', 
                f" [{Text(index + 1, "CYAN")}]" if with_ids else '', 
                sep = ''
            )

    def get(self, auto = False) -> models.Subnet:
        subnets = self.client.list_subnets(self.compartment_id).data

        if not subnets:
            return self.create(auto)
        
        if auto or len(subnets) == 1:
            self.print(subnets, is_first_selected = True)
            return subnets[0]
        
        self.print(subnets, with_ids = True)

        index = input('\n' + "Enter the ID of the subnet to be selected: " + Text.codes["CYAN"])
        print(Text.codes["RESET"], end = '')

        while True:
            try:
                index = int(index) - 1
                if 0 <= index < len(subnets):
                    break
            except ValueError:
                pass

            index = input('\033[F' + "Enter the ID of the subnet to be selected: " + '\033[K' + Text.codes["CYAN"])
            print(Text.codes["RESET"], end = '')

        print("selected subnet: " + Text(subnets[index].display_name, "BRIGHT_YELLOW"))

        return subnets[index]
    
class Vcn:
    def __init__(self, client: VirtualNetworkClient, compartment_id: str) -> None:
        self.client = client
        self.compartment_id = compartment_id

    def build(self, **kwargs) -> CreateVcnDetails:
        required_kwargs = [
            "compartment_id"
        ]

        missing_kwargs = [key for key in required_kwargs if key not in kwargs]
        if missing_kwargs:
            raise ValueError(f"Vcn.build() has missing kwargs: {missing_kwargs}")

        optional_kwargs = [
            "display_name"
        ]

        extra_kwargs = [key for key in kwargs if key not in required_kwargs + optional_kwargs]
        if extra_kwargs:
            raise ValueError(f"Vcn.build() has extra kwargs: {extra_kwargs}")
        
        return CreateVcnDetails(
            compartment_id = kwargs["compartment_id"], 
            display_name = kwargs.get("display_name", default_name("subnet"))
        )

    def create(self, auto = False) -> models.Vcn:
        print("No virtual cloud networks detected:")

        if auto:
            name = default_name("vcn")
            print(f"  - Creating new virtual cloud network... [{Text(name, "BRIGHT_YELLOW")}]")
        else:
            name = input("  - Enter the name of the virtual cloud network to be created: " + Text.codes["BRIGHT_YELLOW"])
            print(Text.codes["RESET"], end = '')
        
        try:
            details = self.build(
                compartment_id = self.compartment_id, 
                display_name = name
            )

            vcn = self.client.create_vcn(details).data
            print("  - " + Text("Virtual cloud network successfully created!", "BOLD", "BRIGHT_GREEN"))
            
            return vcn
        except:
            raise Exception("Failed to create a virtual cloud network!")
        
    def print(self, vcns: list, is_first_selected = False, with_ids = False) -> None:
        print(f"{len(vcns)} virtual cloud network{'s'[:len(vcns) > 1]} detected:")
        
        for index, vcn in enumerate(vcns):
            print(
                f"  - {Text(vcn.display_name, "BRIGHT_YELLOW")}", 
                f" [{Text("auto-selected", "CYAN")}]" if index == 0 and is_first_selected else '', 
                f" [{Text(index + 1, "CYAN")}]" if with_ids else '', 
                sep = ''
            )

    def get(self, auto = False) -> models.Vcn:
        vcns = self.client.list_vcns(self.compartment_id).data

        if not vcns:
            return self.create(auto)
        
        if auto or len(vcns) == 1:
            self.print(vcns, is_first_selected = True)
            return vcns[0]
        
        self.print(vcns, with_ids = True)

        index = input('\n' + "Enter the ID of the virtual cloud network to be selected: " + Text.codes["CYAN"])
        print(Text.codes["RESET"], end = '')

        while True:
            try:
                index = int(index) - 1
                if 0 <= index < len(vcns):
                    break
            except ValueError:
                pass

            index = input('\033[F' + "Enter the ID of the virtual cloud network to be selected: " + '\033[K' + Text.codes["CYAN"])
            print(Text.codes["RESET"], end = '')

        print("selected virtual cloud network: " + Text(vcns[index].display_name, "BRIGHT_YELLOW"))

        return vcns[index]