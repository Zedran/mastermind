# Mastermind

## Introduction

This is the implementation of the Mastermind game written in Python. It is one of my early programming projects. The code is not top quality (I work on it in my spare time), but it works decently and the game is fun to play, therefore I have decided to upload it to Github and make the repository public.

Mastermind is a two-player game in which one person sets the secret code and the other tries to figure it out. In my version of the game, the AI sets the code randomly and the player attempts to break it.

## Features

* Customizable theme
* Languages:
    * en - English
    * pl - Polish
    * ru - Russian

## Running the game

The game requires a non-ancient Python interpreter fitted with pygame library. You can use the `MM.bat` file in the main directory or run the `Mastermind.pyw` directly.

## Modifying the game

At present, there is no in-game way to change language, theme or resolution. You have to edit the proper variables in json files within `/res/settings` using your favorite text editor.

### Config

Two important options in `config.json` are `lang` and `res`. The first one determines the language of the game. Its value is a two-letter name of the dictionary contained in `langs.json`. The second one holds the window resolution in pixels - [width, height]. 

You can also adjust `fps` (frames per second) value. Keep in mind that low fps will make the interface laggy. `repetitions` is a placeholder, changing its value will have no effect on the game.

### Language

You can add your own language to `langs.json`. Just copy one of the dictionaries, paste it anywhere within outer brackets and replace the values with your own. Make sure to name your language dictionary uniquely.

### Theme

Theme information is stored within `theme.json`. It holds a dictionary of HTML color codes. The proper description of this file will be created on a later date.

## Rules

* The code consists of 4 elements with no repetitions
* There are 8 different elements to chose from. They all have a unique color and are numbered for convenience
* Once the code is set, *the guesser* attempts to break the code
* Each time *the guesser* submits the code, *the setter* evaluates it with feedback flags - one per code element. Their order does not match that of the code. There are three kinds of feedback responses:
    * Red flag indicates that one of the elements is of a correct kind and in a proper place within a code sequence
    * White flag indicates that one of the elements is of a correct kind but in an incorrect place
    * Empty feedback field means that one of the elements does not exist in the code
* The game is over once *the guesser* breaks the code or fails to do so in 12 attempts.

## Resources

* [Pygame](https://www.pygame.org/)

## License

This software is available under MIT license.
