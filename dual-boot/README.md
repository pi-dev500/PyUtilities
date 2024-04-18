# A simple script allowing to reboot to windows
 - This simple script, based on efibootmgr use, allows to do the same thing as a GRUB could do: It reboots the machine from linux to the first Windows EFI found by efigrubmgr.
 - To use it, you just have to put it (bootwindows.py) in **/usr/bin** and add the desktop entry (microsoft.windows.desktop) in a xdg desktop dir (most commonly /usr/share/applications)
 - After the app starts, it just ask for your admin password and reboot to windows boot manager within seconds.
 - The only problem is the fact that it forces the reboot, without giving the time to the apps to quit safely.
