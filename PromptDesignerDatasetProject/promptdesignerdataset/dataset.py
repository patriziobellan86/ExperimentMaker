import codecs
from copy import deepcopy
import os
from collections import defaultdict
import json


def SaveJsonData(data, filename=None):
    # try:
    # print(type(data))
    with open(filename, 'w') as fout:
        json.dump(data, fout)
    return True
    # except:
    #     return False


def LoadJsonData(filename):
    try:
        with open(filename, 'r') as fin:
            return json.load(fin)
    except:
        return False

_default_prompt = '''
This is a default PROMPT

you questions goes here {question}
'''


class PromptDesignerDataset:
    DEFAULT_PROMPT = _default_prompt
    LOGPROBS = 'log-probs'
    QUESTION = 'question'
    TEMPERATURE = 'temperature'
    NUCLEUS = 'nucleus'
    # SAMPLING_MODE = 'sampling-mode'
    DATETIME = 'datetime'
    ENGINE = 'engine'
    N_ = 'n_'
    STOPWORDS_LIST = 'stopwords-list'
    PROMPT = 'prompt-name'
    PROMPT_TEXT = 'prompt-text'
    PRESENCE_PENALTY = 'presence-penality'
    FREQUENCY_PENALTY = 'frequence-penality'
    MAX_TOKEN = 'max-token'
    ANSWERS = 'answers'
    JSON_RESPONSE = 'response-json'

    ANSWER_DATA_DICT = {QUESTION: None,
                        JSON_RESPONSE: dict(),
                        TEMPERATURE: 0.,
                        NUCLEUS: 0.,
                        # SAMPLING_MODE: None,
                        N_: 1,
                        DATETIME: None,
                        ENGINE: None,
                        STOPWORDS_LIST: None,
                        PROMPT: None,
                        PROMPT_TEXT: None,
                        PRESENCE_PENALTY: 0.,
                        FREQUENCY_PENALTY: 0.,
                        MAX_TOKEN:150.,
                        ANSWERS: list()}

    DATA_QUESTIONS = 'questions'
    DATA_PROMPTS_LABEL = 'prompts'
    DATA_QUESTIONS_LIST = 'questions-list'
    DATA_PROMPT_COMMENT = 'prompt-comment'
    DATA_SESSION = 'data-session'

    FILTER_NAMES = [PROMPT,
                    TEMPERATURE,
                    NUCLEUS,
                    PRESENCE_PENALTY,
                    FREQUENCY_PENALTY,
                    ENGINE,
                    ]

    def GetAnswerDataEmptyDict(self):
        return deepcopy(self.ANSWER_DATA_DICT)


    def t(self, temperature):
        return round(float(temperature),1)

    def __init__(self,
                 filename=None # 'answerdata'
                ):
        self.filename = filename

        self.__init_variables__()

    def __init_variables__(self):
        self.data = {self.DATA_QUESTIONS: defaultdict(list),
                     self.DATA_PROMPTS_LABEL: dict(),
                     self.DATA_QUESTIONS_LIST: dict(),
                     self.DATA_PROMPT_COMMENT: dict(),
                     self.DATA_SESSION: ''}
        ##################################################################
        #  data structure
        # self.DATA_QUESTIONS = {question: [
        #                                            {question paramater t, answers,
        #                                               that ADD prompt}
        #                                         ]
        # self.DATA_QUESTIONS_LIST = 'questions-list-name': list of questions in txt

    def IsQuestionsListPresent(self, questions_list_name):
        return questions_list_name in self.data[self.DATA_QUESTIONS_LIST].keys()

    def AddQuestionsList(self,
                         question_list_name,
                         questions):
        self.data[self.DATA_QUESTIONS_LIST][question_list_name] = questions

    def RemoveQuestionsList(self, questions_list_name):
        self.data[self.DATA_QUESTIONS_LIST].pop(questions_list_name)

    def GetQuestionsListNames(self):
        return sorted(self.data[self.DATA_QUESTIONS_LIST].keys())

    def GetQuestionsList(self, question_list_name):
        return self.data[self.DATA_QUESTIONS_LIST][question_list_name]

    def AddQuestionAnswer(self,
                          parameters,
                          answers):
        parameters[self.ANSWERS] = answers
        question = parameters[self.QUESTION]
        self.data[self.DATA_QUESTIONS][question].append(parameters)


    def AddPrompt(self,
                  prompt_name,
                  prompt):
        self.data[self.DATA_PROMPTS_LABEL][prompt_name] = prompt

    def AddCommentPrompt(self,
                         prompt_name: str,
                         comment: str):
        self.data[self.DATA_PROMPT_COMMENT][prompt_name] = comment

    def IsCommentPromptPresent(self,
                               prompt_name):
        return prompt_name in self.data[self.DATA_PROMPT_COMMENT].keys()

    def GetCommentPrompt(self,
                         prompt_name):
        return self.data[self.DATA_PROMPT_COMMENT][prompt_name]

    def IsPromptPresent(self, prompt_name):
        return prompt_name in self.data[self.DATA_PROMPTS_LABEL].keys()


    def RemovePrompt(self, prompt_name):
        self.data[self.DATA_PROMPTS_LABEL].pop(prompt_name)

    def GetPrompt(self, prompt_name):
        try:
            return self.data[self.DATA_PROMPTS_LABEL][prompt_name]
        except KeyError:
            # print('prompt {} not found'.format(prompt_name))
            return self.DEFAULT_PROMPT

    def GetPromptNames(self):
        return sorted(list(
                        self.data[self.DATA_PROMPTS_LABEL].keys()))
    def GetTemperatures(self)-> list:
        temperatures = set()
        for question, answers in sorted(list(self.data[self.DATA_QUESTIONS].items())):
            # print(question)
            # print(answers)
            for answer in answers:
                temperatures.add(answer[self.TEMPERATURE])
        return list(temperatures)

    def GetNucleus(self)-> list:
        nucleus = set()
        for question, answers in sorted(list(self.data[self.DATA_QUESTIONS].items())):
            # print(question)
            # print(answers)
            for answer in answers:
                nucleus.add(answer[self.NUCLEUS])
        return list(nucleus)

    def GetPresencePenalty(self) -> list:
        presence_penalty = set()
        for question, answers in sorted(list(self.data[self.DATA_QUESTIONS].items())):
            # print(question)
            # print(answers)
            for answer in answers:
                presence_penalty.add(answer[self.PRESENCE_PENALTY])
        return list(presence_penalty)

    def GetEngines(self) -> list:
        engines = set()
        for question, answers in sorted(list(self.data[self.DATA_QUESTIONS].items())):
            # print(question)
            # print(answers)
            for answer in answers:
                engines.add(answer[self.ENGINE])
        return list(engines)

    def GetFrequencyPenalty(self) -> list:
        frequency_penalty = set()
        for question, answers in sorted(list(self.data[self.DATA_QUESTIONS].items())):
            # print(question)
            # print(answers)
            for answer in answers:
                frequency_penalty.add(answer[self.FREQUENCY_PENALTY])
        return list(frequency_penalty)

    def GetQuestions(self)-> list:
        return sorted(
                    list(set(
                        [question for question in self.data[self.DATA_QUESTIONS].keys()]
                    )))

    def GetPromptsOfQuestion(self,
                             question)-> list:
        answers = self._get_answer(question)
        prompts = list(set([ans[self.PROMPT] for ans in answers]))

        return sorted(prompts)

    def GetEnginesOfQuestion(self,
                             question)-> list:
        answers = self._get_answer(question)
        engines = list(set([ans[self.ENGINE] for ans in answers]))

        return sorted(engines)

    def GetNucleusOfQuestion(self,
                                  question):
        answers = self._get_answer(question)
        presence = list(set([ans[self.NUCLEUS] for ans in answers]))

        return sorted(presence)

    def GetPresencePenalityOfQuestion(self,
                                  question):
        answers = self._get_answer(question)
        presence = list(set([ans[self.PRESENCE_PENALTY] for ans in answers]))

        return sorted(presence)

    def GetFrequencyPenalityOfQuestion(self,
                                  question):
        answers = self._get_answer(question)
        frequency = list(set([ans[self.FREQUENCY_PENALTY] for ans in answers]))

        return sorted(frequency)

    def GetTemperaturesOfQuestion(self,
                                  question)-> list:
        answers = self._get_answer(question)
        temperatures = list(set([ans[self.TEMPERATURE] for ans in answers]))
        return temperatures
        return sorted(temperatures)
    #
    # def AddQuestionsAnswersSession(self,
    #                                filename,
    #                                prompt_name):
    #     # prompt
    #
    #     #  parse file
    #     data = self.parser_answers.ParseFile(filename=filename)
    #     for quest in data:
    #         self._add_a_qa(quest, prompt_name)
    #     #  check if prompt name exist
    #     if not self.IsPromptPresent(prompt_name=prompt_name):
    #         self.AddPrompt(prompt_name=prompt_name,
    #                        prompt='<<No Prompt Found!>>')

    def LoadData(self, filename):
        if os.path.exists(filename):
            self.filename = filename
            return self._load_data(self.filename)
        return False

    def SaveData(self, filename):
        self.filename = filename
        return self._save_data(self.filename)

    def UpdateData(self):
        return self._save_data(self.filename)
    #
    # def IsQuestionAsked(self, question,
    #                     prompt=None,
    #                     temperature=None,
    #                     nucleous=None):
    #     if any([prompt, temperature, nucleous]):
    #         if question in self.data[self.DATA_QUESTIONS].keys():
    #             quests = self.data[self.DATA_QUESTIONS][question]
    #             if prompt:
    #                 quests = self._filter_answer_by_prompt(quests, [prompt])
    #             if temperature:
    #                 quests = self._filter_answer_by_temperature(quests, [temperature])
    #             if nucleous:
    #                 quests = self._filter_answer_by_nucleus(quests, [temperature])
    #             return len(quests) > 0
    #         else:
    #             return False
    #     else:
    #         return question in self.data[self.DATA_QUESTIONS].keys()

    def IsQuestionAsked(self, question,
                        filters=dict(),
                        ):
        if len(self.GetAnswers(question, filters)) > 0:
            return True
        return False
    # def GetAnswers(self,
    #                question,
    #                filter_prompts='all',
    #                filter_temperatures='all',
    #                filter_nucleus='all',
    #                filter_presence_penalty='all',
    #                filter_frequency_penalty='all')-> list:
    #
    #     answers = self._get_answer(question)
    #     #  filter by prompt
    #     if filter_prompts != 'all':
    #         if type(filter_prompts) == list:
    #             answers = self._filter_answer_by_prompt(answers,
    #                                                         filter_prompts)
    #         else:
    #             answers = self._filter_answer_by_prompt(answers,
    #                                                     [filter_prompts])
    #     #  filter by temperatures
    #     if filter_temperatures != 'all':
    #         if type(filter_temperatures) == list:
    #             answers = self._filter_answer_by_temperature(answers,
    #                                                              filter_temperatures)
    #         else:
    #             answers = self._filter_answer_by_temperature(answers,
    #                                                          [float(filter_temperatures)])
    #     if filter_nucleus != 'all':
    #         if type(filter_nucleus) == list:
    #             answers = self._filter_answer_by_nucleus(answers,
    #                                                      filter_nucleus)
    #         else:
    #             answers = self._filter_answer_by_nucleus(answers,
    #                                                      [float(filter_nucleus)])
    #     if filter_presence_penalty != 'all':
    #         if type(filter_presence_penalty) == list:
    #             answers = self._filter_answer_by_presence_penalty(answers,
    #                                                              filter_presence_penalty)
    #         else:
    #             answers = self._filter_answer_by_presence_penalty(answers,
    #                                                          [float(filter_presence_penalty)])
    #
    #     if filter_frequency_penalty != 'all':
    #         if type(filter_frequency_penalty) == list:
    #             answers = self._filter_answer_by_frequency_penalty(answers,
    #                                                               filter_frequency_penalty)
    #         else:
    #             answers = self._filter_answer_by_frequency_penalty(answers,
    #                                                               [float(filter_frequency_penalty)])
    #
    #     answers = sorted(answers, key=lambda x: x[self.PROMPT],)
    #
    #     return answers

    def GetAnswers(self,
                   question,
                   filters={},
                   )-> list:

        answers = self._get_answer(question)

        if len(answers) == 0:
            return list()

        for filter_name in self.FILTER_NAMES:
            try:
                if filters[filter_name] != 'all':
                    answers = self._filter_answers(answers=answers,
                                                   filter_type=filter_name,
                                                   filter_value=filters[filter_name])
                    # check if len is greater than zero
                    if len(answers) == 0:
                        return list()
            except KeyError:
                #  filer not setted:
                pass
        answers = sorted(answers, key=lambda x: x[self.PROMPT],)
        return answers

    def RemoveQuestion(self,
                       question):
        self.data[self.DATA_QUESTIONS].pop(question)


    def _filter_answers(self,
                        answers: str,
                        filter_type: str,
                        filter_value: list):
        return list(filter(lambda x: x[filter_type]==filter_value, answers))

    def _get_answer(self, question):
        return self.data[self.DATA_QUESTIONS][question]

    def UpdateSession(self, session):
        self.data[self.DATA_SESSION] = session

    def GetSession(self):
        return self.data[self.DATA_SESSION]

    def ExportSession(self,
                      filename: str):
        codecs.open(filename, 'w', 'utf-8').write(self.data[self.DATA_SESSION])

    def _load_data(self, filename):
        data = LoadJsonData(filename=filename)
        if data:
            self.data = data
            self.data[self.DATA_QUESTIONS] = defaultdict(list, self.data[self.DATA_QUESTIONS])
            return True
        else:
            return False

    def _save_data(self, filename):
        return SaveJsonData(data=self.data,
                            filename=filename)


