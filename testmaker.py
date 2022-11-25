# System imports
import argparse
import json
import copy
from string import Template
from collections import OrderedDict
import os
import sys
# local imports
import config
import numpy as np

# new template files can be created in Qualtrics by creating a
# question with your specifications and exporting the survey file
# json_filename = "combined-template.json"
json_filename = "combined-template.json"
save_as = "output-survey.qsf"
# audio templates should not be changed
audio_html_template = "audio_template.html"
video_html_template = "video_template.html"
image_html_template = "image_template.html"
# play_button = "play_button.html"
question_text_container_html = "question_text_container.html"
useVideo = True

# load JSON template from file
def get_basis_json():
    with open(json_filename, encoding='utf8') as json_file:
        return json.load(json_file)

# standard audio player for all question types except MUSHRA
def get_player_html(url, qid):
    with open(audio_html_template) as html_file:
        return Template(html_file.read()).substitute(url=url, qid=qid)

# standard video player for all question types except MUSHRA
def get_video_player_html(url, qid):
    with open(video_html_template) as html_file:
        return Template(html_file.read()).substitute(url=url, qid=qid)

# Get images from speakers
def get_image_html(url, qid):
    with open(image_html_template) as html_file:
        return Template(html_file.read()).substitute(url=url, qid=qid)

# question phrase text container (it is an html object so that it can be hidden)
def get_question_text_html(qid):
    with open(question_text_container_html) as html_file:
        return Template(html_file.read()).substitute(qid=qid)

# audio player with only play/pause controls for MUSHRA tests
# to prevent participants identifying hidden reference by duration
def get_play_button(url, n): # player n associates play button with a specific audio
    # with open(play_button) as html_file:
    #     return Template(html_file.read()).substitute(url=url, player=n)
    pass

# makes lists of formatted urls from the filenames in the config file
def format_urls(question_type, file_1, file_2=None, file_3=None):
    with open(file_1) as f1:
        try:
            with open(file_2) as f2: # only -ab & -abc have >1 url file
                # helper lambda saves some code later on "gf" means get first
                gf = lambda x: x.split()[1]
                if question_type == 'ab': # returns list of url pairs
                    return [(gf(line1),gf(line2))for line1, line2 in zip(f1,f2)], []
                elif question_type == 'abc':
                    with open(file_3) as f3: # returns list of url trios & empty list
                        return [(gf(line1),gf(line2),gf(line3))
                                for line1, line2, line3 in zip(f1, f2, f3)], []
        except:
            if question_type == 'mos' or question_type == 'trs' or question_type == 'trs_video':
                return [l for l in f1], []
            elif question_type == 'mc':
                names, urls= zip(*(l.replace('\n','').split(' ', 1)  for l in f1))
                return urls, names
            elif question_type == 'mc_audio':
                names, urls, urls_images = zip(*(l.replace('\n', '').split(' ') for l in f1)) #line has 3 columns
                return urls, urls_images, names
            elif question_type == 'mushra': # returns test & reference url lists
                lines = f1.readlines()
                # make ref audio urls to embedded in the question text
                ref_url_list =  [os.path.join(config.mushra_root,
                                config.mushra_ref_folder,
                                line.replace("\n", ""))for line in lines]
                # creates list containing sets of urls which vary only by folder name
                test_url_list = [[os.path.join(config.mushra_root,
                                folder, line.replace("\n", ""))
                                for folder in config.mushra_folders]
                                for line in lines]
                return test_url_list, ref_url_list

# load sentences from text file, to be embedded into MC question text
def get_sentences(sentence_file):
    lines = open(sentence_file, encoding="utf8").readlines()
    return {line.split(' ', 1)[0] : line.split(' ', 1)[1].replace('\n', '') for line in lines}

