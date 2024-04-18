#!/usr/bin/python
import sys
import os
import subprocess
win_boot=subprocess.check_output(["bash","-c","efibootmgr | grep 'Windows Boot Manager'"]).decode().split(' ')[0].replace("Boot","").replace("*","")
print(win_boot)
if os.system("pkexec efibootmgr --bootnext "+win_boot) != 0:
	quit(0)
os.system("reboot")
