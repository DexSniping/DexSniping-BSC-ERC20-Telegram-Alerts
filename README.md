Forked from https://github.com/SavannahCaToken/Pancakeswap_BSC_Sniper_Bot_Fullversion/

# 🚀 Pancakeswap BSC - Uniswap ERC-20 Sniper Bot 🚀
Web3 Pancakeswap Sniper & Take Profit/StopLoss bot written in python3

**For now, ERC-20 and Telegram Alerts are under devedevelopment.**
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
**First of all, you need install Python3+**
Run on Android you need Install [Termux](https://termux.com/)  
```shell
termux: $ pkg install python git
Debian/Ubuntu: $ sudo apt install python3 git make gcc
Windows: Need to install Visual Studio BuildTools & Python3
```

### Setup your Address and secret key in Settings.json.

Clone Repo:  
```shell
git clone https://github.com/DexSniping/DexSniping-BSC-ERC20-Telegram-Alerts.git
cd DexSniping-BSC-ERC20-Telegram-Alerts
```

Install Requirements:  
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