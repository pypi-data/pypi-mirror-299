# Text Adventure

This library aims to enable you to easily create your own text adventure games!

## Getting started
Simply install the library using `pip` or your package manager:
```shell
pip install textadventure
```

Import the package in your code:
```python
import textadventure
```

And you're good to go!

## Loading and running scenes
The scene language enables you to create your own text adventure games with almost zero code!

To load scenes from a file, use the `load_scenes` method:
```python
import textadventure

textadventure.load_scene("Scenes.txt")
```
You can load scenes from any generic text file.
You can load scenes from as many files as you want, the only thing to remember is that the first scene in the first file you load will become the starting scene.

To run your game using those scenes, call the `start_game` method:
```python
import textadventure

textadventure.load_scene("Scenes.txt")
textadventure.start_game()
```

And that's all the code you will need to run your text adventure games!

## Getting to know Scene
Scene is the mini 'language' I created to remove all the coding from making a text adventure game.
The Scene language is very basic and should be relatively easy to get your head around.

In the Scene language, everything is done using `ACTION`s.
An action is defined by an opening square bracket `[` followed by the action name (which is preferable written in uppercase but this is not required) and ending with a closing square bracket `]` (so it should look like this `[ACTION]`).
All text following an action is treated as a parameter.

The following is a list of all current actions:
- `[SCENE]` - This indicates the beginning of a new scene. The subsequent text until the next action is treated as the name or title of the scene. All subsequent actions are read as a part of the same scene until the next `[SCENE]` action.
- `[TEXT]` - All subsequent text until the next action is printed for the user to see. This is useful for story telling.
- `[GOTO]` - All subsequent text until the next action is read as a scene name. This action ends the current scene and starts another specified scene.
- `[OPTIONS]` - This indicates the start of a list of options from which the user must select one. All subsequent text until the first option action is treated as the option's description (which will be printed for the user to see).
- `[OPTION]` - This indicates a singular option. All subsequent text until the next action will be treated as part of the option. This can **only** follow an `[OPTIONS]` action or another `[OPTION]` action and can **only** be followed by a `[GOTO]` action.
- `[INTERACTION]` - This indicates an interaction must occur from the player. The subsequent two space separated 'words' must be the ASCII key which the user must press followed by the number of seconds the user has to press this key (in that order).
- `[SUCCESS]` - This is a conditional statement indicating the user completed the above interaction action successully. This can **only** follow an `[INTERACTION]` action or a `[FAIL]` action and can **only** be followed by a `[GOTO]` action.
- `[FAIL]` - This is a conditional statement indicating the user did not complete the above interaction action successully. This can **only** follow an `[INTERACTION]` action or a `[SUCCESS]` action and can **only** be followed by a `[GOTO]` action.

More information:
> The Scene language is currently a very basic prototype, it is my intention to make this into a full-fledged custom programming language which can be run using this module or transpiled to C++ and compiled using a tool I will create when the language is much more complete.

## A basic demo
`main.scn`:
```
[SCENE] Generic Scene

[TEXT] Multiline
description!

[OPTIONS] Pick an option:
[OPTION] A
[GOTO] Scene A
[OPTION] B
[GOTO] Scene B
[OPTION] C
[GOTO] Scene C

[SCENE] Interactive Scene

[TEXT]
Quick! Press the space key within two seconds!

[INTERACTION] SPACE 2
[SUCCESS]
[GOTO] Interaction Success
[FAIL]
[GOTO] Interaction Fail

[SCENE] Scene A

[TEXT]
This is Scene A!

[GOTO] Interactive Scene

[SCENE] Scene B

[TEXT]
This is Scene B!

[GOTO] Interactive Scene

[SCENE] Scene C

[TEXT]
This is Scene C!

[GOTO] Interactive Scene

[SCENE] Interaction Success

[TEXT]
You did it!

[GOTO] Final Scene

[SCENE] Interaction Fail

[TEXT]
Oh no! You didn't interact in time...

[GOTO] Final Scene

[SCENE] Final Scene

[TEXT]
That's all for now folks!

[END]
```
<a rel="license" href="http://creativecommons.org/licenses/by-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nd/4.0/">Creative Commons Attribution-NoDerivatives 4.0 International License</a>.
