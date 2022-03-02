import os
import sys
import time
from telethon.sync import TelegramClient
from telethon import functions, types


def print_help() -> None:
    print('Usage:')
    print('\tpython main.py <api_id> <api_hash>')


def get_dirty_channels() -> list:
    with open(os.path.join(os.path.dirname(os.path.relpath(__file__)), 'dirty_channels.txt'), 'r') as fp:
        dirty_channels = fp.readlines()

    return dirty_channels


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_help()
        exit(1)

    api_id = int(sys.argv[1])
    api_hash = sys.argv[2]

    dirty_channels = get_dirty_channels()

    with TelegramClient('ReportDirtyChannels', api_id, api_hash) as client:
        for dirty_channel in dirty_channels:
            dirty_channel = dirty_channel.strip()
            try:
                result = client(functions.account.ReportPeerRequest(
                    peer=client.get_entity(dirty_channel),
                    reason=types.InputReportReasonOther(),
                    message='The channel undermines the integrity of the Ukrainian state. Spreading fake news, misleading people and oman. Block it ASAP'
                ))
                print('{}: {}'.format(dirty_channel, result))
                time.sleep(0.3)
            except Exception as e:
                print('{}: error'.format(dirty_channel))
