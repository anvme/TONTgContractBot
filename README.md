# TONTgContractBot Readme
This is telegram bot for fast contract publication. 
 
 Just 25 seconds. just send to your bot *.sol file and wait

Tested on ubuntu 18.04 & python 3.6.9 (To check your python version, put to the terminal # python3 --version )
 

## Installation in 6 simple steps (2-3 minutes, and your bot is ready)

 1. Create your personal telegram bot and get Api Token. [Instruction](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0)
 2. Send to your new bot command /start and go to the next step
 3. Run command below
```sh
$ git clone -v https://github.com/anvme/TONTgContractBot.git /opt/tontgbotcontract && chmod +x /opt/tontgbotcontract/installsbot.sh
```
 4. Open /opt/tontgbotcontract/config.py in any editor and change values in TONTgBot from *Edit starts here* till *Edit ends here*. If you dont know your id(tg value), Just send message to @TONTgIDBot in telegram.
 5. Run 
 ```sh
$ sudo /bin/bash /opt/tontgbotcontract/installsbot.sh
```

## What to do if something not working?
Find in bot.py telebot.logger.setLevel(logging.ERROR) and change ERROR to DEBUG, restart tontgbot service and execute
  ```sh
$ journalctl -e -u tontgbot > /opt/tontgbot/servicelog.log
```
Then sent this log to my telegram @anvme