# make a new question using basis question and urls
def make_question(qid, urls, basis_question,question_type,
                  question_function, question_text):
    new_q = copy.deepcopy(basis_question)
    # Set the survey ID
    new_q['SurveyID'] = config.survey_id
    # Change all the things that reflect the question ID
    new_q['Payload'].update({'QuestionID' : f'QID{qid}',
                                   'DataExportTag' : f'QID{qid}',
                                   'QuestionDescription' : f'Q{qid}:{question_type}',
                                   'QuestionText': question_text})
    new_q.update({'PrimaryAttribute' : f'QID{qid}',
                        'SecondaryAttribute' : f'QID{qid}: {question_type}' })

    if useVideo:
        #update ids from video, audio, play_button and question_text_container html objects:
        if question_type == 'mc' or question_type == 'mc_audio':
            new_q['Payload']['QuestionJS'] = new_q['Payload']['QuestionJS'].replace('play_button',f'play_button{qid}')
            new_q['Payload']['QuestionJS'] = new_q['Payload']['QuestionJS'].replace('video',f'video{qid}')
            new_q['Payload']['QuestionJS'] = new_q['Payload']['QuestionJS'].replace('audio',f'audio{qid}')
            new_q['Payload']['QuestionJS'] = new_q['Payload']['QuestionJS'].replace('image', f'image{qid}')
            new_q['Payload']['QuestionJS'] = new_q['Payload']['QuestionJS'].replace('question_text_container',f'question_text_container{qid}')
        elif question_type == 'trs_video':
            new_q['Payload']['QuestionJS'] = new_q['Payload']['QuestionJS'].replace('play_button', f'play_button{qid}')
            new_q['Payload']['QuestionJS'] = new_q['Payload']['QuestionJS'].replace('video', f'video{qid}')

    try: # call handler function for each question type
        question_function(new_q, urls, qid)
    except TypeError:
        pass
    return new_q

# handler function for ab/abc questions
def ab_q(new_q, urls, qid=None):
    choice_template = new_q['Payload']['Choices']['1']# make choice template
    # empty 'Choices' so flexible number can be added using Choice template
    new_q['Payload']['Choices'] = {}
    for i, url in enumerate(urls):
        choice = copy.deepcopy(choice_template)
        choice['Display'] = get_player_html(url, qid) # add audio player as choice
        new_q['Payload']['Choices'][f'{i+1}'] = choice
    return new_q

 # handler function for mushra questions
def mushra_q(new_q, urls, qid):
    choice_template = new_q['Payload']['Choices']['1']# make choice template
    # empty 'Choices' so flexible number can be added using Choice template
    new_q['Payload']['Choices'] = {}
    for i, url in enumerate(urls):
        choice = copy.deepcopy(choice_template)
        audio_id = (qid-1)*len(urls)+i+qid # unique int id for every sample
        choice['Display'] = get_play_button(url, audio_id) # add audio player as choice
        new_q['Payload']['Choices'][f'{i+1}'] = choice
        # set the choice logic to require that 1+ audio samples are rated == 100
        (new_q['Payload']
              ['Validation']
              ['Settings']
              ['CustomValidation']
              ['Logic']
              ['0']
              [f'{i}']).update({ # update logic settings with Q & A numbers
                    'QuestionID' : f"QID{qid}",
                    'QuestionIDFromLocator' : f"QID{qid}",
                    'ChoiceLocator' : f"q://QID{qid}/ChoiceNumericEntryValue/{i+1}",
                    'LeftOperand' : f"q://QID{qid}/ChoiceNumericEntryValue/{i+1}"})
    return new_q

# make n new blocks according to the survey_length
def make_blocks(num_questions, basis_blocks, qinitial):
    new_blocks = basis_blocks
    block_elements = []
    for i in range(qinitial,qinitial+num_questions):
        block_element = OrderedDict()
        block_element['Type'] = 'Question'
        block_element['QuestionID'] = f'QID{i}'
        block_elements.append(block_element)
    new_blocks['Payload'][0]['BlockElements'] = block_elements

    return new_blocks

