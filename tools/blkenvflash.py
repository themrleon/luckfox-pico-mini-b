#!/usr/bin/python3

# == BLKENVFLASH == written by Rene K. Mueller <spiritdude@gmail.com>
#
# Description:
#    Writes an image (.img) or to the SD card direct from existing .env.txt for LuckFox Pico Pro/Max
#
#       % ./blkenvflash disk.img
#       -- inquery with `lsblk` which device is your SD card resides --
#       % sudo dd if=disk.img of=/dev/sdX bs=1M; sync
#
#       -- or do in one step -- 
#       % sudo ./blkenflash /dev/sdX
#
# License: MIT
#
# History:
# 2024/06/18: after the hint by A. Schuetz https://github.com/LuckfoxTECH/luckfox-pico/issues/129 was able to make script functional
# 2024/06/10: start

import os, sys, re, subprocess, shutil
import atexit

VERSION = '0.0.1'

me = sys.argv.pop(0)
path = os.path.dirname(me)
me = os.path.basename(me)

step = 'sdcard'            # -- hard-codec to do one sdcard writing

if len(sys.argv) != 1:
   print(f'''USAGE {me} <file or device>
   examples:
      % ./{me} disk.img
      % lsblk     -- and check output on which /dev/sdX your SD card resides --
      % sudo dd if=disk.img of=/dev/sdX bs=1M; sync
      
      -- or in one step --
      % sudo ./{me} /dev/sdX
''')
   sys.exit(-1)
   
dev = sys.argv.pop(0)

print(f"== {me} {VERSION} ==")
print(f"writing to {dev}")
   

# -- a few helpers to en/decode nice numbers
def true_size(s):
   u = { 'B': 1, 'K': 1024, 'M': 1024*1024, 'G': 1024*1024*1024 }
   if m := re.search(r'(\d+)([BKMG])',s):
      return int(m.group(1)) * u[m.group(2)]
   return 0

def nice_size(n):
   u = { 'B': 1, 'K': 1024, 'M': 1024*1024, 'G': 1024*1024*1024 }
   for k,v in reversed(u.items()): 
      if n >= v and n % v == 0:
         return f"{n//v:,}{k}"
   return f"{n:,}B"

def cleanup():
   if os.path.exists(".env.txt.orig"):
      os.rename(".env.txt.orig",".env.txt")
   print("done.")

atexit.register(cleanup)
   
with open(".env.txt") as fh:
   env2 = [ ]
   for l in fh.readlines():
      if m := re.search(r'(blkdevparts|sd_parts)=(\w+)',l):
         _type = m.group(1)
         _dev = m.group(2)
         l = re.sub(r'blkdevparts=\w+:','',l)
         p = l.split(',')
         c_off = 0
         if step=='sdcard' and _dev == 'mmcblk1': 
            for e in p:
               #print(e)
               if (m := re.search(r'(\d+[KMG])@(\d+[KMG])\((\w+)\)',e)) or (m := re.search(r'(\d+[KMG])\((\w+)\)',e)):
                  if len(m.groups())==3:
                     size = true_size(m.group(1))
                     off = true_size(m.group(2))
                     name = m.group(3)
                  else:
                     size = true_size(m.group(1))
                     name = m.group(2)
                     off = 0
                  print(f"   {_dev}: {name}.img size:{size:,}/{nice_size(size)} (offset:{off:,}/{nice_size(off)})",end='')
                  if os.path.exists(f"{name}.img"):
                     size_ = os.path.getsize(f"{name}.img")           # -- actual size
                     print(f" imgsize:{size_:,} ({nice_size(size_)})")
                     if step=='sdcard':
                        # -- it seems the explicit `off` seems not taking effect?
                        cmd = ['dd',f"if={name}.img",f"of={dev}","bs=1k",f"seek={c_off//1024}"]
                        try:
                           res = subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
                        except subprocess.CalledProcessError as e:
                           print(f"ERROR: {e}",e.stderr)
                           sys.exit(-1)
                     c_off += size
                  else:
                     print()
                     print(f"ERROR: '{name}.img' not found")
                     sys.exit(-1)
                     
         if _dev == 'mmcblk0':
            env2.append(l)

if step=='emmc':           # -- untested, not needed as 'upgrade_tool' does this already 
   shutil.copy(".env.txt",".env.txt.orig")
   with open(".env.txt","w") as fh:
      fh.write("\n".join(env2))

   # -- prepare upgrade_tool call to write to eMMC
   print(f"{path}/upgrade_tool")
   subprocess.run([f'{path}/upgrade_tool','uf','update.img'])   
               
