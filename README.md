# tweethunter
tweethunter is a Python script to make queries containing a huge number of terms using 
[Twint](https://github.com/twintproject/twint). It can also take screenshots of the tweets found. 
Feel free to use this tool if you are lazy enough to run Twint multiple times.

Written and tested using Python 3.8.10 on Ubuntu 20.04.2.


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
You need to edit the file conf.json located in the conf folder. In the inTwitter array are the main terms of the 
search; you need at least one. The inTweets array stores the secondary terms; for example, if you want the 
tweets that have the word "torvalds", along with at least one of these terms: "linux", "unix", "computers", etc., you 
need to put the term "torvalds" in inTwitter and "linux", "unix", "computers" in inTweets. 
The remove array stores the names of the Twitter accounts you do not want tweets from.
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
| -s, --since | Search since this date. Format: YYYY/MM/DD |
| -u, --until | Search until this date. Format: YYYY/MM/DD |
| -c, --conf | Configuration file path. conf/conf.json if not specified. |
| -ac, --all-columns | Get all columns from tweets. |
| -ss, --screenshots | Take screenshots of tweets (experimental). |
| -hl, --headless | Headless screenshots (experimental). |

### Usage examples
Get tweets between a date range. If not used, the tweets returned are from seven days ago until the current day.
```bash
python tweethunter.py -s "2020-01-12" -u "2021-01-12"
```
Specify a configuration file.
```bash
python tweethunter.py -c "conf/custom_config.json"
```
Take screenshots of the tweets found. If you are using the Docker version, you have to use the -hl argument, too.
```bash
python tweethunter.py -ss
```
Take screenshots, with a headless navigator, of the tweets found. If the argument -ss is not used, 
then this one is ignored.
```bash
python tweethunter.py -ss -hl
```
Get all columns.
```bash
python tweethunter.py -ac
```


## Docker
Alternatively, you can run tweethunter using Docker.

### Build Image
```bash
docker build -t tweethunter .
```

### Run Image as a Container
```bash
docker run -it --rm \
  -v "$PWD/docker/output":/home/th/output \
  -v "$PWD/docker/images":/home/th/images \
  -v "$PWD/conf":/home/th/conf \
  tweethunter ARGS
```

### Pull from Docker Hub
```bash
docker pull sergiormh/tweethunter
```

### Run Pulled Image
First, you need to create the folders in which the output will be stored.
```bash
mkdir docker && \
  mkdir docker/output && \
  mkdir docker/images
```
Next, create the folder in which the configuration files will be stored. Inside this folder, you have tu create your
own configuration file. Referer to the [Configuration File](#configuration-file) section for more information on this topic.
```bash
mkdir conf
```
It is now ready to be run.
```bash
docker run -it --rm \
  -v "$PWD/docker/output":/home/th/output \
  -v "$PWD/docker/images":/home/th/images \
  -v "$PWD/conf":/home/th/conf \
  sergiormh/tweethunter ARGS
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)