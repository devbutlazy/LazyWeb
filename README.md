# LazyWeb // devbutlazy

![image](https://github.com/user-attachments/assets/9501a332-293e-4da6-9b8e-bfb2e9b8e31b)

## Instalation guide(with Docker):
`1` Download and install Python from [python.org](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe)  
`2` Download and install git from [git-scm.com](https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe)  
`3` Download and install docker:  
```
- Ubuntu:
[1] sudo apt update
[2] sudo apt install docker.io docker-compose

- Windows:
[1] Download and install docker from https://www.docker.com/products/docker-desktop/
[2] Read the docs installation guide: https://docs.docker.com/desktop/install/windows-install/
```
`4` Clone this repository and [DDrive](https://github.com/forscht/ddrive) (using --recursive)
```
git clone https://github.com/devbutlazy/LazyWeb --recursive
```
`5` Create `.env` file in `src/app/main/config/` and fill out the environmental variables in it:  
```
DB_NAME=database
TELEGRAM_CHAT_ID=
BOT_TOKEN=
BOT_ADMIN_ID=
```
`6` Edit the `index.html` and images according to you  
`7` Build the docker-compose
```
sudo docker-compose up -d --build (linux)
```
`8` Run docker-compose in the background
```
sudo docker-compose up -d (linux)
```

`9` Manually run the DDrive using Docker manual from [README tutorial](https://github.com/forscht/ddrive/blob/4.x/README.md)


## After completing the guide, your website should run on http://localhost:8000 


### TODO:
- [x] Follow the SOLID, DRY and Clean-Architecture rules
- [x] Visits counter on main page 
- [x] Send messages to telegram through website
- [x] Connect DDrive (https://ddrv.devbutlazy.xyz/)
- [x] Blogging system (https://blog.devbutlazy.xyz/)

## Feel free to open [issues](https://github.com/devbutlazy/LazyWeb/issues) or [pull requests](https://github.com/devbutlazy/LazyWeb/pulls) if you have encountered any kind of problems.

### (c) LazyWeb License: MIT-LICENSE