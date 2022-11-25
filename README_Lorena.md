This is a tool for automating the process of creating online listening tests in Qualtrics. If you have any issues using it please submit here https://github.com/CSTR-Edinburgh/qualtreats/issues


## Running the script

To create trs questions with video stimuli run:

python testmaker.py -trs_video 

To create MC questions with video stimuli run:

python testmaker.py -mc

To create MC questions with audio-only stimuli run:

python testmaker.py -mc_audio #for mc audio-only questions
python testmaker.py -mc_audio -nblocks 10
