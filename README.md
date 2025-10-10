# What is this ?
This is the documentation on how to get started and moving around with the **Luckfox Pico Mini B**, since it's hard and scarce to find clean and updated instructions, I decided to organize and document things myself, including couple experiments to test the board capabilities. I will be using SD card for pico images, Buildroot OS for the experiments and a laptop with Linux as the host development environment (Lubuntu 24.04).

# Luckfox Pico Mini B

<img width="476" height="296" alt="image" src="https://github.com/user-attachments/assets/1c2d5bec-3074-46e2-bde0-f2966a4bd539" />

It's a tiny $9 Linux capable board, with low energy consumption and some interesting performance and capabilites. As opposite to a more tradicional, well supported and known SBC like the Raspberry Pi, this one will require to deal with lower level development, configurations and hardware knowledge, things will be harder and more challenging, but all that will help you to understand how things work and are connected, also force you to keep a more lean system, and be less wasteful on resources usage.

Altought this verison has 128 MB Flash, that is too small for the experiments I will be doing, that is why my focus will be using SD card. The SDK is the official tool supplied by Luckfox, which allows the creation of OS images from scratch, using a thing called **buildroot** alongside with their `build.sh` script and couple other config files. Some settings will not be possible to be changed in an existing OS image, those cases will require the generation of a new image, keep that in mind when using an existing image versus being able to compile and generate one yourself.

The 128 MB flash may be enough once you get your OS image optimized to only contain what is really needed by your application. That is the challenge, learn to survive with only 128 MB of disk once you reach that point! 

| **Category**       | **Specification**                              |
|--------------------|------------------------------------------------|
| **Processor**      | 32-bit ARM Cortex A7 @ 1.2GHz + RISC-V         |
| **NPU**            | 0.5TOPS, supports int4, int8 and int16         |
| **ISP**            | Input 4M @30fps (Max)                          |
| **Memory**         | 64MB DDR2                                      |
| **USB**            | USB 2.0 Host/Device                            |
| **Camera**         | MIPI CSI 2-lane                                |
| **GPIO**           | 17 × GPIO pins                                 |
| **Default Storage**| SPI NAND FLASH (128MB) |

Notice although it has a RISC-V **MCU**, info about it is rarely found, the main SoC and where everything happens is in the ARM v7.  
<img width="1017" height="837" alt="image" src="https://github.com/user-attachments/assets/bf2b6627-f2e0-46bf-b742-df9c8c6ccf66" />
<img width="1107" height="461" alt="image" src="https://github.com/user-attachments/assets/218060b0-ab7a-442f-b486-03a574b00f4f" />
<img width="3000" height="2205" alt="image" src="https://github.com/user-attachments/assets/3561d0bb-bf7c-49d9-a5ca-5fe01d22fab3" />

# Rockchip RV1103 vs RV1106
Despite this verions having a **RV1103** SoC, you'll notice many files using configurations from the **RV1106** as well, so don't disregard RV1106-specific content, because most things are compatible between them.

| Parameter | RV1103 | RV1106 |
|:---|:---:|:---:|
| **Processor** | Single-core Cortex-A7 @ 1.5GHz | Single-core Cortex-A7 @ 1.5GHz |
| **Process Node** | 14nm | 14nm |
| **Cache** | 32KB I/D + 128KB L2 | 32KB I/D + 128KB L2 |
| **NPU** | 0.5TOPs (INT4/INT8/INT16) | 0.5TOPs (INT4/INT8/INT16) |
| **MCU** | RISC-V @ 400MHz | RISC-V @ 400MHz |
| **ISP** | 4 million pixels | 5 million pixels |
| **Video Encoding** | H.265/H.264 4MP@30 | H.265/H.264 5MP@30 |
| **Video Decoding** |  |  |
| **Memory Support** | DDR2 | DDR3L |
| **Built-in Memory** | 64MB DDR2 | 128MB DDR3L |
| **External Storage** | 16Bit, SPI FLASH, SD3.0, MMC ver4.5 | 16Bit, eMMC 4.51, SPI FLASH, SD3.0, MMC ver4.51 |
| **Interface Support** | Dual MIPI CSI/LVDS | Dual MIPI CSI/LVDS + DVP |
| **Camera Support** | 2xMIPI-CSI (4MP) + 1xDVP | 2xMIPI-CSI (5MP) + 1xDVP |
| **Display Interface** |  | 1xMCU TX, 1xUART TX, 1xBT.1120 TX, 1xRGB666 |
| **Max Display Resolution** |  | 1280x720 |
| **USB** | 1xUSB 2.0 OTG | 1xUSB 2.0 OTG |
| **Ethernet** | 1xEthernet (100M/10M) | 1xEthernet (100M/10M) |
| **Audio Interface** | Audio Codec | 1xI2S (8ch) + 3xI2S (2ch) + Audio Codec |
| **I/O Interfaces** | 2xSPI, 5xI2C, 12xUART, 6xPWM, 1xADC, 12xGPIO | 2xSPI, 5xI2C, 6xUART, 12xPWM, 6xADC, 1xDAC, 12xGPIO |
| **Package** | QFN88 (9mm x 9mm, 0.35mm pitch) | QFN128 (12.3mm x 12.3mm, 0.35mm pitch) |
| **Operating System** | Linux | Linux |
| **Temperature Range** | -40°C to 125°C (storage), 0°C to 80°C (operating) | -40°C to 125°C (storage), 0°C to 80°C (operating) |
| **Key Features** | Fast boot, Low power consumption, 4th gen NPU | Fast boot, Low power consumption, 4th gen NPU |
| **Applications** | IP Camera, Visual processing AI applications | IP Camera, Visual processing AI applications |

# Getting started
To start quickly, plug your SD card on the host machine and download `Ubuntu_Luckfox_Pico_Mini_B_MicroSD_250313.zip` from here:
https://drive.google.com/drive/folders/14kFWY93MZ4Zga4ke2PVQgUs1y9xcMG0S

