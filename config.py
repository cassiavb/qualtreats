# survey_id should remain unchanged
survey_id = "SV_4TLSPrwNIjymdh3"

# the below variables should be set according to your survey specifications

# this text will appear in each question
ab_question_text = "Which of the following sounds the most natural?"
mc_question_text= "" #For this type of question edit phrasing in file question_text_container.html
trs_question_text = "Please type the sentence the speaker in the video said."
mushra_question_text = "How natural are the following speech recordings? <br> Reference: "
mos_question_text = "Listen to this speech sample, then rate the quality of the speech."
# the answer options for multiple choice questions
mc_choice_text = ['Yes', 'No']

# these files should contain the urls to be embedded in questions/choices
# each file should have a filename and url per line, separated by whitespace
ab_file1 = "resources/ab-urls-1.txt"
ab_file2 = "resources/ab-urls-2.txt"
abc_file1 = "resources/abc-urls-1.txt"
abc_file2 = "resources/abc-urls-2.txt"
abc_file3 = "resources/abc-urls-3.txt"
# mc_file = "resources/mc-urls.txt"
# mc_file = "pilot_test_resources/mc-video-urls.txt"
# mc_file = "pilot_test_resources/mc-video-urls_practice.txt"
mc_file = "evaluation_resources/mc-video-urls_evaluation_w_validation.txt"
# mc_audio_file = "resources/mc-audio-urls.txt"
# mc_audio_file = "pilot_test_resources/mc-audio-urls.txt"
#audio_only evaluation:
# mc_audio_file = "evaluation_resources/ao_mc_audio_urls.txt"
# mc_audio_file = "evaluation_resources/ao_mc_audio_and_images_urls.txt"
### Check and practice files:
mc_audio_file = "evaluation_resources/ao_mc_audio_PRACTICE_and_images_urls.txt"
trs_file = "resources/trs-urls.txt"
# trs_file = "evaluation_resources/trs_videos-urls.txt"
# trs_video_file = "resources/trs_video-urls.txt"
# trs_video_file = "resources/trs_videos-urls_4.txt"
# trs_video_file = "resources/trs_videos-urls_practice.txt"
# trs_video_file = "resources/trs_videos-url.txt"
trs_video_file = "evaluation_resources/trs_videos-urls.txt"
# trs_video_file = "pilot_test_resources/trs_videos-urls_practice.txt"
mos_file = "resources/mos-urls.txt"
# mushra filenames should be the same across folders
# audiofile urls should vary only by folder name
# any number of folders can be specified
mushra_files = "resources/mushra-urls.txt"
mushra_root = "https://groups.inf.ed.ac.uk/cstr3/cvbotinh/Mushra_example/samples"
# the hidden reference folder should be included in both mushra_folders and mushra_ref_folder
mushra_folders = ["G1","G1H","G1HA","G1TH", "G1THA"]
mushra_ref_folder = "G1THA"

# MC questions have sentence text embedded
# this file should have a filename and corresponding sentence string per line
# mc_sentence_file = "resources/sentences.txt"
# mc_sentence_file = "pilot_test_resources/pilot_alternatives_120.txt"
# mc_sentence_file = "pilot_test_resources/pilot_alternatives_practice.txt"
# mc_sentence_file = "evaluation_resources/mc-video-alternatives_w_validation.txt"
# mc_audio
# mc_sentence_file = "evaluation_resources/ao_mc-audio-alternatives_file.txt"
### Check and practice files:
mc_sentence_file = "evaluation_resources/ao_mc-audio-PRACTICE_alternatives_file.txt"