# class ParseAnswerFile:
#     def __init__(self):
#         #  store questions asked
#         self.questions = list()
#
#
#         self.QUESTION_ = 'question'
#         self.TEMPERATURE_ = 'temperature'
#         self.ANSWERS_ = 'answers'
#
#         self.QUESTION_DICT = {self.QUESTION_: None,
#                               self.TEMPERATURE_: None,
#                               self.ANSWERS_: list()}
#
#     def t(self, temperature):
#         return round(float(temperature),1)
#
#     def save_question(self,
#                       question):
#         self.questions.append(question)
#
#     def ParseFile(self, filename):
#         quest = deepcopy(self.QUESTION_DICT)
#         answers_list = list()
#
#         with codecs.open(filename, 'r', 'utf-8') as fin:
#             for line in fin.readlines():
#                 line = line.strip()
#                 #  blank line
#                 if not line:
#                     continue
#                 if line.startswith('Q:'):
#                     # # start collecting a new question
#
#                     # save previous results
#                     if quest[self.QUESTION_] != None:
#                         quest[self.ANSWERS_] = answers_list
#                         self.save_question(quest)
#
#                         # reset variables
#                         quest = deepcopy(self.QUESTION_DICT)
#                         answers_list = list()
#
#                     # #  start collecting a new question
#                     question = line.replace('Q:', '').strip()
#                     question, temperature = question.split('--t:')
#                     temperature = self.t(temperature)
#                     question = question.strip()
#                     quest[self.QUESTION_] = question
#                     quest[self.TEMPERATURE_] = temperature
#
#                 if line.startswith('A:'):
#                     answer = line.replace('A:', '').replace('\n', '').strip()
#                     answers_list.append(answer)
#
#             # save last result
#             quest[self.ANSWERS_] = answers_list
#             self.save_question(quest)
#         return self.get_question_data()
#
#     def get_question_data(self):
#         return self.questions
#
#
#
#
# if __name__ == '__main__':
#     filename = 'other/asking knowledge to GPT3-general questions-base-what-is'
#     parser = ParseAnswerFile()
#     from pprint import pprint
#
#     pprint(parser.ParseFile(filename))
#
#     ds = PromptDesignerDataset()
#     prompt_test = '''
#     this is a dev test
#
#     ciao :)
#     '''
#     ds.AddPrompt('test', prompt_test)
#     print(ds.GetPromptNames(),
#           ds.GetQuestions())
#
#     # data = parser.ParseFile(filename)
#     ds.AddQuestionsAnswersSession(filename, 'test')
#     ds.AddQuestionsAnswersSession(filename, 'test2')
#     q = ds.GetQuestions()[-1]
#     a = ds.GetAnswers(q)
#     b = ds.GetAnswers(q,filter_temperatures=[0, 0.5])
#     c = ds.GetAnswers(q, filter_prompts=['test'])
#     d = ds.GetAnswers(q, filter_prompts=['test'], filter_temperatures=[.5])
#     print()
#     pprint(b)
#     print()
#     pprint(c)
#     print()
#     pprint(d)
