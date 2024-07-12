# LazyDev Website 
## Website written by lazy developer, using Python (Backend Fastapi), HTML + CSS + JS (Frontend)

## DEMO: https://devbutlazy.vn.ua

## Manual:
`1` Download python from [python.org](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe)  
`2` Install git from [git-scm.com](https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe)  
`3` Clone this repository and [DDRV](https://github.com/forscht/ddrive) (using --recursive)
```
git clone https://github.com/devbutlazy/lazy-website --recursive
```
`4` Go to `cmd.exe`, `cd PROJECT_PATH` and `pip install -r requirements.txt` to install required packages   
`5` Enter the valid config to .config.env, to correctly run the website backend    
`6` Edit the `index.html` and other files according to you and your information (because you are not me 😊)   
`7` Run the backend using uvicorn 
```
uvicorn main:app --port 8000 --reload
```
`8` When the console has printed "The app is starting up", open the `index.html` file, and the website is done. 

`+` Manually run the DDRV using docker as in their [README tutorial](https://github.com/forscht/ddrive/blob/4.x/README.md)


# What is in the backend?

    - Global visits counter. 
      When someone visits site, it adds +1 to the counter. 
      It also stores it in a sqlite database, so after restart the counter will remain.
    - Sending messages to telegram using requests.

# Docker configuration (soon)

# Deploy on VPS (soon)


# TODO:
- [x] Visits counter using async db
- [x] Send messages to telegram, using requests
- [x] Connect ddrv to https://ddrv.devbutlazy.vn.ua/
- [ ] Blogging system
- [ ] Add authorisation for blogging system (only for admins)

### License: GNU GPL 3.0 
