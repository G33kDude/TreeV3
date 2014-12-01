TreeV3
======

A web interface for turning on/off Christmas trees using the [Dexter Industries dSwitch](http://www.dexterindustries.com/site/?product=dswitch-lego-mindstorms-nxt) with [ev3dev](http://www.ev3dev.org/)

Tree button modified from Free Design File's [Christmas tree flat vector icons](http://freedesignfile.com/125016-christmas-tree-flat-vector-icons/) under the CC Attribution 3.0 license.

---

Installing TreeV3
-----------------

First off, you have to set up ev3dev as per their [Getting Started with ev3dev](http://www.ev3dev.org/docs/getting-started/) guide.

---

After ev3dev is set up, you have to install nginx and php:

```
sudo apt-get install nginx
```

On ev3dev, you'll run across an error while installing nginx, because IPv6 is disabled in ev3dev. You'll have to open up `/etc/nginx/sites-available/default` and remove or comment out the line that looks like this:

```
listen [::]:80 default
```

Once that's removed, re-run apt-get to finish installing nginx.

```
sudo apt-get install nginx
```

After nginx has finished installing, ensure that it is running correctly by navigating to your/ev3dev's IP address in a web browser. You should see the [default nginx web page](http://i.imgur.com/ekpVUg1.png). If you do not see the webpage, run

```
sudo service nginx start
```

and try again.

---

Now that you've confirmed nginx is working, it's time to install php.

```
sudo apt-get install php5-fpm
```

This should run without any errors.

---

Once they're installed, you need to configure them. Ensure that `/etc/php5/fpm/php.ini` has the following option set:

```
cgi.fix_pathinfo=0
```

> "If this number is kept as 1, the php interpreter will do its best to process the file that is as near to the requested file as possible. This is a possible security risk. If this number is set to 0, conversely, the interpreter will only process the exact file path—a much safer alternative."

---

Then, ensure that `/etc/php5/fpm/pool.d/www.conf` has the following option set:

```
listen = /var/run/php5-fpm.sock
```

This makes sure nginx will call php successfully, and through the best possible method.

---

Open up the `treev3` file found in the root of this repository, and make sure `root /home/pi/TreeV3/www;` is pointing at the `www` folder in this repo.

For example, if your username was `user` and you had cloned to the folder `desktop`, you'd want to set it to `root /home/user/desktop/TreeV3/www;`

---

Now that php is set up, we'll need to set up nginx to call it. First you'll want to move the file `treev3` into `/etc/nginx/sites-available`. Then, navigate to `etc/nginx/sites-enabled` and remove the symlink to `default`, and add your own symlink to the `treev3` file.

```
sudo mv treev3 /etc/nginx/sites-available/
cd /etc/nginx/sites-enabled/
sudo rm default
sudo ln -s /etc/nginx/sites-available/treev3
```

---

Finally, restart nginx and php to let all the changes take effect.

```
sudo service nginx restart
sudo service php5-fpm restart
```

Congratulations, everything should be installed now!

---

Using TreeV3
------------

Before using TreeV3, ensure your dSwitch is connected to port A on the EV3. After you are sure it is connected, you'll need to put port A into `rcx-led` mode by running:

```
sudo echo rcx-led > /sys/bus/legoev3/devices/outA/mode
```

This will have to be done every time you restart your EV3.

---

Once port A is set to rcx-led mode, navigate to your EV3's IP address in a web browser. TreeV3 should be ready for use now!

TreeV3 API
----------

To write your own interface for TreeV3, simply send a `GET` or `POST` request to your EV3's IP adress, with the parameters "on" or "off" set. For example, `http://ipa.ddr.ess/?on` and `http://ipa.ddr.ess/?off`