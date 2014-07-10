#RPi Remote

**RPi Remote** busca tomar el control de la Raspberry Pi de forma remota, sin importortar el dispositivo, esto gracias a la interfaz Web en la que se enfoca el proyecto. Con esto es tan facil como acceder a la direccion IP del RPi desde cualquier navegador Web y tener el control del mismo, ver informacion importante del sistema como **RAM** en uso y libre, % **CPU**, Discos y almacenamiento, **temperatura**, entre otros, ademas el acceso a las carpetas publicas o que se quieran compartir, asi como el poder compartir la musica que se tenga almacenada en un dispositivo externo.

##Acerca del proyecto
RPi Remote esta completamente escrito en el lenguaje de programacion **Python**, (A exepcion del modulo visual HTML, JS, CSS. Ver [Twitter Bootstrap](http://getbootstrap.com)). Se decide el uso de Python por su sencillez y su capacidad de llamar a funciones de mas bajo niver (informacion del sistema, PIPEs, etc.).

El proyecto hace uso de diversas librerias de Python que se deben tener pre-instaladas.

##Requerimientos 
RPi Remote esta diseñado para Raspberry Pi, su compativilidad con otros sitemas Unix (Linux, GNU, Darwin [OSX]) es parcial, y su compatividad con Microsoft Windows es casi nula.

###Se debe tener pre-instalado
Las siguientes librerias se deben tener pre-instaldas en el sistemas, la instalacion de estas es facil mediante el siguiente comando

``` 
# Raspbian && Debian-like
$ sudo apt-get install python-pip

$ sudo pip install <libreria>
```

* **Flask**: Flask es un micro framework web, con el se hace el core principal de la aplicacion pues el el encargado de procesar las peticiones HTTP. [Ver Flask](http://flask.pocoo.org)

```
$ sudo pip install Flask
```



* **Requests**: Requests permite hacer peticiones HTTP de forma facil, esta es usada por ```cron.py``` para consultar la direccion IP externa y notificar si existe un cambio.

```
$ sudo pip install requests
```

