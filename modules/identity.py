from oci.identity import IdentityClient
from modules.utils import Text

class AvailabilityDomains:
    def __init__(self, config: dict) -> None:
        self.client = IdentityClient(config)
        self.compartment_id = config["tenancy"]

    def print(self, availability_domains: list) -> None:
        print(f"{len(availability_domains)} availability domains detected:")

        for availability_domain in availability_domains:
            print(f"  - {Text(availability_domain.name, "BRIGHT_YELLOW")}")

    def get(self) -> list:
        availability_domains = self.client.list_availability_domains(self.compartment_id).data

        if not availability_domains:
            raise Exception("No availability domains in user's compartment!")
        
        self.print(availability_domains)

        return availability_domains