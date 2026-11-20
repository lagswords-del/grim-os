#!/usr/bin/env bash
# Boots Grim Void in a QEMU window (UEFI).  ./run-vm.sh        boot the ISO
#                                           ./run-vm.sh disk   boot the installed disk
cd "$(dirname "$(readlink -f "$0")")"
iso=$(ls -t out/grim-void-*.iso | head -1)
vars=vm/vars-iso.fd; boot=(-drive file="$iso",media=cdrom,if=none,id=cd -device ide-cd,drive=cd,bootindex=0)
[[ ${1:-} == disk ]] && { vars=vm/vars.fd; boot=(); }
exec qemu-system-x86_64 -name "Grim Void" -enable-kvm -cpu host -smp 4 -m 6144 -machine q35 \
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/edk2/x64/OVMF_CODE.4m.fd \
  -drive if=pflash,format=raw,file=$vars \
  -drive file=vm/disk.qcow2,if=virtio,format=qcow2 \
  "${boot[@]}" \
  -nic user,model=virtio-net-pci \
  -device virtio-vga -device qemu-xhci -device usb-tablet -display gtk,zoom-to-fit=on -monitor none \
  -qmp unix:vm/qmp.sock,server,nowait
