import random
import config
import tweepy
import csv
import traceback
import time
import re

def login():
    # takes all keys from config.py
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_token_secret = config.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

def new_output():

    # gets a random number in the range of rows in the csv file
    def get_random():
        return random.randint(1,206197)

    # gets unique numbers for rows from csv
    def get_nums():
        lines_list = []

        num1 = get_random()
        num2 = get_random()

        if num1 != num2:
            lines_list.append(num1)
            lines_list.append(num2)

            return lines_list
        else:
            lines_list = get_nums()

    # returns just the two rows that i put in the list w/o loading the whole csv into memory
    def read_my_lines(csv_reader, line_list):
        for line_number, row in enumerate(csv_reader):
            if line_number in line_list:
                yield line_number, row



    f = open("new_data.csv")
    r = csv.reader(f)
    L = get_nums()

    # makes a list with just the data from the two rows i asked for
    choices = [line for line_number, line in read_my_lines(r, L)]

    category = choices[0][0]
    value = choices[0][1]
    prompt = choices[0][2]
    answer = choices[1][3]

    # string together result
    result = "I'll take " + category + " for " + value + "." + "\n" + prompt + "..." + "\n" + "What is " + answer + "?" + "\n" + "We were looking for " + choices[0][3]

    return result + "\n #jeopardy #bot"

def send_tweet(debug):
    # log me in!
    api = login()
    try:
        # make an output and tweet it
        output = new_output()
        if debug:
            print(output)
        else:
            api.update_status(status=output)
            print(output)
    except:
        # if there's an error, print the error message
        error_msg = traceback.format_exc().split("\n", 1)[1][-130:]
        print(error_msg)

send_tweet(False)
