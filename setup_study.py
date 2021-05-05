#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


def main():
    participant_id = 1

    while True:
        os.system(f'python3 reaction_time.py {participant_id}')
        participant_id = participant_id + 1
        # break


if __name__ == '__main__':
    main()