Extract and run the [`blkenvflash`](#blkenvflashpy-tool) tool inside:
```bash
$ unzip Ubuntu_Luckfox_Pico_Mini_B_MicroSD_250313.zip
$ cd Ubuntu_Luckfox_Pico_Mini_B_MicroSD_250313
$ sudo python3 blkenvflash.py /dev/sdb
== blkenvflash.py 0.0.1 ==
writing to /dev/sdb
   mmcblk1: env.img size:32,768/32K (offset:0/0B) imgsize:32,768 (32K)
   mmcblk1: idblock.img size:524,288/512K (offset:32,768/32K) imgsize:188,416 (184K)
   mmcblk1: uboot.img size:262,144/256K (offset:0/0B) imgsize:262,144 (256K)
   mmcblk1: boot.img size:33,554,432/32M (offset:0/0B) imgsize:3,150,336 (3,150,336B)
   mmcblk1: oem.img size:536,870,912/512M (offset:0/0B) imgsize:113,909,760 (111,240K)
   mmcblk1: userdata.img size:268,435,456/256M (offset:0/0B) imgsize:9,999,360 (9,765K)
   mmcblk1: rootfs.img size:6,442,450,944/6G (offset:0/0B) imgsize:1,136,914,432 (1,110,268K)
done.
```
Where `/dev/sdb` is your SD Card device. The process may take a while, be patient (it's not stuck), once it's done, remove the SD card, plug into the pico and follow [this](#how-to-access-pico-via-usb-cable).

# What is RNDIS ?
This is what enables the connection to the pico via USB cable:
> Remote Network Driver Interface Specification (RNDIS) is a Microsoft proprietary protocol used primarily on top of USB to provide a virtual Ethernet link between a host computer and a remote device

# How to boot from the Flash vs SD Card ?
If there is no SD card inserted, it will boot from the external SPI Flash chip, otherwise will boot from the SD card.

# Pico USB modes
Pico can be in two USB modes:
* Device/Peripheral: Work as a RNDIS network interface to the host computer
* Host: Acts as a USB host, allowing to connect other peripherals and devices to it
> [!TIP]
> If connecting things to pico USB port changes nothing on `dmesg` nor `lsusb`, that means it's in device mode

# How to switch USB modes ?
There are two ways: **SDK** and **config tool** (already inside the OS images).

### SDK
From the SDK root folder edit `sysdrv/source/kernel/arch/arm/boot/dts/rv1103g-luckfox-pico-mini.dts` and change `dr_mode` to `host`:
```bash
/**********USB**********/
&usbdrd_dwc3 {
        status = "okay";
        dr_mode = "host";
};
```
After that, all images built will have the chosen mode by default.

### Config tool
Run `sudo luckfox-config` inside the OS:  
<img width="351" height="249" alt="image" src="https://github.com/user-attachments/assets/b886a545-9c29-44e1-bac3-04a9c8de8a29" />  

Note that it will only take effect after a reboot (and persist too).

# How to access Pico via USB cable
Connect pico to computer via USB cable, after a while a new RNDIS network interface should be detected:
```bash
$ ifconfig 
enxae935ce313b2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::6f2d:eea0:cff2:7aa6  prefixlen 64  scopeid 0x20<link>
        ether ae:93:5c:e3:aa:b2  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 13  bytes 2518 (2.5 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
> [!TIP]
> Run `watch ifconfig` and wait until the new interface show up

Set the new interface ip to **172.32.0.100/16** (same subnet as the pico, in the Ubuntu OS is `172.32.0.70`, but sometimes it's final `.93`, make sure to know based on your OS) and enable **internet sharing** if you want access to internet from the pico OS. On Lubuntu, the options are located here:  

<img width="569" height="545" alt="image" src="https://github.com/user-attachments/assets/52d58af2-b89f-4b4c-a920-e6c78e5009af" />  

After applying the new setting, check `ifconfig` for the ip `172.32.0.100` assigned to the interface:
```bash
enxae935ce313b2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.31.0.100  netmask 255.255.0.0  broadcast 172.31.255.255
```
Now try to ping pico:
```bash
$ ping 172.32.0.70
PING 172.32.0.70 (172.32.0.70) 56(84) bytes of data.
64 bytes from 172.32.0.70: icmp_seq=1 ttl=64 time=0.433 ms
64 bytes from 172.32.0.70: icmp_seq=2 ttl=64 time=0.377 ms
64 bytes from 172.32.0.70: icmp_seq=3 ttl=64 time=0.493 ms
```
And scan pico open ports:  
```bash
$ nmap 172.32.0.70
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-09-20 00:21 -03
Nmap scan report for 172.32.0.70
Host is up (0.0027s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp   open  ssh
5555/tcp open  freeciv
```
In this case SSH and ADB are available.

# How to connect via SSH
First make sure the OS have an SSH server running and that you know its credentials, for example with the Ubuntu OS image, user `pico`:
```
$ ssh pico@172.32.0.70
```
<img width="509" height="566" alt="image" src="https://github.com/user-attachments/assets/9dd0d830-4715-4a09-ba08-29721a95007b" />

# How to transfer files to/from pico
There are many ways, here are some handy ones.

## Using network
First make sure to have an SSH server installed, on the Ubuntu images it's already by default, on Buildroot select `openssh` and related tools server in the menu. SSH enables SFTP too, so you can use Filezilla or any other client to connect to pico (port 22) or for a command line only solution with `scp <source> <destination>`:  
* Copy local `file.txt` to pico as **root** user, to `/root` folder: `scp file.txt root@172.32.0.70:`
* Copy local `file.txt` to pico as **pico** user, to `/home/pico/luckfox` folder: `scp file.txt pico@172.32.0.70:luckfox`

## Using external USB flash disk
Put pico in USB host mode then connect a USB flash disk and mount, ex: `sudo mount /dev/sdb1 /mnt/mydrive`

## Using custom overlay
Use a custom folder that will end up inside pico images, follow [this](#custom-overlay).

# How to connect via ADB
Using the USB cable and in device mode, setup the RNDIS interface with `172.32.0.100`, and: 
```bash
$ adb connect 172.32.0.93
connected to 172.32.0.93:5555

$ adb devices
List of devices attached
2be53eb6debe9106        no permissions (missing udev rules? user is in the plugdev group); see [http://developer.android.com/tools/device.html]
172.32.0.93:5555        device

$ adb -s 172.32.0.93:5555 shell
```
And that is it, you are inside pico:
```bash
# ls
media          linuxrc        usr            opt            dev
lib64          root           var            oem            bin
lib32          sbin           sys            mnt
rockchip_test  proc           tmp            lib
userdata       data           run            etc
```

# Getting internet inside pico
Using the USB cable and in device mode:
1. Setup the RNDIS interface with `172.32.0.100` ip
2. Connect to pico via SSH or ADB
3. From inside the pico run `route add default gw 172.32.0.100`
4. Ping something like `ping www.google.com` to confirm it's working

If you are having DNS issues, add `nameserver 8.8.8.8` to `/etc/resolv.conf` (Google DNS). To persist the changes: 
```bash
$ sudo bash -c 'echo "route add default gw 172.32.0.100" >> /etc/rc.local'
$ sudo chmod +x /etc/rc.local
```

# What OS can be used ?
These are some I could find, the key is to look for OS that can run on rv1103 / rv1106:

| OS               | Resource Usage       | Use Case                           | Development Flexibility | Pre-configured Tools        | 
|------------------|----------------------|------------------------------------|-------------------------|-----------------------------|
| Buildroot        | Low                  | Embedded minimal systems           | High (customizable)      | Basic Linux utilities       | 
| Ubuntu 22.04     | Moderate to High     | Full-featured development          | High                     | Extensive packages          | 
| Foxbuntu         | Moderate             | Low-power, networking apps         | Medium                   | Meshtastic, LoRa tools      | 
| Alpine Linux     | Very Low             | Security-focused minimal systems   | High (package-based)     | apk package manager         | 

## Foxbuntu
Foxbuntu is optimized for specific networking applications. I haven't tried, but you can find more info and OS images here:  
https://github.com/femtofox/femtofox  
https://github.com/femtofox/femtofox/wiki/Getting-Started

## Alpine
Alpine is a community-supported option known for its exceptional small footprint and security focus. I haven't tried, but you can find more info and OS images here:  
https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-Alpine-Linux-1/#introduction-why-adapt-to-alpine-linux
https://drive.google.com/file/d/1ZS6SdgfCzaJRSzucv6WKHHRT24mmi9sV/view

## Ubuntu
Ubuntu provides the most desktop-like development experience. Unfortunately it's no longer supported by Luckfox as it once was:  
https://github.com/LuckfoxTECH/luckfox-pico/issues/273#issuecomment-2870461201  
https://github.com/LuckfoxTECH/luckfox-pico/issues/288#issuecomment-2933309966  

I am using the latest SDK version from master branch as of now, which is this:
```bash
commit 994243753789e1b40ef91122e8b3688aae8f01b8 (HEAD -> main, origin/main, origin/HEAD)
Date:   Thu Aug 14 14:38:50 2025 +0800
```
The only OS option available is `buildroot` with `Linux kernel 5.10.160`, but you may try to go back to an older SDK version/commit and see if the `ubuntu` option still there. Otherwise stick with pre-existing images:  
https://drive.google.com/drive/folders/14kFWY93MZ4Zga4ke2PVQgUs1y9xcMG0S

## Buildroot
Buildroot remains as the only official supported OS from Luckfox via their SDK:  
https://github.com/LuckfoxTECH/luckfox-pico

It comes with busybox and you'll noticed how some things will be more limited due to its purpose and nature. Buildroot idea is that it contains almost nothing, and you add as you go/need, that way you keep track and control over what is being part of the OS and its final size as well.

### What is Busybox ?
> BusyBox is a single executable that provides a comprehensive suite of simplified Unix tools packaged into one compact binary, designed specifically for embedded systems and recovery environments with limited resources. It combines stripped-down versions of common command-line utilities like ls, cp, grep, and shell functionality into a multi-call binary that creates the illusion of a full-featured system while dramatically reducing storage space and memory footprint. Often called "The Swiss Army Knife of Embedded Linux," BusyBox achieves this efficiency through code sharing between utilities and is commonly used in initramfs images, IoT devices, and as the core userland environment in minimalist Linux distributions, providing essential system administration capabilities where a full GNU toolchain would be impractical.

# SDK
The SDK is where everything is done from scratch, giving us full autonomy. The SDK allows the building of the firmware, OS images, add/remove features to the system as well as compile the Linux kernel. Start by following the instructions here:  
https://github.com/LuckfoxTECH/luckfox-pico

Once you ran the build script successfully the images will be ready at `output/image`:
```bash
$ cd output/image
$ ls -lh
-rw-r--r-- 1 root root 3,4M Sep 19 17:46 boot.img
-rw-r--r-- 1 root root 263K Sep 19 17:44 download.bin
-rw-r--r-- 1 root root  32K Sep 19 17:48 env.img
-rw-r--r-- 1 root root 184K Sep 19 17:44 idblock.img
-rw-r--r-- 1 root root  43M Sep 19 17:48 oem.img
-rw-r--r-- 1 root root 195M Sep 19 17:48 rootfs.img
-rw-r--r-- 1 root root 1,3K Sep 19 17:48 sd_update.txt
-rw-r--r-- 1 root root 1,3K Sep 19 17:48 tftp_update.txt
-rw-r--r-- 1 root root 256K Sep 19 17:44 uboot.img
-rw-r--r-- 1 root root 251M Sep 19 17:48 update.img
-rw-r--r-- 1 root root 9,6M Sep 19 17:48 userdata.img
```
From there you just need to copy them to the SD card with the [`blkenvflash`](#blkenvflashpy-tool) tool.

> [!IMPORTANT]
> You'll need to run this process every time you make changes within the SDK files. The first build is slow because it compiles everything from scratch. After that, builds are faster as they only compile the parts you've changed.

# Firmware files
There is a bunch of `.img` files when building with the SDK or downloading images from somewhere, here is their meaning (the size is just for example purposes):

| File | Size | Description | Contents / Examples | Boot Order |
|------|------|-------------|---------------------|------------|
| **idblock.img** | 184KB | Rockchip bootloader identification and verification block | Boot signature, chip initialization parameters, security data | 1st |
| **download.bin** | 263KB | Rockchip proprietary low-level bootloader component | DDR memory controller setup, early hardware initialization | 2nd |
| **uboot.img** | 256KB | Main U-Boot bootloader - initializes hardware and loads kernel | Das U-Boot, Rockchip modifications, boot menu, environment access | 3rd |
| **env.img** | 32KB | U-Boot environment storage with boot parameters and partition config | `bootargs`, `bootcmd`, `baudrate`, partition layout, environment variables | 4th |
| **boot.img** | 3.4MB | Linux kernel with embedded device tree - core operating system | zImage, FIT image, device tree blobs, kernel modules, initramfs | 5th |
| **rootfs.img** | 195MB | Root filesystem containing operating system libraries and utilities | BusyBox, system libraries, configuration files, core utilities, /bin, /etc, /lib | 6th |
| **oem.img** | 43MB | OEM partition for vendor-specific data and applications | Pre-installed apps, proprietary libraries, camera calibration data, AI models | 7th |
| **userdata.img** | 9.6MB | User data partition for application storage and persistent data | Application data, user configurations, logs, writable user space | 8th |
| **update.img** | 251MB | Complete firmware package for easy single-file flashing | Combined image containing all partitions for end-user distribution | N/A |
| **sd_update.txt** | 1.3KB | SD card flash configuration script | Partition layout, flash instructions, update parameters for SD programming | N/A |
| **tftp_update.txt** | 1.3KB | TFTP network flash configuration script | Network boot parameters, TFTP server settings, remote update instructions | N/A |

> [!IMPORTANT]
> Notice how the `update.img` file size is the same as the sum of all the rest

## Boot Process Summary
1. **Hardware Init**: `idblock.img` → `download.bin` (Rockchip proprietary)
2. **Bootloader**: `uboot.img` loads `env.img` for configuration
3. **Kernel**: `boot.img` (Linux kernel + device tree)
4. **System**: `rootfs.img` (root filesystem)
5. **Applications**: `oem.img` + `userdata.img` (vendor and user data)

## Key Notes
- **Rockchip-specific**: `idblock.img`, `download.bin` are proprietary formats
- **Essential files**: Minimum required for boot: `idblock.img`, `uboot.img`, `boot.img`, `rootfs.img`
- **Flash tools**: Use `sd_update.txt` or `tftp_update.txt` with `rkflash.sh` scripting
- **User data**: `userdata.img` persists across firmware updates

# blkenvflash.py tool
This is a third party tool that allows to copy all the `.img` files to the SD card on Linux environment, replacing the need to use the Rockchip tools which are often buggy, confusing and sometimes in Chinese and/or only works on Windows.  
> [!TIP]
> Since this tool will be used very often, I recommend you to keep it ready in your environment path (like `/usr/bin`)

You must run the tool from the folder where all the `.img` files are, with `sudo` and `python3`, also make sure to know where is your SD card entry, in this example `/dev/sdb` (don't use partitions like `sdb1`):  
```bash
$ sudo python3 blkenvflash.py /dev/sdb
== blkenvflash.py 0.0.1 ==
writing to /dev/sdb
   mmcblk1: env.img size:32,768/32K (offset:0/0B) imgsize:32,768 (32K)
   mmcblk1: idblock.img size:524,288/512K (offset:32,768/32K) imgsize:188,416 (184K)
   mmcblk1: uboot.img size:262,144/256K (offset:0/0B) imgsize:262,144 (256K)
   mmcblk1: boot.img size:33,554,432/32M (offset:0/0B) imgsize:3,150,336 (3,150,336B)
   mmcblk1: oem.img size:536,870,912/512M (offset:0/0B) imgsize:113,909,760 (111,240K)
   mmcblk1: userdata.img size:268,435,456/256M (offset:0/0B) imgsize:9,999,360 (9,765K)
   mmcblk1: rootfs.img size:6,442,450,944/6G (offset:0/0B) imgsize:1,136,914,432 (1,110,268K)
done.
```
Larger files will take more time, be patient (it's not stuck), once it's done remove the SD card and plug into the pico.

> [!WARNING]
> To work with the SPI Flash memory, Rockchip proprietary tools still required

# Customizing Buildroot
From the SDK root folder run `sudo ./build.sh buildrootconfig`, once you are done run `sudo ./build.sh` that will udpate all the images in the output folder, then just copy to SD card with the `blkenvflash.py` tool:  

<img width="895" height="440" alt="image" src="https://github.com/user-attachments/assets/27eb8b2b-026b-48c1-8ab0-6e0e138fb955" />

> [!TIP]
> You can search for things by typing `/`, also to use backspace you have to hold `ctrl`

> [!TIP]
> To check if a new tool was added look at `output/target/usr/bin`, that is where buildroot will put them, and instead of building a whole new image just to check the new added binary/ies, alternatively just copy from that folder into the running pico using scp, ftp or any other method you may have

# Customizing Kernel
From the SDK root folder `sudo ./build.sh kernelconfig`, once you are done run `sudo ./build.sh` that will udpate all the images in the output folder, then just copy to SD card with the `blkenvflash.py` tool:  

<img width="886" height="448" alt="image" src="https://github.com/user-attachments/assets/cbcd47d4-7fdc-4055-994b-690fcdafc1c9" />

> [!TIP]
> You can search for things by typing `/`

# Why there isn't 64MB RAM available ?
The SDK generate images allocating 24MB of RAM to the CMA, you can claim it back by setting to 1MB as per Luckfox recommendation, but first check your OS RAM situation:  

CMA using 24MB of RAM, only 34MB RAM left:
```bash
$ cat /proc/meminfo 
MemTotal:          34316 kB
CmaTotal:          24576 kB
```

Full RAM available:
```bash
$ cat /proc/meminfo 
MemTotal:          57372 kB
CmaTotal:           1024 kB
```
You can make a persistent change but that needs to compile and generate new images with the SDK, or change the kernel boot param `rk_dma_heap_cma=1M` to quickly test it. To use the SDK, from its root folder, edit `RK_BOOTARGS_CMA_SIZE="1M"` here:
```bash
$ nano project/cfg/BoardConfig_IPC/BoardConfig-SD_CARD-Buildroot-RV1103_Luckfox_Pico_Mini-IPC.mk
```

# How can I see the kernel boot args being used in my OS ?
Note the boot args are being passed by the U-Boot bootloader, but Linux keeps a copy here:
```bash
$ cat /proc/cmdline 
user_debug=31 storagemedia=sd androidboot.storagemedia=sd androidboot.mode=normal  rootwait earlycon=uart8250,mmio32,0xff4c0000 console=ttyFIQ0 root=/dev/mmcblk1p7 snd_soc_core.prealloc_buffer_size_kbytes=16 coherent_pool=0 blkdevparts=mmcblk1:32K(env),512K@32K(idblock),256K(uboot),32M(boot),512M(oem),256M(userdata),6G(rootfs) rootfstype=ext4 rk_dma_heap_cma=1M androidboot.fwver=uboot-03/13/2025
```
# CPU benchmark
I will be using 2 tools and 3 devices:  

Tools  
* Sysbench: https://github.com/akopytov/sysbench
* Single line dd: `dd if=/dev/zero bs=1MB count=1024 | sha512sum` (https://bash-prompt.net/guides/bash-simple-bash-benchmark)

Devices  
* Pico @ 1.2Ghz / Arm v7 single-core 32 bit / Ubuntu 22.04 / Kernel 5.10
* Raspberry Pi 1 model B 512MB @ 1GHz (Arm v6 single-core 32 bit) / Raspbian 10 / Kernel 5.10
* Laptop i5 3210M @ 2.5Ghz (x86 quad-core 64 bit) / Lubuntu 24.04 / Kernel 6.2

### Sysbench
Pico:  
<img width="468" height="451" alt="image" src="https://github.com/user-attachments/assets/075a00db-e201-41fe-b683-9b75d4ebbbdb" />

Raspberry pi:  
<img width="402" height="461" alt="image" src="https://github.com/user-attachments/assets/537729e7-75e0-4f84-9d53-9dcf683eb1f7" />

Laptop:  
<img width="457" height="422" alt="image" src="https://github.com/user-attachments/assets/9bf9db3f-3d0f-4e93-921e-f6b37b4545c0" />

| Device | Speed (events/sec) |
| :--- | :--- |
| Pico | 48.56 |
| Raspberry Pi | 30.22 |
| Laptop | 980.17 |

### DD
* Pico: `1024000000 bytes (1.0 GB, 977 MiB) copied, 88.8576 s, 11.5 MB/s`
* Raspberry Pi: `1024000000 bytes (1.0 GB, 977 MiB) copied, 548.533 s, 1.9 MB/s`
* Laptop: `1024000000 bytes (1,0 GB, 977 MiB) copied, 2,89258 s, 354 MB/s`

| Device | Time | Speed |
| :--- | :--- | :--- |
| Pico | 88.8576 s | 11.5 MB/s |
| Raspberry Pi | 548.533 s | 1.9 MB/s |
| Laptop | 2.89258 s | 354 MB/s |

### Framebuffer
Using [this tool](https://github.com/themrleon/fbmark?tab=readme-ov-file#tests). Benchmarking from an SSH connection Vs using a x11vnc session:

Rectangle:
| x11vnc | SSH |
|------------|---------------|
| 19.82 MPixels/s | 41.58 MPixels/s |

Sierpinski:
| Iterations | x11vnc | SSH |
|------------|-|---------------|
| 1024 iterations | 238.74 Frames/s | 953.31 Frames/s |
| 2048 iterations | 216.80 Frames/s | 748.70 Frames/s |
| 4096 iterations | 169.30 Frames/s | 524.43 Frames/s |
| 8192 iterations | 122.61 Frames/s | 328.75 Frames/s |
| 16384 iterations | 78.19 Frames/s | 188.11 Frames/s |
| 32768 iterations | 42.96 Frames/s | 101.90 Frames/s |
| 65536 iterations | 23.83 Frames/s | 53.14 Frames/s |
| 131072 iterations | 12.46 Frames/s | 27.18 Frames/s |
| 262144 iterations | 6.60 Frames/s | 13.69 Frames/s |

Notice that since running `x11vnc` is a heavy task (x11vnc eats lots of CPU), that degrades the performance in half! (To compare with other devices use the SSH results since that is the one where the CPU is fully avaiable to the test)

# Flash vs SD Card vs RAM benchmark
But at least the onboard 128MB Flash chip is fast, right?! Get the `hdparm` tool from buildroot menu and:
```
$ cat /proc/partitions 
major minor  #blocks  name
   1        0       4096 ram0
   1        1       4096 ram1
   1        2       4096 ram2
   1        3       4096 ram3
   1        4       4096 ram4
   1        5       4096 ram5
   1        6       4096 ram6
   1        7       4096 ram7
   1        8       4096 ram8
   1        9       4096 ram9
   1       10       4096 ram10
   1       11       4096 ram11
   1       12       4096 ram12
   1       13       4096 ram13
   1       14       4096 ram14
   1       15       4096 ram15
  31        0     131072 mtdblock0
 179        0   61069312 mmcblk1
 179        1         32 mmcblk1p1
 179        2        512 mmcblk1p2
 179        3        256 mmcblk1p3
 179        4      32768 mmcblk1p4
 179        5     524288 mmcblk1p5
 179        6     262144 mmcblk1p6
 179        7    8388608 mmcblk1p7
```

Onboard 128MB SPI Flash
```bash
$ hdparm -t /dev/mtdblock0
/dev/mtdblock0:
 Timing buffered disk reads:  14 MB in  3.18 seconds =   4.40 MB/sec
```

64GB Generic SD Card
```bash
$ hdparm -t /dev/mmcblk1p7
/dev/mmcblk1p7:
 Timing buffered disk reads:  66 MB in  3.02 seconds =  21.87 MB/sec
```

DDR2 RAM:
```bash
$ hdparm -t /dev/ram15
/dev/ram15:
 Timing buffered disk reads:   4 MB in  0.02 seconds = 180.71 MB/sec
```
| Device | Path | Type | Speed (MB/sec) |
| :--- | :--- | :--- | :--- |
| **DDR2 RAM** | `/dev/ram15` | RAM Disk | **180.71**  |
| **SD Card** | `/dev/mmcblk1p7` | microSD Card | **21.87** |
| **SPI Flash** | `/dev/mtdblock0` | SPI NAND Flash | **4.40**  |

- **DDR2 RAM is fastest**: As expected, reading from a RAM disk is significantly faster than from flash storage. **180.71 MB/s** is consistent with the capabilities of DDR2 memory used in these boards.
- **SD Card vs. SPI Flash**: The SD card is about **5 times faster** than the onboard SPI NAND Flash, this is typical, as SD cards often have a faster interface (SDIO) compared to SPI.

> [!IMPORTANT]
> This was all tested running OS from SD Card, running from Flash, it gets even slower ~3.68 MB/sec, so stick with the SD card and if you need fast access use one of the RAM banks

# UART connection
To avoid the annoying process of connecting pico as an USB device / RNDIS interface every time, and also to free the USB port, you can just keep a serial/UART (`ttyFIQ0`) connection all the time instead, this is a more raw/low level debugger connection, from where you will be able to see everything pico is doing, also will be the only way to access the bootloader. Any USB/serial converter should work, as long as it works in **3.3v and NOT 5v**, otherwise you will damage the SoC:
<img width="960" height="680" alt="image" src="https://github.com/user-attachments/assets/af13c196-2472-4bfb-81f9-8cd056a55e56" />
<img width="1130" height="810" alt="image" src="https://github.com/user-attachments/assets/d02343b3-38e3-4e39-941b-9a0693e4acd0" />

I am using a ch341 based chip, created at `ttyUSB0`:
```bash
[ 8832.198782] usb 2-1: new full-speed USB device number 7 using xhci_hcd
[ 8832.323090] usb 2-1: New USB device found, idVendor=1a86, idProduct=7523, bcdDevice= 2.64
[ 8832.323108] usb 2-1: New USB device strings: Mfr=0, Product=2, SerialNumber=0
[ 8832.323114] usb 2-1: Product: USB Serial
[ 8832.325225] ch341 2-1:1.0: ch341-uart converter detected
[ 8832.325783] usb 2-1: ch341-uart converter now attached to ttyUSB0
```
And connect using minicom `minicom -D /dev/ttyUSB0` (Keep all default settings, 115200 8N1).

# But can it run DOOM ?
Just because it hasn't video, sound and input, that doesn't mean we cannot run DOOM! here is a test running `fbDOOM` with a virtual framebuffer (`/dev/fb0`) accessed remotely with `x11vnc` via USB RNDIS interface cable:  
[![Watch the video](https://img.youtube.com/vi/6dsxjtB3URw/0.jpg)](https://www.youtube.com/watch?v=6dsxjtB3URw)

CPU usage varies between 65-70%:  
<img width="894" height="193" alt="image" src="https://github.com/user-attachments/assets/47bc2800-27e1-494e-a9b5-f4298fb37930" />  

Power consumption while running on pico:  
<img width="585" height="326" alt="image" src="https://github.com/user-attachments/assets/38fd4dc3-c188-4e80-a9b0-23cbb35f4d1e" />  

For reference here is the power consumption while running in the Raspberry Pi 1 model B 512MB without anything connected to it (overclocked @ 1 Ghz, CPU usage is around 93%):  
<img width="585" height="326" alt="image" src="https://github.com/user-attachments/assets/62626079-12b1-4d9d-8266-68c74cb14973" />  

> [!NOTE]
> You can check the full DOOM on Raspberry Pi test [here](https://github.com/themrleon/rpi-experiments?tab=readme-ov-file#vnc)

## What are the steps to run DOOM ?
A couple things are needed:
1. A framebuffer (`/dev/fb0`) to draw things in there. Follow [this](#getting-a-framebuffer).
2. A DOOM version that can target the framebuffer as video output. Get the binary from [here](https://github.com/themrleon/fbDOOM/releases/tag/1.0).
3. Copy `fbdoom` and `doom1.wad` to the OS image, you can use a [custom overlay](#custom-overlay) for that.
4. A way to see what is being shown in the framebuffer from outside the pico. Select `x11vnc` from the [buildroot menu](#customizing-buildroot).
5. [Build](#sdk-1) all images again
6. Boot the new system and set the framebuffer with `fbset -g 320 200 320 200 16`
7. Run fbdoom in the background `fbdoom -iwad doom1.wad &`
8. Run vnc server: `x11vnc -rawfb console -auth /dev/null -noxdamage -forever -shared  -repeat -defer 0 -wait 0  -noxinerama -nowf  -nowcr -speeds modem -tightfilexfer`
9. Now from another device use a vnc client to access the vnc server using pico's ip, ex on Lubuntu: `vncviewer -SecurityTypes None <pico ip>:0 -CompressLevel 0 -QualityLevel 0 -FullColor 0 -PreferredEncoding raw -AutoSelect=0`

# Custom overlay
In order to customize the root file system (`/`), we can use an overlay, that way it's possible to persist (and overwrite) the rootfs partition image. Go to **[Buildroot menu](#customizing-buildroot) -> System Configuration -> Root filesystem overlay directories** and add an absolute path to your own custom overlay folder:  

<img width="1329" height="660" alt="image" src="https://github.com/user-attachments/assets/284b7b85-4448-4c66-8d88-485d79e336f9" />

In this example the `custom-overlay` folder is in the SDK root path, now to add a file that will end up in the OS/rootfs image `/usr/bin` folder, create that same path in the overlay and copy some binary there:
```bash
$ cd custom-overlay
$ mkdir -p usr/bin
$ cp <binary from somewhere> usr/bin
```
> [!IMPORTANT]
> This will be very useful to overwrite system files and add pre-baked data like network credentials, users, passwords, custom binaries and drivers

# Getting a framebuffer
Check [this](https://github.com/themrleon/rpi-experiments?tab=readme-ov-file#what-is-framebuffer) if you are unfamiliar with the Linux framebuffer and what it can do. On pico I tried all the framebuffer options I could find on the kernel configuration, including device tree changes and kernel boot args, but nothing worked, except this one:

<img width="1133" height="572" alt="image" src="https://github.com/user-attachments/assets/d277cecf-e7a2-442b-8037-fcce1bafac67" />

That is not a 'regular' framebuffer in the sense that everything including the console output is being drawn there too, but rather a **virtual framebuffer**, so it's empty, and forever will be, unless we draw something there on purpose.  

It can be added to the kernel either as built-in or external module. To use as a module:
```bash
$ cd /oem/usr/ko
$ insmod vfb.ko vfb_enable=1
$ lsmod
Module                  Size  Used by    Tainted: G  
vfb                     2753  0 

$ ls /dev/fb0 
/dev/fb0
```
Now set a new size and color:
```bash
$ fbset -g 320 200 320 200 16
$ fbset -i
mode "320x200-367"
    # D: 50.000 MHz, H: 97.656 kHz, V: 367.129 Hz
    geometry 320 200 320 200 16
    timings 20000 64 64 32 32 64 2
    rgba 5/0,6/5,5/11,0/0
endmode

Frame buffer device information:
    Name        : Virtual FB
    Address     : 0xb4a04000
    Size        : 1048576
    Type        : PACKED PIXELS
    Visual      : TRUECOLOR
    XPanStep    : 1
    YPanStep    : 1
    YWrapStep   : 1
    LineLength  : 640
    Accelerator : No
```
You can see these steps in the DOOM demo [video](#but-can-it-run-doom-). To use as a built-in module, check the example [here](#u-boot-and-kernel-parameters).

# U-Boot and kernel boot args
The U-boot bootloader is the one passing the boot arguments to the Linux kernel, they can be changed at runtime or compile-time. At runtime is easier/quicker to test things, but they won't persist after generating new images. To enter the bootloader hold `ctrl + c` and power up pico **only after** until it enters the command line, make sure to be using [UART connection](#uart-connection). Let's do an example adding `video=vfb` to the kernel args:
```bash
=> printenv 
...
sys_bootargs= root=/dev/mmcblk1p7 rootfstype=ext4 rk_dma_heap_cma=1M
...
=> setenv sys_bootargs ${sys_bootargs} video=vfb
=> boot
```

> [!TIP]
> To persist run `saveenv` after `setenv`

In the OS check if `video=vfb` was passed:
```bash
$ cat /proc/cmdline 
...
1:32K(env),512K@32K(idblock),256K(uboot),32M(boot),512M(oem),256M(userdata),6G(rootfs) video=vfb rootfstype=ext4 rk_dma_h
...
```

To persist at compile-time, so that new images will have the args, from the SDK root folder:
1. Edit `build.sh`
2. Change `SYS_BOOTARGS="sys_bootargs="` to `SYS_BOOTARGS="sys_bootargs= video=vfb"`
3. Run `sudo ./build.sh`

Check with `cat output/image/.env.txt`:
```bash
...
sys_bootargs= video=vfb root=/dev/mmcblk1p7 rootfstype=ext4 rk_dma_heap_cma=1M
```

> [!WARNING]
> Editing `.env.txt` directly to add kernel args doesn't work

# Wifi, Bluetooth and Audio
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/92b338e0-7988-4fd6-bf4d-5ef862e4b559" />

You can have all that and much more using USB devices, however it all comes down to driver support, you'll have to find the right driver for your device and OS. Below are examples of how I got audio, camera and wifi working.
> [!IMPORTANT]
> Make sure to use a powered USB hub

## USB sound card
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/1707d395-797f-4906-82de-453fff97c4ba" />

> ALSA (Advanced Linux Sound Architecture) serves as the fundamental audio framework in Linux, providing the essential kernel drivers, libraries, and utilities that enable communication between software applications and sound hardware. It manages the low-level interaction with audio devices, allowing for playback, recording, and volume control directly at the driver level. While modern desktop environments typically use higher-level sound servers like PulseAudio on top of ALSA to handle advanced features such as audio mixing from multiple applications and network streaming, ALSA itself remains the core layer that directly interfaces with the physical sound cards, forming the indispensable foundation of the entire Linux audio stack.

First connect it to a laptop and check `dmesg` for any clue of the driver:
```bash
[ 1413.174330] usb 1-1: New USB device found, idVendor=0d8c, idProduct=000e, bcdDevice= 1.00
[ 1413.174348] usb 1-1: New USB device strings: Mfr=0, Product=1, SerialNumber=0
[ 1413.174353] usb 1-1: Product: Generic USB Audio Device   
[ 1413.204572] cm109: Keymap for Komunikate KIP1000 phone loaded
[ 1413.204712] input: CM109 USB driver as /devices/pci0000:00/0000:00:14.0/usb1/1-1/1-1:1.3/input/input12
[ 1413.204933] usbcore: registered new interface driver cm109
[ 1413.204937] cm109: CM109 phone driver: 20080805 (C) Alfred E. Heggestad
[ 1413.214964] hid: raw HID events driver (C) Jiri Kosina
[ 1413.220331] usbcore: registered new interface driver usbhid
[ 1413.220339] usbhid: USB HID core driver
[ 1413.239408] usbcore: registered new interface driver snd-usb-audio
```
From there I learned it uses the `CM109` driver, then go to pico kernel menu config and search for it:  

<img width="1335" height="657" alt="image" src="https://github.com/user-attachments/assets/a66af298-c343-4555-a968-e58a3ae4d9a8" />

Include as built-in driver, go to buildroot menu and include the ALSA tools, rebuild all images and boot pico, once inside, plug the USB dongle and check `lsusb`, `dmesg` and/or `aplay -l` for any sign of life from it: 
```bash
$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: rvacodec [rv-acodec], device 0: ffae0000.i2s-rv1106-hifi ff480000.acodec-0 [ffae0000.i2s-rv1106-hifi ff480000.acodec-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: Device [Generic USB Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
In this case it was detected as `Generic USB Audio Device` (`card 1`), keeping that in mind, go to `alsamixer`, hit F6 and select it from the list, then increase the volume all way up before testing:  

<img width="1322" height="658" alt="image" src="https://github.com/user-attachments/assets/baf7d326-cc53-4299-9506-37f03097f49f" />

Close `alsamixer` and test with some MP3 file using `mpg123`, ex: `mpg123 -a hw:1,0 sample.mp3` (where 1 is due to `card1`). And here is the result:  
[![Watch the video](https://img.youtube.com/vi/3sC8ylrmZFI/0.jpg)](https://www.youtube.com/watch?v=3sC8ylrmZFI)

## USB camera
<img width="541" height="487" alt="image" src="https://github.com/user-attachments/assets/b517a95c-6ac7-41dd-b496-a8f61a9e4d21" />

>The Video4Linux2 (V4L2) subsystem in Linux provides a unified framework for handling video capture devices, with UVC (USB Video Class) being a critical specification that ensures interoperability for USB cameras. When a UVC-compliant USB webcam is connected, the Linux kernel loads the `uvcvideo` driver, which automatically detects the device and exposes it as a V4L2-compatible interface (typically `/dev/video0`). This abstraction allows applications to interact with the camera through standard V4L2 system calls (ioctls) to query capabilities, negotiate video formats (like MJPEG, YUYV, or H.264), set resolution and frame rate, and manage data streaming via memory-mapped or user-pointer buffers. The UVC driver handles all protocol-specific communication with the camera, while V4L2 provides a consistent API for applications—from simple command-line tools like `fswebcam` to complex GUI software like `guvcview`—enabling seamless video capture, streaming, and control (e.g., adjusting brightness or focus) without requiring device-specific code.

Star by following [this](https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-RV1103/Luckfox-Pico-Plus-Mini/Luckfox-Pico-pinout/Luckfox-Pico-USB#usb-camera). Identify the camera with `v4l2-ctl --list-devices`, and look for which video number was assigned after the `UVC Camera` part:
```bash
[   23.512224] rkcif_tools_id1: update sensor info failed -19
UVC Camera (046d:0821) (usb-xhci-hcd.0.auto-1.1):
[   23.512296] rkcif-mipi-lvds: rkcif_update_sensor_info: stream[2] get remote terminal sensor failed!
        /dev/video0
[   23.512318] rkcif_tools_id2: update sensor info failed -19
        /dev/video1
        /dev/media0
```
In this case the camera is `/dev/video0`, use that for the tools:

* Supported camera formats and resolutions: `v4l2-ctl --device=/dev/video0 --list-formats-ext`  
* Supported camera controls: `v4l2-ctl --device=/dev/video0 --list-ctrls`  
* Set camera controls: `v4l2-ctl --device=/dev/video0 --set-ctrl=<name>=<value>`  
* Take pictures: `fswebcam -d /dev/video0 -r 320x240 image.jpg`  
* Record video: `ffmpeg -f v4l2 -video_size 320x240 -framerate 30 -i /dev/video0 video.mp4`  
* Stream video: `ffmpeg -f v4l2 -video_size 320x240 -framerate 30 -i /dev/video0 -f mpegts "udp://<VLC client ip>:5000"`  

> [!WARNING]
> Unfortunately due to the low amount of RAM in pico, higher resolutions will crash the process  
> Reducing FPS won't help since that seems to affect only CPU usage  
> Higher resolutions work with pictures, but they also crash after a certain point  
> In my tests maximum video before crash was 480x320 and for picture 1600x1200  

Here is the difference in RAM usage for:  
320x240 video:  
<img width="1337" height="180" alt="image" src="https://github.com/user-attachments/assets/a9161c84-abcb-4d58-b1a7-5a3d9fda7780" />

480x320 video:  
<img width="1337" height="212" alt="image" src="https://github.com/user-attachments/assets/d846dced-cd92-4077-88d3-74fae41552a2" />

And at 640x480 it already crashes:
```bash
[  310.102798] oom-kill:constraint=CONSTRAINT_NONE,nodemask=(null),task=ffmpeg,pid=760,uid=0
[  310.102864] Out of memory: Killed process 760 (ffmpeg) total-vm:39616kB, anon-rss:1244kB, file-rss:0kB, shmem-rss:0kB,
```
> [!IMPORTANT]
> There is this [ffmpeg](https://github.com/nyanmisaka/ffmpeg-rockchip) version that seems to support Rockchip hardware video encoding/decoding, but it may be tricky to compile

Here is a test streaming at 320x240 over wifi to a client using VLC, controlling camera zoom and brightness:  
[![Watch the video](https://img.youtube.com/vi/RVOrBzaeajE/0.jpg)](https://www.youtube.com/watch?v=RVOrBzaeajE)

## USB wifi
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/88d6fc2c-9abd-444b-836e-5a7a9f73521d" />

Start by checking if the kernel already has your device drivers, use the **product id** that you get from `lsusb`, in my case `Bus 002 Device 011: ID 0bda:8176 Realtek Semiconductor Corp. RTL8188CUS 802.11n WLAN Adapter`, where `8176` is the product id. From the SDK root folder do a dumb search for that id: `grep -r -s "0x8176"`, the results are:
```bash
sysdrv/source/kernel/drivers/net/wireless/realtek/rtl8xxxu/rtl8xxxu_core.c:             case 0x8176:
sysdrv/source/kernel/drivers/net/wireless/realtek/rtl8xxxu/rtl8xxxu_core.c:{USB_DEVICE_AND_INTERFACE_INFO(USB_VENDOR_ID_REALTEK, 0x8176, 0xff, 0xff, 0xff),
sysdrv/source/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192de/led.c:              if ((rtlpriv->efuse.eeprom_did == 0x8176) ||
sysdrv/source/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192cu/hw.c:                       if (rtlefuse->eeprom_did == 0x8176) {
sysdrv/source/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192cu/sw.c:       {RTL_USB_DEVICE(USB_VENDOR_ID_REALTEK, 0x8176, rtl92cu_hal_cfg)},
sysdrv/source/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8723be/hw.c:                       if (rtlefuse->eeprom_did == 0x8176) {
sysdrv/source/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8723ae/hw.c:               case 0x8176:
sysdrv/source/kernel/drivers/net/wireless/realtek/rtlwifi/pci.h:#define RTL_PCI_8188CE_DID      0x8176  /*8192ce */
sysdrv/source/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192ce/hw.c:                       if (rtlefuse->eeprom_did == 0x8176) {
sysdrv/source/kernel/drivers/net/wireless/realtek/rtlwifi/rtl8192ce/sw.c:       {RTL_PCI_DEVICE(PCI_VENDOR_ID_REALTEK, 0x8176, rtl92ce_hal_cfg)},
```
Although `lsusb` says mine is a `RTL8188CUS`, and after trying a couple of them, I found that `rtl8192cu` was the right one, so keep in mind as this may be tricky. To try a driver, just find it in the kernel menu config and enable, I am keeping as built-in since I will be using often:  

<img width="1341" height="287" alt="image" src="https://github.com/user-attachments/assets/483f4847-2004-44c8-ad0c-2e816a53433b" />

Then rebuild all and test. In this case I was still getting errors about missing bin files:
```bash
[    1.205932] rtl8192cu: Board Type 1
[    1.206089] rtl_usb: rx_max_size 15360, rx_urb_num 8, in_ep 1
[    1.206204] rtl8192cu: Loading firmware rtlwifi/rtl8192cufw_TMSC.bin
[    1.206272] ieee80211 phy0: Selected rate control algorithm 'rtl_rc'
[    1.207903] usb 1-1.1: Direct firmware load for rtlwifi/rtl8192cufw_TMSC.bin failed with error -2
[    1.207969] usb 1-1.1: Direct firmware load for rtlwifi/rtl8192cufw.bin failed with error -2
[    1.207981] rtlwifi: Loading alternative firmware rtlwifi/rtl8192cufw.bin
[    1.207988] rtlwifi: Selected firmware is not available
```
After some search on internet I found this:  
https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/rtlwifi

Which contains those Realtek .bin files, then I downloaded both `rtl8192cufw_TMSC.bin` and `rtl8192cufw.bin` and put in my custom overlay folder like so:
```bash
── lib
│   ├── firmware
│   │   └── rtlwifi
│   │       ├── rtl8192cufw.bin
│   │       └── rtl8192cufw_TMSC.bin
```

And that solved the driver problem, but there still [one thing left](#setup-wifi-connection). Here is a test running DOOM over the wifi connection with pico completely isolated using a powerbank (laggy due to the poor 2.4Ghz connection):  
[![Watch the video](https://img.youtube.com/vi/luljqjPSWxw/0.jpg)](https://www.youtube.com/watch?v=luljqjPSWxw)

# Setup wifi connection
>`ifconfig` configures network interfaces and IP addresses. `iw` manages the wireless link, handling scanning and connection to networks. `wpa_supplicant` is the background service that performs the secure authentication (WPA/WPA2) to encrypted Wi-Fi networks using a password. Together, they enable a Linux system to connect to Wi-Fi: `iw` sets up the link, `wpa_supplicant` handles security, and `ifconfig` assigns the IP address for full network access.

First make sure you you got the proper drivers for your network device, then:
1. Install `ifconfig`, `wpa_supplicant` and `iw`, using Buildroot menu
2. Rebuild all images, copy to SD card and boot pico
3. Find your interface name with `ifconfig -a` (in this example `wlan0`)
4. Run `ifconfig wlan0 up`
5. Create `/etc/wpa_supplicant.conf` with:
```bash
network={
 ssid="your network name"
 psk="password"
}
```
6. Run `wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf` 
7. Run `udhcpc -i wlan0` to get an ip
8. Test, ex: `ping www.google.com`

To make persistent changes, add to `/etc/network/interfaces` this:
```bash
auto wlan0
iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant.conf
```

> [!TIP]
> To scan nearby networks use `iw wlan0 scan` (where `wlan0` is your interface name)  
> To test network speed use `iperf3 -s` on a server (in the same network) and `iperf3 -c <server ip>`

# Cross-compilation
To cross-compile stuff to pico let's use `fbDOOM` as an example. If you installed the SDK at some point you did this:
```
$ cd {SDK_PATH}/tools/linux/toolchain/arm-rockchip830-linux-uclibcgnueabihf/
$ source env_install_toolchain.sh
```
Which installed the toolchain in your system so that your environment always have the `arm-rockchip830-linux-uclibcgnueabihf-` toolchain in the path, like the C compiler `arm-rockchip830-linux-uclibcgnueabihf-gcc`. If not make sure to follow the official SDK Github instructions.

On the host machine/x86, where you installed the SDK, get fbDOOM sources:
```
$ git clone https://github.com/maximevince/fbDOOM.git
$ cd fbDOOM/fbdoom
```
Cross-compile statically linked, so that it becomes a full standalone binary (no external dependencies):
```
$ make CROSS_COMPILE=arm-rockchip830-linux-uclibcgnueabihf- LDFLAGS="-s -static" NOSDL=1
$ ls -lh fbdoom
-rwxrwxr-x 1 note note 666K Sep 24 15:39 fbdoom
$ file fbdoom
fbdoom: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, BuildID[sha1]=df3e06c85e09e42e47937815fa04090df95157f9, for GNU/Linux 3.2.0, stripped
```
> [!WARNING]
> DON'T use `arm-linux-gnueabihf-` to compile things! it may compile and run, but I faced situations where it behaved wrong, make sure to always use `arm-rockchip830-linux-uclibcgnueabihf-` instead!

# Compilation inside pico
Sometimes is just tricky or hard to cross-compile complex things, in thoses cases, you can use the pre-made Ubuntu image which already contains the toolchain and compile natively directly from the pico, will be slow but sometimes it's a sacrifice needed.  

# Hardware interfacing
When connecting anything to pico, refer to the pinout board image, and keep an eye on the pin number (on the edge in blue) since that is what the code uses, also keep an eye on the voltage of each pin, some pins support 3.3v while others only 1.8v, anything above their range **will permanent damage or even kill the SoC**. Also keep in mind the board expose 3 voltages: 5v (from USB host cable), 3.3v (voltage regulator using the USB 5v) and 1.8v, use them when needed.  

<img width="756" height="245" alt="image" src="https://github.com/user-attachments/assets/c32a421e-1b82-4c05-91d3-ece4a1c38d6a" />

For example pin 54 supports 3.3v and can be PWM, UART or GPIO, but you must keep only one active at a time! use the `luckfox-config` tool to enable/disable what will be available for the pin.

## GPIO
> For the full thing follow the official guide: https://wiki.luckfox.com/Luckfox-Pico-Plus-Mini/GPIO

The idea with GPIO is that you first export the pin you want to use, then configure it, then use, and once you are done, unexport to free the pin.

* Setting pin 54 state  
```
Pin 54 ───▒▒▒▒▒▒▒▒(1kΩ)───|>|─── GND
           Resistor       LED
```
```bash
echo 54 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio54/direction
echo 1 > /sys/class/gpio/gpio54/value
echo 0 > /sys/class/gpio/gpio54/value
echo 54 > /sys/class/gpio/unexport
```

* Reading pin 55 state
```
Pin 55 ─────────────────── 1V8(OUT)
```
```bash
echo 55 > /sys/class/gpio/export         
echo in > /sys/class/gpio/gpio55/direction 
cat /sys/class/gpio/gpio55/value
echo 55 > /sys/class/gpio/unexport
```

## PWM
> For the full thing follow the official guide: https://wiki.luckfox.com/Luckfox-Pico-Plus-Mini/PWM

The same idea from GPIO here, export the pin, configure it, use and unexport. Here we can use pin 54 (pwm10_m1), enable it in the `luckfox-config` tool:  

<img width="341" height="177" alt="image" src="https://github.com/user-attachments/assets/863a5ad5-1f81-4f2c-96b6-93ddc8802d30" />  

Here is an example on how to control a servo motor, in short they use a 20ms period whereas within that period a pulse between 1ms-2ms control the arm position, 1ms = 0 degrees and 2ms = 90 degrees (for 90 degree servos, some are 180 or even 360), being 1.5ms the center:  
```
Pin 54 ─── PWM Signal ───┐
                         │
VBUS ───── 5V ───────────│─── Servo Motor
                         │
GND ────── GND ──────────┘
```
```bash
$ echo 0 > /sys/class/pwm/pwmchip10/export
$ echo 1 > /sys/class/pwm/pwmchip10/pwm0/enable
$ echo "normal" > /sys/class/pwm/pwmchip10/pwm0/polarity 
$ echo 20000000 > /sys/class/pwm/pwmchip10/pwm0/period
$ echo 1000000 > /sys/class/pwm/pwmchip10/pwm0/duty_cycle
$ echo 2000000 > /sys/class/pwm/pwmchip10/pwm0/duty_cycle
$ echo 0 > /sys/class/pwm/pwmchip10/unexport
```
> [!IMPORTANT]
> If you can't find any `pwm` entry in `/sys/class` make sure it's enabled in the kernel (in my case with Buildroot it wasn't, the Ubuntu image has it enabled already)
> <img width="1060" height="552" alt="image" src="https://github.com/user-attachments/assets/c784a4c9-c8d2-4b35-8518-6da400dbb6f7" />

## ADC
> For the full thing follow the official guide: https://wiki.luckfox.com/Luckfox-Pico-Plus-Mini/ADC

For this example let's do this:
```
1V8(OUT) ─── LDR ────┐
                     │
                  Pin 145 ───▒▒▒▒▒▒▒▒(1kΩ)─── GND
                     │
                  Analog Input
```
* Creates a voltage divider circuit
* Pin 145 reads analog voltage that varies with light intensity
* Voltage at Pin 145 = 1V8 * (1kΩ / (1kΩ + LDR_resistance))
* Bright light = low LDR resistance = higher voltage
* Dark = high LDR resistance = lower voltage
  
Read pin 145 (ADC channel 1) value with:
```bash
cat /sys/bus/iio/devices/iio\:device0/in_voltage1_raw
```

Here is a video demonstrating PWM (with led and servo on pin 54), GPIO (input pin 55 and output pin 54) and ADC (with an LDR / light sensor on pin 145):  

[![Watch the video](https://img.youtube.com/vi/4hKQG2g6W3k/0.jpg)](https://www.youtube.com/watch?v=4hKQG2g6W3k)

## UART
> For the full thing follow the official guide: https://wiki.luckfox.com/Luckfox-Pico-Plus-Mini/UART/

Pico mini b has 3 UARTs: UART2 which is used for debugging purposes and access the bootloader, so only UART3 and UART4 are available, both should work fine with minicom, ex: `minicom -D /dev/ttyS3`, just make sure to enable them with the `luckfox-config` tool.

# Using the NAND Flash
> For the full thing follow the official guide: https://wiki.luckfox.com/Luckfox-Pico-Plus-Mini/Flash-image#5-image-flashing-linux-environment

The tool needed is available in 3 different sources: at the official guide there is a direct link, in the SDK tools and [this](https://github.com/rockchip-linux/rkdeveloptool) open-source version, pick one, power up pico while holding its **boot** button, and check if is detected as this:
```bash
$ lsusb 
Bus 002 Device 006: ID 2207:110c Fuzhou Rockchip Electronics Company 
```
Then just proceed with the `update.img` running as admin:
```bash
$ sudo ./upgrade_tool uf update.img 
Using /home/note/luckfox/upgrade_tool_v2.17_for_linux/config.ini
Loading firmware...
Support Type:1106       FW Ver:0.0.00   FW Time:2023-10-28 15:25:33
Loader ver:1.01 Loader Time:2023-10-28 15:21:04
Start to upgrade firmware...
Download Boot Start
Download Boot Success
Wait For Maskrom Start
Wait For Maskrom Success
Test Device Start
Test Device Success
Check Chip Start
Check Chip Success
Get FlashInfo Start
Get FlashInfo Success
Prepare IDB Start
Prepare IDB Success
Download IDB Start
Download IDB Success
Download Firmware Start
Download Image... (100%)
Download Firmware Success
Upgrade firmware ok.
```
