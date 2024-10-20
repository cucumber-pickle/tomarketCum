# Tomarket Bot Telegram Automation Script

Auto Claim for tomarket Telegram Bot

[TELEGRAM CHANNEL](https://t.me/cucumber_scripts)

Update 

# Warning

All Risks are borne by the user!

# Updates
### 10.10.24 add:
- Auto complete tasks
-  Auto use free spin
- Auto unlock levels
-  Auto upgrade max level
-  Auto share tg after upgrade

### 20.10.24 add:
- Auto puzzle

# Features

- [x] Auto Claim
- [x] Multi Account Support
- [x] Auto Play Game
- [x] Auto complete tasks
- [x] Auto use free spin
- [x] Auto unlock levels
- [x] Auto upgrade max level
- [x] Auto share tg after upgrade
- [x] Proxy Support
- [x] Auto puzzle

# Register

Click the following url to register : https://t.me/Tomarket_ai_bot/app?startapp=00019Ome 

# How to Use

## About Config

| Name                   | Description                                                                  |
|------------------------|------------------------------------------------------------------------------|
| interval               | downtime between account                                                     |
| play_game              | value must bool (true/false) set true for enable auto play game after claim  |
| complete_task          | value must bool (true/false) set true for enable auto complete_task          |
| use_free_spin          | value must bool (true/false) set true for enable auto use_free_spin          |
| unlock_levels          | value must bool (true/false) set true for enable auto unlock_levels          |
| upgrade_max_level      | value must bool (true/false) set true for enable auto upgrade_max_level      |
| share_tg_after_upgrade | value must bool (true/false) set true for enable auto share_tg_after_upgrade |
| additional_time        | value must bool (true/false) set true for enable auto use_free_spin          |
| game_point             | low : minimum earn from play game <br>high : maximum earn from play game     |



## About Proxy


You can add your proxy list in `proxies.txt` and proxy format is like example below :

Format :

```
http://host:port
http://user:pass@host:port
```

Example :

```
http://127.0.0.1:6969
http://user:pass@127.0.0.1:6969
socks5://127.0.0.1:6969
socks5://user:pass@127.0.0.1:6969
```

## Windows 

1. Make sure you computer was installed python and git.
   
   python site : [https://python.org](https://python.org)
   
   git site : [https://git-scm.com/](https://git-scm.com/)

2. Clone this repository
   ```shell
   git clone https://github.com/cucumber-pickle/tomarketCum.git
   ```

3. go to tomarketod directory
   ```
   cd tomarketCum
   ```

4. install the require library
   ```
   python -m pip install -r requirements.txt
   ```

5. Edit `data.txt`, input you data token in `data.txt` . One line for one data account, if you want add you second account add in new line!

6. execute the main program 
   ```
   python bot.py
   ```

## Linux

1. Make sure you computer was installed python and git.
   
   python
   ```shell
   sudo apt install python3 python3-pip
   ```
   git
   ```shell
   sudo apt install git
   ```

2. Clone this repository
   
   ```shell
   git clone https://github.com/cucumber-pickle/tomarketCum.git
   ```

3. goto tomarketod directory

   ```shell
   cd tomarketCum
   ```

4. Install the require library
   
   ```
   python3 -m pip install -r requirements.txt
   ```

5. Edit `data.txt`, input you data token in `data.txt`. One line for one data account, if you want add you second account add in new line!

6. execute the main program 
   ```
   python bot.py
   ```


## How to get tgWebAppData (query_id / user_id)

1. Login telegram via portable or web version
2. Launch the bot
3. Press `F12` on the keyboard 
4. Open console
5. Сopy this code in Console for getting tgWebAppData (user= / query=):

```javascript
copy(decodeURIComponent(sessionStorage.SourceTarget).split('#tgWebAppData=')[1].split('&tgWebAppVersion=')[0])
```

6. you will get data that looks like this

```
query_id=AA....
user=%7B%22id%....
```
7. add it to `data.txt` file or create it if you dont have one


## This bot helpfull?  Please support me by buying me a coffee: 
``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - BSC (BEP 20)

``` UQBiNbT2cqf5gLwjvfstTYvsScNj-nJZlN2NSmZ97rTcvKz0 ``` - TON

``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - Optimism

``` THaLf1cdEoaA73Kk5yiKmcRwUTuouXjM17 ``` - TRX (TRC 20)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For questions or support, please contact [CUCUMBER TG CHAT](https://t.me/cucumber_scripts_chat)