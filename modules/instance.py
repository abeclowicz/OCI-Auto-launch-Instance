from oci.core import ComputeClient, models
from modules.utils import default_name

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