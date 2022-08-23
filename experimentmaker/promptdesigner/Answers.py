import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
# from promptdesigner.prompt_designer_dataset import PromptDesignerDataset
# from promptdesigner.export_answers import ExportSessionData
from promptdesignerdataset.dataset import PromptDesignerDataset
from promptdesigner.Export import ExportSessionData

class AnswersInterface(tk.Frame):
    _ANSWER_PATTERN_HEADER = 'Engine: {engine} | prompt name: {prompt}\n  - Temperature: {temperature}, Nucleus:{nucleus}, Presence Penalty: {presence_penalty}, Frequency Penalty: {frequency_penalty}'
    _ANSWER_PATTERN_SINGLE = '\tA: {answer}'
    _ANSWER_FILLER = ''#'=' * 80


    def __init__(self, parent, data: PromptDesignerDataset):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title('Answers'
                          )
        self.data = data

        self.__init_variables__()
        self._create_frame()
        self.question_to_retrieve_string.trace_variable('w', self._question_changed)

        self.engine_str.set('all')
        self.temperatures_str.set('all')
        self.nucleus_str.set('all')
        self.frequency_penality.set('all')
        self.presence_penality_str.set('all')

        self.engine_str.trace_variable('w', self._update_answer())
        self.temperatures_str.trace_variable('w', self._update_answer)
        self.prompts_str.trace_variable('w',self._update_answer)
        self.nucleus_str.trace_variable('w',self._update_answer)
        self.presence_penality_str.trace_variable('w',self._update_answer)
        self.frequency_penality_str.trace_variable('w',self._update_answer)

        #  initialize class
        self._load_questions()
        # self._load_prompts_name()

    def __init_variables__(self):
        self.question_to_retrieve_string = tk.StringVar()
        #  list temperatures found
        self.temperatures_list = tk.Variable()
        #  chk status
        self.temperatures_status = tk.BooleanVar()
        #  temperature value
        self.temperatures_str = tk.StringVar()
        self.engine_str = tk.StringVar()
        #  list nucleus found
        self.nucleus_list = tk.Variable()
        #  chk status
        self.nucleus_status = tk.BooleanVar()
        #  nucleus value
        self.nucleus_str = tk.StringVar()

        #  list of prompt tested
        self.prompts_list = tk.Variable()
        #  chk status
        self.prompts_status = tk.BooleanVar()
        #  prompt name
        self.prompts_str = tk.StringVar()

        #  list presence_penality found
        self.presence_penality_list = tk.Variable()
        #  chk status
        self.presence_penality_status = tk.BooleanVar()
        #  presence_penality value
        self.presence_penality_str = tk.StringVar()

        #  list frequency_penality found
        self.frequency_penality_list = tk.Variable()
        #  chk status
        self.frequency_penality_status = tk.BooleanVar()
        #  frequency_penality value
        self.frequency_penality_str = tk.StringVar()



    def _create_frame(self):
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill='both',
                        expand=True)

        frm_cmb = tk.Frame(self.frame)
        frm_cmb.pack(side='top',
                     fill='x',
                     expand=False)
        tk.Label(frm_cmb,
                 text='Select Question:',
                 anchor='center').pack(side='left', expand=False)
        self.question_to_retrieve = ttk.Combobox(frm_cmb,
                                                 width=35,
                                                 textvariable=self.question_to_retrieve_string,
                                                 # validatecommand=self._prompt_changed
                                                 )
        self.question_to_retrieve.bind('<<ComboboxSelected>>', self._question_changed)
        self.question_to_retrieve.pack(side='left',
                                       fill='x',
                                       expand=False)
        # frm_cmb2 = tk.Frame(self.frame)
        # frm_cmb2.pack(side='top',
        #              fill='x',
        #              expand=False)
        tk.Button(frm_cmb,
                  text='Delete this Question',
                  command=self._delete_question,
                  anchor='center',
                  ).pack(side='left')
        tk.Button(frm_cmb,
                  text='Export Answers',
                  anchor='center',
                  command=self._export_answer_data).pack(side='left')

        # tk.Button(frm_cmb2,
        #           text='Load AnswerData',
        #           command=self._load_answers_data,
        #           anchor='center').pack(side='left')

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
        # tk.Checkbutton(frm_temperatures,
        #                text='filter by Temperatures',
        #                anchor='w',
        #                variable=self.temperatures_status,
        #                ).pack(side='left')
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

        frm_presence_penality = tk.Frame(frm_opt_sx)
        frm_presence_penality.pack(side='top', fill='x')
        tk.Label(frm_presence_penality,
                       text='filter by presence_penality',
                       anchor='w').pack(side='left')
        self.presence_penality = ttk.Combobox(frm_presence_penality,
                                         width=5,
                                         textvariable=self.presence_penality_str)
        self.presence_penality.pack(side='right',
                                   fill='y')

        frm_frequency_penality = tk.Frame(frm_opt_sx)
        frm_frequency_penality.pack(side='top', fill='x')
        tk.Label(frm_frequency_penality,
                       text='filter by frequency_penality',
                       anchor='w').pack(side='left')
        self.frequency_penality = ttk.Combobox(frm_frequency_penality,
                                         width=5,
                                         textvariable=self.frequency_penality_str)
        self.frequency_penality.pack(side='right',
                                   fill='y')


        # frm_opt_dx = tk.Frame(frm_opt_body, bg='green')
        # frm_opt_dx.pack(
        #            side='right',
        #            fill='x',
        #            expand=False)
        # tk.Label(frm_opt_dx, text='TEST').pack()

        self.answers_retrieved = tk.Text(self.frame)
        self.answers_retrieved.pack(fill='both',
                                    expand=True)

    def _collect_parameters(self)-> dict:
        def fix_type(parameter):
            try:
                parameter = self.data.t(parameter)
            except:
                # 'all'
                pass
            return  parameter

        parameters = self.data.GetAnswerDataEmptyDict()

        parameters[self.data.PROMPT] = self.prompts_str.get()
        parameters[self.data.TEMPERATURE] = fix_type(self.temperatures_str.get())
        parameters[self.data.NUCLEUS] = fix_type(self.nucleus_str.get())
        parameters[self.data.FREQUENCY_PENALTY] = fix_type(self.frequency_penality_str.get())
        parameters[self.data.PRESENCE_PENALTY] = fix_type(self.presence_penality_str.get())
        parameters[self.data.ENGINE] = self.engine_str.get()

        return parameters

    def _update_answer(self, *event):
        parameters = self._collect_parameters()
        answers = self.data.GetAnswers(self.question_to_retrieve_string.get(),
                                       filters=parameters)
        answers_str_list = list()
        for answer in answers:
            answer = self._format_answer(answer)
            answers_str_list.append(answer)

        answers_str = '\n'.join(answers_str_list)
        #  clear text box
        self.answers_retrieved.delete('1.0', 'end')
        #  update textbox
        self.answers_retrieved.insert('end',
                                      answers_str)

    def _compose_answer_pattern(self,
                                header,
                                body,
                                foot):
        return '\n'.join([foot,
                          header,
                          body,
                          foot])

    def _format_answer(self, answer):
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

    def _question_changed(self, *event):
        self._update_filters_comboboxes()
        self._update_answer()

    def _update_filters_comboboxes(self, *event):
        val = ['all']
        val.extend( self.data.GetPromptsOfQuestion(self.question_to_retrieve_string.get()))
        self.prompts['values'] = val
        self.prompts_str.set('all')

        val = ['all']
        val.extend( self.data.GetEnginesOfQuestion(self.question_to_retrieve_string.get()))
        self.engines['values'] = val
        self.engine_str.set('all')

        val = ['all']
        val.extend(self.data.GetTemperaturesOfQuestion(self.question_to_retrieve_string.get()))
        self.temperatures['values'] = val
        self.temperatures_str.set('all')

        val = ['all']
        val.extend(self.data.GetNucleusOfQuestion(self.question_to_retrieve_string.get()))
        self.nucleus['values'] = val
        self.nucleus_str.set('all')

        val = ['all']
        val.extend(self.data.GetPresencePenalityOfQuestion(self.question_to_retrieve_string.get()))
        self.presence_penality['values'] = val
        self.presence_penality_str.set('all')

        val = ['all']
        val.extend(self.data.GetFrequencyPenalityOfQuestion(self.question_to_retrieve_string.get()))
        self.frequency_penality['values'] = val
        self.frequency_penality_str.set('all')

    def _load_questions(self):
        try:
            self.question_to_retrieve['values'] = [x for x in sorted(self.data.GetQuestions(), key=lambda x: len(x), reverse=False) if len(x.strip())>0]
            self.question_to_retrieve_string.set(self.question_to_retrieve['values'][0])
        except:
            self.question_to_retrieve_string.set('')


        self._update_filters_comboboxes()

        self._update_answer()

    def _delete_question(self, *event):
        ans = messagebox.askyesno('delete answers?',
                                  'Are you sure to delete this question?')
        if ans == tk.YES:
            self.data.RemoveQuestion(self.question_to_retrieve_string.get())
            self._load_questions()
            self.data.UpdateData()


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
    # def _load_prompts_name(self):
    #     self.prompts['values'] = sorted(self.data.GetPromptNames(), reverse=False)
    #     self.prompts_str.set(self.prompts['values'][0])

    def _add_answer_data(self, *event):
        filename = Path(filedialog.askopenfilename())
        prompt_name = self.prompts_str.get()
        if filename.name:
            self.data.AddQuestionsAnswersSession(filename=filename.absolute(),
                                                 prompt_name=prompt_name)
            self._load_questions()
            # self._load_prompts_name()
            messagebox.showinfo('',
                                    'answers data added')

    def _update_answers_data(self, *event):
        if self.data.UpdateData():
            messagebox.showinfo('',
                                'answers data updated')

    def _save_answers_data(self, *event):
        # ask for filename
        filename = Path(filedialog.asksaveasfilename())
        if filename.name:
            if self.data.SaveData(filename.absolute()):
                messagebox.showinfo('',
                                    'answers data saved')

    def show_prompt(self, *event):
        if len(self.lst_prompts.curselection()) != 1:
            return

        prompt_name = self.lst_prompts.get(self.lst_prompts.curselection())
        prompt = self.data.GetPrompt(prompt_name)

        print(prompt)

        p = tk.Toplevel(self.parent)
        p.title(prompt_name)
        text = tk.Text(p)
        text.pack(fill='both', expand=True)
        text.insert('end', prompt)
        p.mainloop()

    def _export_answer_data(self, *event):
        export = tk.Toplevel(self.parent)
        app = ExportSessionData(export, self.data)
        export.mainloop()


if __name__ == '__main__':
    filename = '/Users/patrizio/Documents/ANSWERS-DEV-TEST.json'
    ds = PromptDesignerDataset()
    ds.LoadData(filename=filename)

    root = tk.Tk()
    AnswersInterface(root, ds)
    root.mainloop()