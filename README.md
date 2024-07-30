# OCI Auto-launch Instance

Python script that automates launching an OCI virtual machine instance.

Made especially for *Oracle Cloud Free Tier* - that is, launching instances with ***4 OCPUs*** and ***24 GBs of memory*** and dealing with 
```Out of host capacity``` errors.

## Configuration

This script uses [Oracle Cloud Infrastructure Python SDK](https://github.com/oracle/oci-python-sdk). It can be installed using pip.

```sh
pip install oci
```

OCI SDK requires basic configuration information, like user credentials and tenancy OCID, saved in ```~/.oci/config```.

Example ```~/.oci/config``` file:

```ini
[DEFAULT]
user = ocid1.user.oc1..<unique_ID>
fingerprint = <your_fingerprint>
key_file = %HOMEPATH%\.oci\oci_api_key.pem
tenancy = ocid1.tenancy.oc1..<unique_ID>
region = us-ashburn-1
```

> [!NOTE]
> You can find more information about OCI SDK configuration file [here](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm).

## Usage

To run the script, use the following command:

```sh
python main.py
```

You can also include an ```--auto``` flag, which will set the instance's details automatically without prompting the user.

```sh
python main.py --auto
```

If a virtual machine instance is successfully created, its private key file ```<instance name>-key.pem``` will be saved in current directory. 
You can use it for SSH/SFTP authentication.

> [!WARNING]
> If it cannot be saved to a file, the private key will be displayed in a terminal window.
> Save it immediately - without the key, you won't be able to access the instance.

## License 

Licensed under the Apache License, Version 2.0 (the *License*).

You may not use this file except in compliance with the License.
You may obtain a copy of the License at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an **"AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND**, either express or implied. See the License for the specific language governing permissions and 
limitations under the License.

OCI SDK is a copyrighted (c) property of Oracle and/or its affiliates.