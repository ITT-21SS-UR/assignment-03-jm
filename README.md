# Assignment 3: Experiments, Logging, Visualization
  
**Submission due: Wednesday, 05. May 2021, 23:55**

**Hand in in groups of max. two.**

3.1: Whys and Hows of Experiments in HCI
========================================

Read Kasper Hornbæk's paper ["Some Whys and Hows of Experiments in HCI"](http://www.kasperhornbaek.dk/papers/SomeWhysAndHows.pdf) and answer the following questions in your own words in a plain-text file (no more than 5000 characters):

* What does Hornbæk say about the relationship between self-reported and objectively measured task performance?

* Describe advantages and limitations of research hypotheses.

* Is it acceptable to conduct user studies with media informatics students as participants instead of a broad sample of potential users? What are advantages and limitations? Name one topic for a user study where it would be problematic to have only media informatics students as participants. Name one counter-example. 


Points
--------

* **1** Good answer for the first question.
* **1** Good answer for the second question.
* **2** Good answer for the third question.


3.2: Plan an Experiment
==============================

Plan a single study for measuring the reaction time of users under different conditions.
For the first condition, participants have to react to a single stimulus (e.g. the screen changing its color or a sound being played) by pressing a button on the keyboard.
The second condition should require additional **mental demand** from the user, for example by introducing a decision process or information processing.

Your study should use a within-subjects design with at least 10 repetitions per condition.
Try to minimize confounding and random variables, such as learning effects, fatigue, participants' cognitive properties.

Document your study's goal, hypotheses, setup, participant selection, etc. 
Also document your independent, dependent, and controlled variables.
Document values for controlled variables, e.g. keyboard type.

Hand in the following file: 

**reaction_time_experiment_design.pdf**: a report (2 pages max.) that contains the following sections: 

* *Introduction* which explains the goal of the experiment, 
* *Experimental setup* which documents the factors and variables, and
* *Participants* which describes the participants of the experiment and explains why you chose them.
* *Preliminary Results* which describes initial results from your experiment (we will expand on this later).

You may use any formatting. Properly reference all sources. 

Points
--------

* **2** Experiment design contains all information mentioned above.
* **2** Correct and comprehensive description of all variables.
* **1** Proper formatting and language in the document.


3.3: Implement the Experiment
===============================

Expand `space_counter.py` (or write a new application) so that it displays the necessary information on screen and records all relevant information to a log file.
Build an automatic and modular pipeline so that important aspects of the test application can be set via command line parameters and the whole test setup could in theory run without an experimenter being present.

For every trial, the following information should be logged to a CSV file:

* participant ID
* condition
* shown stimulus (concrete word/color/number/etc.),
* pressed key
* whether the correct key was pressed
* reaction time
* timestamp
* all other information you deem important 

Make sure that the file follows the CSV guidelines given in the lecture slides.

Hand in the following file:

**reaction_time_test.py**: a Python script that implements the above requirements and can be used to conduct the aforementioned test.



Points
------------

* **1** The python script has been submitted, is not empty, and does not print out error messages.
* **2** The script correctly reads the test description and shows the required signals.
* **2** The script correctly logs all information to a CSV file.
* **1** The script is well-structured and follows the Python style guide (PEP 8). 
* **1** It is sufficiently documented how the workload was distributed among team members in terms of implementation in report writing within code comments


3.4: Conduct the Experiment 
=============================

Conduct the study at least three times per team member.
If you have trouble finding participants, you can also participate yourself (repeatedly if necessary).
(Please do a test run beforehand to catch any technical problems.)
Log the results of all participants.

Hand in the following files:

**reaction_time_results.csv**: a CSV file containing concatenated log files of all participants.

**reaction_time_report.txt**: a short report documenting any interesting events during the experiment and all limitations of your experiment that you found when conducting it (e.g., you forgot to explain to all participants what they had to do).


Points
------------

* **2** All four log files have been submitted and are formatted correctly.
* **2** The report is overall plausible and well-written.


3.5: Analyze your experimental data
====================================

Create a Jupyter Notebook that contains the complete analysis and visualization process for your experimental data.

In particular, your notebook should contain the following parts:

* a title (markdown cell) "Reaction Time Analysis"
* a brief description of your experiment, containing the most important details about setup and participants (for an example of how and what to document about your study, see the paper on the 'Shift' input technique mentined below).
* code which imports the raw data from a CSV file and extracts the relevant data for further processing (the CSV file should be in the same directory)
* sensible headings that describe what happens in the following lines
* scatterplots showing reaction times for each of the conditions and for all conditions combined (color-coded).
* boxplots and t-test results
* a brief discussion of the most noteworthy results, including whether there are statistically significant differences between the conditions.

Hand in a file **reaction_time_experiment.ipynb** and one or more CSV files (**data.csv or data1.csv ... dataN.csv**) which must be in the same directory as the notebook.

Points
--------

* **1** The Jupyter Notebook has been submitted, is not empty, and does not print out error messages.
* **2** The notebook correctly reads the data from the file(s) and outputs the required visualizations
* **1** Visualizations are self-explaining and contain units and axis description.
* **1** The notebook is well-structured and generally follows the Python style guide (PEP 8).
* **2** The results are discussed in sufficient detail and clarity.

3.6: Read up on pointing devices
====================================

Read the Wikipedia article on [pointing devices](https://en.wikipedia.org/wiki/Pointing_device) and the paper *Shift: a technique for operating pen-based interfaces using touch* by Daniel Vogel and Patrick Baudisch (a great example of good study design).
Explain in a few sentences:

a) Which advantages do direct pointing devices have over indirect pointing devices? Name one use case where using a direct pointing device would not make any sense.
b) How would you characterize "Shift" based on the classification criteria mentioned in the Wikipedia article?
c) What is the size of the display used in the study?

Points
--------

* **1** Great answer to the first question
* **1** Great answer to the second question
* **1** Great answer to the third question

Hand in a plain-text file **pointing_devices.txt**


3.7: Peer review solutions to Assignment 2
==========================================

**Hand in indiviually**

Review the assigned submissions that are assigned to you in GRIPS and give feedback.
Please read the separate task description in GRIPS for details on the review process.

* **1** You have graded all submissions in time.
* **2** Your grading is plausible (i.e. follows the reviewing guidelines)
* **2** You have given relevant (1 point) or helpful (2 points) feedback.

**Note:** the points for Assignment 3.7 will be assigned to Assignment 2 in GRIPS due to technical reasons.


Submission 
=========================================
Submit via GRIPS until the deadline

All files should use UTF-8 encoding and Unix line breaks.
Python files should use spaces instead of tabs.
