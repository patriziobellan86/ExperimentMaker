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
        #  results should be ordered now!
        # results = OrderResults(results)
        step_results = GetResultItem(self.step_name, results)
        results_content = GetResultsContent(step_results)
        return results_content

class ParseActivityIstances(CreateOntologyIstance):
    def __init__(self):
        super(ParseActivityIstances, self).__init__('st1', {})

    def Parse(self,
              results):

        data_to_write = list()
        # < https: // w3id.org / pet  # MR-ACTIVITY-003-GDAY> <https://w3id.org/pet#hasRuleId> "MR-ACTIVITY-003-GDAY" .
        ntriple_string_template = '<https://w3id.org/pet#{activity_id}> <https://w3id.org/pet#hasRuleId> "{activity_str}" .\n'
        # # <https://w3id.org/pet#MR-ACTIVITY-003-GDAY> <https://w3id.org/pet#monitoredEntity> <https://w3id.org/pet#Running> .
        ntriple_entity_template = '<https://w3id.org/pet#{activity_id}> <https://w3id.org/pet#monitoredEntity> <https://w3id.org/pet#Running> .\n'
        results_ = super(ParseActivityIstances, self).Parse(results)

        for n_, activity_str in enumerate(results_):
            #  activity ID
            activity_id = 'ACTIVITY_ID_{}_{}'.format(n_, activity_str.replace(' ', '_'))
            activity_ntriple_template_str = ntriple_string_template.format(activity_id=activity_id,
                                                                           activity_str=activity_str)
            activity_ntriple_template_entity = ntriple_entity_template.format(activity_id=activity_id)
            data_to_write.append(activity_ntriple_template_str)
            data_to_write.append(activity_ntriple_template_entity)
        #  write data
        codecs.open('Activity N-Triples.txt', 'w', 'utf-8').writelines(data_to_write)

class ParseParticipantIstances(CreateOntologyIstance):
    def __init__(self):
        super(ParseParticipantIstances, self).__init__('cleanstep2results', {})

    def Parse(self,
              results):

        data_to_write = list()
        # < https: // w3id.org / pet  # MR-ACTIVITY-003-GDAY> <https://w3id.org/pet#hasRuleId> "MR-ACTIVITY-003-GDAY" .
        ntriple_string_template = '<https://w3id.org/pet#{participant_id}> <https://w3id.org/pet#hasRuleId> "{participant_str}" .\n'
        # # <https://w3id.org/pet#MR-ACTIVITY-003-GDAY> <https://w3id.org/pet#monitoredEntity> <https://w3id.org/pet#Running> .
        ntriple_entity_template = '<https://w3id.org/pet#{participant_id}> <https://w3id.org/pet#monitoredEntity> <https://w3id.org/pet#Running> .\n'
        results_ = super(ParseParticipantIstances, self).Parse(results)

        for n_, participant_str in enumerate(results_):
            #  activity ID

            participant_id = 'PARTICIPANT_ID_{}_{}'.format(n_, participant_str.replace(' ', '_'))
            participant_ntriple_template_str = ntriple_string_template.format(participant_id=participant_id,
                                                                           participant_str=participant_str)
            participant_ntriple_template_entity = ntriple_entity_template.format(participant_id=participant_id)
            data_to_write.append(participant_ntriple_template_str)
            data_to_write.append(participant_ntriple_template_entity)
        #  write data
        codecs.open('Participant N-Triples.txt', 'w', 'utf-8').writelines(data_to_write)
#