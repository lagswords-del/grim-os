# Grim Void live USB: start the installer on tty1, once per boot
case $- in *i*) ;; *) return 0 ;; esac
if [ "$(tty)" = /dev/tty1 ] && [ ! -e /tmp/.grim-install-started ] && [ "$(basename "$(readlink -f /etc/runit/runsvdir/current)")" != lowram ]; then
    touch /tmp/.grim-install-started
    grim-install
fi
