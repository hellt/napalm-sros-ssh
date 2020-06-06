Nokia SR OS NAPALM driver based on SSH transport.

## Installation
To install the latest version from master:
```
pip install https://github.com/hellt/napalm-sros-ssh/archive/master.zip
```

## Supported NAPALM methods

* `get_config`
* `load_merge_candidate`
* `load_replace_candidate`
* `commit_config`
* `discard_config`
* `compare_config`

## Usage example

```python
import napalm
import sys

driver = napalm.get_network_driver("sros_ssh")

device = driver(
    hostname="192.168.1.10",
    username="admin",
    password="admin",
    optional_args={"fast_cli": True},
)

print("Opening ...")
device.open()

# testing get_config
print(device.get_config()["running"])


"""Load a config for the SR OS device."""
config_file = sys.argv[1]
print("Loading config file {0}.".format(config_file))

print("Loading merge candidate ...")
device.load_merge_candidate(filename=config_file)

# Load replace block
# print("Loading replace candidate ...")
# device.load_replace_candidate(filename=config_file)

# Note that the changes have not been applied yet. Before applying
# the configuration you can check the changes:
print("\nDiff:")
print(device.compare_config())

# You can commit or discard the candidate changes.
try:
    choice = raw_input("\nWould you like to commit these changes? [yN]: ")
except NameError:
    choice = input("\nWould you like to commit these changes? [yN]: ")
if choice == "y":
    print("Committing ...")
    device.commit_config()
else:
    print("Discarding ...")
    device.discard_config()

# close the session with the device.
device.close()
print("Done.")
```

## Napalm-ansible integration
Currently the driver supports the following modules from [napalm-ansible](https://github.com/napalm-automation/napalm-ansible) integration project (check [examples](examples/ansible)):

* napalm_install_config