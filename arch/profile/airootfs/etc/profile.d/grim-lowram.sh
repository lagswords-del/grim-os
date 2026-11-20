# Grim OS: a reminder at login when the system runs in low-RAM mode
if [ -t 1 ] && [ -z "$GRIM_LOWRAM_SHOWN" ] && systemctl is-active -q grim-lowram.target 2>/dev/null; then
    export GRIM_LOWRAM_SHOWN=1
    printf '\n  \033[1;97mLow-RAM mode\033[0m \033[90m— no desktop, no network, nothing in the background.\033[0m\n'
    printf '  \033[31mgrimmode net\033[0m      turn on the network (Wi-Fi: nmtui)\n'
    printf '  \033[31mgrimmode desktop\033[0m  start everything (the login screen and the desktop)\n'
    printf '  \033[31mgrimmode\033[0m          show RAM use and what is running\n\n'
fi
