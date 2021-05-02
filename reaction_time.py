#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from time import sleep
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QStackedLayout
import pandas as pd
import random

CONFIG_FILE_PATH = "order_config.csv"

# 10 random colors to cycle through
random_colors = ["red", "blue", "green", "yellow", "gray", "brown", "orange", "purple", "magenta", "beige"]


def get_trial_order(participant_id: int) -> list[str]:
    # order_df = pd.read_csv(CONFIG_FILE_PATH, sep=",")
    # # get the correct trial order for the given participant id
    # order_entry: pd.Series = order_df[order_df['participant_id'] == participant_id]['trial_order'].str.strip()
    # trial_order: str = list(order_entry)[0]
    # # split the trial order string into separate list entries: ['A B B A'] -> ['A', 'B', 'B', 'A']
    # return trial_order.split()

    # TODO only pseudo-randomized but balanced latin square won't work here -> find a better way to randomize?
    conditions = ["A", "B"]
    repetitions = 10
    trials = list(repetitions * conditions)
    random.shuffle(trials)
    return trials


def get_random_time() -> int:
    """
    Generates a random number between 1 and 6 (inclusive) representing the number of seconds until the stimulus
    is shown. Used to randomize the time until the background color changes.
    @return: integer between 1 and 6
    """
    return random.randint(1, 6)


def get_random_color() -> str:
    """
    Returns a random color from the 'random_colors' - array. Used to show different background colors.
    @return: color as a string
    """
    return random.choice(random_colors)


class ReactionTimeStudy(QtWidgets.QWidget):
    __TASKS = {
        "A": "Klicke die Leertaste so schnell wie möglich, sobald sich der weiße Hintergrund des Bildschirms ändert.",
        "B": "Klicke die Leertaste so schnell wie möglich, wenn sich der Bildschirm-Hintergrund blau verfärbt."
    }

    __MAX_TRIALS = 20
    __COUNTDOWN_DURATION = 3  # seconds  # TODO reset to 10 seconds after testing!
    __PAUSE_DURATION = 60  # one minute pause

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("reaction_time.ui", self)
        self._setup_pages()

        self._current_trial = 0

        self.ui.setFixedSize(650, 400)  # set initial window size
        self.setFocusPolicy(QtCore.Qt.StrongFocus)  # necessary to capture click events!

        try:
            # get the passed command line arguments
            self._participant_id = int(sys.argv[1])
            self._current_trial_order = get_trial_order(self._participant_id)

            self.ui.start_study_btn.clicked.connect(self._go_to_next_page)
            self.ui.start_study_btn.setFocusPolicy(QtCore.Qt.NoFocus)  # prevent auto-focus of the start button
        except ValueError as e:
            print(f"The first command line parameter must be the participant id as an integer!\n{e}")

    def _setup_pages(self):
        # create a stacked layout and add all sub-pages
        self.stackedLayout = QStackedLayout()
        self.firstPage = self.ui.intro
        self.secondPage = self.ui.study
        self.thirdPage = self.ui.questionnaire
        self.stackedLayout.addWidget(self.firstPage)
        self.stackedLayout.addWidget(self.secondPage)
        self.stackedLayout.addWidget(self.thirdPage)

    def _go_to_next_page(self):
        # switch widget index to the next element in the stack (i.e. move to the next page)
        self.stackedLayout.setCurrentIndex(self.stackedLayout.currentIndex() + 1)

        if self.stackedLayout.currentWidget() is self.secondPage:
            self._setup_study()
        elif self.stackedLayout.currentWidget() is self.thirdPage:
            self._setup_questionnaire()

    def _setup_study(self):
        self.ui.setFixedSize(650, 400)
        self.timer = QtCore.QTimer(self)  # init a qt Timer to show a countdown before every trial
        self.time_remaining = ReactionTimeStudy.__COUNTDOWN_DURATION

        self._update_ui()
        self._start_task()

    def _update_ui(self):
        current_condition = self._get_current_condition()
        current_task = ReactionTimeStudy.__TASKS[current_condition]
        self.ui.task_description.setText(current_task)
        self.ui.trial_number.setText(str(self._current_trial))

    def _start_task(self):
        self.ui.countdown_label.show()
        self.ui.countdown_num.show()
        self._show_remaining_time()

        # start countdown
        self.timer.timeout.connect(self._on_countdown)
        self.timer.start(1000)  # every second

    def _on_countdown(self):
        self.time_remaining -= 1

        if self.time_remaining == 0:
            # reset counters
            self.time_remaining = ReactionTimeStudy.__COUNTDOWN_DURATION
            self.ui.countdown_label.hide()
            self.ui.countdown_num.hide()

            # disconnect this from the timer so it isn't called infinitely
            self.timer.timeout.disconnect(self._on_countdown)

            # TODO log start after countdown finished

            # start current trial
            condition = self._get_current_condition()
            self._init_condition_A()
            # if condition == "A":
            #     self._init_condition_A()
            # else:
            #     self._init_condition_B()
        else:
            self._show_remaining_time()

    def _show_remaining_time(self):
        # update the countdown ui
        self.ui.countdown_num.setStyleSheet("QLabel { font-weight: bold; color : red;}")
        self.ui.countdown_num.setText(str(self.time_remaining))

    def _get_current_condition(self) -> str:
        return self._current_trial_order[self._current_trial]

    def _init_condition_A(self):
        timeout = get_random_time()
        sleep(timeout)  # wait until changing the background color for a random time to make it less predictable
        self.setStyleSheet("background-color: orange;")  # change window background color

    def _init_condition_B(self):
        # TODO stop this loop if space pressed!
        while True:
            sleep(1)
            color = get_random_color()
            self.setStyleSheet(f"background-color: {color};")
            if color == "blue":
                break

    # TODO log too early clicks and time needed
    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            if not self.stackedLayout.currentWidget() is self.secondPage:
                # if key pressed on the wrong page, do nothing
                return

            self.setStyleSheet(f"background-color: white;")  # reset the window background color
            self._current_trial += 1
            # check after ech trial if halfway there (after 10th trial) and if yes, make a short pause
            if self._current_trial == ReactionTimeStudy.__MAX_TRIALS/2 + 1:
                self.ui.task_description.setText("Du hast die Hälfte geschafft! Ruhe dich kurz aus,"
                                                 "in einer Minute geht es weiter!")
                sleep(ReactionTimeStudy.__PAUSE_DURATION)
            elif self._current_trial == 21:
                # show questionnaire after 20 trials
                self._go_to_next_page()
                return

            sleep(1)
            self._update_ui()
            self._start_task()
            # self.update()  # this triggers an async repaint of the widget (paintEvent() is called)

        # elif ev.text() == "h":
        #     print("Hallo welt")
        #     # TODO anderer key als space?

    def _setup_questionnaire(self):
        self.ui.setFixedSize(650, 720)
        self.ui.finish_study_btn.clicked.connect(self._save_answers)

    def _save_answers(self):
        # TODO connect to ui elements and log answers to file
        #  -> validate before? or just allow all of them to be optional
        self.close()


def main():
    if len(sys.argv) > 1:
        app = QtWidgets.QApplication(sys.argv)
        study = ReactionTimeStudy()
        study.show()
        sys.exit(app.exec_())
    else:
        raise IOError("Failed to setup study because no arguments were given!")


if __name__ == '__main__':
    main()
