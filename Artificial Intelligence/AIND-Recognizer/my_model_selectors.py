import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        #Model selection: the lower the BIC the better the model
        #Initialize best score & model
        best_model = self.base_model(self.min_n_components)
        best_score = float('inf') #initial state

        for m in range(self.min_n_components, self.max_n_components+1):
            try:
                model = self.base_model(m)
                #L is the likelihood of the fitted model
                logL = model.score(self.X, self.lenghts)
                ##number of data points
                logN = np.log(self.X.shape)
                #p:number of parameters
                #p = num_states ^2 + 2*num_features * num_states-1
                p = m**2 + 2 + 2*self.X.shape[1]*m-1
                #BIC = -2 * logL + p * logN
                score = -2*logL + p * logN
                #find the least score
                if score < best_score:
                    best_score, best_model = score, model

            except:
                pass
        return best_model

class SelectorDIC(ModelSelector):

    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        # Unlike, BIC, DIC takes into account the goal of the models
        # Initialize best score & model
        best_model = self.base_model(self.min_n_components)
        best_score = float('-inf')

        for m in range(self.min_n_components, self.max_n_components+1):
            try:
                model = self.base_model(m)
                logL = model.score(self.X, self.lenghts)
                scores = [model.score(x, lenght) for word, (x, length) in self.hwords.items() if word!=self.this_word]
                score = logL - np.mean(scores)
                #find the highest score score
                if score > best_score:
                    best_score, best_model = score, model
            except:
                pass
        return best_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV.
        # kFold = KFold(n_splits=10, shuffle=True, random_state=None)

        # Initialize best score & model
        best_model = self.base_model(self.n_constant)
        best_score = float("-inf")
        # Get KFold split indicies (# of splits is 3 by default)
        split_method = KFold(n_splits=3, shuffle=True, random_state=None)

        for n in range(self.min_n_components, self.max_n_components+1):
            # Initialize empty scores
            scores = []
            # see ig enough data to split in 3
            if len(self.lengths) < 3:
                return self.base_model(self.n_constant)

            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                #Creating Test and Train sets
                cv_train_X, cv_train_lengths = combine_sequences(cv_train_idx, self.sequences)
                cv_test_X, cv_test_lengths = combine_sequences(cv_test_idx, self.sequences)
                try:
                    # Train HMM
                    hmm_model = GaussianHMM(n_components=n_comps, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(cv_train_X, cv_train_Lengths)
                    # Score HMM
                    scores.append(hmm_model.score(cv_test_X, cv_test_lengths))
                except Exception:
                    continue

            # Calculate cv score
            cv_score = np.average(scores) if len(scores) > 0 else float("-inf")

            # Select highest score
            if cv_score > best_score:
                best_score = cv_score
                best_model = hmm_model

        return best_model
