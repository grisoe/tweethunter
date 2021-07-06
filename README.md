# tweethunter
Tweethunter is a Python script to search for tweets containing a main term and at least one secondary term. It returns
a json file with all the tweets found and their information. Written and tested using Python 3.8.10.


## Requirements
Use the apt package manager to install the webdriver for Firefox.
```bash
sudo apt install firefox-geckodriver
```
Next, use pip to install the required libraries.
```bash
pip install -r requirements.txt
```


## Configuration File
You need to edit the file conf.json located in the conf folder. In the "inTwitter" array are the main terms of the 
search, you need at least one main term. The "inTweets" array stores the secondary terms; for example, if you want the 
tweets that have the word "torvalds", along with at least one of these terms: linux, unix, computers, etc., you 
need to put the term "torvalds" in inTwitter and "linux", "unix", "computers" in "inTweets". 
The "remove" array stores the names of the Twitter accounts you do not want tweets from.
```json
{
  "inTwitter": [
    "torvalds",
    "ritchie"
  ],
  "inTweets": [
    "linux",
    "unix",
    "computers"
  ],
  "remove": [
    "microsoft",
    "apple"
  ]
}
```


## Usage
| Argument        | Description |
| ------------- |:-------------|
| -h, --help | Display a help message and exit. |
| -s, --since | Search since this date. |
| -u, --until | Search until this date. |
| -c, --conf | Configuration file path. |
| -ac, --all-columns | Get all columns from tweets. |
| -ss, --screenshots | Take screenshots of tweets (experimental). |
| -hl, --headless | Headless screenshots (experimental). |

### Usage examples
Get tweets between a date range. If not used, the tweets returned are from seven days ago until the current day.
```bash
python tweethunter.py -s "2020-01-12" -u "2021-01-12"
```
Specify a configuration file. If unsed, then conf/conf.json is used as the default.
```bash
python tweethunter.py -c "conf/custom_config.json"
```
Take screenshots of the tweets found.
```bash
python tweethunter.py -ss
```
Take screenshots, with a headless navigator, of the tweets found. If the argument -ss is not used, 
then this one is ignored.
```bash
python tweethunter.py -ss -hl
```
Get all columns from the tweets.
```bash
python tweethunter.py -ac
```


## Docker
Alternatively, you can run tweethunter using Docker.
### Prerequisites
If you want the output of the execution of tweethunter to be saved in the host machine, first you need to create the
folder and set the permissions.
```bash
mkdir docker
chown -R :1024 docker
chmod -R 775 docker
chmod -R g+s docker
```
### Build Image
```bash
docker build -t tweethunter .
```
### Run Image as a Container
```bash
docker run -it --rm -v "$PWD/docker/output":/home/th/output -v "$PWD/docker/images":/home/th/images -v "$PWD/conf":/home/th/conf tweethunter
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
