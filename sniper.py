# -*- coding: utf-8 -*-

##
## Forked & Inspired by https://github.com/SavannahCaToken/Pancakeswap_BSC_Sniper_Bot_Fullversion/
##

from txns import TXN
import argparse, math, sys, json, requests, getpip
from time import sleep
from halo import Halo
from style import style

ascii = """
________                   _________      .__                     
\______ \   ____ ___  ___ /   _____/ ____ |__|_____   ___________ 
 |    |  \_/ __ \\  \/  / \_____  \ /    \|  \____ \_/ __ \_  __  \ 
 |    `   \  ___/ >    <  /        \   |  \  |  |_> >  ___/|  | \/
/_______  /\___  >__/\_ \/_______  /___|  /__|   __/ \___  >__|   
        \/     \/      \/        \/     \/   |__|        \/       
"""

parser = argparse.ArgumentParser(description='Set your Token and Amount example: "sniper.py -t 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52 -a 0.2"')
parser.add_argument('-t', '--token', help='str, Token for snipe e.g. "-t 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52"')
parser.add_argument('-a', '--amount', default=0, help='float, Amount in Bnb to snipe e.g. "-a 0.1"')
parser.add_argument('-tx', '--txamount', default=1, nargs="?", const=1, type=int, help='int, how mutch tx you want to send? It Split your BNB Amount in e.g. "-tx 5"')
parser.add_argument('-sp', '--sellpercent', default=100, nargs="?", const=1, type=int, help='int, how mutch tokens you want to sell? Percentage e.g. "-sp 80"')
parser.add_argument('-hp', '--honeypot', default=False, action="store_true", help='Check if your token to buy is a Honeypot, e.g. "-hp" or "--honeypot"')
parser.add_argument('-nb', '--nobuy', action="store_true", help='No Buy, Skipp buy, if you want to use only TakeProfit/StopLoss/TrailingStopLoss')
parser.add_argument('-tp', '--takeprofit', default=0, nargs="?", const=True, type=int, help='int, Percentage TakeProfit from your input BNB amount "-tp 50" ')
parser.add_argument('-sl', '--stoploss', default=0, nargs="?", const=True, type=int, help='int, Percentage Stop loss from your input BNB amount "-sl 50" ')
parser.add_argument('-tsl', '--trailingstoploss', default=0, nargs="?", const=True, type=int, help='int, Percentage Trailing-Stop-loss from your first Quote "-tsl 50" ')
parser.add_argument('-wb', '--awaitBlocks', default=0, nargs="?", const=True, type=int, help='int, Await Blocks before sending BUY Transaction "-wb 5" ')
parser.add_argument('-cmt', '--checkMaxTax',  action="store_true", help='get Token Tax and check if its higher.')
parser.add_argument('-cc', '--checkcontract',  action="store_true", help='Check is Contract Verified and Look for some Functions.')
parser.add_argument('-so', '--sellonly',  action="store_true", help='Sell all your Tokens from given address')
parser.add_argument('-bo', '--buyonly',  action="store_true", help='Buy Tokens with from your given amount')
parser.add_argument('-cl', '--checkliquidity',  action="store_true", help='with this arg you use liquidityCheck')
parser.add_argument('-r', '--retry', default=3, nargs="?", const=True, type=int, help='with this arg you retry automatically if your tx failed, e.g. "-r 5" or "--retry 5" for max 5 Retrys')
parser.add_argument('-sec', '--SwapEnabledCheck',  action="store_true", help='this argument disabled the SwapEnabled Check!')
args = parser.parse_args()


