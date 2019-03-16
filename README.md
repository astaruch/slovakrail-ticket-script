# slovakrail-ticket-script

Automated **free** ticket buying at [www.zssk.sk](https://www.zssk.sk/).

Script will click on buttons and fill up the input boxes for you with the predefined data in `person.txt` file.

## Requirements
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

## Installation

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
rm -v geckodriver-v0.24.0-linux64.tar.gz

# 3) repository
git clone https://github.com/astaruch/slovakrail-ticket-script.git
cd slovakrail-ticket-script

# 4) requirements
python3.6 -m pip install -r requirements.txt

# 5) help test
python3.6 buy_ticket.py --help
```

3. See [*Usage*](https://github.com/astaruch/slovakrail-ticket-script#usage) section

## Usage

* help
	```sh
	python3.6 buy_ticket -h
	```

* Define the **exact** time, date, destinations (from and to) of your train.<br>Example:<br>
	```sh
	./buy_ticket.py -de "Bratislava hl.st." -ar "Kúty" -t "05:16" -d "18.03.2019"
	python buy_ticket.py -de "Bratislava hl.st." -ar "Kúty" -t "05:16" -d "18.03.2019"
	```

## Help

If you have purchased a wrong ticket you are able to cancel it [here](https://ikvc.slovakrail.sk/inet-sales-reimb/pages/connection/search.xhtml).

## Contributing

Feel free to contribute via opening a [pull request](https://help.github.com/articles/creating-a-pull-request/) or an [issue](https://help.github.com/articles/creating-an-issue/).

## License

This project is available as open source under the terms of the [GPL-3.0 License](https://github.com/europ/slovakrail-ticket-script/blob/master/LICENSE).
