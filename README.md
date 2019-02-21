# check_game

This package only runs on Sand currently.

This is the development build and is intended just to question the results of dominance_check.py

-------------------------------

There are two programs you'll need to run.

## Run dominance_check.py:

Usage: python dominance_check.py _folder-name_

This will create a folder on Sand under /scratch/william/_folder-name_ for storage of all output files.

The output files created include:
* states for symmetric Model
* models for each adversary against
* a log file
* the output of extended prism when calculating adversaries (this shows multiple optimal strategies)
  * These files are named opt_gen_x.txt where x = 0 for KAKA, 1 for KWKW and 2 for WAWA

It will take ~ 5 minutes for this program to terminate.

## Run opt_gen_scraper.py:

Usage: python2 opt_gen_scraper.py _output-of-extended-prism_ _states-for-corresponding-model_

for example, if I wanted to check the relevant states for KWKW and had run dominance_check.py dir1 
then I would need to run python2 opt_gen_scraper.py /scratch/william/dir1/opt_gen_1.txt /scratch/william/dir1/KWKW.sta

The output of this program is all of the relevant state descriptions from which there are multiple actions leading to the same likelihood of player 1 winning.




### Changing the configurations

There are 5 configurations {A-E} stored as .txt files in /configurations

Feel free to copy them into char_info.txt to change the configuration you run the program for.


### TODO:

I will update domiance_check to deal with symmetry soon and I will add run_experiment under a new name of dominanted_search in the coming week.

