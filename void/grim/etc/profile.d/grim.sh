# Grim Void: banner, low-RAM hint and desktop autostart on console logins
case $- in *i*) ;; *) return 0 ;; esac
if [ -z "$GRIM_LOGIN_DONE" ]; then
    export GRIM_LOGIN_DONE=1
    grim-login
fi
