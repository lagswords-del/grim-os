# Grim Void: banner, low-RAM hint and desktop autostart on console logins
if status is-login; and status is-interactive; and not set -q GRIM_LOGIN_DONE
    set -gx GRIM_LOGIN_DONE 1
    grim-login
end
