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
        help='the time the program starts. E.g. "20:00"',
        type=str
    )
    
    parser.add_argument(
        '-a',
        '--all',
        help='show all programs for the chosen channel',
        action='store_true'
    )
    
    return parser.parse_args()


def get_soup(URL='https://tvtid.tv2.dk/'):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
    cookies = dict(cookies_are='working')
    response = requests.get(URL, headers=headers, cookies=cookies)
    return BeautifulSoup(response.text, 'html.parser')


def get_channels(soup) -> list:
    """Find all channels with programs, and return the list"""
    channels = soup.find_all('article', class_='tv2epg-channel')
    return channels


def get_programs(channel_list: list, channels: list) -> dict:
    """Find the programs for the specified channels and return a dict with them where the channels are the keys"""
    channel_index = {
        'dr1': 0,
        'tv2': 1,
        'tv3': 2
    }
    
    program_dict = {}

    for channel in channels:
        channel = channel.lower()

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
        print(f'\n{channel.upper()}')
        for program in program_dict[channel]:
            for prog in program:
                print(f"{prog.time.text} > {prog.strong.text}")


def print_time_program(program_dict: dict, time: str):
    """Find and print the program at the specified time on the channels defined in program_dict"""
    progsTime = {}

    # Check if channel is in channel_indix dict, if not add channel as key
    for channel in program_dict.keys():
        if channel not in progsTime.keys():
            progsTime.update({channel: []})

    for channel in program_dict.keys():
        for program in program_dict[channel]:
            for prog in program:
                # Append only the programs that start at the specified time
                if prog.time.text == time:
                    progsTime[channel].append(prog)


    for channel in progsTime.keys():
        print(f'{channel.upper()}')
        if len(progsTime[channel]) != 0:
            print(f'{time} > {progsTime[channel][0].strong.text}\n')
        else:
            print(f'There is no programs that start at this time: {time}\n')


def main(args):
    if args.channel == None:
        print('You haven\'t chosen one or more channels')
        return

    soup = get_soup()
    channel_list = get_channels(soup)
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
