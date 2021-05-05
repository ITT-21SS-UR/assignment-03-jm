#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import time
import os.path
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import QTimer, QEventLoop
from PyQt5.QtWidgets import QStackedLayout
import pandas as pd
import random
from enum import Enum

CONFIG_FILE_PATH = "order_config.csv"

# random colors to cycle through
random_colors = ["red", "blue", "green", "yellow", "gray", "brown", "orange"]  # "purple", "magenta", "beige"]


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
    @return: the time in milliseconds (between 1000 and 6000)
    """
    return random.randint(1, 6) * 1000


def get_random_color() -> str:
    """
    Returns a random color from the 'random_colors' - array. Used to show different background colors.
    @return: color as a string
    """
    return random.choice(random_colors)


# make the pyqt event loop wait for the given time without freezing everything (as with sleep(...)),
# see https://stackoverflow.com/a/48039398
def _pause_task(pause_duration: int):
    loop = QEventLoop()
    QTimer.singleShot(pause_duration * 1000, loop.quit)
    loop.exec_()


class ReactionTimeStudy(QtWidgets.QWidget):
    __TASKS = {
        "A": "Klicke die Leertaste so schnell wie möglich, sobald sich die Hintergrundfarbe des Bildschirms ändert.",
        "B": "Klicke die Leertaste so schnell wie möglich, wenn sich der Bildschirm-Hintergrund blau verfärbt."
    }

    __TRIAL_COUNT = 4
    __COUNTDOWN_DURATION = 2  # seconds
    __PAUSE_DURATION = 2  # one minute pause
    __STUDY_DATA_CSV_NAME = './reaction_time_log.csv'
    __QUESTIONNAIRE_DATA_CSV_NAME = "./questionnaire_log"
    __press_key_condition_reached = False
    __press_key_condition_reached_timestamp = None

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("reaction_time.ui", self)
        self._setup_pages()
        self._current_trial = 0
        self.ui.setFixedSize(650, 500)  # set initial window size
        self.setFocusPolicy(QtCore.Qt.StrongFocus)  # necessary to capture click events!

        self.StudyStates = Enum('StudyStates', 'StartScreen Trial Pause Questionnaire Done')
        self.__current_status = self.StudyStates.StartScreen

        self.__study_data = self.__init_study_data()
        self.__questionnaire_data = self.__init_questionnaire_data()
        self.__wrong_key_presses = 0
        self.__key_presses_before_condition = 0

        try:
            # get the passed command line arguments
            self._participant_id = int(sys.argv[1])
            self._current_trial_order = get_trial_order(self._participant_id)

            # TODO delete me later:
            self.ui.debug_btn.clicked.connect(self._debug_show_questionnaire)
            self.ui.start_study_btn.clicked.connect(self._go_to_next_page)
            self.ui.start_study_btn.setFocusPolicy(QtCore.Qt.NoFocus)  # prevent auto-focus of the start button
        except ValueError as e:
            print(f"The first command line parameter must be the participant id as an integer!\n{e}")

    def __init_study_data(self):
        # check if the file already exists
        if os.path.isfile(self.__STUDY_DATA_CSV_NAME):
            study_data = pd.read_csv(self.__STUDY_DATA_CSV_NAME)
        else:
            study_data = pd.DataFrame(
                columns=['timestamp', 'participantID', 'condition', 'wrongKeysPressedCount',
                         'conditionNotReachedPressesCount',
                         'reactionTimeInMs'])
        return study_data

    def __init_questionnaire_data(self):
        if os.path.isfile(self.__QUESTIONNAIRE_DATA_CSV_NAME):
            study_data = pd.read_csv(self.__QUESTIONNAIRE_DATA_CSV_NAME)
        else:
            study_data = pd.DataFrame(
                columns=['timestamp', 'participantID', 'age', 'gender', 'occupation', 'usedHand', 'keyboardType',
                         'keyboardUsage', 'hasEyeImpairment', 'eyeImpairment'])
        return study_data

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
            self.__current_status = self.StudyStates.Questionnaire
            self._setup_questionnaire()

    # TODO: debug function to skip to questionnaire immediately; delete this later!
    def _debug_show_questionnaire(self):
        self.stackedLayout.setCurrentIndex(2)
        self._setup_questionnaire()

    def _setup_study(self):
        self.ui.setFixedSize(650, 500)
        self.ui.max_trial_number.setText(str(ReactionTimeStudy.__TRIAL_COUNT))  # set the max number of trials

        self.timer = QtCore.QTimer(self)  # init a qt Timer to show a countdown before every trial
        self.time_remaining = ReactionTimeStudy.__COUNTDOWN_DURATION
        self._update_ui()
        self._start_task()

    def _update_ui(self):
        current_condition = self._get_current_condition()
        current_task = ReactionTimeStudy.__TASKS[current_condition]
        self.ui.task_description.setText(current_task)
        self.ui.trial_number.setText(str(self._current_trial + 1))  # +1 so the first task is shown as 1 (instead of 0)

    def _start_task(self):
        self.ui.countdown_label.show()
        self.ui.countdown_num.show()
        self._show_remaining_time()
        self.__current_status = self.StudyStates.Pause
        # start countdown
        self.timer.timeout.connect(self._on_countdown)
        self.timer.start(1000)  # every second

    def _on_countdown(self):
        self.time_remaining -= 1

        if self.time_remaining == 0:
            self._show_remaining_time()
            self.__current_status = self.StudyStates.Trial
            # reset counters
            self.time_remaining = ReactionTimeStudy.__COUNTDOWN_DURATION
            self.ui.countdown_label.hide()
            self.ui.countdown_num.hide()

            # disconnect this from the timer so it isn't called infinitely
            self.timer.timeout.disconnect(self._on_countdown)

            # start current trial based on condition
            condition = self._get_current_condition()
            if condition == "A":
                self._init_condition_a()
            else:
                self._init_condition_b()
        else:
            self._show_remaining_time()

    def _show_remaining_time(self):
        # update the countdown ui
        self.ui.countdown_num.setStyleSheet("QLabel { font-weight: bold; color : red;}")
        self.ui.countdown_num.setText(str(self.time_remaining))

    def _get_current_condition(self) -> str:
        try:
            return self._current_trial_order[self._current_trial]
        except IndexError as ie:
            print(f"Tried to get current condition with a wrong index: \n{ie}")

    def _condition_a_reached(self):
        self.__press_key_condition_reached = True
        self.__press_key_condition_reached_timestamp = time.time()
        self.setStyleSheet("background-color: orange;")

    def _init_condition_a(self):
        timeout = get_random_time()
        print("start condition a")
        # wait until changing the background color for a random time to make it less predictable
        QTimer.singleShot(timeout, lambda: self._condition_a_reached())

    def _init_condition_b(self):
        self._finish_loop = False
        while True:
            # stop this loop if space is pressed before blue appeared otherwise it will run infinitely!
            if self._finish_loop is True:
                self.setStyleSheet(f"background-color: white;")
                self._finish_loop = False  # reset so we can run this loop again
                break

            _pause_task(1)  # wait one second between
            color = get_random_color()
            self.setStyleSheet(f"background-color: {color};")
            if color == "blue":
                self.__press_key_condition_reached = True
                self.__press_key_condition_reached_timestamp = time.time()
                break

    def keyPressEvent(self, ev):
        print(str(self.__current_status) + " " + str(self.__press_key_condition_reached))
        if self.__current_status is self.StudyStates.Trial:

            # if not self.stackedLayout.currentWidget() is self.secondPage:
            if ev.key() == QtCore.Qt.Key_Space:
                # if key pressed on the wrong page, do nothing
                if self.__press_key_condition_reached:

                    if self._get_current_condition() == "B":
                        # we pressed space during the infinite loop; kill it in case the user clicked too early
                        self._finish_loop = True

                    self.setStyleSheet(f"background-color: white;")  # reset the window background color
                    self._current_trial += 1
                    # check after ech trial if halfway there (after 10th trial) and if yes, make a short pause
                    self._log_trial_data()

                    if self._current_trial == ReactionTimeStudy.__TRIAL_COUNT / 2:
                        self.ui.task_description.setText("Du hast die Hälfte geschafft! Ruhe dich kurz aus, "
                                                         "in einer Minute geht es weiter!")

                        self.__current_status = self.StudyStates.Pause
                        _pause_task(ReactionTimeStudy.__PAUSE_DURATION)
                    elif self._current_trial == ReactionTimeStudy.__TRIAL_COUNT:
                        # show questionnaire after user finished trials
                        self._go_to_next_page()
                        return

                    self._update_ui()
                    self._start_task()
                    # self.update()  # this triggers an async repaint of the widget (paintEvent() is called)
                else:
                    self.__key_presses_before_condition += 1
                    return

            else:
                self.__wrong_key_presses += 1

    def _log_trial_data(self):
        # 'timestamp', 'participantID', 'condition', 'keyPressed', 'correctKeyWasPressed', 'reactionTime'
        self.__study_data = self.__study_data.append({'timestamp': time.time(), 'participantID': self._participant_id,
                                                      'condition': self._get_current_condition(),
                                                      'wrongKeysPressedCount': self.__wrong_key_presses,
                                                      'conditionNotReachedPressesCount': self.__key_presses_before_condition,
                                                      'reactionTimeInMs': time.time() - self.__press_key_condition_reached_timestamp},
                                                     ignore_index=True)
        self.__press_key_condition_reached = False
        self.__press_key_condition_reached_timestamp = None
        self.__key_presses_before_condition = 0
        self.__wrong_key_presses = 0
        print(self.__study_data)
        self.__study_data.to_csv(self.__STUDY_DATA_CSV_NAME, index=False)

    def _setup_questionnaire(self):
        self.ui.setFixedSize(700, 720)
        self.ui.finish_study_btn.clicked.connect(self._save_answers)

    def _save_answers(self):
        # timestamp', 'participantID', 'age', 'gender', 'occupation', 'usedHand', 'keyboardType', 'keyboardUsage', 'hasEyeImpairment', 'e
        participant_age = str(self.ui.age_selection.value())
        participant_gender = str(self.ui.gender_selection.currentText())
        participant_occupation = str(self.ui.occupation_input.text())
        used_hand = str(self.ui.hand_selection.currentText())
        keyboard_type = str(self.ui.keyboard_type_input.text())
        keyboard_affinity = str(self.ui.keyboard_affinity_slider.value())
        has_eye_impairment = str(self.ui.color_deficiency_selection.currentText())
        eye_impairment = str(self.ui.color_deficiency_input.text())

        self.__questionnaire_data = self.__questionnaire_data.append({'timestamp': time.time(),
                                                                      'participantID': self._participant_id,
                                                                      'age': participant_age,
                                                                      'gender': participant_gender,
                                                                      'occupation': participant_occupation,
                                                                      'usedHand': used_hand,
                                                                      'keyboardType': keyboard_type,
                                                                      'keyboardUsage': keyboard_affinity,
                                                                      'hasEyeImpairment': has_eye_impairment,
                                                                      'eyeImpairment': eye_impairment},
                                                                     ignore_index=True)
        self.__questionnaire_data.to_csv(self.__QUESTIONNAIRE_DATA_CSV_NAME, index=False)
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
