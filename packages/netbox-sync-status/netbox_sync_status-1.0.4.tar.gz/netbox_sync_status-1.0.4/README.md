# Netbox Sync Status

[Netbox](https://github.com/netbox-community/netbox) plugin that adds the capability to report system sync status backup to NetBox


It works by having the user create a number of `Sync Systems`, each sync system can then report back a `Sync Status` for a device, so that the end user will be able to see how it went. 

A full log of how all sync's went is saved so you can go back in history and view errors if needed.

## Compatibility

This plugin in compatible with [NetBox](https://netbox.readthedocs.org/) 4.0 and later.

## Installation

If Netbox was installed according to the standard installation instructions. It may be necessary to activate the virtual environment.

```
source /opt/netbox/venv/bin/activate
```

The plugin is available as a Python package in pypi and can be installed with pip

```
pip install netbox-sync-status
```
Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ["netbox-sync-status"]
```
Restart NetBox and add `netbox-sync-status` to your local_requirements.txt

## Screenshots
<p align="middle">
    <img align="top" src="/screenshots/sync_status_list.png?raw=true" width="32%" />
    <img align="top" src="/screenshots/sync_status_list.png?raw=true" width="32%" /> 
    <img align="top" src="/screenshots/sync_system_view.png?raw=true" width="32%" />
</p>


## Contributing
Developing tools for this project based on [ntc-netbox-plugin-onboarding](https://github.com/networktocode/ntc-netbox-plugin-onboarding) repo.

Issues and pull requests are welcomed.
