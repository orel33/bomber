### Bomber Game ###

This is a simple "bomber man" game written in Python 2/3, based on the *pygame* library.

## Download & Install ##

First clone the project available on GitHUB under GPL:

  $ git clone https://github.com/orel33/bomber

To install Python (root privilege required):

  $ sudo apt get install python pip      # python 2
  $ sudo apt get install python3 pip3    # python 3

To install the *pygame* library, without root privilege:

  $ pip install pygame                   # python 2
  $ pip3 install pygame                  # python 3

To start the game:

  $ python2 game.py                      # python 2
  $ python3 game.py                      # python 3

## Rules ##

Règles du jeu :

une sorte de "bomber man"... les bananes rapportent +10 points de vie, les bombes coûtent - 10 points de vie... chaque joueur démarre à 50 points. à zéro point, t'est mort !

* flêches pour se déplacer
* space: poser une bombe
* escape: quitter
* tab : pour changer de joueurs (en version standalone)

## Known Bug ##

The game uses 100% of CPU on some *pygame* version :-(

## Documentation ##

  * https://www.pygame.org
  * https://openclassrooms.com/courses/interface-graphique-pygame-pour-python/tp-dk-labyrinthe
