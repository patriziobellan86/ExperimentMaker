from promptdesignerdataset.dataset import PromptDesignerDataset, LoadJsonData, SaveJsonData
from copy import deepcopy
from itertools import chain
from collections import OrderedDict


class Pipeline:
    INPUT_TYPE_ENTIRE = 'file-type-entire'
    INPUT_TYPE_LIST = 'file-type-list'

    def __init__(self):
        self.data = {'file': None, # this file path
                    'input-files' : list(),

                    'output-script-modules': list(),
                    'output-item-filter-modules': list(),
                    # 'input-text-filename': None,
                    # 'input-type': None,

                    'apply-script-output': list(),
                    'script-name': None,
                    'pipeline-name': None,
                    'pipeline': list(),

                    'gpt3-settings': {},
                    'steps': 0,

                     'prompts': list()}

    def AddPrompt(self,
                  prompt_name,
                  prompt_template):
        #  add a prompt template
        self.data['prompts'].append(tuple([prompt_name,
                                           prompt_template]))

    def GetPromptNames(self):
        #  return prompts names
        prompt_names = [name for name, template in self.data['prompts']]

        return prompt_names

    def GetPrompt(self,
                  prompt_name):
        #  return a prompt template

        prompt_item = list(filter(lambda x: x[0] == prompt_name, self.data['prompts']))[0]
        prompt_template = prompt_item[1]

        return prompt_template

    def RemoveItem(self,
                   item_name):

        for n_, item in enumerate(self.GetItems()):
            if item.Name() == item_name:
                self.data['pipeline'].pop(n_)


    def __len__(self):
        return len(self.data['pipeline'])

    def AddOutputScriptModule(self, module_path):
        self.data['output-script-modules'].append(module_path)

    def AddOutputFilter(self,
                        filter_name):
        self.data['apply-script-output'].append(filter_name)

    def ClearOutputFilters(self):
        self.data['apply-script-output'] = list()

    def GetOutputFilters(self):
        return self.data['apply-script-output']

    def GetOutputScriptModules(self):
        return self.data['output-script-modules']

    def AddItemOutputScriptModule(self, module_path):
        self.data['output-item-filter-modules'].append(module_path)

    def GetItemOutputScriptModules(self):
        return self.data['output-item-filter-modules']

    def SetFile(self,
                file_):
        self.data['file'] = file_

    def GetFile(self):
        return self.data['file']

    def GetGPT3Settings(self):
        return self.data['gpt3-settings']

    def AddGPT3Settings(self,
                        settings):
        self.data['gpt3-settings'] = settings

    def SetName(self, name):
        self.data['pipeline-name'] = name

    def GetName(self):
        return self.data['pipeline-name']

    def Clear(self):
        self.data['input-files'].clear()
        self.data['output-script-modules'].clear()
        self.data['output-item-filter-modules'].clear()
        self.data['apply-script-output'].clear()
        self.data['pipeline'].clear()
        self.data['prompts'].clear()

        self.reset_step_counter()

    def _increment_step(self):
        self.data['steps'] += 1

    def reset_step_counter(self):
        self.data['steps'] = 0

    def total_steps(self):
        return self.data['steps']

    def AddItem(self,
                item,
                autoset_step=True):
        print(type(item))
        #  autoset set automatically set the step,
        # use false in load to manually set the step
        self._increment_step()
        if autoset_step:
            item.SetStep(self.total_steps())
        self.data['pipeline'].append(item)

    def PrepareDataToSave(self):
        #  return a dict of the pipeline data
        data_to_save = deepcopy(self.data)
        data_to_save['pipeline'] = [item.GetItemDict() for item in self.GetItems()]
        return data_to_save

    def SavePipeline(self, filename):
        data_to_save = self.PrepareDataToSave()
        data_to_save['file'] = filename

        return SaveJsonData(data_to_save, filename)

    def AddInputFile(self, inputfile_dict):
        # 'file_': None,
        # 'input-type': None,
        # 'content'
        # 'mnemonic-name
        self.data['input-files'].append(inputfile_dict)

    def GetInputFilesMnemonicNames(self):
        return [item['mnemonic-name'] for item in self.data['input-files']]

    def GetItem(self,
                item_name):
        for item in self.data['pipeline']:
            if item.Name() == item_name:
                return item
        raise AttributeError('Item not present in the pipeline')

    def GetInputFileContent(self,
                            mnemonic_name):
        for inp in self.data['input-files']:
            if inp['mnemonic-name'] == mnemonic_name:
                return inp['content']

    def GetInputFilesItems(self):
        return self.data['input-files']

    def GetItems(self):
        items = list()

        unsorted = [item for item in self.data['pipeline']]
        return sorted(unsorted, key=lambda x: x.GetStep())

    def LoadPipelilne(self, filename):
        data = LoadJsonData(filename)
        if data:
            # promptdesignerdataset = deepcopy(promptdesignerdataset)
            try:

                self.SetName(data['pipeline-name'])
                #  add input files
                for fileitem in data['input-files']:
                    self.AddInputFile(fileitem)

                self.AddGPT3Settings(data['gpt3-settings'])
                self.SetFile(data['file'])

                for mod in data['output-script-modules']:
                    self.AddOutputScriptModule(mod)

                for mod in data['output-item-filter-modules']:
                    self.AddItemOutputScriptModule(mod)
                #  add output scripts to list box
                for filter in data['apply-script-output']:
                    self.AddOutputFilter(filter)

                for item in data['pipeline']:
                    # input_item = {'apply-item-filters': item['input-item']['apply-item-filters'],
                    #               'input-bindings': item['input-item']['input-bindings'],
                    #               }
                    pitem = PipelineItem()
                    pitem.SetData(item)
                    # pitem.SetData(name=item['name'],
                    #               prompt=item['prompt'],
                    #               input_item=item['input_item'])
                    # pitem.SetStep(item['step'])
                    self.AddItem(deepcopy(pitem))

                for prompt_name, prompt_template in data['prompts']:
                    self.AddPrompt(prompt_name, prompt_template)
            except KeyError:
                print('FILE NOT VALID.')

    def ExportResults(self):
        # return a dict of results
        results = OrderedDict()
        for item in self.GetItems():
            item_data = {'step': item.GetStep(),
                         'results-raw': item.data['results-raw'],
                         'results-filtered': item.data['results-filtered']} #  the last one! }
            results[item.Name()] = item_data
        return results

    def ClearResults(self):
        for item in self.GetItems():
            item.ClearResults()


