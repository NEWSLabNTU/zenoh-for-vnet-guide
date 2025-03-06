# Banana Pi BPI-R3 Mini Guide

This guide is a step by step guide to flash the Banana Pi BPI-R3 Mini with the latest OpenWRT operating system and manual to make a basic configuration.


## Installing OpenWRT on eMMC memory

The device BPI-R3 Mini supports installing operating system on the eMMC and NAND memory. For our use-cases, i.e., using Zenoh and other advanced packages, we choose using eMMC due to being faster and bigger memory. However, feel free to try the NAND memory and provide the comparation feedback.

### Preparation

Download all required files from the official OpenWRT webpage:
```
https://downloads.openwrt.org/snapshots/targets/mediatek/filogic/
```

Look for the images and files that start with:
```
bananapi_bpi-r3-mini-*
```

and includes *emmc* as part of its name. The full list of files is provided as follows:
```
*-emmc-bl31-uboot.fip
*-emmc-gpt.bin
*-emmc-preloader.bin
*-initramfs-recovery.itb
*-squashfs-sysupgrade.itb
```

Move all the files (5 in total) onto USB-A Flash Drive. 

To install the images onto the eMMC memory, a switch on the BPI-R3 board must be switched in NAND mode as it is illustrated on the picture. 

![eMMC/NANC Switch](https://wiki.banana-pi.org/images/a/af/R3mini_NANDBOOT2.png)

### Console connection

The following steps describes communication between BPI-R3 Mini connected by a USB-C cable to a Linux computer. 

The BPI-R3 Mini provides two USB interfaces: a) USB-C that is used to power the device and for console communication; b) USB-A that is used for data transfer and connecting other peripheries.

Connect the BPI-R3 Mini by the USB-C interface with the linux PC and checked if the device was correctly recognized by executing:
```
sudo dmesg | grep uart
```

You should see an output similar to this line:
```
[1379597.621620] usb 1-5: ch341-uart converter now attached to ttyUSB0
```

The host system signals that the device is connected via *ttyUSB0*. Then check, if the device is still present in the list of devices by executing:
```
ls /dev/ttyU*
```

If you do not see the device, check the troubleshooting section. Otherwise, connect to the device using **screen** application (make sure, it is installed on the host machine, and have the right permissions).
```
sudo screen /dev/ttyUSB0 115200
```

If success, you should see command line interface of the device.
```
root@OpenWrt:/# 
```

### Flashing the device

Since you are connected via console, attach the prepared USB-A Flash Drive into the USB-A port and check if the flash drive is auto-mounted. 
```
df
```

If not, do it manualy by the following command:
```
mount -t vfat /dev/sda /mnt/sda
```

Otherwise, you will see the mounted flash drive as follows:
```
/dev/sda              30704976    108528  30596448   0% /mnt/sda
```

Change the current directory to the flash drive by:
```
cd /mnt/sda
```


Write GPT partition table to eMMC using the *dd* tool. Copy the *\*emmc-gpt.bin* file to the device block */dev/mmcblk0*. Make sure you copy the right files. 

**Change the images' names accordingly to the downloaded naming!**

**Do not copy and paste the commands that include *dd*!**
```
dd if=openwrt-*-r3-mini-emmc-gpt.bin of=/dev/mmcblk0
```

Reboot the device executing:
```
reboot
```

After the reboot, change the dir to the */mnt/sda*. And copy the remaining files to the corresponding blocks as follows:
```
echo 0 > /sys/block/mmcblk0boot0/force_ro
dd if=openwrt-*-bananapi_bpi-r3-mini-emmc-preloader.bin of=/dev/mmcblk0boot0
dd if=openwrt-*-bananapi_bpi-r3-mini-emmc-bl31-uboot.fip of=/dev/mmcblk0p3
dd if=openwrt-*-bananapi_bpi-r3-mini-initramfs-recovery.itb of=/dev/mmcblk0p4
dd if=openwrt-*-bananapi_bpi-r3-mini-squashfs-sysupgrade.itb of=/dev/mmcblk0p5
sync
```


1. Remove the device from power. 
2. Set the boot switch to eMMC.
3. Power on the device.
4. Connect an ethernet cable to the LAN port.
5. The device' default IP address is 192.168.1.1 

