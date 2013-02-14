import random

TIPS = [
    "Fun fact: if you're using Firefox, you can use the freaking awesome right-click menu features!  Try it by right-clicking a wallpaper tile.",
]

def tips(request):
    return { 'random_tip': random.choice(TIPS) }
