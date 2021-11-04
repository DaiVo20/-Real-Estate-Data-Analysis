### Set up
Create virtual environment
1. $ sudo apt install python3.9-venv
2. $ python3 -m venv venv
3. $ source venv/bin/activate

### Create Scrapy empty project
1. $ sudo apt install python3-scrapy
2. $ scrapy startproject tutorial

### Starting crwal
To crawl data from website run:
1. $ scrapy crawl <name>

To save data run:
1. scrapy crawl <name> -o <filename>.csv