class PipelineItem:
    """
    name = self.pipeline_item_name.get(),
    input_item = item_input,
    apply_filter_to_output = self.chk_apply_filter_to_pipeline_item_output.get(),
    filter_on_output_name = self.pipeline_output_filter_name.get())

        item_input = {'setting-type': self.experiment_setting_range_type.get(),
                      'apply-filter-script': self.chk_apply_filter_to_pipeline_item_output.get(),
                      'filter-script-name': self.pipeline_item_output_filter_name.get(),
                      'input-bindings': list()
                      }
        item_input['input-bindings'].append({'prompt-key': child[0],
                                                 'key-value': child[1],
                                                 'type': child[2]})

    """

    def __init__(self):
        self.data = {'input_item': {
                                    'apply-item-filters': list(),
                                    'input-bindings': list(),
                                    },
                     'results-raw': list(),
                     'results-filtered': list()}
    def SetData(self,
                data):
        self.data = data


    def SetInput(self,
                 input_item):
        self.data['input_item'] = input_item
    # def SetData(self,
    #              name,
    #              prompt,
    #              input_item,
    #              ):
    #     self.promptdesignerdataset['name'] = name
    #     self.promptdesignerdataset['prompt'] = prompt
    #     self.promptdesignerdataset['input_item'] = input_item

    def SetPrompt(self,
                  prompt):
        self.data['prompt'] = prompt

    def GetPrompt(self):
        return self.data['prompt']

    def SetStep(self, step_n):
        self.data['step'] = step_n

    def GetStep(self):
        return self.data['step']

    def GetItemFilterNames(self):
        """
         Generator of filter to apply to the item output
        :return:
        """
        # ['input_item']{'apply-item-filters': [i for i in self.lst_item_filters.get(0, 'end')],
        #                      # self.chk_apply_filter_to_pipeline_item_output.get(),
        #                      'filter-script-name': self.pipeline_item_output_filter_name.get(),
        #                      'input-bindings': list()
        #                      }
        for filter in self.data['input_item']['apply-item-filters']:
            yield filter

    def GetPromptName(self):
        return self.data['prompt']

    def AddResultsRaw(self,
                      result,
                      key_value_pair):
        #  results is the result of GPT
        #  key_value_pair is the dict of k,v pairs - prompt key, value
        self.data['results-raw'].append({'result': result,
                                         'key-value-pair': key_value_pair})
        # self.promptdesignerdataset['results-raw'] = {'result': result,
        #                             'key-value-pair': key_value_pair}


    def AddResultsFiltered(self,
                           results,
                           # key_value_pair,
                           filter_name):
        # self.promptdesignerdataset['results-filtered'].extend([{'result': results,
        self.data['results-filtered'].append([{'result': results,
        #                                       'key-value-pair': key_value_pair,
                                              'filter-name': filter_name}])


    def GetResultsContent(self):
        # return the results raw if no filter is applied.
        results = list()
        if self.data['results-filtered']:
            for item in self.data['results-filtered'][-1]:
                results.append(item['result'])
            #  flatten the list
            results = list(chain(*results))

        else:
            for item in self.data['results-raw']:
                results.append(item['result'])
            # if len(results) > 1:
            #     results = list(chain(*results))
        return results
    #
    # def GetResults(self):
    #     # return the results raw if no filter is applied.
    #
    #     #  always return a list and a list of dict
    #
    #     results = list()
    #     params = list()
    #
    #     if self.promptdesignerdataset['results-filtered']:
    #         return self.promptdesignerdataset['results-filtered'][-1]
    #         for item in self.promptdesignerdataset['results-filtered'][-1]:
    #             results.append(item.promptdesignerdataset['result'])
    #             params.append()
    #     else:
    #         print('here')
    #
    #         for item in self.promptdesignerdataset['results-raw']:
    #             results.append(item['result'])
    #     return results, params

    def ClearResults(self):
        self.data['results-raw'].clear()
        self.data['results-filtered'].clear()

    def GetPromptParameters(self):
        parameters = dict()
        for row in self.data['input_item']['input-bindings']:
            parameters[row['prompt-key']] = row['key-value']

        return parameters

    def GetItemDict(self):
        return self.data

    def GetTreeItem(self):
        return  (self.data['name'],
                 self.data['prompt'],
                 '; '.join(['({}= {})'.format(item[list(item.keys())[0]], item[list(item.keys())[1]])
                            for item in self.data['input_item']['input-bindings']]).strip(),
                 self.data['input_item']['apply-item-filters'])

    def Name(self):
        return self.data['name']
    def SetName(self, name):
        self.data['name'] = name
