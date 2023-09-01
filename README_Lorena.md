This is a tool for automating the process of creating online listening tests in Qualtrics. If you have any issues using it please submit here https://github.com/CSTR-Edinburgh/qualtreats/issues


## Running the script

To create trs questions with video stimuli run:

python testmaker.py -trs_video 

To create MC questions with video stimuli run:

python testmaker.py -mc -nblocks 17
python testmaker_avsec2_2023.py -mc -nblocks 17

To create MC questions with audio-only stimuli run:

python testmaker.py -mc_audio #for mc audio-only questions
python testmaker.py -mc_audio -nblocks 10

IMPORTANT: Remember to update the Javascript code depending on the type of evaluation
mc or mc_audio
Update line ~228~ 239 of the file combined_template.json