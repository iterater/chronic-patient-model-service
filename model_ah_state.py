import pickle

from ch_pat_model import ChPatModel


class StateAHModel(ChPatModel):
    """Test model with simple AH rules."""

    def __init__(self):
        super().__init__()
        self._model_description = 'Detection AH type model'
        # Feature order for model, don't change
        self.cols_for_model = [
            # TODO: gender?
            'sex',
            'height',
            'weight',
            'smoking',
            'alcohol_regularity',
            'creatinine_level',
            'effusions',
            'arrhythmia',
            'stenocardia',
            'heart_attack',
            'max_sbp',
            'mean_sbp',
            'age',
        ]
        self.feature_coding = {
            # TODO: gender?
            'sex': dict(zip(['female', 'male'], [0, 1])),
            'smoking': dict(zip([False, True], [-1, 1])),
            'alcohol_regularity': dict(zip(['regular', 'weekly',
                                            'rarely', 'deny'],
                                           [3, 2, 1, 0])),
            'effusions': dict(zip([False, True], [0, 1])),
            'arrhythmia': dict(zip([False, True], [0, 1])),
            'stenocardia': dict(zip([False, True], [0, 1])),
            'heart_attack': dict(zip([False, True], [0, 1]))
        }
        self.result_name = 'states'
        self.dt_path = 'AhStateClassifier/decision_tree_ah_state.pkl'

    def check_applicability(self, patient_dict):
        return all(map(lambda col: col in patient_dict, self.cols_for_model))

    def code_feature(self, col_name, value):
        if self.feature_coding.get(col_name):
            return self.feature_coding[col_name][self.try_cast(value)]
        return value

    @staticmethod
    def try_cast(value):
        try:
            return eval(value)
        except NameError:
            return value

    def apply(self, patient_dict):
        # TODO: добавить заполнение пропусков
        res_dict = patient_dict.copy()
        if self.result_name not in res_dict:
            res_dict[self.result_name] = []

        feature_vector = [[self.code_feature(col, patient_dict[col])
                           for col in self.cols_for_model]]

        state_pred_model = pickle.load(open(self.dt_path, 'br'))
        # 0 - вторичная, 1 - первичная
        state = state_pred_model.predict(feature_vector)[0]

        # TODO: добавить комментарий к болезни
        res_dict[self.result_name].append({'title': 'Класс АГ',
                                           'comment': 'Класс характеризуется повышенным риском...'}
                                          )
        if state:
            res_dict[self.result_name][-1]['value'] = '№1'
        else:
            res_dict[self.result_name][-1]['value'] = '№2'
        print('res_dict', res_dict)
        return res_dict
