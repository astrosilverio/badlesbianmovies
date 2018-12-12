import random
from itertools import izip

from models import Movie, Tweet
from badmovie.plots import all_plots
from badmovie.sideplots import all_sideplots
from badmovie.names import main_names, setting_names, incongruous_objects, bad_music, titles, descriptions
from badmovie.sexscenes import bad_sex_scenes
from badmovie.dialog import dialog


MINUTE_GAPS = {
    'small': (0,0),
    'medium': (6,11),
    'large': (12,14),
}

SECOND_GAPS = {
    'small': (10, 59),
}

def interleave(*args):
    iters = sum(([iter(arg)]*len(arg) for arg in args), [])
    random.shuffle(iters)
    return map(next, iters)


def generate_single_time(previous_time):
    if previous_time == '00:00':
        gap_length = 'small'
    else:
        gap_length = random.choice(['small', 'medium', 'large'])

    previous_minutes, previous_seconds = previous_time.split(":")
    previous_minutes = int(previous_minutes)
    previous_seconds = int(previous_seconds)

    extra_min = random.randint(MINUTE_GAPS[gap_length][0], MINUTE_GAPS[gap_length][1])
    if gap_length == 'small':
        extra_sec = random.randint(SECOND_GAPS[gap_length][0], SECOND_GAPS[gap_length][1])
    else:
        extra_sec = 0

    new_minutes = previous_minutes + extra_min
    if extra_sec == 0:
        new_seconds = random.choice([0, 30])
    else:
        new_seconds = previous_seconds + extra_sec

    if new_seconds >= 60:
        new_minutes += 1
        new_seconds = new_seconds % 60


    return "{strmin}:{strsec}".format(
        strmin=str(new_minutes).zfill(2),
        strsec=str(new_seconds).zfill(2))


def generate_timestamps(num_times):
    time = "00:00"
    timestamps = []
    for _ in range(num_times):
        time = generate_single_time(time)
        timestamps.append(time)
    return timestamps


def generate_movie():
    """All movies have a plot and a sideplot;
    all movies have two main names, a setting name, an incongruous object, and a bad_music_choice
    all movies have two bad sex scenes
    depending on length, some movies have another bad sex scene or a line of dialog
    """

    main1, main2 = random.sample(main_names, 2)
    setting = random.choice(setting_names)
    incongruous_object = random.choice(incongruous_objects)
    bad_music_choice = random.choice(bad_music)
    all_modifiers = {
        'main1': main1,
        'main2': main2,
        'setting': setting,
        'incongruous_object': incongruous_object,
        'bad_music_choice': bad_music_choice,
    }

    plot_choice = random.choice(all_plots)
    sideplot_choice = random.choice(all_sideplots)
    sex_scenes = random.sample(bad_sex_scenes, 3)
    extra_sex_scene = sex_scenes.pop()
    line_of_dialog = random.choice(dialog)

    if (len(plot_choice) + len(sideplot_choice)) < 10:
        sex_scenes.append(random.choice([extra_sex_scene, line_of_dialog]))

    raw_tweets = interleave(plot_choice, sideplot_choice, sex_scenes)
    text_tweets = [tweet.format(**all_modifiers) for tweet in raw_tweets]
    timestamps = generate_timestamps(len(text_tweets))
    timed_text_tweets = ["\t".join([time, text]) for time, text in izip(timestamps, text_tweets)]

    plot_point_tweets = [Tweet(text) for text in timed_text_tweets]

    title = random.choice(titles)
    description = random.choice(descriptions)
    intro_word = random.choice(['Introducing', 'Presenting'])
    intro_tweet_text = "{intro_word} {title}, {description}".format(intro_word=intro_word, title=title, description=description)
    tweets = [Tweet(intro_tweet_text)]
    tweets.extend(plot_point_tweets)

    return Movie(tweets)
