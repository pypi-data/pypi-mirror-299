from threading import Thread
from typing import Generator, Callable, Any
from time import sleep, time
from sys import stdout

from .colors import Color, Fade
from .pattern import Pattern
from .system import sys, System
from .ansi import CLEAR, RESET, TITLE


__all__ = [
    'FadeAnimation', 'PatternAnimation', 'ProgressBar',
    'TitleFadeInAnimation', 'AnimConcactner', 'smooth_show'
]



class AnimationBase:

    def getframes(self) -> Generator[str, None, None]:
        ...


    def animate(self,
                duration: float | None = None,
                interval: float = 0.05,
                callback: Callable[[str], Any] | None = None,
                system: System = sys) -> None:
        """
        Animate the animation.

        ### arguments
         - `duration?`: The duration of the animations in seconds.
         - `interval?`: The interval between each frame of the animation in seconds.
         - `system?`: The ZXFade system that the animation will be rattached to.
        """
        passed = False
        cursor = system.cursor
        system.cursor = False

        def wait():
            nonlocal passed
            if duration:
                sleep(float(duration))
            else:
                input()
            passed = True

        Thread(target=wait).start()

        gen = self.getframes()

        while not passed:
            try:
                frame = next(gen)
            except:
                break

            towrite = CLEAR + frame
            system.writefunc(towrite)
            sleep(interval)

        gen.close()
        sys.clear()
        system.cursor = cursor


    __call__ = animate



class FadeAnimation(AnimationBase):
    banner: str
    """The text to be animated."""
    fade: Fade
    """The fade that move over the text"""

    __slots__ = ('banner', 'fade')

    def __init__(self,
                 banner: str,
                 fade: Fade) -> None:
        """
        Create an animation of a fade mooving on a text.

        ### arguments
         - `banner`: The text to be animated.
         - `fade`: The fade that move over the text
        """
        self.banner = banner
        self.fade = fade


    def getframes(self):
        decal = 0
        while True:
            colored = self.fade.colorate(self.banner, decal)
            yield colored
            decal += 1


class PatternAnimation(AnimationBase):
    banner: str
    """The text to be animated."""
    pattern: Pattern
    """The pattern that animate"""

    __slots__ = ('banner', 'pattern')

    def __init__(self,
                 banner: str,
                 pattern: Pattern) -> None:
        """
        Create an animation of a pattern with the fades mooving on a text.

        ### arguments
         - `banner`: The text to be animated.
         - `pattern`: The pattern that animate
        """
        self.banner = banner
        self.pattern = pattern


    def getframes(self):
        decal = 0
        while True:
            colored = self.pattern.colorate(self.banner, decal)
            yield colored
            decal += 1


class ProgressBar:
    name: str
    """The name of the progress bar"""
    steps: int
    """The number of steps the progress bar can reach"""
    color: Color | Fade
    """The color or fade the progress bar will have on it reached part"""
    length: int
    """The length of the progress bar"""
    step: int
    """The current step where the progress bar is"""
    step_comment: str | None
    """The text that is displayed next to the bar to show a comment"""

    __slots__ = ('name', 'steps', 'color',
                 'length', 'step', 'step_comment')

    def __init__(self,
                 name: str,
                 steps: int,
                 color: Fade,
                 length: int = 20) -> None:
        """
        Create a progress bar that can increment and show comments.

        ### arguments
         - `name`: The name of the progress bar.
         - `steps`: The number of steps the progress bar can reach.
         - `color`: The color or fade the progress bar will have on it reached part.
         - `length?`: The length of the progress bar.
        """
        self.name = name
        self.steps = steps
        self.color = color
        self.length = length
        self.step = 0
        self.step_comment = None


    def increment(self,
                  steps: int = 1,
                  comment: str | None = None) -> None:
        """
        Increment the progress.

        ### arguments
         - `steps?`: The number of steps to increment
         - `comment?`: An optional comment to show next to the bar
        """
        self.step += steps
        self.step_comment = comment


    def show(self,
             interval: float = 0.05,
             lpadding: int = 0) -> None:
        """
        Show the progress bar.

        ### arguments
         - `interval?`: The interval between each reload of the progress bar in seconds.
         - `lpadding?`: The left padding margin of the progress bar.
        """
        cursor = sys.cursor
        sys.cursor = False

        def _show():
            if isfade := isinstance(self.color, Fade):
                colcount = len(self.color.getcolors()) * 2
                decal = colcount

            while True:
                progress = self.step / self.steps
                bar_length = int(self.length * progress)

                reached = '█' * bar_length
                if isfade:
                    colored_reached = self.color.colorate(reached, decal) + RESET
                    decal -= 1
                    if decal <= 0:
                        decal = colcount
                else:
                    colored_reached = self.color + reached

                rest = Color(25, 25, 25) + ('█' * (self.length - bar_length))
                comment = self.step_comment or ''
                stats = Color(100, 100, 100) + f'{self.step}/{self.steps}'
                bar = self.name + ' ' + colored_reached + rest + ' ' + stats + ' ' +  comment

                stdout.write('\r' + (' ' * lpadding) + bar + RESET)

                if self.step >= self.steps:
                    break
                sleep(interval)

            sys.cursor = cursor
            stdout.write(RESET)

        Thread(target=_show).start()


    __call__ = show


class TitleFadeInAnimation(AnimationBase):
    title: str
    """The title you want to show"""

    def __init__(self, title: str) -> None:
        self.title = title

    def getframes(self):
        i = 0
        for i in range(len(self.title) + 1):
            yield TITLE.format(self.title[:i])



class AnimConcactner(AnimationBase):
    things: list[tuple[AnimationBase | str, float]]

    def __init__(self) -> None:
        self.things = []


    def add(self,
            thing: AnimationBase | str,
            duration: float) -> None:
        self.things.append((thing, duration))


    def getframes(self):
        for thing, dur in self.things:
            if isinstance(thing, AnimationBase):
                gen = thing.getframes()
            start_time = time()

            while time() - start_time < dur:
                if isinstance(thing, AnimationBase):
                    frame = next(gen, None)
                else:
                    frame = thing

                if frame:
                    yield frame



def smooth_show(wait: bool = False,
                interval: float = 0.005,
                transparency: int = 255) -> None:
    """
    Show the terminal smoothly with its transparency.

    ### arguments
     - `wait?`: If the fonction should wait the terminal to have  the given final opacity.
     - `interval?`: The interval between each transparency update in seconds.
     - `transparency?`: The final transparency
    """
    def show():
        for i in range(transparency + 1):
            sys.transparency = i
            sleep(interval)

    if wait:
        show()
    else:
        Thread(target=show).start()