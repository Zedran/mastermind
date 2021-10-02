# Mastermind

## Introduction

This is the implementation of the Mastermind game written in Python.
Mastermind is a two-player game in which one person sets the secret code and the other tries to figure it out. 
In my version of the game, the AI sets the code randomly and the player attempts to break it.

## Features

* Customizable theme
* Languages:
    * EN - English
    * PL - Polish

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
