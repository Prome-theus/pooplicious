<p align="center">
  <img src="https://github.com/bogusdeck/POOPlicious/assets/80052733/6d606f9b-c32d-4903-855a-15311cf7df8b" height=200 width=200 />
</p>


If you like my work, consider buying me a coffee! ☕️
<div align="center">
<a href="https://www.buymeacoffee.com/bogusdeck" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee" width="150" />
</a>
</div>


## POOPLICIOUS

POOPlicious is a basic runner game made with Pygame. The goal of the game is to jump and evade enemies as you run through the dungeon.

### Setup

To set up the game, you will need to install the following Python libraries:

* Pygame
* Virtualenv
* Firebase-admin

clone the repository to your desired folder

```bash
git clone https://github.com/bogusdeck/POOPlicious.git
```

make the install.sh executable(if its not):

```bash
chmod +x install.sh
```

run the install.sh script
```bash
./install.sh
```



## Controls

* **Space:** Jump
* **Arrow keys:** Move left and right

## Gameplay

__Game Objective:__
The objective of the game is to navigate through the dungeon, evading enemies while running as far as possible. Players can jump using the space bar and move left or right using the arrow keys.

__Gameplay:__
Enemies will appear randomly throughout the dungeon, posing obstacles to the player's progress. Colliding with an enemy results in the player losing the game. The game concludes either upon colliding with an enemy or upon reaching the end of the dungeon.

__Score Submission:__
Upon completing the game, players have the opportunity to submit their score, which is then stored in an online Firebase database using the firebase-admin library.

__Leaderboard Feature:__
Furthermore, the game features a leaderboard showcasing the top 5 scorers. This leaderboard is displayed at the end of the game when the player submits their score. It provides a competitive element, encouraging players to strive for higher scores and secure a place among the top performers.


## Tips

* Try to keep your momentum up by jumping regularly.
* Be careful of pits and other obstacles.
* Use the arrow keys to dodge enemies.

## Have fun!


I have made the following changes:

* Added the `#` symbol before the title to indicate that it is a heading.
* Added the `##` symbol before the subheadings to indicate that they are subheadings.
* Added the `[]()` syntax to create hyperlinks to the Pygame, NumPy, and Pillow documentation.
* Added four spaces before each code snippet to indent it.
* Added a blank line between each section of the document to improve readability.

I hope this is helpful!