class SniperBot():

    def __init__(self):
        self.parseArgs()
        self.settings = self.loadSettings()
        self.SayWelcome()

    def loadSettings(self):
        with open("Settings.json", "r") as settings:
            settings = json.load(settings)
        return settings

    def SayWelcome(self):
        self.TXN = TXN(self.token, self.amountForSnipe)
        print(style().YELLOW + ascii + style().RESET)
        print(style().GREEN + "Start Sniper Tool with following arguments:" + style().RESET)
        print(style().BLUE + "---------------------------------" + style().RESET)
        print(style().YELLOW + "Amount for Buy:", style().GREEN + str(self.amount) + " BNB" + style().RESET)
        print(style().YELLOW + "Token to Interact :", style().GREEN + str(self.token) + style().RESET)
        print(style().YELLOW + "Token Name:", style().GREEN + str(self.TXN.get_token_Name()) + style().RESET)
        print(style().YELLOW + "Token Symbol:", style().GREEN + str(self.TXN.get_token_Symbol()) + style().RESET)
        print(style().YELLOW + "Transaction to send:", style().GREEN + str(self.tx) + style().RESET)
        print(style().YELLOW + "Amount per transaction :", style().GREEN + str("{0:.8f}".format(self.amountForSnipe)) + style().RESET)
        print(style().YELLOW + "Await Blocks before buy :", style().GREEN + str(self.wb) + style().RESET)

        if self.tsl != 0:
            print(style().YELLOW + "Trailing Stop loss Percent :", style().GREEN + str(self.tsl) + style().RESET)
        if self.tp != 0:
            print(style().YELLOW + "Take Profit Percent :", style().GREEN + str(self.tp) + style().RESET)
        if self.sl != 0:
            print(style().YELLOW + "Stop loss Percent :", style().GREEN + str(self.sl) + style().RESET)
        print(style().BLUE + "---------------------------------" + style().RESET)

    def parseArgs(self):
        self.token = args.token
        if self.token == None:
            print(style.RED+"Please Check your Token argument e.g. -t 0xaAA9c55FF5ce8e6431d84BE3cf9d0Ba39742ac52")
            print("exit!")
            raise SystemExit

        self.amount = args.amount
        if args.nobuy != True:
            if not args.sellonly:
                if self.amount == 0:
                    print(style.RED+"Please Check your Amount argument e.g. -a 0.01")
                    print("exit!")
                    raise SystemExit

        self.tx = args.txamount
        self.amountForSnipe = float(self.amount) / float(self.tx)
        self.hp = args.honeypot
        self.wb = args.awaitBlocks
        self.tp = args.takeprofit
        self.sl = args.stoploss
        self.tsl = args.trailingstoploss
        self.cl = args.checkliquidity
        self.stoploss = 0
        self.takeProfitOutput = 0 
        if self.tp != 0:
            self.takeProfitOutput = self.calcProfit()
        if self.sl != 0:
            self.stoploss = self.calcloss()

    def calcProfit(self):
        if self.amountForSnipe == 0.0:
            self.amountForSnipe = self.TXN.getOutputTokenToBNB(percent=args.sellpercent)[0] / (10**18)
        a = ((self.amountForSnipe * self.tx) * self.tp) / 100
        b = a + (self.amountForSnipe * self.tx)
        return b

    def calcloss(self):
        if self.amountForSnipe == 0.0:
            self.amountForSnipe = self.TXN.getOutputTokenToBNB(percent=args.sellpercent)[0] / (10**18)
        a = ((self.amountForSnipe * self.tx) * self.sl) / 100
        b = (self.amountForSnipe * self.tx) - a
        return b

    def calcNewTrailingStop(self, currentPrice):
        a = (currentPrice * self.tsl) / 100
        b = currentPrice - a
        return b

    def awaitBuy(self):
        spinner = Halo(text='await Buy', spinner='dots')
        spinner.start()
        for i in range(self.tx):
            spinner.start()
            self.TXN = TXN(self.token, self.amountForSnipe)
            tx = self.TXN.buy_token(args.retry)
            spinner.stop()
            print(tx[-1])
            if tx[0] != True:
                raise SystemExit

    def awaitSell(self):
        spinner = Halo(text='await Sell', spinner='dots')
        spinner.start()
        self.TXN = TXN(self.token, self.amountForSnipe)
        tx = self.TXN.sell_tokens(args.sellpercent)
        spinner.stop()
        print(tx[1])
        if tx[0] != True:
            raise SystemExit

    def awaitApprove(self):
        spinner = Halo(text='await Approve', spinner='dots')
        spinner.start()
        self.TXN = TXN(self.token, self.amountForSnipe)
        tx = self.TXN.approve()
        spinner.stop()
        print(tx[1])
        if tx[0] != True:
            raise SystemExit

    def awaitBlocks(self):
        spinner = Halo(text='await Blocks', spinner='dots')
        spinner.start()
        waitForBlock = self.TXN.getBlockHigh() + self.wb
        while True:
            sleep(0.13)
            if self.TXN.getBlockHigh() > waitForBlock:
                spinner.stop()
                break
        print(style().GREEN+"[DONE] Wait Blocks finish!")

    def CheckVerifyCode(self):
        while True:
            req = requests.get(
                f"https://api.bscscan.com/api?module=contract&action=getsourcecode&address={self.token}&apikey=YourApiKeyToken")
            if req.status_code == 200:
                getsourcecode = req.text.lower()
                jsonSource = json.loads(getsourcecode)
                if not "MAX RATE LIMIT REACHED".lower() in str(jsonSource["result"]).lower():
                    if not "NOT VERIFIED".lower() in str(jsonSource["result"]).lower():
                        print("[CheckContract] IS Verfied")
                        for BlackWord in self.settings["cc_BlacklistWords"]:
                            if BlackWord.lower() in getsourcecode:
                                print(
                                    style().RED+f"[CheckContract] BlackWord {BlackWord} FOUND, Exit!")
                                raise SystemExit
                        print(style().GREEN +
                              "[CheckContract] No known abnormalities found.")
                        break
                    else:
                        print(
                            style().RED+"[CheckContract] Code Not Verfied, Can't check, Exit!")
                        raise SystemExit
                else:
                    print("Max Request Rate Reached, Sleep 5sec.")
                    sleep(5)
                    continue
            else:
                print("BSCScan.org Request Faild, Exiting.")
                raise SystemExit

    def awaitLiquidity(self):
        spinner = Halo(text='await Liquidity', spinner='dots')
        spinner.start()
        while True:
            sleep(0.07)
            try:
                self.TXN.fetchOutputBNBtoToken()[0]
                spinner.stop()
                break
            except Exception as e:
                if "UPDATE" in str(e):
                    print(e)
                    raise SystemExit
                continue

        print(style().GREEN+"[DONE] Liquidity is Added!" + style().RESET)

    def fetchLiquidity(self):
        liq = self.TXN.getLiquidityUSD()[1]
        print(style().GREEN+"[LIQUIDTY] Current Token Liquidity:", round(liq, 3), "USD" + style().RESET)
        if float(liq) < float(self.settings["MinLiquidityUSD"]):
            print(style.RED+"[LIQUIDTY] <- TO SMALL, EXIT!")
            raise SystemExit
        return True

    def awaitEnabledBuy(self):
        spinner = Halo(text='await Dev Enables Swapping', spinner='dots')
        spinner.start()
        while True:
            sleep(0.07)
            try:
                if self.TXN.checkifTokenBuyDisabled() == True:
                    spinner.stop()
                    break
            except Exception as e:
                if "UPDATE" in str(e):
                    print(e)
                    raise SystemExit
                continue
        print(style().GREEN+"[DONE] Swapping is Enabeld!" + style().RESET)

    def awaitMangePosition(self):
        highestLastPrice = 0
        if self.tp != 0:
            self.takeProfitOutput = self.calcProfit()
        if self.sl != 0:
            self.stoploss = self.calcloss()
        TokenBalance = round(self.TXN.get_token_balance(), 5)
        while True:
            try:
                sleep(0.9)
                LastPrice = float(
                    self.TXN.getOutputTokenToBNB(args.sellpercent)[0] / (10**18))
                if self.tsl != 0:
                    if LastPrice > highestLastPrice:
                        highestLastPrice = LastPrice
                        self.TrailingStopLoss = self.calcNewTrailingStop(
                            LastPrice)
                    if LastPrice < self.TrailingStopLoss:
                        print(style().GREEN + "[TRAILING STOP LOSS] Triggert!" + style().RESET)
                        self.awaitSell()
                        break

                if self.takeProfitOutput != 0:
                    if LastPrice >= self.takeProfitOutput:
                        print()
                        print(style().GREEN + "[TAKE PROFIT] Triggert!" + style().RESET)
                        self.awaitSell()
                        break

                if self.stoploss != 0:
                    if LastPrice <= self.stoploss:
                        print()
                        print(style().GREEN + "[STOP LOSS] Triggert!" + style().RESET)
                        self.awaitSell()
                        break

                msg = str("Token Balance: " + str("{0:.5f}".format(
                    TokenBalance)) + " | CurrentOutput: "+ str("{0:.7f}".format(LastPrice))+"BNB")
                if self.stoploss != 0:
                    msg = msg + " | Stop loss below: " + str("{0:.7f}".format(self.stoploss)) + "BNB"
                if self.takeProfitOutput != 0:
                    msg = msg + " | Take Profit Over: " + str("{0:.7f}".format(self.takeProfitOutput)) + "BNB"
                if self.tsl != 0:
                    msg = msg + " | Trailing Stop loss below: " + str("{0:.7f}".format(self.TrailingStopLoss)) + "BNB"
                print(msg, end="\r")

            except Exception as e:
                if KeyboardInterrupt:
                    raise SystemExit
                print(style().RED + f"[ERROR] {str(e)},\n\nSleeping now 30sec and Reinit RPC!" + style().RESET)
                sleep(30)
                self.TXN = TXN(self.token, self.amountForSnipe)
                continue

        print(style().GREEN + "[DONE] Position Manager Finished!" + style().RESET)

    def StartUP(self):
        self.TXN = TXN(self.token, self.amountForSnipe) 

        if args.sellonly:
            print("Start SellOnly, for selling tokens!")
            self.awaitApprove()
            if args.SwapEnabledCheck == True:
                self.awaitEnabledBuy()
            if args.sellpercent > 0 and args.sellpercent < 100:
                print(self.TXN.sell_tokens(args.sellpercent)[1])
            else:
                percent = int(input("Enter Percent you want to sell: "))
                print(self.TXN.sell_tokens(percent)[1])
            raise SystemExit

        if args.buyonly:
            print(f"Start BuyOnly, buy now with {self.amountForSnipe}BNB tokens!")
            print(self.TXN.buy_token(args.retry)[1])
            raise SystemExit

        if args.nobuy != True: 
            self.awaitLiquidity()
            if args.SwapEnabledCheck == True:
                self.awaitEnabledBuy()

        if args.checkcontract:
            self.CheckVerifyCode()

        if self.hp == True:
            try:
                honeyTax = self.TXN.checkToken()
                print(style().YELLOW + "Checking Token..." + style().RESET)

                if honeyTax[2] == True:
                    print(style.RED + "Token is Honeypot, exiting")
                    raise SystemExit
                elif honeyTax[2] == False:
                    print(style().GREEN + "[DONE] Token is NOT a Honeypot!" + style().RESET)
            except Exception as e:
                self.i = input(style().RED+"Error in HoneyPot Check, HIGH Risk to enter a Honeypot!\n" + style().GREEN + " Exiting? y/n \n > " + style().RESET)
                if self.i.lower() == "y":
                    raise SystemExit

        if args.checkMaxTax == True:
            try:
                honeyTax = self.TXN.checkToken()
                print(style.GREEN + "[TOKENTAX] Current Token BuyTax:", honeyTax[0], "%" + style.RESET)
                print(style.GREEN + "[TOKENTAX] Current Token SellTax:", honeyTax[1], "%" + style.RESET)
                if honeyTax[1] > self.settings["MaxSellTax"]:
                    print(style().RED+"Token SellTax exceeds Settings.json, exiting!")
                    raise SystemExit
                if honeyTax[0] > self.settings["MaxBuyTax"]:
                    print(style().RED+"Token BuyTax exceeds Settings.json, exiting!")
                    raise SystemExit
                if honeyTax[1] < self.settings["MinSellTax"]:
                    print(style().RED+"Token SellTax is bellow Settings.json, exiting!")
                    raise SystemExit
                if honeyTax[0] < self.settings["MinBuyTax"]:
                    print(style().RED+"Token BuyTax is bellow Settings.json, exiting!")
                    raise SystemExit
            except Exception as e:
                if self.i:
                    if self.i.lower() == "y":
                        raise SystemExit
                else:
                    self.i = input(style().RED+"Error in Token Tax Check, HIGH Risk to enter a Honeypot!\n" + style().GREEN + "Exiting? y/n \n > " + style().RESET)
                    if self.i.lower() == "y":
                        raise SystemExit

        if self.wb != 0:
            self.awaitBlocks()

        if self.cl == True:
            if self.fetchLiquidity() != False:
                pass

        if args.nobuy != True:
            self.awaitBuy()

        # Give the RPC/WS some time to Index your address nonce, make it higher if " ValueError: {'code': -32000, 'message': 'nonce too low'} "

        if self.tsl != 0 or self.tp != 0 or self.sl != 0:
            sleep(7)
            self.awaitApprove()
            self.awaitMangePosition()

        print(style().GREEN + "[DONE] Sniper Bot finish!" + style().RESET)


SniperBot().StartUP()