# make n new blocks according to the survey_length
def make_multiple_blocks(num_questions_per_block, basis_blocks, qinitial, num_blocks):

    new_blocks = basis_blocks

    qcounter = qinitial
    for j in range(num_blocks):

        block_elements = []
        for i in range(qcounter,qcounter+num_questions_per_block):
            block_element = OrderedDict()
            block_element['Type'] = 'Question'
            block_element['QuestionID'] = f'QID{i}'
            block_elements.append(block_element)

        new_block = {}
        new_block['BlockElements'] = block_elements
        new_block['Type'] = "Standard"
        new_block["Description"] = f"Block {j+1}"
        new_block["ID"] = new_blocks['Payload'][0]["ID"] + f"_{j+1}"

        if j>0: # create new blocks
            new_blocks['Payload'].append(new_block)
        else:
            new_block['Type'] = "Default"
            new_block["ID"] = new_blocks['Payload'][0]["ID"]
            new_blocks['Payload'][0] = new_block
        
        # print(new_blocks['Payload'][j])
        qcounter += num_questions_per_block

    return new_blocks
    

# sets the survey ID for any object which needs it
def set_id(obj):
    obj['SurveyID'] = config.survey_id
    return obj

def main():
    parser = argparse.ArgumentParser() # add question types
    parser.add_argument("-ab", action='store_true',
                        help="make A/B questions (like preference test)")
    parser.add_argument("-abc", action='store_true',
                        help="make A/B/C questions (like preference test)")
    parser.add_argument("-mc", action='store_true',
                        help="make multiple choice questions"
                        "(like error detection)")
    parser.add_argument("-mc_audio", action='store_true',
                        help="make multiple choice questions with audio stimuli ")
    parser.add_argument("-trs", action='store_true',
                        help="make transcription questions (with text field)")
    parser.add_argument("-trs_video", action='store_true',
                        help="make transcription questions (with text field)")
    parser.add_argument("-mushra", action='store_true',
                        help="make MUSHRA questions with sliders")
    parser.add_argument("-mos", action='store_true',
                        help="make Mean Opinion Score questions with sliders")
    parser.add_argument("-name", dest='survey_name', default='survey_name', help="survey name")
    parser.add_argument("-qinitial", dest='qinitial', default='1', help="question counter initial value")
    parser.add_argument("-nblocks", dest='nblocks', default='1', help="number of blocks")

    args = parser.parse_args()
    survey_name = args.survey_name
    qinitial = int(args.qinitial)
    nblocks = int(args.nblocks)

    # get only args which were specified on command line
    args = [key for key, value in vars(args).items() if value==True]

    # store the arguments passed to format_urls() when executed
    argument_dict = {'ab':[config.ab_file1, config.ab_file2],
                     'abc':[config.abc_file1, config.abc_file2, config.abc_file3],
                     'mc':[config.mc_file],
                     'mc_audio': [config.mc_audio_file],
                     'trs':[config.trs_file],
                     'trs_video':[config.trs_video_file],
                     'mushra':[config.mushra_files],
                     'mos':[config.mos_file]
                     }
    # create a dictionary with key=command line arg & value= output of format_urls()
    # function's arguments are taken from argument_dict

    url_dict = {arg:format_urls(arg, *argument_dict[arg]) for arg in args}

    # format_urls() returns tuple of urls & anything else that's embedded in question
    # (for MC & trs it's the sentence text, for MUSHRA it's the reference URL)
    # split dictionary value tuples into keyyed subdictionary
    for key, value in url_dict.items():
        if key == 'mc_audio':
            url_dict[key] = {'urls': value[0], 'urls_images': value[1], 'extra': value[2]}  # url, filename. Key is the question type
        else:
            url_dict[key] = {'urls': value[0], 'extra': value[1]}  # url, filename. Key is the question type
        # print(url_dict[key]['extra'])
        # print(url_dict[key]['urls_images'])
    # get sentences from file to embed in multiple choice questions
    mc_sentences = get_sentences(config.mc_sentence_file)




    # get json to use as basis for new questions
    basis_json = get_basis_json()
    elements = basis_json['SurveyElements']

    # Set the survey ID in all survey_elements
    elements = list(map(set_id, elements))


    # get question template blocks from elements JSON
    # element order is survey-dependent- check if you're using a new template
    basis_question_dict = {'ab': elements[12],
                           'mc': elements[8],
                           'mc_audio': elements[8],
                           'trs':elements[11],
                           'trs_video':elements[14],
                           'abc': elements[13],
                           'mushra': elements[9],
                           'mos':elements[10]}

    # update multiple choice answer text in template to save computation
    #Multiple choice question answers are provided in file sentences.txt
    # (basis_question_dict['mc']['Payload']['Choices']
    #                     ['1']['Display']) = config.mc_choice_text[0]
    # (basis_question_dict['mc']['Payload']['Choices']
    #                     ['2']['Display']) = config.mc_choice_text[1]

    # turn off answer order randomisation for MC questions (ie Yes/No)
    # comment out these 2 lines to add randomisation
    d = basis_question_dict['mc']['Payload']
    basis_question_dict['mc'].update({'Payload': {i:d[i] for i in d if i!='Randomization'}})
    d = basis_question_dict['mc_audio']['Payload']
    basis_question_dict['mc_audio'].update({'Payload': {i: d[i] for i in d if i != 'Randomization'}})

    # get basic survey components from elements JSON
    basis_blocks = elements[0]
    basis_flow = elements[1]
    rs = elements[2]
    basis_survey_count = elements[7]

    # store question text set in config.py, add an audio player where required
    #Here we can add html elements to the question structure
    q_text_dict = { 'ab': config.ab_question_text,
                    'abc': config.ab_question_text,
                    'mc': f"{get_video_player_html('$urls', '$qid')}\
                            {get_question_text_html('$qid')}\
                            {config.mc_question_text} ",
                    'mc_audio': f"{get_image_html('$urls_images', '$qid')}\
                                {get_player_html('$urls', '$qid')} \
                                {get_question_text_html('$qid')}\
                                {config.mc_question_text}",
                    'trs': f"{config.trs_question_text}\
                             {get_player_html('$urls', '$qid')}",
                    'trs_video': f"{get_video_player_html('$urls', '$qid')}\
                            {config.trs_question_text}",
                    'mushra': f"{config.mushra_question_text}\
                                {get_play_button('$ref_url', '$ref_id')}",
                    'mos': f"{config.mos_question_text}\
                             {get_player_html('$urls', '$qid')}"
    }

    # keys=question types and values= functions for making questions
    handler_dict = {'ab': ab_q,
                    'abc': ab_q,
                    'mc': None,
                    'mc_audio':None,
                    'trs': None,
                    'trs_video': None,
                    'mushra': mushra_q,
                    'mos': None}

    # create list to store generated question blocks
    questions = []

    # create counters to use when indexing optional lists
    q_counter = qinitial # qualtrics question numbering starts at 1
    mc_counter = 0
    mc_audio_counter = 0
    mushra_counter = 0

    num_answers_in_closed_set = 5

    for arg in args:
        for n, url_set in enumerate(url_dict[arg]['urls']): # for each url set for that question type
            # get MUSHRA reference url if the current flag == -mushra
            ref_url = url_dict['mushra']['extra'][mushra_counter] if arg == 'mushra' else None
            # get MC sentence if the current flag == -mc
            if arg == 'mc':
                sentence = mc_sentences[url_dict['mc']['extra'][mc_counter]]
            elif arg == 'mc_audio':
                sentence = mc_sentences[url_dict['mc_audio']['extra'][mc_audio_counter]]
            else:
                sentence = None
            if sentence is not None:
                # remove start and end quotes
                sentence = sentence.strip('\'')
                # split sentence to get words
                split_sentence = sentence.split(' ')
                # update answers to questions based on sentence files
                for x in range(num_answers_in_closed_set):
                    #this is where words from file sentences.txt are added as answer options in multiple choice questions
                    if arg == 'mc':
                        if x == num_answers_in_closed_set-1:
                            basis_question_dict['mc']['Payload']['Choices'][str(x + 1)]['Display'] = 'none of these'.strip('\'')  # strip is ued to remove the last ' after none
                        else:
                            basis_question_dict['mc']['Payload']['Choices'][str(x + 1)]['Display'] = split_sentence[x].strip('\'') #strip is ued to remove the last ' after none
                    elif arg == 'mc_audio':
                        if x == num_answers_in_closed_set-1:
                            basis_question_dict['mc_audio']['Payload']['Choices'][str(x + 1)]['Display'] = 'none of these'.strip('\'')  # strip is ued to remove the last ' after none
                        else:
                            basis_question_dict['mc_audio']['Payload']['Choices'][str(x + 1)]['Display'] = split_sentence[x].strip('\'') #strip is ued to remove the last ' after none
            mushra_ref_id = n*(len(url_set)+1) # unique id for every ref sample
            #update url of speaker image:
            if arg == 'mc_audio':
                image_url = url_dict[arg]['urls_images'][n] #todo: with n or without it
            # print(image_url)

            # embed required url or sentence into the question text
            text = Template(q_text_dict[arg]).substitute(ref_url=ref_url,
                                                         ref_id=mushra_ref_id,
                                                         urls=url_set,
                                                         urls_images=image_url,
                                                         sentence=sentence,
                                                         qid=str(q_counter)
                                                         )

            # make a new question and add it to the list of questions
            questions.append(make_question(
                                # question number (starting at 1)
                                qid=q_counter,
                                # set of audio urls
                                urls=url_set,
                                # template for that question type
                                basis_question=basis_question_dict[arg],
                                question_type=arg,
                                # handler function for that question type
                                question_function=handler_dict[arg],
                                question_text=text,  # as set above
                                ))
            q_counter += 1
            # increment these counters when a question of that type is created
            # except for the last question (to prevent IndexError)
            mc_counter += (1 if arg == 'mc' and
                           mc_counter+1 < len(url_dict['mc']['urls']) else 0)
            mc_audio_counter += (1 if arg == 'mc_audio' and
                                mc_audio_counter + 1 < len(url_dict['mc_audio']['urls']) else 0)
            mushra_counter += (1 if arg == 'mushra' and
                               mushra_counter+1 < len(url_dict['mushra']['urls']) else 0)

    # survey_length is determined by number of questions created
    survey_length = len(questions)

    # Create all the items in survey elements, with helper function where doing so is not trivial
    if nblocks==1:
        num_questions_per_block = survey_length
        blocks = make_blocks(survey_length, basis_blocks, qinitial)
    else:
        assert (survey_length % nblocks) == 0
        num_questions_per_block = int(survey_length/nblocks)
        blocks = make_multiple_blocks(num_questions_per_block, basis_blocks, qinitial, nblocks)

    flow = basis_flow
    flow['Payload']['Properties']['Count'] = survey_length
    survey_count = basis_survey_count
    survey_count['SecondaryAttribute'] = str(survey_length)
    # add all the created elements together
    elements = [blocks, flow] + elements[2:7]  + questions + [rs]

    # Add the elements to the full survey
    # Not strictly necessary as we didn't do deep copies of elements
    out_json = basis_json
    out_json['SurveyElements'] = elements

    out_json["SurveyEntry"]["SurveyName"]= survey_name

    print(f'Generated survey with {survey_length} questions')
    print(f"Number of blocks: {nblocks}")
    print(f"Number of questions per block: {num_questions_per_block}")

    with open(save_as, 'w+') as outfile:
        json.dump(out_json, outfile, indent=4)

if __name__ == "__main__":
    main()
