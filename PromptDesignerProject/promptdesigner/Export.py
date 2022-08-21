import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
# from promptdesigner.prompt_designer_dataset import PromptDesignerDataset
from promptdesignerdataset.dataset import PromptDesignerDataset
from fpdf import FPDF

class ExportSessionData(tk.Frame):
    _ANSWER_PATTERN_HEADER = 'Engine: {engine} | prompt name: {prompt}\n  - Temperature: {temperature}, Nucleus:{nucleus}, Presence Penalty: {presence_penalty}, Frequency Penalty: {frequency_penalty}'
    _ANSWER_PATTERN_SINGLE = '\tA: {answer}'
    _ANSWER_FILLER = ''#'=' * 80

    ENGINES_LIST = [
        'text-davinci-001',
        'text-curie-001',
        'text-babbage-001',
        'text-ada-001']

    def __init__(self,
                 parent,
                 data: PromptDesignerDataset):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Export Answers")
        self.data = data

        self.__init_variables__()
        self._create_frame()
        self._fill_filters_comboboxes()

        self.temperatures_str.trace_variable('w', self.retrieve_questions_list)
        self.engine_str.trace_variable('w', self.retrieve_questions_list)
        self.prompts_str.trace_variable('w', self.retrieve_questions_list)
        self.nucleus_str.trace_variable('w', self.retrieve_questions_list)
        self.presence_penalty_str.trace_variable('w', self.retrieve_questions_list)
        self.frequency_penalty_str.trace_variable('w', self.retrieve_questions_list)
        self.retrieve_questions_list()

    def __init_variables__(self):
        self.question_to_retrieve_string = tk.StringVar()
        #  temperature value
        self.temperatures_str = tk.StringVar()
        #  nucleus value
        self.nucleus_str = tk.StringVar()
        #  prompt name
        self.prompts_str = tk.StringVar()
        # engine
        self.engine_str = tk.StringVar()
        #  presence_penality value
        self.presence_penalty_str = tk.StringVar()
        #  frequency_penality value
        self.frequency_penalty_str = tk.StringVar()

    def _create_frame(self):
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill='both',
                        expand=True)

        frm_opt_body = tk.Frame(self.frame)
        frm_opt_body.pack(
                   side='top',
                   fill='x',
                   expand=False)

        frm_opt_sx = tk.Frame(frm_opt_body)
        frm_opt_sx.pack(
                   side='left',
                   fill='x',
                   expand=False)

        frm_temperatures = tk.Frame(frm_opt_sx)
        frm_temperatures.pack(side='top', fill='x')
        tk.Label(frm_temperatures,
                 text='filter by Temperatures',
                 anchor='w').pack(side='left')
        self.temperatures = ttk.Combobox(frm_temperatures,
                                         width=5,
                                         textvariable=self.temperatures_str)
        self.temperatures.pack(side='right',
                                   fill='y')

        frm_nucleus = tk.Frame(frm_opt_sx)
        frm_nucleus.pack(side='top', fill='x')
        tk.Label(frm_nucleus,
                   text='filter by nucleus',
                   anchor='w').pack(side='left')
        self.nucleus = ttk.Combobox(frm_nucleus,
                                         width=5,
                                         textvariable=self.nucleus_str)
        self.nucleus.pack(side='right',
                                   fill='y')
        frm_engines = tk.Frame(frm_opt_sx)
        frm_engines.pack(side='top', fill='x')
        ttk.Label(frm_engines,
                  text='filter by Engine',
                  anchor='w').pack(side='left')
        self.engines = ttk.Combobox(frm_engines,
                                    width=25,
                                    textvariable=self.engine_str)
        self.engines.pack(side='right',
                          fill='y')
        frm_prompts = tk.Frame(frm_opt_sx)
        frm_prompts.pack(side='top', fill='x')
        ttk.Label(frm_prompts,
                        text='filter by Prompt',
                        anchor='w').pack(side='left')
        self.prompts = ttk.Combobox(frm_prompts,
                                    width=25,
                                    textvariable=self.prompts_str)
        self.prompts.pack(side='right',
                              fill='y')

        frm_presence_penality = tk.Frame(frm_opt_sx)
        frm_presence_penality.pack(side='top', fill='x')
        tk.Label(frm_presence_penality,
                       text='filter by presence_penality',
                       anchor='w').pack(side='left')
        self.presence_penality = ttk.Combobox(frm_presence_penality,
                                              width=5,
                                              textvariable=self.presence_penalty_str)
        self.presence_penality.pack(side='right',
                                    fill='y')

        frm_frequency_penality = tk.Frame(frm_opt_sx)
        frm_frequency_penality.pack(side='top', fill='x')
        tk.Label(frm_frequency_penality,
                       text='filter by Frequency Penality',
                       anchor='w').pack(side='left')
        self.frequency_penality = ttk.Combobox(frm_frequency_penality,
                                               width=5,
                                               textvariable=self.frequency_penalty_str)
        self.frequency_penality.pack(side='right',
                                   fill='y')


        frm_opt_dx = tk.Frame(frm_opt_body, bg='green')
        frm_opt_dx.pack(
                   side='right',
                   fill='x',
                   expand=False)
        tk.Label(frm_opt_dx, text='TEST').pack()

        frm_questions_to_export = tk.Frame(self.frame)
        frm_questions_to_export.pack(fill='both',
                                         expand=True)

        self.questions_list_retrieved = tk.Listbox(frm_questions_to_export,
                                                   selectmode=tk.MULTIPLE,
                                                   exportselection=False,
                                                   )
        # self.questions_list_retrieved.bind('<Double-Button>', self.show_answer_preview)
        self.questions_list_retrieved.pack(side='left',
                                           fill='both',
                                           expand=True)

        ys = ttk.Scrollbar(frm_questions_to_export,
                           orient='vertical',
                           command=self.questions_list_retrieved.yview)
        self.questions_list_retrieved['yscrollcommand'] = ys.set
        ys.pack(side='right', fill='y')

        tk.Button(self.frame,
                  text='Export Data',
                  command=self.export_data).pack(fill='x')

    # def export_data(self):
    #     filename = Path(filedialog.asksaveasfilename())
    #     parameters = self._collect_parameters()
    #     if filename.name:
    #         questions_to_export = [self.questions_list_retrieved.get(index)
    #                                for index in self.questions_list_retrieved.curselection()]
    #         if questions_to_export:
    #             filename = str(filename.absolute())
    #             with codecs.open(filename, 'w', 'utf-8') as fout:
    #                 for question in questions_to_export:
    #                     answers = self.data.GetAnswers(question=question,
    #                                                    filters=parameters)
    #
    #                     # write question
    #                     question_txt = '\n Question: {}\n'.format(question)
    #                     fout.write(question_txt)
    #                     for answer in answers:
    #                         for ans in answer[self.data.ANSWERS]:
    #                             answer_txt = '\t\tA: {}\n'.format(ans)
    #                             # write answer
    #                             fout.write(answer_txt)
    #
    #                     # write end of question
    #                     eoq = '='*80
    #                     eoq_txt = '\n{}\n\n'.format(eoq)
    #                     fout.write(eoq_txt)
    #             messagebox.showinfo('', 'answers data exported successfully :) ')
    def export_data(self):
        color_dark_blue = (0, 0, 139)
        color_black = (0, 0, 0)
        color_bk = (255, 255, 255)
        color_red = (220, 20, 60)
        color_blue = (0, 0, 255)
        color_confl_blue = (100, 149, 237)
        color_blueviolette = (138, 43, 226)

        # width, height = A4
        width = 200 # mm

        filename = Path(filedialog.asksaveasfilename(initialdir=str(Path(__file__).absolute()),
                                                     title="Select file to save",
                                                     filetypes=(('.pdf file', '*.pdf'),)))
        parameters = self._collect_parameters()
        if filename.name:
            questions_to_export = [self.questions_list_retrieved.get(index)
                                   for index in self.questions_list_retrieved.curselection()]
            if questions_to_export:
                fileout = str(filename.absolute())

                pdf = FPDF()
                pdf.set_margins(1.5, 1, 1.5)
                pdf.add_page()
                pdf.set_author('Prompt Designer')
                for question in questions_to_export:
                    pdf.set_text_color(*color_black)
                    pdf.set_font("Arial", size=15)
                    pdf.multi_cell(width, 10, txt=question)  # , align="J", )

                    answers = self.data.GetAnswers(question)
                    for answer in answers:
                        header_answer = self._ANSWER_PATTERN_HEADER.format(engine=answer[self.data.ENGINE],
                                                                           prompt=answer[self.data.PROMPT],
                                                                           temperature=answer[self.data.TEMPERATURE],
                                                                           nucleus=answer[self.data.NUCLEUS],
                                                                           presence_penalty=answer[
                                                                               self.data.PRESENCE_PENALTY],
                                                                           frequency_penalty=answer[
                                                                               self.data.FREQUENCY_PENALTY],
                                                                           )
                        pdf.set_font("Arial", size=8)
                        pdf.set_text_color(*color_red)
                        pdf.multi_cell(width,
                                       5,
                                       txt=header_answer,
                                       # align="J",
                                       )

                        for ans_text in answer[self.data.ANSWERS]:
                            answer_text = '--  A: {}'.format(ans_text)
                            pdf.set_font("Arial", size=12)
                            pdf.set_text_color(*color_confl_blue)
                            pdf.multi_cell(width, 10,
                                           txt=answer_text,
                                           align="J",
                                           )

                pdf.output(fileout)

                messagebox.showinfo('', 'answers data exported successfully :) ')

    def _compose_answer_pattern(self,
                                header,
                                body,
                                foot)-> str:
        return '\n'.join([foot,
                          header,
                          body,
                          foot])

    def format_answer(self, answer)-> str:
        #  collect answers collection
        answers = [self._ANSWER_PATTERN_SINGLE.format(answer=ans) for ans in answer[self.data.ANSWERS]]
        answers_str = '\n'.join(answers)

        return self._compose_answer_pattern(
            header=self._ANSWER_PATTERN_HEADER.format(engine=answer[self.data.ENGINE],
                                                      prompt=answer[self.data.PROMPT],
                                                      temperature=answer[self.data.TEMPERATURE],
                                                      nucleus=answer[self.data.NUCLEUS],
                                                      presence_penalty=answer[self.data.PRESENCE_PENALTY],
                                                      frequency_penalty=answer[self.data.FREQUENCY_PENALTY],
                                                      ),
            body=answers_str,
            foot=self._ANSWER_FILLER)


    def _fill_filters_comboboxes(self, *event):
        val = ['all']
        val.extend( self.data.GetPromptNames())
        self.prompts['values'] = val
        self.prompts_str.set('all')

        val = ['all']
        val.extend(self.data.GetEngines())
        self.engines['values'] = val
        self.engine_str.set('all')

        val = ['all']
        val.extend(self.data.GetTemperatures())
        self.temperatures['values'] = val
        self.temperatures_str.set('all')

        val = ['all']
        val.extend(self.data.GetNucleus())
        self.nucleus['values'] = val
        self.nucleus_str.set('all')

        val = ['all']
        val.extend(self.data.GetPresencePenalty())
        self.presence_penality['values'] = val
        self.presence_penalty_str.set('all')

        val = ['all']
        val.extend(self.data.GetFrequencyPenalty())
        self.frequency_penality['values'] = val
        self.frequency_penalty_str.set('all')

    def _collect_parameters(self):
        def fix_type(parameter):
            try:
                parameter = self.data.t(parameter)
            except:
                # 'all'
                pass
            return parameter

        parameters = self.data.GetAnswerDataEmptyDict()
        parameters[self.data.ENGINE] = self.engine_str.get()
        parameters[self.data.PROMPT] = self.prompts_str.get()
        parameters[self.data.TEMPERATURE] = fix_type(self.temperatures_str.get())  # self.data.t(self.temperature_str.get())
        parameters[self.data.NUCLEUS] = fix_type(self.nucleus_str.get())  # self.data.t(self.nucleus_str.get())
        parameters[self.data.FREQUENCY_PENALTY] = fix_type(self.frequency_penalty_str.get())  # self.data.t(self.frequency_penalty_str.get())
        parameters[self.data.PRESENCE_PENALTY] = fix_type(self.presence_penalty_str.get())  # self.data.t(self.presence_penalty_str.get())

        return parameters

    def retrieve_questions_list(self, *event):
        questions = self.data.GetQuestions()
        questions_filtered = list()
        parameters = self._collect_parameters()

        for question in questions:
            answers = self.data.GetAnswers(question=question,
                                           filters=parameters)
            if answers:
                questions_filtered.append(question)
        # print('here')
        self.questions_list_retrieved.delete(0, 'end')
        for question in  questions_filtered:
            self.questions_list_retrieved.insert('end', question)

    def _load_answers_data(self, *event):
        filename = Path(filedialog.askopenfilename())
        if filename:
            if self.data.LoadData(filename.absolute()):
                messagebox.showinfo('',
                                    'answers data loaded')
                self._load_questions()
                # self._load_prompts_name()
                self._set_title(filename)
    #
    # def show_answer_preview(self, *event):
    #     try:
    #         question = self.questions_list_retrieved.get(self.questions_list_retrieved.curselection()[-1])
    #     except IndexError:
    #         return
    #
    #     preview = tk.Toplevel(self.parent)
    #     preview.title(question)
    #
    #     txt = tk.Text(preview)
    #     txt.pack(fill='both')
    #     answers = self.data.GetAnswers(question=question,
    #                                    filter_prompts=self.prompts_str.get(),
    #                                    filter_temperatures=self.temperatures_str.get(),
    #                                    filter_nucleus=self.nucleus_str.get(),
    #                                    filter_presence_penalty=self.presence_penalty_str.get(),
    #                                    filter_frequency_penalty=self.frequency_penalty_str.get())
    #     for answer in answers:
    #       answer_txt = self.format_answer(answer=answer)
    #     txt.insert('end', answer_txt)
    #
    #     preview.mainloop()

#
# if __name__ == '__main__':
#     filename = '/Users/patrizio/Documents/ANSWERS-DEV-TEST.json'
#     ds = PromptDesignerDataset()
#     ds.LoadData(filename=filename)
#
#     root = tk.Tk()
#     ExportSessionData(root, ds)
#     root.mainloop()