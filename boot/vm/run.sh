#!/usr/bin/env bash
# Boot the Grim Boot test image in QEMU as a USB stick.   ./run.sh [uefi|bios] [IMAGE]
cd "$(dirname "$(readlink -f "$0")")"
mode=${1:-uefi} img=${2:-grimboot-test.img}
fw=()
if [[ $mode == uefi ]]; then
    [[ -f vars.fd ]] || cp /usr/share/edk2/x64/OVMF_VARS.4m.fd vars.fd
    fw=(-drive if=pflash,format=raw,readonly=on,file=/usr/share/edk2/x64/OVMF_CODE.4m.fd -drive if=pflash,format=raw,file=vars.fd)
fi
exec qemu-system-x86_64 -name "Grim Boot ($mode)" -enable-kvm -cpu host -smp 4 -m 6144 -machine q35 "${fw[@]}" \
  -device qemu-xhci -drive file="$img",format=raw,if=none,id=stick,snapshot=on -device usb-storage,drive=stick,bootindex=0 \
  -device usb-tablet -nic user,model=virtio-net-pci -device virtio-vga -display gtk,zoom-to-fit=on -monitor none \
  -qmp unix:qmp.sock,server,nowait
