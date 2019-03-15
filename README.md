# slovakrail-ticket-script

Script for automated buying **free** ticket for slovak rails https://www.slovakrail.sk/sk/internetovy-obchod/internetovy-obchod-zssk.html

Script will click on buttons, and fill up the input boxes for you, from the file `person.txt`. Source code is self-explanatory with comments, so you can edit it, with the proper values (e.g. I am student, if you are not, you need to change it in source).

# Requirements
- python3.6
- pip packages:
  - flake8 = 2.5.4
  - mccabe = 0.4.0
  - pep8 = 1.7.0
  - pyflakes = 1.0.0
  - selenium = 2.53.2
  - Unidecode = 0.4.19
  - Firefox < 47
- geckodriver = 0.24.0

# Installation

### Ubuntu 16.04.6

1. Set your account in `person.txt`

2. Initialize the environment via these commands

```sh
# 1) python3.6 + pip3
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6 python3-pip

# 2) geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
tar -xvzf geckodriver-v0.24.0-linux64.tar.gz
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin

# 3) repository
git clone https://github.com/astaruch/slovakrail-ticket-script.git
cd slovakrail-ticket-script

# 4) requirements
python3.6 -m pip install -r requirements.txt

# 5) help test
python3.6 buy_ticket.py --help
```

3. See *Usage* section

# Usage

* help
	```sh
	python3.6 buy_ticket -h
	```

* Define the **exact** time, date, destinations (from and to) of your train.<br>Example:<br>
	```sh
	./buy_ticket.py buy -f 'Bratislava hl.st.' -to 'Kúty' -t '05:16' -d '16.03.2019'

	python3.6 buy_ticket.py buy -f 'Bratislava hl.st.' -to 'Kúty' -t '05:16' -d '16.03.2019'
	```
