import random

from models import Movie, Tweet
from badmovie.plots import instant_love, breakup_cycle, married_lady, closeted_homo, philosophical_discussion, surprise_death
from badmovie.sideplots import family_problems, wacky_mom, exes_get_together, troll_doll, sportsball, straight_friend, bi_friend
from badmovie.names import main_names, setting_names, incongruous_objects, bad_music
from badmovie.sexscenes import bad_sex_scenes
from badmovie.dialog import dialog

all_plots = [instant_love, breakup_cycle, married_lady]
all_sideplots = [family_problems, wacky_mom, exes_get_together, troll_doll, sportsball, straight_friend, bi_friend]


def interleave(*args):
    iters = sum(([iter(arg)]*len(arg) for arg in args), [])
    random.shuffle(iters)
    return map(next, iters)


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
    tweets = [Tweet(text) for text in text_tweets]

    return Movie(tweets)
