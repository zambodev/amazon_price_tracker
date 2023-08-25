# Amazon price tracker

A small program made to keep track of your desired items on amazon 

## Setup

**Version**: python 3.11

Required pip3 packages
```
pip3 install requests bs4
```
Copy the template.json and fill it with as many links as you want

## How to run
```
python3 apt.py <file>.json
```
Add new items on the go:
```
python3 apt.py <file>.json <title>:'<link>'
```

**Note**: links in argv are optional

## Showcase
```
> python3.11 apt.py file.json
Object: gygabyte_3070_it
Range: 423.00€ - 475.00€
Avg: 449.00€
Latest: 475.07€
--------------------------------
```
Note: Price history data is collected only when the script is runned
