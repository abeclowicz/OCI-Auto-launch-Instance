from oci.core import ComputeClient
from oci.core import models
from modules.utils import Text, default_name

class Image:
    def __init__(self, config: dict) -> None:
        self.client = ComputeClient(config)
        self.compartment_id = config["tenancy"]

    def group_by_os(self, images: list) -> dict:
        images_os = {}
        
        for index, image in enumerate(images):
            if image.operating_system not in images_os:
                images_os[image.operating_system] = []

            images_os[image.operating_system].append((index, image))

        return images_os
    
    def print_with_ids(self, images: list) -> None:
        for os, indexed_images in self.group_by_os(images).items():
            print(os + ':')

            for index, image in indexed_images:
                print(f"  - {Text(image.display_name, "BRIGHT_YELLOW")} [{Text(index + 1, "CYAN")}]")

    def get(self, auto = False) -> models.Image:
        images = self.client.list_images(
            compartment_id = self.compartment_id, 
            shape = "VM.Standard.A1.Flex"
        ).data

        if not images:
            raise Exception("No images in user's compartment for shape 'VM.Standard.A1.Flex'!")

        if auto:
            print(f"\"Auto\" mode is {Text("enabled", "BOLD", "BRIGHT_GREEN")}, selecting image automatically...")

            image = next(
                (image for image in images if "Ubuntu" in image.display_name), 
                images[0]
            )
        else:
            print(f"\"Auto\" mode is {Text("disabled", "BOLD", "BRIGHT_RED")}, please select image manually.")
            print(Text(f"{len(images)} image{'s'[:len(images) > 1]} available:", "BOLD", "BRIGHT_GREEN"), end = 2 * '\n')

            self.print_with_ids(images)

            index = input('\n' + "Enter the ID of the image to be selected: " + Text.codes["CYAN"])
            print(Text.codes["RESET"], end = '')

            while not index.isdigit() or not int(index) - 1 in range(len(images)):
                index = input('\033[F' + "Enter the ID of the image to be selected: " + Text.codes["CYAN"] + '\033[K')
                print(Text.codes["RESET"], end = '')

            image = images[int(index) - 1]
        
        print("selected image: " + Text(image.display_name, "BRIGHT_YELLOW"))
        return image

class Instance:
    def __init__(self, config: dict):
        self.client = ComputeClient(config)
        self.compartment_id = config["tenancy"]

    def build(self, **kwargs) -> models.LaunchInstanceDetails:
        required_kwargs = [
            "availability_domain", 
            "image_id", 
            "ssh_authorized_keys", 
            "subnet_id"
        ]

        missing_kwargs = [key for key in required_kwargs if key not in kwargs]
        if missing_kwargs:
            raise ValueError(f"Instance.build() has missing kwargs: {missing_kwargs}")
        
        optional_kwargs = [
            "boot_volume_size_in_gbs", 
            "boot_volume_vpus_per_gb", 
            "display_name", 
            "memory_in_gbs", 
            "ocpus"
        ]

        extra_kwargs = [key for key in kwargs if key not in required_kwargs + optional_kwargs]
        if extra_kwargs:
            raise ValueError(f"Instance.build() has extra kwargs: {extra_kwargs}")
        
        return models.LaunchInstanceDetails(
            agent_config = models.LaunchInstanceAgentConfigDetails(
                plugins_config = [
                    models.InstanceAgentPluginConfigDetails(
                        name = "Vulnerability Scanning",
                        desired_state = "DISABLED"),
                    models.InstanceAgentPluginConfigDetails(
                        name = "Compute RDMA GPU Monitoring",
                        desired_state = "DISABLED"),
                    models.InstanceAgentPluginConfigDetails(
                        name = "Compute Instance Monitoring",
                        desired_state = "ENABLED"),
                    models.InstanceAgentPluginConfigDetails(
                        name = "Compute HPC RDMA Auto-Configuration",
                        desired_state = "DISABLED"),
                    models.InstanceAgentPluginConfigDetails(
                        name = "Compute HPC RDMA Authentication",
                        desired_state = "DISABLED"),
                    models.InstanceAgentPluginConfigDetails(
                        name = "Block Volume Management",
                        desired_state = "DISABLED"),
                    models.InstanceAgentPluginConfigDetails(
                        name = "Bastion",
                        desired_state = "DISABLED")
                ]
            ), 
            availability_domain = kwargs["availability_domain"], 
            compartment_id = self.compartment_id, 
            create_vnic_details = models.CreateVnicDetails(
                assign_public_ip = True, 
                subnet_id = kwargs["subnet_id"]
            ), 
            display_name = kwargs.get("display_name", default_name("instance")), 
            metadata = {
                "ssh_authorized_keys": kwargs["ssh_authorized_keys"]
            }, 
            shape = 'VM.Standard.A1.Flex', 
            shape_config = models.LaunchInstanceShapeConfigDetails(
                memory_in_gbs = kwargs.get("memory_in_gbs", 24), 
                ocpus = kwargs.get("ocpus", 4)
            ), 
            source_details = models.InstanceSourceViaImageDetails(
                boot_volume_size_in_gbs = kwargs.get("boot_volume_size_in_gbs", 200), 
                boot_volume_vpus_per_gb = kwargs.get("boot_volume_vpus_per_gb", 120), 
                image_id = kwargs["image_id"], 
                source_type = "image"
            )
        )

    def launch(self, **kwargs) -> None:
        details = self.build(**kwargs)

        try:
            self.client.launch_instance(details).data
        except Exception as e:
            raise Exception(e.message)