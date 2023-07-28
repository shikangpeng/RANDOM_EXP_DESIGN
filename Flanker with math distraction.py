#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:48:43 2022

@author: lucian
"""

#=====================
#IMPORT MODULES
#=====================
import numpy as np
from psychopy import visual, core, gui, visual, event, monitors
import json
import os
import random
import pandas as pd
import datetime as datetime
#=====================
#PATH SETTINGS
#=====================
directory = os.getcwd()
path = os.path.join(directory, 'dataFiles')
if not os.path.exists(path):
    os.makedirs(path)
   
#=====================
#COLLECT PARTICIPANT INFO
#=====================
#-create a dialogue box that will collect current participant number, age, handedness
expInfo = {'subject_nr':0, 'age':0, 'handedness':('right','left','ambi')}

#Display the dialog box
my_dlg = gui.DlgFromDict(dictionary=expInfo,title = ('Subject Info'),
                         order=('subject_nr', 'age', 'handedness'),
                         tip=None, screen=-1, sortKeys = True,
                         copyDict=False, labels=None, show=True)

expInfo['date'] = datetime.datetime.now() #get today's date time
filename = (str(expInfo['subject_nr']) + '_outputFile.csv')

#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
nTrials = 12
nBlocks = 3
totalTrials = nTrials*nBlocks
nEach = int(totalTrials/3)

#create the stimulus list
word = ['red','green','blue']
ink = ['red','green','blue']
trials = []
#create a list of paired stimuli for one block
for m in word:
    for n in ink:
        trials.append((m,n))
for item in word:
    trials.append((item,item))

    

#=====================
#PREPARE CONDITION LISTS
#=====================
#random shuffle each list to make them in random order for each block
trials_1 = trials
trials_2 = trials
trials_3 = trials
random.shuffle(trials_1)
random.shuffle(trials_2)
random.shuffle(trials_3)
trials = trials_1 + trials_2 + trials_3

#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
words = [0]*totalTrials
inks = [0]*totalTrials
accuracies = [0]*totalTrials
responseTimes = [0]*totalTrials
trialNumbers = [0]*totalTrials
blockNumbers = [0]*totalTrials
#=====================
#CREATION OF WINDOW AND STIMULI
#=====================
mon = monitors.Monitor('myMonitor', width=35.56, distance=60)
mon.setSizePix([1920, 1080])

win = visual.Window(
 fullscr=False, 
 monitor=mon, 
 size=(600,600), 
 color='grey', 
 units='pix'
)
#instruction text defined by psychopy 
instructText = visual.TextStim(win, text='Press r for word red, g for word green, b for word blue')
stim = visual.TextStim(win, text = 'blue', color='black') 
fixation = visual.TextStim(win, text='+', color='black')
myMouse = event.Mouse(visible=False,win=win)
#=====================
#START EXPERIMENT
#=====================
instructText.draw()
win.flip()
event.waitKeys()

trial_timer = core.Clock()
#=====================
#BLOCK SEQUENCE
#=====================
for iblock in range(nBlocks):
    #start message for each block
    instructText.text = 'Press any key to begin Block ' + str(iblock+1)
    instructText.draw()
    #show the message and wait for keypress
    win.flip()
    event.waitKeys()
    #=====================
    #TRIAL SEQUENCE
    #=====================    
    for itrial in range(nTrials):
        #=====================
        #START TRIAL
        #=====================   
        #define the number of trials have done so far
        overallTrial = iblock*nTrials+itrial
        blockNumbers[overallTrial] = iblock+1
        trialNumbers[overallTrial] = itrial+1
 
        words[overallTrial] = trials[overallTrial][0]
        inks[overallTrial] = trials[overallTrial][1]    
        
        #define the stimulus color setting for each trial
        stim.text= str(trials[overallTrial][0])
        stim.color = str(trials[overallTrial][1])
        
        trial_timer.reset() #reset the trial timer
        #display fixation for 300 ms
        while trial_timer.getTime() < 0.25: 
            fixation.draw()
            win.flip()
        #display the word
        trial_timer.reset() #reset the timer to reflect the RT
        stim.draw() 
        win.flip() 

        #wait for only the r, g and b keypresses
        keys=event.waitKeys(keyList=['r','g','b'])
        responseTimes[overallTrial] = trial_timer.getTime() #get the RT
        
        #identify whether the keypress is correct for this trial
        if keys:
            responseTimes[overallTrial] = trial_timer.getTime() 
            if trials[overallTrial][1] == 'red': #check whether the ink is red or not, if so, proceed, no, go to other ink color
                if keys[0] == 'r':
                    accuracies[overallTrial] = 'Correct'
                else:
                    accuracies[overallTrial] = 'Incorrect'
            elif trials[overallTrial][1] == 'blue':
                if keys[0] == 'b':
                    accuracies[overallTrial] = 'Correct'
                else:
                    accuracies[overallTrial] = 'Incorrect'
            else:
                if keys[0] == 'g':
                    accuracies[overallTrial] = 'Correct'
                else: 
                    accuracies[overallTrial] = 'Incorrect'
                    
        print(
         'Block:',
         iblock+1,
         ', Trial:', 
         itrial+1, 
         ',word[', 
         trials[overallTrial][0],
         '],ink[',
         trials[overallTrial][1],
         ']:', 
         accuracies[overallTrial], 
         ', RT:', 
         responseTimes[overallTrial]
        )

win.close()

#======================
# END OF EXPERIMENT
df = pd.DataFrame(data={
  "Block Number": blockNumbers, 
  "Trial Number": trialNumbers, 
  'Word': words,
  "Ink": inks, 
  "Accuracy": accuracies, 
  "Response Time": responseTimes
})
df.to_csv(os.path.join(path, filename), sep=',', index=False)

#close the experiment
win.close()
# #======================        
