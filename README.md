
# Name: SpaceExplorer
![image](https://github.com/TaroBus/SpaceExplorer/assets/118489515/d416fa4b-a995-4d54-abe9-67ab9a806ea5)

# Description:

Welcome to the SpaceExplorer!  In this game,  you control a spaceship and navigate through space while shooting down meteors to earn points.

## Usage

1.  Run the game: "main.py"
2.  Use the arrow keys to control the spaceship:
    -   Press the W key to move up.
    -   Press the S key to move down.
    -   Press the D key to move left.
    -   Press the A key to move right.
3.  Press the space bar to shoot projectiles and destroy meteors.
4.  Your score will increase for each meteor destroyed.
5.  You can only be hit 5 times by the meteors, if you get hit 5 times you blow up!
6.  Survive for the highest score! Afterwards press Enter to restart the game!

## File Structure

The project structure is organized as follows:

-  main.py`: The main entry point of the game.
-   `spaceship.py`: Contains the  `Spaceship, Health, and Projectile`  class -  `Spaceship`: the class dealing with the player-controlled spaceship including rotation around the mouse -  `Health`: the class involving bliting a health bar in the main code depending on the health left -  `Projectile`: the class involving all projectiles spawned by the user
-   `meteor.py`: Contains the  `Meteor`  class representing the meteors that the player needs to destroy.
-   `start.py`: Contains the code for running the start screen and returning the username.
-   `README.md`: This file, providing information about the project.

## Dependencies (Installation)

`pip install pygame`

The following dependencies are required to run the game:

-   Python 3
-   Pygame
-   math
-   random
-   mixer
-   os
-   sys

## Mechanics

-   For the spaceship, the spaceship follows the mouse cursor. The position of the player and position of the mouse (which are vector points) are subtracted, getting the distance between each point. You then can use trigonometry to find the angle, and use the pygame.transform function to show the rotating sprite.
-   For the meteors, all different images of the meteors are put into the Sprite Group (similar to a list)  `meteor_images`  and are chosen randomly. Their speed is also randomized. Then they are blit into the main game from the group.
-   For the projectiles (lasers), they are blit onto the screen at the center of the spaceship and go toward the mouse cursor's position at that time using trig and the ship angle of rotation to go a set speed of 8.

------------


*-J & J*
