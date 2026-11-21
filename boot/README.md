# Grim Boot

A GRUB-based ISO launcher, like Ventoy. Put ISO files on a USB stick and boot it. GRUB opens the ISO files itself, works out what kind of ISO each one is, and boots it the right way. Nothing gets unpacked onto the stick.

```
grim-boot                     every USB stick: ✓/✗ Grim Boot, and the ISO files on it
grim-boot install /dev/sdX    put Grim Boot on a stick (ERASES it)
grim-boot add FILE.iso        copy an ISO onto the Grim Boot stick (into /isos)
grim-boot remove NAME         delete an ISO from it
grim-boot update              refresh the boot menu and artwork, keeping the ISOs
grim-boot image FILE [SIZE]   a Grim Boot disk image instead of a stick (for VMs)
```

To install it as a command: `ln -s "$PWD/grim-boot" ~/.local/bin/grim-boot`

## The stick

| Partition | Filesystem | What's on it |
|---|---|---|
| 1 `GRIMBOOT` | exFAT, all but 128 MiB | your ISO files (top level, `/isos`, or `/isos/<folder>`) |
| 2 `GRIMBOOTEFI` | FAT32, 128 MiB, active | GRUB for 64-bit UEFI, 32-bit UEFI and BIOS, the menu, the artwork |

The disk uses an MBR partition table, so it boots on both BIOS and UEFI PCs. Windows, macOS and Linux can all copy ISOs onto the exFAT partition; you don't need the `grim-boot` command for that.

## What boots (tested in QEMU, Grim Boot 1.0.0)

| ISO | How Grim Boot boots it | UEFI | BIOS |
|---|---|---|---|
| Grim Void 1.2.2, Void Linux | dracut `iso-scan/filename=` | ✓ | ✓ |
| Grim OS 1.1.5, Arch Linux | the ISO's own `loopback.cfg` (`img_dev` + `img_loop`) | ✓ | ✓ |
| Ubuntu and family | casper `iso-scan/filename=` | untested | untested |
| Debian live, Kali, MX | live-boot `findiso=` | untested | untested |
| Fedora live | dracut `iso-scan/filename=` | untested | untested |
| FreeBSD 15.1 | `kfreebsd` + the whole ISO as a memory disk | ✗ | ✓ |
| OpenBSD 8.0 (`cdXX.iso`) | `kopenbsd` on `bsd.rd` | ✗ | ✓ |
| NetBSD 11.1 | ✗ GRUB's `knetbsd` hangs with NetBSD 9+ amd64 kernels | ✗ | ✗ |
| Windows installers | not yet | ✗ | ✗ |

GRUB's BSD loaders only work from BIOS. Under UEFI, Grim Boot says this in the menu instead of letting the PC reset. To boot BSDs on a UEFI PC, Grim Boot would need what Ventoy has: an EFI driver that shows the ISO file to the firmware as a virtual CD. That's the next step for BSD support.

## Testing

```
sudo vm/make-test-image.sh     # vm/grimboot-test.img with the Grim ISOs and test-isos/*.iso on it
vm/run.sh uefi                 # or: vm/run.sh bios
```

`vm/qmp.py vm/qmp.sock shot FILE | keys down ret | type TEXT | quit` drives the VM. To refresh the menu on the test image without root: `mcopy -o -i vm/grimboot-test.img@@OFFSET grub/grub.cfg ::/boot/grub/grub.cfg`, where OFFSET is the start of partition 2 in bytes (`sfdisk -d`).
