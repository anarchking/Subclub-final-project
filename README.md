# SubClub Web Application
#### Video Demo:  <URL HERE>
#### Description:
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
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
        <li><a href="#installation">Installation</a></li>
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

[![Product Name Screen Shot][product-screenshot]](https://example.com)

There are many great README templates available on GitHub; however, I didn't find one that really suited my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should implement DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have contributed to expanding this template!

Use the `BLANK_README.md` to get started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Flask][Flask.com]][Flask-url]
* [![Jinja][Jinja.com]][Jinja-url]
* [![SQLite][SQLite.com]][SQLite-url]
* [![HTML][HTML.com]][HTML-url]
* [![CSS][CSS.com]][CSS-url]
* [![Javascript][Javascript.com]][Javascript-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]
* [![Scratch][Scratch.com]][Scratch-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.


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


### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
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

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Stephen Littman - [My Facebook](https://www.facebook.com/stephen.littman.9)
Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [GitHub](https://github.com)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


[product-screenshot]: images/screenshot.png

[Flask.com]: https://flask.palletsprojects.com/en/3.0.x/_images/flask-horizontal.png
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
[Scratch.com]: <img href="https://scratch.mit.edu/static/assets/90fb0caa5319c39b24946476dd32bb0d.svg" alt="Logo" width="80" height="80">
[Scratch-url]: https://scratch.mit.edu/
[YouTube.com]: https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white
[YouTube-url]: https://youtube.com/


