## Introduction

The goal of this study was to find differences in the reaction time of users under different conditions. For this purpose a small experiment was designed where users had to react to two different visual stimuli by clicking a key on their keyboard as fast as possible. Both conditions varied in their complexity and mental demand which enabled a comparison of the reaction times between the conditions. The application used in the study was created with Qt Designer [1] and implemented in Python with the PyQt-Framework [2].



## Experiment Setup

At the start the participants were shown a small explanation of the study and the tasks and were instructed to use only the index finger to prevent confounding results due to different fingers used. They could choose which hand they wanted to use but were asked to not switch it during the experiment. They were also given an approximate duration of the study and were asked to make sure that they were in an undisturbed place for this time so they would be able to concentrate.

Afterwards, the participants were given one of two different tasks where the space key had to be pressed one time as fast as possible after the background of the current window changed. In one condition they were asked to press it as soon as the background changed while in the other condition the background color changed rapidly and they should only press the key if the current background color switched to blue. They had to do this 20 times in total, 10 times for each condition. The order of the conditions was randomized for each participant to prevent any ordering bias or learn effects. Before each trial the current task and a 10 second countdown were shown so the participants had time to read the instruction before the task started. This gave the participants a small time slot to prepare for the next task to prevent too much mental demand and fatigue effects. For the same reason the participants were also given 30 seconds to relax after half of the tasks were finished. After the participant finished all 20 tasks he was asked to fill out a short questionnaire containing demographic questions and questions about used keyboard type, the hand the participant used to press the space key and any color vision deficiencies.

Overall, we used a within-subjects design with two conditions and ten repetitions per condition. Our dependent variable was the reaction time of the user (i.e. the time between the color change and the key press) while our independent variable was the given task (i.e. stimulus with or without additional decision process). Control variables were collected in the questionnaire at the end in the form of used keyboard type (external, laptop, ...), the participant's amount of keyboard usage in daily life on a seven point likert scale, which hand he used for the experiment (weak or strong, left or right) as well as demographics like his age, gender and current occupation. During the study the number of errors (too early key presses) for each task was logged as well. Additionally, we controlled which key ("space") and which finger (index finger) was used during the study. Confounding variables such as the size of the pressed key, the used finger or if the user has any form of color blindness were taken into account while designing the study by specifying them clearly or collecting them in the questionnaire. A random variable which could potentially influence the results slightly might be that some people are simply more accustomed to such tasks which enables them to perform better, for example if they had taken part in a similar study before. Or some people are simply a little bit better in recognizing the colors that we chose earlier than others.



## Participants

The study was conducted by 9 participants ranging in age from 22 to 31 years (m = 26,67, sd = 3,68). 6 participants were male and 3 female. In a more optimal setting, the study would have been conducted with a lot more participants (n > 30) from different social and ethnic backgrounds as well as different age groups to get more generalizable results. It would also be useful to acquire participants with different levels of technological affinity, especially related to the use of keyboards.

As the study requires reacting to a changing color as stimulus, only participants without a color vision deficiency (e.g. red green color blindness) should take part in the experiment.



## Preliminary Results

As the second condition required an additional decision process after each color was shown, we assumed that the reaction time would be slower for this condition as it required more mental effort than the first. Therefore, our alternative hypothesis was that the reaction time of our participants were slower in the condition where they should only press the space key if the background color changed to blue while our null hypothesis stated that no significant differences in the reaction times for both conditions would be found.

However, our results show that there was no significant difference in the participant's reaction times between the two conditions. Even though the second condition required an additional decision process it does not influence the reaction time as much as we thought it would.


<br>

[1] Qt Designer. (2021). *Qt Designer Manual*. Retrieved May 4, 2021, from https://doc.qt.io/qt-5/qtdesigner-manual.html

[2] PyQt. (2021). *What is PyQt?*. Retrieved May 4, 2021, from https://riverbankcomputing.com/software/pyqt
