import requests
from bs4 import BeautifulSoup
import argparse


def argparse_setup():
    """Setup and return argparse."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c',
        '--channel',
        help='the channel with the user want to see programs from',
        action='append'
    )
    
    parser.add_argument(
        '-t',
        '--time',
        help='the time the program starts. E.g. "20:00". Format is: "hh:mm"',
        type=str
    )
    
    parser.add_argument(
        '-a',
        '--all',
        help='show all programs for the chosen channel(s)',
        action='store_true'
    )
    
    return parser.parse_args()


def get_soup(URL='https://tvtid.tv2.dk/'):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
    cookies = dict(cookies_are='working')
    response = requests.get(URL, headers=headers, cookies=cookies)
    return BeautifulSoup(response.text, 'html.parser')


def get_channels() -> list:
    """Find all channels with programs, and return the list"""
    soup = get_soup()
    channels = soup.find_all('article', class_='tv2epg-channel')
    return channels


def get_programs(channel_list: list, channels: list) -> dict:
    """Find the programs for the specified channels and return a dict with them where the channels are the keys"""
    channel_index = {
        'dr1': 0,
        'tv2': 1,
        'tv3': 2,
        'dr2': 3,
        'tv2-charlie': 4,
        'tv2-news': 5,
        'kanal-5': 6,
        'tv3-plus': 7,
        'tv2-zulu': 8,
        'dr-ramasjang': 9,
        'kanal-4': 10,
        'tv2-sport': 11,
        'tv2-sport-x': 12,
        'tv3-sport': 13,
        'tv3-puls': 14,
        '6eren': 15,
        'disney-channel': 16,
        'tv2-fri': 17,
        'canal-9': 18,
        'discovery-channel': 19,
        'tlc': 20,
        'nickelodeon': 21,
        'national-geographic-channel': 22,
        'tv3-max': 23,
        'cartoon': 24,
        'disney-junior': 25,
        'dk4': 26,
        'mtv': 27,
        'animal-planet': 28,
        'investigation-discovery': 29,
        'vh1': 30,
        'eurosport-2': 31,
        'boomerang': 32,
    }
    
    program_dict = {}

    allChannelsChosen = False

    if channels[0] == 'all':
        allChannelsChosen = True

    if not allChannelsChosen:
        for channel in channels:
            channel = channel.lower()

            # Check if channel is in channel_indix dict, if not add channel as key
            if channel not in program_dict.keys():
                program_dict.update({channel: []})

            # Get index from dict
            index = channel_index[channel]
            # Add all program in channel to program_dict
            program_dict[channel].append(channel_list[index].find_all('a', class_='tv2epg-program-link'))
    else:
        for channel in channel_index.keys():
            # Check if channel is in channel_indix dict, if not add channel as key
            if channel not in program_dict.keys():
                program_dict.update({channel: []})

            # Get index from dict
            index = channel_index[channel]
            # Add all program in channel to program_dict
            program_dict[channel].append(channel_list[index].find_all('a', class_='tv2epg-program-link'))
    
    return program_dict


def print_all_programs(program_dict: list):
    """Print all the programs in the provided dict"""
    for channel in program_dict.keys():
        print(f'\n{channel.upper().replace("-", " ")}')
        for program in program_dict[channel]:
            for prog in program:
                timeStart = prog.time.text
                progsTitle = prog.strong.text
                print(f"{timeStart} > {progsTitle}")


def print_time_program(program_dict: dict, timeStart: str):
    """Find and print the program at the specified time on the channels defined in program_dict"""
    # Contains the program(s) that start at the specified time
    progsTime = {}

    # Contains the program after the program(s) that is stored in progsTime, to later get when the program(s) ends
    progsAfter = {}

    # Check if channel is in progsTime dict, if not add channel as key
    for channel in program_dict.keys():
        if channel not in progsTime.keys():
            progsTime.update({channel: []})
    
    # Check if channel is in progsAfter dict, if not add channel as key
    for channel in program_dict.keys():
        if channel not in progsAfter.keys():
            progsAfter.update({channel: []})


    for channel in program_dict.keys():
        for program in program_dict[channel]:
            for index, prog in enumerate(program):
                # Append only the programs that start at the specified time to progsTime
                if prog.time.text == timeStart:
                    progsTime[channel].append(prog)
                    progsAfter[channel].append(program[index+1])


    for channel in progsTime.keys():
        if len(progsTime[channel]) > 0:
            timeEnd = progsAfter[channel][0].time.text
            progsTitle = progsTime[channel][0].strong.text
            print(f'{channel.upper().replace("-", " ")}')
            print(f'{timeStart} - {timeEnd} > {progsTitle}\n')
        else:
            print(f'{channel.upper().replace("-", " ")}')
            print(f'There is no programs that start at this time: {timeStart}\n')


def main(args):
    if args.channel == None:
        print('You haven\'t chosen one or more channels')
        return

    channel_list = get_channels()
    program_dict = get_programs(channel_list, args.channel)
    if args.time:
        print_time_program(program_dict, args.time)
    if args.all:
        print_all_programs(program_dict)



if __name__ == "__main__":
    args = argparse_setup()
    try:
        main(args)
    except KeyError:
        print(f'Check channel name or this scraper can\'t use one of the chosen channels')
