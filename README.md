factorio-serverlist
===================

Usage
-----

* Set the environment variable HOME to your user directory if it isn't already set.
* Create a Factorio dedicated server in a directory named `factorio` in your user directory
* Add your website username and password in data/server-settings.json
* Start the dedicated server: `bin/x64/factorio --server-settings data/server-settings.json --start-server randomgamesave.zip`
* Stop it again
* Run app.py and navigate to <ip>:24527, or add app to WSGI container
