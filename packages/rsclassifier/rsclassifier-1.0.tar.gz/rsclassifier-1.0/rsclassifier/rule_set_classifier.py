import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.special import betainc
from rsclassifier.feature_selection import feature_importances_using_random_forest
from rsclassifier.quine_mccluskey import minimize_dnf
from rsclassifier.entropy_based_discretization import find_pivots

class Error(Exception):
    pass

class RuleSetClassifier:
    def __init__(self):
        self.semantics = {} # Maps propositional symbols to pairs [type, feature, value].
        self.rules = [] # Each rule is a pair [output, terms]. If one of the terms is true, classifier returns output.
        self.default_prediction = None # If none of the terms in rules matches, this is the output.
        
        self.is_initialized = False
        self.is_fitted = False

        self.X = None
        self.y = None

    def booleanize_categorical_features(self, X, categorical_features):
        local_X = X.copy()
        for feature in categorical_features:
            unique_values = local_X[feature].unique()
            new_columns = {}
            if len(unique_values) > 2:
                for value in unique_values:
                    new_columns[feature + ' = ' + str(value)] = (local_X[feature] == value)
                    self.semantics[feature + ' = ' + str(value)] = ['categorical', feature, value]
            else:
                value = unique_values[0]
                new_columns[feature + ' = ' + str(value)] = (local_X[feature] == value)
                self.semantics[feature + ' = ' + str(value)] = ['categorical', feature, value]
            local_X = pd.concat([local_X, pd.DataFrame(new_columns)], axis = 1)
        local_X.drop(columns = categorical_features, inplace = True)
        return local_X

    def booleanize_numerical_features(self, X, y, numerical_features):
        local_X = X.copy()
        for feature in tqdm(numerical_features, total = len(numerical_features), desc = 'Discretizing numerical features...'):
            Z = pd.concat([local_X[feature], y], axis = 1)
            pivots = find_pivots(Z)
            if len(pivots) == 0:
                # No suitable pivot found, so we ignore this feature.
                continue
            new_columns = {}
            for pivot in pivots:
                new_columns[f'{feature} > {pivot:.2f}'] = local_X[feature] > pivot
                self.semantics[f'{feature} > {pivot:.2f}'] = ['numerical', feature, pivot]
            local_X = pd.concat([local_X, pd.DataFrame(new_columns)], axis = 1)
        local_X.drop(columns = numerical_features, inplace = True)
        return local_X

    def get_type(self, row):
        type = []
        for atom in row.keys():
            if row[atom] == True:
                type.append([1, atom])
            else:
                type.append([0, atom])
        return type

    # 
    # Given labeled data, discretize it and store it for fitting purposes.
    # 
    # @param[in]    self
    # @param[in]    X               
    # @param[in]    y
    # @param[in]    categorical     List of categorical features.
    # @param[in]    numerical       List of numerical features.
    def load_data(self, X, y, categorical = [], numerical = []):
        bool_X = X.copy()
        if len(categorical) > 0:
            bool_X = self.booleanize_categorical_features(bool_X, categorical)
        if len(numerical) > 0:
            bool_X = self.booleanize_numerical_features(bool_X, y, numerical)
        self.X = bool_X
        self.y = y
        self.is_initialized = True

    def form_rule_list(self, features, default_prediction, silent):
        self.rules = []
        local_X = self.X[features]

        types = []
        type_scores = {}
        unique_y = list(self.y.unique())

        for index, row in tqdm(local_X.iterrows(), total=len(local_X), desc = 'Calculating probabilities...', disable = silent):
            type = self.get_type(row)
            type_code = hash(str(type))
            if not type_code in type_scores:
                types.append(type)
                type_scores[type_code] = {v: 0 for v in unique_y}
            type_scores[type_code][self.y.loc[index]] += 1

        if default_prediction is None:
            self.default_prediction = self.y.value_counts().idxmax()
        else:
            self.default_prediction = default_prediction
        unique_y.remove(self.default_prediction)
        rules = {v: [] for v in unique_y}

        for type in tqdm(types, total = len(types), desc = 'Forming the classifier...', disable = silent):
            type_code = hash(str(type))
            output = max(type_scores[type_code], key=type_scores[type_code].get)
            if output != self.default_prediction:
                rules[output].append(type)

        # Remove empty rules.
        rules = {k: v for k, v in rules.items() if v}
        
        self.rules = list(rules.items())

    def prune_terms_using_domain_knowledge(self, terms):
        simplified_terms = []
        for term in terms:
            simplified_term = []
            positive_categories = []
            upper_bounds = {}
            lower_bounds = {}
            for literal in term:
                meaning = self.semantics[literal[1]]
                if meaning[0] == 'categorical':
                    if literal[0] == 0:
                        simplified_term.append(literal)
                    if literal[0] == 1 and meaning[1] not in positive_categories:
                        positive_categories.append(meaning[1])
                        simplified_term.append(literal)
                if meaning[0] == 'numerical':
                    if literal[0] == 0:
                        if meaning[1] not in upper_bounds or meaning[2] <= upper_bounds[meaning[1]]:
                            upper_bounds[meaning[1]] = meaning[2]
                    if literal[0] == 1:
                        if meaning[1] not in lower_bounds or meaning[2] > lower_bounds[meaning[1]]:
                            lower_bounds[meaning[1]] = meaning[2]
            for feature in upper_bounds.keys():
                simplified_term.append([0, f'{feature} > {upper_bounds[feature]:.2f}'])
            for feature in lower_bounds.keys():
                simplified_term.append([1, f'{feature} > {lower_bounds[feature]:.2f}'])
            simplified_terms.append(simplified_term)
        return simplified_terms

    def evaluate_term(self, term, prediction):
        T = len(self.X)
        
        # Identify rows where the prediction is correct
        correct_prediction_mask = (self.y == prediction)
        P = correct_prediction_mask.sum()

        # Check whether each row satisfies the term
        term_mask = np.ones(len(self.X), dtype = bool)
        for literal in term:
            term_mask &= (self.X[literal[1]] == literal[0])

        # Number of rows where term is true (t) and correct prediction (p)
        t = term_mask.sum()
        p = (term_mask & correct_prediction_mask).sum()

        # This approximates the probability that a random rule with the same coverage as term would get at least as good accuracy as t.
        score = betainc(p, t - p + 1, P / T)
        return score
    
    def prune_term(self, term, prediction):
        local_term = term.copy()
        while True:
            lowest_score = self.evaluate_term(local_term, prediction)
            best_term = local_term
            for i in range(len(local_term)):
                reduced_term = local_term[:i] + local_term[i + 1:]  # Avoid deep copy
                score = self.evaluate_term(reduced_term, prediction)
                if score < lowest_score:
                    lowest_score = score
                    best_term = reduced_term
            if best_term == local_term:
                break
            local_term = best_term
        return local_term

    # Determines whether term2 is entailed by term1.
    def entails(self, term1, term2):
        for l2 in term2:
            # We need to check that term1 contains a literal l1 which entails l2.
            entailed = False
            for l1 in term1:
                if l1[0] == l2[0]:
                    meaning1 = self.semantics[l1[1]]
                    meaning2 = self.semantics[l2[1]]
                    if meaning1[1] == meaning2[1]:
                        if meaning1[0] == 'categorical' and meaning1[2] == meaning2[2]:
                            entailed = True
                            break
                        elif meaning1[0] == 'numerical':
                            if l1[0] == 0 and meaning2[2] >= meaning1[2]:
                                entailed = True
                                break
                            elif meaning2[2] <= meaning1[2]:
                                entailed = True
                                break
            if not entailed:
                return False
        return True
    
    def simplify(self):
        simplified_rules = []
        for rule in self.rules:
            prediction = rule[0]
            terms = rule[1]
            
            # Step 1. Boolean optimization + domain knowledge.
            simplified_terms = self.prune_terms_using_domain_knowledge(minimize_dnf(terms))

            # Step 2. Further pruning based on probabilistic heuristics.
            for i in tqdm(range(len(simplified_terms)), desc = f'Pruning terms for class {prediction}...'):
                simplified_terms[i] = self.prune_term(simplified_terms[i], prediction)

            # Step 3. Pruning can cause some of the rules to become redundant. Remove them.
            necessary_terms = []
            for i in range(len(simplified_terms)):
                necessary = True
                for j in range(i + 1, len(simplified_terms)):
                    if self.entails(simplified_terms[i], simplified_terms[j]):
                        necessary = False
                        break
                if necessary:
                    necessary_terms.append(simplified_terms[i])
            
            simplified_rules.append([prediction, necessary_terms])

        # TODO: Pruning can also lead to conflicts between rules. Is this a problem?

        self.rules = simplified_rules

    def fit(self, num_prop, default_prediction = None, silent = False):
        if not self.is_initialized:
            raise Error('Data has not been loaded.')
        
        used_props = feature_importances_using_random_forest(self.X, self.y, num_prop)
        self.form_rule_list(used_props, default_prediction, silent)
        self.simplify()
        self.is_fitted = True

    def evaluate(self, assignment):
        for rule in self.rules:
            output = rule[0]
            terms = rule[1]
            for term in terms:
                truth_value = True
                for literal in term:
                    interpretation = self.semantics[literal[1]]
                    if interpretation[0] == 'numerical':
                        if literal[0] != (assignment[interpretation[1]] > interpretation[2]):
                            truth_value = False
                            break
                    else:
                        if literal[0] != (assignment[interpretation[1]] == interpretation[2]):
                            truth_value = False
                            break
                if truth_value:
                    return output
        return self.default_prediction

    def predict(self, X):
        if not self.is_fitted:
            raise Error('Model has not been fitted.')
        def get_prediction(row):
            assignment = row.to_dict()
            return self.evaluate(assignment)
        return X.apply(get_prediction, axis=1)

    def term_support_and_confidence(self, term, prediction):
        # Identify rows where the prediction is correct
        correct_prediction_mask = (self.y == prediction)

        # Check whether each row satisfies the term
        term_mask = np.ones(len(self.X), dtype = bool)
        for literal in term:
            term_mask &= (self.X[literal[1]] == literal[0])

        # Number of rows where term is true (t) and correct prediction (p)
        t = term_mask.sum()
        p = (term_mask & correct_prediction_mask).sum()

        return t, (p/t)

    def __str__(self):
        output = str()
        for i in range(len(self.rules)):
            rule = self.rules[i]
            if i > 0:
                output += 'ELSE IF\n'
            else:
                output += 'IF\n'
            prediction = rule[0]
            terms = rule[1]
            for i in range(len(terms)):
                if i > 0:
                    output += 'OR '
                output += '('
                term = terms[i]
                for j in range(len(term)):
                    if j > 0:
                        output += ' AND '
                    if term[j][0] == 0:
                        meaning = self.semantics[term[j][1]]
                        if meaning[0] == 'categorical':
                            output += f'NOT {term[j][1]}'
                        else:
                            output += f'{meaning[1]} <= {meaning[2]}'
                    else:
                        output += term[j][1]
                support, confidence = self.term_support_and_confidence(term, prediction)
                output += f') {{support: {support}, confidence: {confidence:.2f}}}\n'
            output += f'THEN {rule[0]}\n'
        output += f'ELSE {self.default_prediction}\n'
        return output