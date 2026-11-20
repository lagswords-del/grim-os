#!/usr/bin/env bash
# Boots Grim OS in a QEMU window (UEFI).  ./run-vm.sh        boot the ISO
#                                         ./run-vm.sh disk   boot the installed disk
cd "$(dirname "$(readlink -f "$0")")"
iso=$(ls -t out/grimos-*.iso | head -1)
# ISO boots get fresh firmware settings so a boot entry left by an earlier install can't win
cp /usr/share/edk2/x64/OVMF_VARS.4m.fd vm/vars-iso.fd
vars=vm/vars-iso.fd; boot=(-cdrom "$iso" -boot order=d)
[[ ${1:-} == disk ]] && { vars=vm/vars.fd; boot=(-boot order=c); }
exec qemu-system-x86_64 -name "Grim OS" -enable-kvm -cpu host -smp 4 -m 4096 \
  -machine q35 \
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/edk2/x64/OVMF_CODE.4m.fd \
  -drive if=pflash,format=raw,file=$vars \
  -drive file=vm/disk.qcow2,if=virtio,format=qcow2 \
  "${boot[@]}" \
  -nic user,model=virtio-net-pci \
  -device virtio-vga -display gtk,zoom-to-fit=on -monitor none \
  -qmp unix:vm/qmp.sock,server,nowait
