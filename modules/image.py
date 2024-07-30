from oci.core import ComputeClient
from modules.utils import Text

class Image:
    def __init__(self, config):
        self.client = ComputeClient(config)
        self.compartment_id = config["tenancy"]

    def get(self, auto = False):
        images_list = self.client.list_images(
            compartment_id = self.compartment_id, 
            shape = "VM.Standard.A1.Flex"
        ).data

        if(not images_list):
            print(Text("No images available!", "BRIGHT_RED"))
            return None

        if(auto):
            print(f"\"Auto\" mode is {Text("enabled", "BOLD", "BRIGHT_GREEN")}, selecting image automatically...")

            image = next(
                (image for image in images_list if "Ubuntu" in image.display_name), 
                images_list[0]
            )
        else:
            print(f"\"Auto\" mode is {Text("disabled", "BOLD", "BRIGHT_RED")}, please select image manually.")
            print(Text(f"{len(images_list)} image{'s'[:len(images_list) > 1]} available:", "BOLD", "BRIGHT_GREEN"), end = 2 * '\n')

            os_images_list = {}

            for index, image in enumerate(images_list):
                if(image.operating_system not in os_images_list):
                    os_images_list[image.operating_system] = []

                os_images_list[image.operating_system].append((index, image))

            for operating_system, indexed_images in os_images_list.items():
                print(operating_system)
                
                for index, image in indexed_images:
                    print("  * " + Text(image.display_name, "BRIGHT_YELLOW") + f" [{Text(index + 1, "CYAN")}]")

            index = input('\n' + "Enter the ID of the image to be selected: " + Text.codes["CYAN"])
            print(Text.codes["RESET"], end = "")

            while((not index.isdigit()) or (not int(index) - 1 in range(len(images_list)))):
                index = input('\033[F' + "Enter the ID of the image to be selected: " + Text.codes["CYAN"] + '\033[K')
                print(Text.codes["RESET"], end = "")

            image = images_list[int(index) - 1]
        
        print("selected image: " + Text(image.display_name, "BRIGHT_YELLOW"))
        return image