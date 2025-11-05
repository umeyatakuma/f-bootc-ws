Memo - booted with Fedora's netinst image, and used the following ks.cfg. Connectd a physical ethernet to my laptop for the install. Formattd USB and put ks.cfg at its root directory. 

$ cat ks.cfg 
# Run following on 10.0.0.100 at the directory where ks.cfg is present: $ python -m http.server
# Specify the following as an additional parameter: inst.ks=http://10.0.0.100/ks.cfg or inst.ks=hd:sda:/ks.cfg
# Make sure to replace PASSPHRASE in the following lines to match your choice of decrypt password. 
text

network --bootproto=dhcp 


# Disk Partitioning for old system 
#clearpart --all --initlabel
#part biosboot --size=1 --fstype=biosboot  # Create a 1MiB biosboot partition
#part /boot/efi --size=200 --fstype=efi     # Create EFI System Partition
#part /boot --size=512 --fstype=xfs          # Create a separate /boot partition
#part pv.1 --size=15000 --grow              # Allocate the remaining space to the physical volume
#volgroup fedora pv.1
#logvol --name=root --vgname=fedora --size=15000 --fstype=xfs --encrypt --passphrase=PASSPHRASE /

# Disk Partitioning for new ones 
clearpart --all --initlabel --drives=nvme0n1
part /boot/efi --size=200 --fstype=efi --ondisk=nvme0n1
part /boot --size=512 --fstype=xfs --ondisk=nvme0n1
part pv.01 --size=1 --grow --fstype=xfs --ondisk=nvme0n1
volgroup fedora pv.01
logvol --size=1 --grow --name=root --vgname=fedora --fstype=xfs --encrypt --passphrase=PASSPHRASE /

ostreecontainer --url quay.io/umeyatakuma/f-bootc-ws:latest

# Password generated with: $ openssl passwd -6 <password> 
rootpw --iscrypted ENCRYPTEDPASSWORD

# User addition (use encrypted password) Remove --gid and --uid if that's not necessary. 
user --name=tumeya --iscrypted --password=ENCRYPTEDPASSWORD --groups=wheel --gid=YOURGID --uid=YOURUID
