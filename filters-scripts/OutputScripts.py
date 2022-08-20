import codecs
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from copy import deepcopy
from itertools import chain
import os

_ACTIVITY = 'Activity'
_PARTICIPANT = "Participant"
_ACTIVITYPARTICIPANT = "Activity-Participant"
_FLOW = "Flow"

def OrderResults(results):
    results = deepcopy(results)
    results_keys = list(results.keys())
    keys_step_n_pairs = [(k, results[k]['step']) for k in results_keys]
    keys_step_n_pairs_ordered = sorted(keys_step_n_pairs, key=lambda x: x[1])
    keys_ordered = [k for k, s in keys_step_n_pairs_ordered]
    results_ordered = {k: results[k] for k in keys_ordered}
    return results_ordered

def GetResultItem(step_name,
                  results):
    results = deepcopy(results)

    for key in results:
        if key == step_name:
            return results[key]

def GetResultsContent(result_step):
    #  GET THE CONTENT FROM A RESULTS_STEP

    results_content = list()
    if result_step['results-filtered']:
        for item in result_step['results-filtered'][-1]:
            results_content.append(item['result'])
        #  flatten the list
        results_content = list(chain(*results_content))

    else:
        for item in result_step['results-raw']:
            results_content.append(item['result'])
        # if len(results) > 1:
        #     results = list(chain(*results))
    return results_content

def GetResultOutputContent(step_name,
              results):
    #  GET THE OUTPUT FROM A LIST OF RESULTS
    # results = deepcopy(results)
    # return the results raw if no filter is applied.
    results_content = list()
    if results[step_name]['results-filtered']:
        for item in results[step_name]['results-filtered'][-1]:
            results_content.append(item['result'])
        #  flatten the list
        results_content = list(chain(*results_content))

    else:
        for item in results[step_name]['results-raw']:
            results_content.append(item['result'])
        # if len(results) > 1:
        #     results = list(chain(*results))
    return results_content


class output_base:
    def __init__(self):
        self.filaname = None

    def ask_save_filename(self):
        app = tk.Tk()
        app.geometry('0x0')
        filename = Path(filedialog.asksaveasfilename())
        if filename.name:
            self.filename = str(filename.absolute())
            return self.filename
        else:
            return False

    def Parse(self):
        raise NotImplementedError

class CreateOntologyIstance(output_base):
    def __init__(self,
                 step_name,
                 ontology_params):
        super(CreateOntologyIstance, self).__init__()

        self.step_name = step_name
        self.ontology_params = ontology_params

    def Parse(self,
              results):
        results = OrderResults(results)
        step_results = GetResultItem(self.step_name, results)
        results_content = GetResultsContent(step_results)
        return results_content

class ParseActivityIstances(CreateOntologyIstance):
    def __init__(self):
        super(ParseActivityIstances, self).__init__('step1', {})
    #
class ParseActivityParticipantIstances(CreateOntologyIstance):
    def __init__(self):
        super(ParseActivityParticipantIstances, self).__init__('step1', {})
    #
    # def Parse(self,
    #           results):
    #     # if not self.ask_save_filename(): return
    #     super_step_results = super(ParseActivityIstances, self).Parse(results)
    #     activities_list = GetResultsContent(super_step_results)
    #     print('--- activity list ---')
    #     print(activities_list)
    #     # codecs.open(self.filename, 'w', 'utf8').write('\n\n--- activity list ---\n')
    #     # codecs.open(self.filename, 'a', 'utf8').writelines(activities_list)
    #     return activities_list

class ParseParticipantIstances(CreateOntologyIstance):
    def __init__(self):
        super(ParseParticipantIstances, self).__init__('step2', {})

    # def Parse(self,
    #           results):
    #     # if not self.ask_save_filename(): return
    #     super_ste_results = super(ParseParticipantIstances, self).Parse(results)
    #     participant_list = GetResultsContent(super_ste_results)
    #     print('--- participant list ---')
    #     print(participant_list)
    #     # codecs.open(self.filename, 'w', 'utf8').write('\n\n--- participant list ---\n')
    #     # codecs.open(self.filename, 'a', 'utf8').writelines(participant_list)
    #     print('--- unique participants ---')
    #     unique_participant = list(set(participant_list))
    #     print(unique_participant)
    #     # codecs.open(self.filename, 'a', 'utf8').write('\n\n--- unique participants ---\n')
    #     # codecs.open(self.filename, 'a', 'utf8').writelines(participant_list)
    #     return participant_list


class ParseFlowIstances(CreateOntologyIstance):
    def __init__(self):
        super(ParseFlowIstances, self).__init__('step1', {})
    #
class ParseInstance(output_base):

    def __init__(self):
        super(ParseInstance, self).__init__()

    def Parse(self,
              results):
        self.activity = ParseActivityIstances().Parse(results)
        self.participant = ParseParticipantIstances().Parse(results)
        self.activityparticipant = ParseActivityParticipantIstances().Parse(results)
        self.flow = ParseFlowIstances().Parse(results)

