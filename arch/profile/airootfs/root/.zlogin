# fix for screen readers
if grep -Fqa 'accessibility=' /proc/cmdline &> /dev/null; then
    setopt SINGLE_LINE_ZLE
fi

~/.automated_script.sh

# Grim OS welcome, only on the first console
if [[ $(tty) == /dev/tty1 ]]; then
    clear
    grim-banner "live medium"
    print -P "   Type %B%F{white}griminstall%f%b to install Grim OS."
    print -P "   %Bgrimhelp%b for help   ·   %Bgrimfetch%b for system info"
    print -P "   Wi-Fi: %Biwctl%b   ·   wired networks connect automatically."
    print
fi
