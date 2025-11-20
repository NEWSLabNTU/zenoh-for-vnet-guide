# Package Installation
Since Banana Pi R3 uses ARM-v8 architecture, it is 64 bit and mostly the things are fine.

## Package Manager
In the login message we can see the package manager has been switched from `opkg` to `apk`, you can see the table.

| OPKG Command          | APK Equivalent      | Description             |
|-----------------------|---------------------|-------------------------|
| `opkg install <pkg>`  | `apk add <pkg>`     | Install a package       |
| `opkg remove <pkg>`   | `apk del <pkg>`     | Remove a package        |
| `opkg upgrade`        | `apk upgrade`       | Upgrade all packages    |
| `opkg files <pkg>`    | `apk info -L <pkg>` | List package contents   |
| `opkg list-installed` | `apk info`          | List installed packages |
| `opkg update`         | `apk update`        | Update package lists    |
| `opkg search <pkg>`   | `apk search <pkg>`  | Search for packages     |

## Connect to computer
Since I don't know how to connect to the internet in R404, I decide to connect to the internet via my laptop.
Connect the WAN port of Banana Pi with the computer you want to share the network.
For Ubuntu, you need to change the config of IPv4 Method (the topmost content within IPv4 tab in the config page) to "Shared to other computers".
Connect the LAN port of Banana Pi with the computer you want to use SSH to control Banana Pi.
```
WAN - computer1 - Internet
LAN - computer2
```
My laptop can have 2 Ethernet ports, so I connect both to the same machine.
Now you should have the accessibility of the internet.

## Update package lists
```sh
apk update
```
You would see a lot of lists being updated. If you see
```
fetch https://downloads.openwrt.org/snapshots/targets/mediatek/filogic/kmods/6.6.74-1-f364c944b08df2b4a72a3622abb9722a/packages.adb
WARNING: updating and opening https://downloads.openwrt.org/snapshots/targets/mediatek/filogic/kmods/6.6.74-1-f364c944b08df2b4a72a3622abb9722a/packages.adb: remote server returned error (try 'apk update')
```
, this is just a warning, and you would always see the warning.

## Install packages
Before installation, you can peek the information by `apk info <package>`.
Install packages with
```sh
apk add <package>
```
Remember, the WARNING message is not an error, it just check all the repositories every time.
