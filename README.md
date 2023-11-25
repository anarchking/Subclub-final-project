# SubClub Web Application

<a name="readme-top"></a>

<br />

  <h3 align="center">Final Project</h3>

  <p align="center">
    This is Stephen Littman's CS50 Final Project.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

#### Video Demo:  [![SubClub walk thru video][YouTube.com]][YouTube-url]


[![Index page Screen Shot][product-screenshot]](https://youtu.be/I2C0B-_EbtU)



The Goal in mind for this project is to build a server to help SubClub to:
* Live a great story and share it with others.
* Boost awareness of our threatened Water Ecosystems.
* Help restore their beauty.
* Keep the waterways safe for all life, while having a good time.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- BUILT WITH -->
### Built With

These are the frameworks,libraries and softwares used to bring this project to life.


* [![Flask][Flask.com]][Flask-url]
* [![Jinja][Jinja.com]][Jinja-url]
* [![SQLite][SQLite.com]][SQLite-url]
* [![HTML][HTML.com]][HTML-url]
* [![CSS][CSS.com]][CSS-url]
* [![Javascript][Javascript.com]][Javascript-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]
* [![Nginx][Nginx.com]][Nginx-url]
* [![Gunicorn][Gunicorn.com]][Gunicorn-url]
* [![Scratch][Scratch.com]][Scratch-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
To get server up and running follow this steps.


* Start by Updating local package index on Server
  ```sh
  sudo apt-get update
  ```
* Next Upgrade software on Server
  ```sh
  sudo apt-get upgrade
  ```
* Next Add a user to Server "NOT a good idea to run on root"
  ```sh
  sudo adduser "New user name"
  ```
* Give user a password and confirm it
* Give user sudo privileges
  ```sh
  usermod -aG sudo "New user name"
  ```
* Navigate to ssh config file
  ```sh
  vim /etc/ssh/sshd_config
  ```
* Remove "#" to uncomment this line in config file to allow user to ssh into server.
  ```sh
  From "#PasswordAuthentication" to PasswordAuthentication
  ```
* Restart with changes
  ```sh
  systemctl restart sshd
  ```
* Set up python virtual enviroment
  ```sh
  python3 -m venv ~/env/server
  ```
* Activate python virtual enviroment
  ```sh
  source ~/env/server/bin/activate
  ```
* Follow all steps in <a href="#prerequisites">Prerequisites</a>
* Navigate to your webapps folder
* Make a wsgi "Web Server Gateway Interface" file
  ```sh
  vim wsgi.py
  ```
* Add this to wsgi.py
  ```sh

  from app import app

  if __name__ == "__main__":
      app.run()
  ```
* Make sure gunicorn is running
  ```sh
  gunicorn --bind 0.0.0.0:5000 wsgi:app
  ```
* Check ip:port number to make sure it come up
* Deactivate Virtual Enviroment
  ```sh
  deactivate
  ```
* Create a file to start app enviroment on boot
  ```sh
  sudo vim /etc/systemd/system/server.service
  ```
* In server.service file type the following below then save
  ```sh
  [Unit]
  Description=Gunicorn instance to serve Subclub Flask app
  After=network.target

  [Service]
  User="username"
  Group=www-data
  WorkingDirectory=/home/"username"/server
  Environment="PATH=/home/'username'/env/server/bin"
  ExecStart=/home/'username'/env/server/bin/gunicorn --workers 3 --bind unix:app.sock -m
  007 wsgi:app

  [Install]
  WantedBy=multi-user.target
  ```
* Reload daemons
  ```sh
  sudo systemctl daemon-reload
  ```
* Start the daemon
  ```sh
  sudo systemctl start server
  ```
* Finally enable the daemon
  ```sh
  sudo systemctl enable server
  ```
* Check status to make sure its up and running
  ```sh
  sudo systemctl status server
  ```
* Make sure it says active and running

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ALL DEPENDENCIES -->
### Dependencies

This is a list of Dependencies needed to run the Server.

* Flask
  ```sh
  pip install flask
  ```
* Flask Session
  ```sh
  pip install flask_session
  ```
* Gunicorn
  ```sh
  pip install gunicorn
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

First navigate to url of Web App. Next, browse your heart out.
If you would like to join in the discussions (Forum), Register by making an account then login.
Thats it, all set to float around anywhere.


[![Index page Screen Shot][product-screenshot2]](https://example.com/)
This is in example of the Forums Profanity filter in action.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Profanity Filter
- [x] Add Forum
- [x] Add SubClub Cleanup Game
- [ ] Add password visibility checkbox
- [ ] Get Signed Consent Documents for ALL people in Photographs
- [ ] Get Background Images
    - [ ] Spring
    - [ ] Summer
    - [ ] Fall
    - [ ] Winter
- [ ] Deploy
- [ ] Add other Profanity word filter tables
    - [ ] Hate Words

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Stephen Littman - [My Facebook](https://www.facebook.com/stephen.littman.9)

Project Link - [SubClub-Final-project](https://github.com/anarchking/Subclub-final-project)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This is a list of some useful tool and resources used in the study of this project.


* [GitHub](https://github.com)
* [Stackoverflow](https://stackoverflow.co/)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [How to Deploy Flask with Gunicorn and Nginx (on Ubuntu)](https://www.youtube.com/watch?v=KWIIPKbdxD0)
* [SubClub Cleanup Game was a Remix of Pickleblast's Mario Cart 3D](https://scratch.mit.edu/projects/777460692)
* [Profanity filter built from csv file found at this github](https://github.com/surge-ai/profanity)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



[product-screenshot]: Screenshots/Screenshot(5).png
[product-screenshot2]: Screenshots/Screenshot(6).png
[Flask.com]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[Jinja.com]: https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black
[Jinja-url]: https://jinja.palletsprojects.com/
[SQLite.com]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://sqlite.org/
[HTML.com]: https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[HTML-url]: https://www.w3.org/html/
[CSS.com]: https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://www.w3.org/Style/CSS/Overview.en.html
[Javascript.com]: https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E
[Javascript-url]: https://www.javascript.com/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[Scratch.com]: https://en.scratch-wiki.info/w/skins/ScratchWikiSkin2/resources/Scratch-logo-sm.png
[Scratch-url]: https://scratch.mit.edu/
[Nginx.com]: https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white
[Nginx-url]: https://www.nginx.com/
[Gunicorn.com]: https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white
[Gunicorn-url]: https://gunicorn.org/
[YouTube.com]: https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white
[YouTube-url]: https://youtu.be/I2C0B-_EbtU


