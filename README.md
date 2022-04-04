# 🚀 Pancakeswap BSC - Uniswap ERC-20 Sniper Bot 🚀
Web3 Pancakeswap Sniper & Take Profit/StopLoss bot written in python3


https://etherscan.io/tx/0x6d0ccefbaa2947f3eec6d54ebc7af6b079b379ce2317e2405bdf581f34389591
https://etherscan.io/tx/0x8c18fcba662a99f76f01e0032b6a512175ad643eec8e9f9ed6c7d41a2a43d5ab

![image](https://user-images.githubusercontent.com/102369376/161604174-dc2d4ba8-0f73-4f63-98be-1ccb1ba963d4.png)


**For now, Telegram Alerts are under development.**
## Our thanks:

BOT is free-to-use, but you are welcome to appreciate my work ☺️

ETH - 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52

BNB - 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52

# Features
- HoneyPot checker
- Trailing target profit & Stop loss
- Liquidity sniping
- Minimum taxes check (lot of rugs/scam have 0% taxes)
- Coming soon: ERC-20 support
- Coming soon: Telegram Alerts with custom bot

![Sniper](screenshot.png)  

# Download
### If you are not familiar with Python please have a look at [Releases]

# Install
**I'm using version 3.9.12 of Python, you can download it here (Be sure to use this version at least to avoid problems with the bot)**: https://www.python.org/downloads/release/python-3912/

Run on Android you need Install [Termux](https://termux.com/)  
```shell
termux: $ pkg install python git
Debian/Ubuntu: $ sudo apt install python3 git make gcc
Windows: Need to install Visual Studio BuildTools & Python3
```

**For Windows:**
Download Windows BuildTools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

And install **BuildTools C++**

![buildtools](buildtools.png)  



### Setup your address (just under your account name) and secret key in Settings.json.

![howto](how-to-export.gif)  

Clone Repo:  
```shell
git clone https://github.com/DexSniping/DexSniping-BSC-ERC20-Telegram-Alerts.git
cd DexSniping-BSC-ERC20-Telegram-Alerts
```

Install Requirements:  

**Try to add "3" after python if you have problems, like: python3 sniper.py...**

```python
python -m pip install -r requirements.txt
```  

Start Sniper:  
```python
python Sniper.py -t <TOKEN_ADDRESS> -a <AMOUNT> -tx <TXAMOUNT> -hp -wb <BLOCKS WAIT BEFORE BUY> -tp <TAKE PROFIT IN PERCENT> -sl <STOP LOSE IN PERCENT>
python Sniper.py -t 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52 -a 0.001 -tx 2 -hp  -wb 10 -tp 50
python Sniper.py -t 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52 --sellonly
python Sniper.py -t 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52 -a 0.001 --buyonly
python Sniper.py -t 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52 -tsl 10 -nb
```  

Here are all options with infos:  
```python3
*'-t' or '--token', Token for snipe e.g. "-t 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52"
'-a' or '--amount', float, Amount in Bnb to snipe e.g. "-a 0.1"

'-tx' or '--txamount', how mutch tx you want to send? It split your BNB amount in e.g. "-tx 5"

'-wb' or '--awaitBlocks', default=0, Await Blocks before sending BUY Transaction. e.g. "-ab 50" 

'-hp' or '--honeypot', if you use this Flag, your token get checks if token is honypot before buy!

'-nb' or '--nobuy', No Buy, Skipp buy, if you want to use only TakeProfit/StopLoss/TrailingStopLoss
'-tp' or '--takeprofit', Percentage TakeProfit from your input BNB amount. e.g. "-tp 50" 
'-tsl'or '--trailingstoploss', 'Percentage Trailing-Stop-loss from your first Quote "-tsl 50"

'-so' or '--sellonly', Sell ALL your Tokens from given token address
'-bo' or '--buyonly', Buy Tokens with your given amount

* = require every time its runs!
```
## Trailing-Stop-Loss:
<img src="https://i.ytimg.com/vi/dZFb0-fwqOk/maxresdefault.jpg" height="400">


## Troubleshooting:

<em>Problem: My bot does not start and displays a "loadTokens" or "unknown opcode" error:</em>

Solution: I'm using version 3.9.12 of Python, you can download it here (Be sure to use this version at least to avoid problems with the bot): https://www.python.org/downloads/release/python-3912/

<em>Problem: "python" does not work, what to do?</em>

Solution: Try to add "3" after python if you have problems, like: python3 sniper.py...

<em>Problem: I have a problem when I try to install the requirements</em>

Solution: Be sure to download and install **BuildTools C++** https://visualstudio.microsoft.com/visual-cpp-build-tools/
