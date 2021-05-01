#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from time import sleep
from PyQt5 import QtWidgets, QtCore, uic
import pandas as pd
import random

CONFIG_FILE_PATH = "order_config.csv"

# colors for making one word blue,
# see https://stackoverflow.com/questions/52946332/how-to-print-specific-words-in-colour-on-python
blue = "\033[34m"
black = "\033[39m"

# random colors to cycle through
random_colors = ["red", "blue", "green", "yellow", "gray", "brown", "orange", "purple"]


def get_trial_order(participant_id: int) -> list[str]:
    order_df = pd.read_csv(CONFIG_FILE_PATH, sep=",")
    # get the correct trial order for the given participant id
    order_entry: pd.Series = order_df[order_df['participant_id'] == participant_id]['trial_order'].str.strip()
    trial_order: str = list(order_entry)[0]
    # split the trial order string into separate list entries: ['A B B A'] -> ['A', 'B', 'B', 'A']
    return trial_order.split()


def get_random_time() -> int:
    """
    Generates a random number between 1 and 10 (inclusive) representing the number of seconds until the stimulus
    is shown. Used to randomize the time until the background color changes.
    @return: integer between 1 and 10
    """
    return random.randint(1, 10)


def get_random_color():
    """
    Gets a random color from the 'random_colors' - array. Used to show different background colors.
    @return: color as a string
    """
    return random.choice(random_colors)


class ReactionTimeIntro(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("reaction_time_intro.ui", self)

        try:
            # get the passed command line arguments
            self._participant_id = int(sys.argv[1])
            self._current_trial_order = get_trial_order(self._participant_id)

            self._study = ReactionTimeStudy(self._participant_id, self._current_trial_order)
            self.ui.start_study_btn.clicked.connect(self._start_study)
        except ValueError as e:
            print(f"The first parameter must be the participant id as an integer!\n{e}")

    def _start_study(self):
        # hide this window and show the actual study ui
        self.hide()
        self._study.show()


class ReactionTimeQuestionnaire(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("post_questionnaire.ui", self)
        self.ui.finish_study_btn.clicked.connect(self._save_answers)

    def _save_answers(self):
        # TODO connect to ui elements and log answers to file
        #  -> validate before? or just allow all of them to be optional
        self.close()


class ReactionTimeStudy(QtWidgets.QWidget):
    __TASKS = {
        "A": "Klicke die Leertaste so schnell wie möglich, sobald sich die Farbe des Bildschirms ändert.",
        "B": f"Klicke die Leertaste so schnell wie möglich, wenn sich der Bildschirm {blue}blau{black} verfärbt."
    }

    __MAX_TRIALS = 20
    __COUNTDOWN_DURATION = 10  # seconds  # TODO is 10 too long ?
    __PAUSE_DURATION = 60  # one minute pause

    def __init__(self, participant_id, trial_order):
        super().__init__()
        self._participant_id = participant_id
        self._trial_order = trial_order
        self._current_trial = 0

        self.ui = uic.loadUi("reaction_time_study.ui", self)

        self._init_ui()
        self._start_task()

    def _init_ui(self):
        self._update_ui()
        # widget should accept focus by click and tab key
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def _update_ui(self):
        current_task = ReactionTimeStudy.__TASKS[self._trial_order[self._current_trial]]
        self.ui.task_description = current_task
        self.ui.trial_number = self._current_trial

    def _start_task(self):
        self._display_countdown()
        # TODO log start after countdown finished
        condition = self._trial_order[self._current_trial]
        if condition == "A":
            self._init_condition_A()
        else:
            self._init_condition_B()

    def _display_countdown(self):
        # see https://stackoverflow.com/questions/17220128/display-a-countdown-for-the-python-sleep-function
        for time_remaining in range(ReactionTimeStudy.__COUNTDOWN_DURATION, 0, -1):
            self.ui.countdown_num = time_remaining
            # sys.stdout.write("\r")
            # sys.stdout.write("{:2d} seconds remaining.".format(time_remaining))
            # sys.stdout.flush()
            sleep(1)  # countdown every second

    def _init_condition_A(self):
        self.setStyleSheet("background-color: blue;")

    def _init_condition_B(self):
        pass

    # TODO log too early clicks and time needed
    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            self._current_trial += 1
            # check after ech trial if halfway there (after 10th trial) and if yes, make a short pause
            if self._current_trial == ReactionTimeStudy.__MAX_TRIALS/2 + 1:
                sleep(ReactionTimeStudy.__PAUSE_DURATION)

            sleep(1)
            self._update_ui()
            self._start_task()
            # self.update()  # this triggers an async repaint of the widget (paintEvent() is called)


def main():
    if len(sys.argv) > 1:
        app = QtWidgets.QApplication(sys.argv)
        intro = ReactionTimeIntro()
        intro.show()
        sys.exit(app.exec_())
    else:
        raise IOError("Failed to setup study because no arguments were given!")


if __name__ == '__main__':
    main()
