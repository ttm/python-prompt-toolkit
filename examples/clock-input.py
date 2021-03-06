#!/usr/bin/env python
"""
Example of a 'dynamic' prompt. On that shows the current time in the prompt.
"""
from prompt_toolkit import CommandLineInterface
from prompt_toolkit.layout import Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.processors import Processor
from prompt_toolkit.layout.utils import token_list_len
from pygments.token import Token

import datetime
import time


class ClockPrompt(Processor):
    def run(self, cli, buffer, tokens):
        now = datetime.datetime.now()
        before = [
            (Token.Prompt, '%s:%s:%s' % (now.hour, now.minute, now.second)),
            (Token.Prompt, ' Enter something: ')
        ]

        return before + tokens, lambda i: i + token_list_len(before)

    def invalidation_hash(self, cli, buffer):
        return datetime.datetime.now()


def main():
    cli = CommandLineInterface(layout=Window(BufferControl(input_processors=[ClockPrompt()])))

    def on_read_start():
        """
        This function is called when we start reading at the input.
        (Actually the start of the read-input event loop.)
        """
        # Following function should be run in the background.
        # We do it by using an executor thread from the `CommandLineInterface`
        # instance.
        def run():
            # Send every second a redraw request.
            while cli.is_reading_input:
                time.sleep(1)
                cli.request_redraw()

        cli.run_in_executor(run)
    cli.onReadInputStart += on_read_start

    code_obj = cli.read_input()
    print('You said: %s' % code_obj.text)


if __name__ == '__main__':
    main()