Connect to the device by *ssh* as *root* by:
 ```
 ssh root@192.168.1.1
 ```
 
 Done! 
 
 If you connect "internet" to the WAN port, you can update packages by executing: 
 ```
 apk update
 ```

Internet is required for the next section!
 
 ... let's [use the remaining space on our disk](#Creating-a-new-partition) :)
 
#### Troubleshooting:
 
- If the device connects and then disconnects (i.e., ttyUSB0), then remove the 'brltty' package (solution found at [askubuntu.com](https://askubuntu.com/questions/1482767/error-while-connecting-a-device-with-ch341))
```
sudo apt autoremove brltty
```

- Permission denied to connect to the device via screen.
```
sudo usermod -aG dialout $USER
```

- Unable to detach from the 'screen' console, press:
```
ctrl+a + d
```


## Creating a new partition

The default installation OpenWRT images includes pre-defined size of partitions. However, our BPI-R3 Mini includes larger disk so we must extend or create a new partition (our case) to utilise the full disk space.

Install required packages (required internet access):
```
apk update
apk add parted e2fsprogs block-mount
```

Print the info about the block devices:
```
parted /dev/mmcblk0 print
```

Modify the block device */dev/mmcblk0* using the tool *parted* executing:
```
parted /dev/mmcblk0
```

It opens an interactive interface so continue by:
1. OK
2. fix

and entry the parted mode.

Find the 'end' of the last partition from the printed info (e.g., 537 MB) and use the ending size to start a new partition. Executing the following command, you creaet a new partition with the *ext4* file system, starting from the 537MB (change this number accordinly) up to the 100% of the size of the drive.
```
(parted) mkpart primary ext4 537MB 100%
```

Name the new partition, e..g, 'data' and use the next partition number that is printed as the last from the printed into, e.g, 6. The command then be as: 
*name <partition_number> <partition_name>*
```
 (parted) name 6 data
```

Exit the interactive parted mode:
```
(parted) quit
```

Format the newly created partition. **Note that the 'p6' at the end is the parition number!** (please, change it accordingly).
```
mkfs.ext4 /dev/mmcblk0p6
```

Create a mounting point, e.g., /mnt/data
```
mkdir -p /mnt/data
```

Create a record in the */etc/fstab* according to the naming from prevous steps:
*echo '<partition_name> <mounting_point> ext4 defaults 0 0' >> /etc/fstab'*
```
echo '/dev/mmcblk0p6 /mnt/data ext4 defaults 0 0' >> /etc/fstab
```

Mount all partitions in *fstab*:
```
mount -a
```

Check the sizes. You should see that the new partition mounted to */mnt/data* is using the remaining space of the disk.
```
df -h
```

If you see utilising the full disk, then enable auto-mounting after bootup.

Generate a default (i.e., the current) configuration by executing:
```
block detect | uci import fstab
```

Open the config file:
```
vim /etc/config/fstab
```

Configure the '*config mount*' section according to the parameters of the partition, i.e., *target block device, uuid, target directory, enabled'*. 
Note that the parameters should be already correct and not to be modified.
```
config mount
        option target '/mnt/mmcblk0p6'
        option uuid '<UUID OF THE DISK>'
        option target '/mnt/data'
        option enabled '1'
```

Reboot...
```
# reboot
```

...and check, if the partition is mounted at the '/mnt/data' folder:
```
# df -h
```

Done!

Let's introduce you into the other networking configuration files :)

## Network configuration

The main configuration is present in the files:

wired interface -> /etc/config/network
wireless interface -> /etc/config/wireless

## Wired Interface

The device BPI-R3 Mini includes two ethernet ports marked as LAN and WAN. They can be configured independently and changed the original functionality. However, the default configuration is as follows:

```
config interface 'loopback'
	option device 'lo'
	option proto 'static'
	option ipaddr '127.0.0.1'
	option netmask '255.0.0.0'

config globals 'globals'
	option ula_prefix 'fdce:ae9:5f67::/48'

config device
	option name 'br-lan'
	option type 'bridge'
	list ports 'eth0'

config interface 'lan'
	option device 'br-lan'
	option proto 'static'
	option ipaddr '192.168.1.2'
	option netmask '255.255.255.0'
	option ip6assign '60'

config device
	option name 'eth1'
	option macaddr 'b2:9c:3b:32:dd:b7'

config interface 'wan'
	option device 'eth1'
	option proto 'dhcp'

config interface 'wan6'
	option device 'eth1'
	option proto 'dhcpv6'
```

The first step is to configure a device in a section as 'config device'. 
```
config device
	option name 'br-lan'
	option type 'bridge'
	list ports 'eth0'
    
config device
	option name 'eth1'
	option macaddr 'b2:9c:3b:32:dd:b7'
```

Two devices are configured, one as the *br-lan* that includes list of ports. Due to the limitation of having only two ports which one is marked as LAN and second as WAN, only the port *eth0* is added into this bridge. The second device (i.e., WAN port) is the *eth1*. 

Configuring an interface adds properties to the network. The default configuration includes following interfaces:
```
config interface 'loopback'
	option device 'lo'
	option proto 'static'
	option ipaddr '127.0.0.1'
	option netmask '255.0.0.0'
    
config interface 'lan'
	option device 'br-lan'
	option proto 'static'
	option ipaddr '192.168.1.2'
	option netmask '255.255.255.0'
	option ip6assign '60'
    
config interface 'wan'
	option device 'eth1'
	option proto 'dhcp'
```
The first *loopback* is local address. The second interface *lan* is the configuration for ports that are part of the device *br-lan* configured in the previous step. It includes static IP address and mask. The *wan* interface uses the device *eth1* and expects to get and IP address via DHCP v4. **Note when you look at the BRP-R3 Mini you see a red sticker such as A or B. It is used to recognised the IP address of the device, i.e., A = 192.168.1.1, B = 192.168.1.2.**

```
config interface 'wan6'
	option device 'eth1'
	option proto 'dhcpv6'
```
The last interface *wan6* uses the same device *eth1* and is configured to get IP address via DHCP v6.


## Wireless Network
[OpenWRT Wireless Doc](https://openwrt.org/docs/guide-user/network/wifi/basic)
The device BPI-R3 Mini includes radio transmitter supporting Wifi 6 and frequencies 2.4 GHz and 5 GHz. Each band can be configured separatelly and follows the same approach as in the case of ethernet ports. The sample configuration is as follows:
```
config wifi-device 'radio0'
	option type 'mac80211'
	option path 'platform/soc/18000000.wifi'
	option band '2g'
	option channel '1'
	option htmode 'HE20'
	option disabled '1'

config wifi-iface 'default_radio0'
	option device 'radio0'
	option network 'lan'
	option mode 'ap'
	option ssid 'OpenWrt'
	option encryption 'none'

config wifi-device 'radio1'
	option type 'mac80211'
	option path 'platform/soc/18000000.wifi+1'
	option band '5g'
	option channel '100'
	option htmode 'HE160'
	option country 'TW'

config wifi-iface 'default_radio1'
        option device 'radio1'    
        option network 'lan'      
        option mode 'ap' 
        option ssid 'OpenWrt_5G'  
        option encryption 'sae'   
        option key 'mysecretpassword'  
```

At first, a wireless device must be connfigured. This config changes settings for the driver of each band. Because the supported wireless network is IEEE 802.11, some of the following parameters can't be change. However, let's explain the meaning:
- **type** determines the chipset driver type (not need to change it)
- **path** identifies the device's path (**Do not change it**)
- **band** specifies eather 2g for 2.4 GHz or 5g for 5 GHz
- **htmode** identifies the throughput mode, e.g., HE160 is 160 MHz
- **channel** specifies the wireless channel
```
config wifi-device 'radio0'
	option type 'mac80211'
	option path 'platform/soc/18000000.wifi'
	option band '2g'
	option htmode 'HE20'
    option channel '1'
    
 config wifi-device 'radio1'
	option type 'mac80211'
	option path 'platform/soc/18000000.wifi+1'
	option band '5g'
    option htmode 'HE160'
	option channel '100'
	option country 'TW'  
```

Having configured the wireless devices, to configure the WiFi, we need to define a wireless interface as a section *wifi-iface*:
- **device** specifies which wireless device is used for the interface (see *wifi-device* section)
- **network** determines in which network is the interface part of, i.e., the network interface created in the network section as *config interface 'lan'*.
- **mode** specifies in which mode the interface is operating, e.g., ap = access point
- ssid, encryption, key and others
```
config wifi-iface 'default_radio0'
	option device 'radio0'
	option network 'lan'
	option mode 'ap'
	option ssid 'OpenWrt'
	option encryption 'none'

config wifi-iface 'default_radio1'
        option device 'radio1'    
        option network 'lan'      
        option mode 'ap' 
        option ssid 'OpenWrt_5G'  
        option encryption 'sae'   
        option key 'mysecretpassword'  
```


## System Configuration
[OpenWRT System Doc](https://openwrt.org/docs/guide-user/base-system/system_configuration)

Change the default parameters for your location accordingly, i.e., hostname, timezone, zonename.

```
config system
	option hostname 'OpenWrt'
	option timezone 'GMT8'
	option zonename 'Asia/Taipei'
```

### Init Script
[OpenWRT Init-Script Doc](https://openwrt.org/docs/guide-developer/procd-init-script-example)

Folder to paste the binary *zenohd*:
```
/usr/bin/zenohd
```

Create a file at the path:
```
/etc/init.d/zenohd
```

With the following content:
```
#!/bin/sh /etc/rc.common
USE_PROCD=1
START=95
STOP=01
start_service() {
    procd_open_instance
    procd_set_param command /usr/bin/zenohd --config /etc/config/zenohd.yaml 
    procd_set_param stdout 1
    procd_set_param stderr 1
    procd_close_instance
}
```

To enable the service after bootup:
```
/etc/init.d/zenohd enable
```

To verify if the service is registered:
```
ls -la /etc/rc.d/S*
```

To manualy control (e.g., start) the service
```
/etc/init.d/zenohd start
```

### Set the current time
[OpenWRT NTP Doc](https://openwrt.org/docs/guide-user/services/ntp/client-server)

The devices can not hold the precise time so they need to synchronize it using the Network Time Protocol (NTP). One way is to connect the BPI to the internet via WAN port and get time time from a NTP server. 

If you do not want to connect the BPI to the internet (prefered), install NTP server on your local computer and configure the corresponding server based on your location ([for Taiwan](https://www.ntppool.org/zone/tw)). Than connect your computer to the same network (e.g., by cable) as the BPI while being connected to the internet (e.g., by wifi). On all BPIs execute requesting for the actual time.
```
ntpd -q -p <server_ip>
```

If you use the same computer for the experiments and have a static IP address, you can also adjust the configuration at: */etc/config/system* as follows:
```
config timeserver 'ntp'
	option enabled '1'
	option enable_server '0'
	list server '<ntp_server_ip>'
```

# Zenoh Deployment
[Zenoh Full Config JSON File](https://github.com/eclipse-zenoh/zenoh/blob/main/DEFAULT_CONFIG.json5)


The device BPI-R3 Mini is SoC ARM based (aarch64) so to compile the Zenoh project on x86 platform, a cross-compyling approch must be choosen. 


### Cargo config
Add the target:
```
rustup target add aarch64-unknown-linux-musl
```

Verify if the toolchain is correctly installed:
```
rustup target list --installed
```

Add the configuration to use *gcc* as the linker at the file: *.cargo/config.toml*
as follows:
```
[target.aarch64-unknown-linux-musl]
rustflags = "-Ctarget-feature=-crt-static"
linker = "aarch64-linux-musl-gcc"
```

### Compiler toolchain
In order to cross-compile the project, musl tools are required. Jump to the folder where the tools to instlal and then execute:
```
wget -qO- https://musl.cc/aarch64-linux-musl-cross.tgz | tar zxvf -
```

Add the tools to *path*:
```
export PATH="$PATH:$(pwd)/aarch64-linux-musl-cross/bin"
```

Verify if the installation was successful:
```
aarch64-linux-musl-gcc --version
```

If so, define *CC* env variable to use the musl-gcc toolchain:
```
export CC=aarch64-linux-musl-gcc
```l

### Build
Build the Zenoh project for the *aarch64* target:
```
cargo build --release --target=aarch64-unknown-linux-musl
```

### Deploy
If successfull build, then move the binary onto the BPI into the folder */usr/bin/* using scp:
```
scp ./target/aarch64-unknown-linux-musl/release/zenohd root@192.168.1.1:/usr/bin/zenohd
```

Done!

In case of any errors, try any of those:

If missign some tools for compilation, install the *musl-tools*:
```
sudo apt install musl-tools
```

Set the variable *CC_aarch64_unknown_linux_musl* to the linker:
```
export CC_aarch64_unknown_linux_musl=aarch64-linux-musl-gcc
```