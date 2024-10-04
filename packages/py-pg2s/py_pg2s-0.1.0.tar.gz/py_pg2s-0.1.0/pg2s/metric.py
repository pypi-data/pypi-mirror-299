import numpy as np
from typing import List, Tuple
from pg2s import wv, nlp, model



def pg2s_score(plans: Tuple[Tuple[List[str]]],
        alpha: float = 0.5 ) -> float:

    '''
    Compute the Planing Goal Semantic Score (PG2S) metric.
    -'plans' should be a tuple of tuples of lists of the form:
    plans = {
        "name-of-the-task": {
            'truth':[
        'Action 1',
        'Action 2',
        ...
        'Action N'
                    ],
            'predict':[
        'Action 1',
        'Action 2',
        ...
        'Action M'
                ]
        }
    }
    -alpha is an hyperparameter that can be tuned to give more importance to 
    the goal-wise similarity or to the sentence-wise similarity. Default value is 0.5
    '''
    

    def framing(sentences):
        '''
            create actions from the sets
        '''
        actions_and_states = []
        for sentence in sentences:
            sentence = sentence.lower()
            doc = nlp(sentence)
            for token in doc:
                if token.pos_ == "VERB":
                    subjects_or_objects = [child.text for child in token.children if child.dep_ in ["dobj", "nsubj"]]
                    if subjects_or_objects:
                        actions_and_states.append([token.text] + subjects_or_objects)
        return actions_and_states

    def goal_wise_similarity(truth, pred):
        '''
            Taken in input two sets of actions give the result of the similarity 
        '''
        truth_list = truth.copy()
        pred_list = pred.copy()
        conf = []
        for element in truth_list:
            verb = element[0]
            nouns = element[1:]
            best = None
            max_similarity = 0
            for element2 in pred_list:
                verb2 = element2[0]
                nouns2 = element2[1:]
                verbs_similarity = wv.similarity(verb, verb2)
                nouns_similarity = []
                min_len = min(len(nouns), len(nouns2))
                if len(nouns) != len(nouns2) and min_len == 0:
                    nouns_similarity = 0
                else:
                    if len(nouns) < len(nouns2):
                        nouns_similarity = [1 if wv.similarity(nouns[i], nouns2[i]) >= 0.708 else 0 for i in range(min_len)]
                    else:
                        nouns_similarity = [1 if wv.similarity(nouns2[i], nouns[i]) >= 0.708 else 0 for i in range(min_len)]
                    if not nouns_similarity:
                        nouns_similarity = 1
                    else:
                        nouns_similarity = np.mean(nouns_similarity)
                if verbs_similarity * nouns_similarity > max_similarity and verbs_similarity > 0.708:
                    max_similarity = verbs_similarity * nouns_similarity
                    best = element2
            if best is not None:
                index_delete = pred_list.index(best)
                pred_list.pop(index_delete)
                conf.append(1)
            else:
                conf.append(0)
        if not conf:
            return 0
        return np.mean(conf)

    def sentence_similarity(list1,list2):
        '''
            Taken in input two sets of sentences give the similarity between the plans
        '''
        truth_copy = list1.copy()
        pred_copy = list2.copy()
        conf = []
        for i in range(len(truth_copy)):
            max = float("-inf")
            best = None
            embeddings = model.encode(truth_copy[i])
            for j in range(len(pred_copy)):
                embeddings2 = model.encode(pred_copy[j])
                similarity = np.dot(embeddings,embeddings2)/(np.linalg.norm(embeddings)*np.linalg.norm(embeddings2))
                if similarity > max and similarity > 0.675:
                    max = similarity
                    best = pred_copy[j]

            if best is not None:
                pred_copy.remove(best)
                conf.append(1)
            else:
                conf.append(0)
        if len(conf) == 0:
            return 0
        return np.mean(conf)

    task = list(plans.keys())[0]
    truth = plans[task]["truth"]
    predict = plans[task]["predict"]
    truth_actions = framing(truth)
    predict_actions = framing(predict)
    goal_wise = goal_wise_similarity(truth_actions,predict_actions)
    sentence_wise = sentence_similarity(truth,predict)

    return goal_wise * alpha + sentence_wise * (1.0-alpha)
