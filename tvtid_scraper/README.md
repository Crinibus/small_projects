## How to use

Command using all flags:
```
python3 scraper.py -c [channel] -t [time] -a
```
An example with 'real' values:
```
python3 scraper.py -c dr1 -c tv2 -t 20:00
```
This prints only the tv-shows that start at 8 pm on the channels DR1 and TV2. 

<br/>

# Avalible flags
- ```-c [channel]``` or ```--channel [channel]```
- ```-t [hh:mm]``` or ```--time [hh:mm]```
- ```-a``` or ```--all```

<br/>

By using the flag "-c" or "--channel" you specify which channels you want the program to show tv-shows from. Replace "[channel]" with wanted channel, e.g. "dr1". <br/>
You can specify multiple channels just by using the "-c" flag again.<br/>
For example:
```
python3 scraper.py -c [channel_1] -c [channel_2]
```
**OBS**: when specifing channels with a space such as "TV2 News", use a dash (-) instead of a space.

<br/>

By using the flag "-t" or "--time" you can specify a time for the program to find a tv-show that starts at the specified time.<br/>
Time must be formatted like this: "hh:mm".

By using the flag "-a" or "--all" you want to see all the programs running today at the specified channels.

<br/>

Right now all the channels on "tvtid.tv2.dk" is supported with is:
- dr1
- tv2
- tv3
- dr2
- tv2-charlie
- tv2-news
- kanal-5
- tv3-plus
- tv2-zulu
- dr-ramasjang
- kanal-4
- tv2-sport
- tv2-sport-x
- tv3-sport
- tv3-puls
- 6eren
- disney-channel
- tv2-fri
- canal-9
- discovery-channel
- tlc
- nickelodeon
- national-geographic-channel
- tv3-max
- cartoon
- disney-junior
- dk4
- mtv
- animal-planet
- investigation-discovery
- vh1
- eurosport-2
- boomerang

<br/>

## TODO

- Add support for multiple "--time" flags
- Add support for "all" with the flag "--channel" for choosing all channels