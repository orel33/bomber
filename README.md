# Bomber Man #

This is a simple "Bomber Man" game written in Python 2/3, based on the *pygame* library.

![Bomber Man Snapshot](bomberman.png?raw=true "snapshot")


## Download & Install ##

First clone the project available on GitHUB under GPL:

```
  $ git clone https://github.com/orel33/bomber
```

To install Python (root privilege required):

```
  $ sudo apt get install python pip      # for python 2
  $ sudo apt get install python3 pip3    # for python 3
```

To install the *pygame* library (user privilege enough):

```
  $ pip install pygame                   # for python 2
  $ pip3 install pygame                  # for python 3
```

To start the game:

```
  $ python2 bomberman.py                      # for python 2
  $ python3 bomberman.py                      # for python 3
```

By default, the map "maps/map0" is used, but you can generate you own map (*mymap*) and use it as follows:

```
  $ python3 bomberman.py maps/mymap
```

## Rules ##

This game is similar to a classic "Bomber Man". This is a *standalone* version of the game for a single player. Each character starts the game with an initial amount of 50 health points. Each fruit brings the character with 10 extra health points, while each bomb blast removes 10 health points. A character is dead when its health points reach zero. A character gets immunity for a while after he's hit by a bomb blast. After a character drops a bomb, he is disarmed for a while.

To play, just use the following keys:
  * use *arrows* to move the current character
  * press *space* to drop a bomb, that will explode after a delay of 5 seconds
  * press *escape* to quit the game
  * press *tab* to change the current character (circular swap)
  * press *k* to kill the current character

## Known Bugs ##

The game uses 100% of CPU on some *pygame* version :-(

## Documentation ##

  * https://www.pygame.org
  * https://openclassrooms.com/courses/interface-graphique-pygame-pour-python/tp-dk-labyrinthe
