#!/usr/bin/env python
"""
Example of a 'dynamic' prompt. On that shows the current time in the prompt.
"""
from prompt_toolkit import CommandLine
from prompt_toolkit.prompt import Prompt
from pygments.token import Token

import datetime
import time


class ClockPrompt(Prompt):
    def get_default_prompt(self):
        now = datetime.datetime.now()
        yield (Token.Prompt, '%s:%s:%s' % (now.hour, now.minute, now.second))
        yield (Token.Prompt, ' Enter something: ')


class ClockCommandLine(CommandLine):
    prompt_factory = ClockPrompt
    enable_concurency = True

    def on_read_input_start(self):
        self.run_in_executor(self._clock_update)

    def _clock_update(self):
        # Send every second a redraw request.
        while self.is_reading_input:
            time.sleep(1)
            self.request_redraw()


def main():
    cli = ClockCommandLine()

    code_obj = cli.read_input()
    print('You said: ' + code_obj.text)


if __name__ == '__main__':
    main()