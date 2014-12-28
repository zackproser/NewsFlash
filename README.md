NewsFlash
=========

Python script to get top news headlines and links, and top news keywords (courtesy of AlchemyAPI) directly to your Gmail inbox in a few seconds.

Getting Started
===============

You'll need: 

- [An AlchemyAPI Key](http://www.alchemyapi.com/)
- A Gmail Account
- Python installed on your system

1. Follow the steps [here](http://www.alchemyapi.com/developers/sdks/) to get your AlchemyAPI script working
2. Edit lines 14, 47 and 48 of newsflash.py to use your own private Gmail credentials
3. Run ~python newsflash.py 

You'll get an email with two scrollable boxes, one with linked Headlines and one with top Keywords. This script gathers data from NYtimes and BBC World. You can extend it yourself to include your own favorite news sources. 
