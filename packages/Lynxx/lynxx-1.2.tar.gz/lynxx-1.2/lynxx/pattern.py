from .ansi import RESET
from .colors import Color, Fade
from .typess import *



__all__ = ['Pattern']



class Pattern:
    pattern: dict[str, Color | Fade]
    """A dictionary mapping characters to Color or Fade"""

    __slots__ = ('pattern',)

    def __init__(self, pattern: dict[str, Color | Fade]) -> None:
        """
        Initialize a Pattern with the specified pattern.

        ### arguments:
         - pattern: A dictionary mapping characters to Color or Fade.
        """
        self.pattern = pattern


    def __add__(self, text: AnyStringT) -> AnyStringT:
        return self.colorate(text) + RESET


    def colorate(self,
                 text: AnyStringT,
                 decal: int = 0) -> AnyStringT:
        """
        Apply the pattern to a text.

        ### arguments:
         - text: The text to which the pattern will be applied.
         - decal: The starting offset for the pattern fades.

        ### returns:
            The input text string with the pattern applied.
        """
        colored_text = ''
        fadestates: dict[str, int] = {}

        for match in self.pattern.keys():
            for c in match:
                fadestates[c] = decal

        for char in text:
            color = None
            for match, ccolor in self.pattern.items():
                if char in match:
                    color = ccolor
                    break

            if not color:
                colored_text += RESET + char

            else:
                if isinstance(color, Color):
                    colored_text += color.colorate(char)

                elif isinstance(color, Fade):
                    colindex = fadestates[char]
                    fadecolors = color.getcolors()
                    fadecolors += list(reversed(fadecolors))

                    charcol = fadecolors[colindex % len(fadecolors)]
                    colored_text += charcol.colorate(char)

            for match, color in self.pattern.items():
                passed = ''
                if isinstance(color, Fade):
                    for c in match:
                        if c in passed:
                            continue

                        passed += c

                        if color.direction == 'horizontal':
                            if char == '\n':
                                fadestates[c] = decal
                            else:
                                fadestates[c] += 1

                        elif color.direction == 'vertical':
                            if char == '\n':
                                fadestates[c] += 1

        return colored_text