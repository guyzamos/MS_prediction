import pickle
import pandas as pd
import statistics as stats
# import forestci as fci
# from sklearn.ensemble import RandomForestRegressor
# import sklearn.model_selection as xval
# from sklearn.datasets import fetch_openml

def predictions(features_dictionary):

    missing_values_dictionary = missing_values_dictionary_func()
    fixed_dictionary = check_validate_values(features_dictionary, missing_values_dictionary)
    rrms = predict_RRMS("trained_merged_df_RF_classifier.sav", fixed_dictionary)
    edss = predict_EDSS("trained_merged_df_RF_regressor.sav", fixed_dictionary)
    predictions_dictionary = {
        "RRMS": rrms,
        "EDSS": edss,
        "message": edss_dictionary(edss)
        # "RRMS": predict_RRMS("DFDB1Final.pkl", fixed_dictionary),
        # "EDSS": predict_EDSS("DFDB2Final.pkl", fixed_dictionary)
    }
    # predictions_dictionary = {
        # "RRMS": predict_RRMS("trained_merged_df_RF_classifier.sav", fixed_dictionary),
        # "EDSS": predict_EDSS("trained_merged_df_RF_regressor.sav", fixed_dictionary)
        # "RRMS": predict_RRMS("DFDB1Final.pkl", fixed_dictionary),
        # "EDSS": predict_EDSS("DFDB2Final.pkl", fixed_dictionary)
    # }
    return predictions_dictionary


def missing_values_dictionary_func():

    df = pd.read_excel('dfMergedcheck.xlsx')
    missing_values_dictionary = {
        "MRI_lesion_mass": stats.median(df['MRI_lesion_mass']),
        "primary_EDSS_at_diagnosis": stats.median(df['primary_EDSS_at_diagnosis']),
        "age_at_diagnosis": stats.mode(df['age_at_diagnosis']),
        "TIM3_RQ": stats.median(df['TIM3_RQ']),
        "TIGIT_RQ": stats.median(df['TIGIT_RQ']),
        "PD-1_RQ": stats.median(df['PD-1_RQ']),
        "LAG3_RQ": stats.median(df['LAG3_RQ']),
        "Male": stats.mode(df['Male']),
        "positive_OCB": stats.mode(df['positive_OCB'])
    }
    return missing_values_dictionary


def check_validate_values(features_dictionary, missing_values_dictionary):

    if features_dictionary.get('MRI_lesion_mass') == '':
        features_dictionary['MRI_lesion_mass'] = missing_values_dictionary.get('MRI_lesion_mass')

    if features_dictionary.get('primary_EDSS_at_diagnosis') == '':
        features_dictionary['primary_EDSS_at_diagnosis'] = missing_values_dictionary.get('primary_EDSS_at_diagnosis')

    if features_dictionary.get('age_at_diagnosis') == '':
        features_dictionary['age_at_diagnosis'] = missing_values_dictionary.get('age_at_diagnosis')

    if features_dictionary.get('TIM3_RQ') == '':
        features_dictionary['TIM3_RQ'] = missing_values_dictionary.get('TIM3_RQ')

    if features_dictionary.get('TIGIT_RQ') == '':
        features_dictionary['TIGIT_RQ'] = missing_values_dictionary.get('TIGIT_RQ')

    if features_dictionary.get('PD-1_RQ') == '':
        features_dictionary['PD-1_RQ'] = missing_values_dictionary.get('PD-1_RQ')

    # if features_dictionary.get('PD1') == '':
    #     features_dictionary['PD1'] = missing_values_dictionary.get('PD1')

    if features_dictionary.get('Male') == '':
        features_dictionary['Male'] = missing_values_dictionary.get('Male')

    if features_dictionary.get('LAG3_RQ') == '':
        features_dictionary['LAG3_RQ'] = missing_values_dictionary.get('LAG3_RQ')

    if features_dictionary.get('positive_OCB') == '':
        features_dictionary['positive_OCB'] = missing_values_dictionary.get('positive_OCB')

    return features_dictionary


def predict_RRMS(filename, features_dictionary):

    loaded_model = pickle.load(open(filename, 'rb'))
    df_input = pd.DataFrame(columns=['MRI_lesion_mass', 'primary_EDSS_at_diagnosis','age_at_diagnosis','TIM3_RQ', 'TIGIT_RQ', 'LAG3_RQ', 'PD-1_RQ', 'Male', 'positive_OCB'])
    MRI_lesion_mass= features_dictionary.get('MRI_lesion_mass')
    primary_EDSS_at_diagnosis = features_dictionary.get('primary_EDSS_at_diagnosis')
    age_at_diagnosis = features_dictionary.get('age_at_diagnosis')
    TIM3_RQ = features_dictionary.get('TIM3_RQ')
    TIGIT_RQ= features_dictionary.get('TIGIT_RQ')
    LAG3_RQ= features_dictionary.get('LAG3_RQ')
    PD1_RQ= features_dictionary.get('PD-1_RQ')
    Male= features_dictionary.get('Male')
    positive_OCB= features_dictionary.get('positive_OCB')
    df_input.loc[0] = [MRI_lesion_mass, primary_EDSS_at_diagnosis, age_at_diagnosis, TIM3_RQ, TIGIT_RQ, LAG3_RQ, PD1_RQ, Male, positive_OCB]
    # Make predictions on training set:
    predictor_var = ['MRI_lesion_mass', 'primary_EDSS_at_diagnosis', 'age_at_diagnosis', 'TIM3_RQ', 'TIGIT_RQ', 'LAG3_RQ', 'PD-1_RQ', 'Male', 'positive_OCB']
    predictions = loaded_model.predict(df_input[predictor_var])
    if predictions[0] == 0:
        return "SPMS"
    else:
        return "RRMS"


def predict_EDSS(filename, features_dictionary):

    loaded_model = pickle.load(open(filename, 'rb'))
    df_input = pd.DataFrame(columns=['MRI_lesion_mass', 'primary_EDSS_at_diagnosis','age_at_diagnosis','TIM3_RQ', 'TIGIT_RQ', 'LAG3_RQ', 'PD-1_RQ', 'Male', 'positive_OCB'])
    MRI_lesion_mass= features_dictionary.get('MRI_lesion_mass')
    primary_EDSS_at_diagnosis = features_dictionary.get('primary_EDSS_at_diagnosis')
    age_at_diagnosis = features_dictionary.get('age_at_diagnosis')
    TIM3_RQ = features_dictionary.get('TIM3_RQ')
    TIGIT_RQ= features_dictionary.get('TIGIT_RQ')
    LAG3_RQ= features_dictionary.get('LAG3_RQ')
    PD1_RQ= features_dictionary.get('PD-1_RQ')
    Male= features_dictionary.get('Male')
    positive_OCB= features_dictionary.get('positive_OCB')
    df_input.loc[0] = [MRI_lesion_mass, primary_EDSS_at_diagnosis, age_at_diagnosis, TIM3_RQ, TIGIT_RQ, LAG3_RQ, PD1_RQ, Male, positive_OCB]
    # Make predictions on training set:
    predictor_var = ['MRI_lesion_mass', 'primary_EDSS_at_diagnosis', 'age_at_diagnosis', 'TIM3_RQ', 'TIGIT_RQ', 'LAG3_RQ', 'PD-1_RQ', 'Male', 'positive_OCB']
    predictions = loaded_model.predict(df_input[predictor_var])
    # confidence_interval = fci.random_forest_error(loaded_model, predictor_var)
    return predictions[0]



def edss_dictionary(edss):
    edss_key = edss*100
    predictions_dictionary = {
        range(0, 0): 'fully ambulatory',
        range(0, 401): 'fully ambulatory, self-sufficient and up 12 hours a day despite relatively severe disability. Able to walk at least 500 meters without aid/rest.',
        range(401, 451): 'fully ambulatory, able to work a full day, may require minimal assistance. Able to walk at least 300 meters without aid/rest.',
        range(451, 501): 'ambulatory for 200 meters without aid/rest; disability that impairs full daily activities (eg, to work full day without special provisions).',
        range(551, 601): 'ambulatory for 100 meters without aid/rest; disability precludes full daily activities.',
        range(601, 651): 'intermittent or unilateral constant assistance required to walk 100 meters, with/without resting.',
        range(651, 701): 'constant bilateral assistance (canes, crutches, or braces) required to walk 20 meters without resting.',
        range(701, 751): 'unable to walk >5 meters even with aid; (restricted to wheelchair); wheels self in standard wheelchair and transfers alone.',
        range(751, 801): 'unable to take more than steps; restricted to wheelchair; may need aid in transfer; wheels self but cannot use standard wheelchair a full day; may require motorized wheelchair.',
        range(801, 851): 'restricted to bed/chair or perambulated in wheelchair, but may be out of bed itself much of the day; retains many self-care functions; generally has effective use of arms.',
        range(851, 901): 'restricted to bed much of the day; has some effective use of arms; retains some self-care functions.',
        range(901, 951): 'helpless bed patient; can communicate and eat.',
        range(951, 1000): 'totally helpless bed patient; unable to communicate effectively or eat/swallow.',
        range(1000, 2001): 'death due to MS.',
    }

    key = key_range(edss_key, predictions_dictionary)

    return predictions_dictionary.get(key)


def key_range(edss, dictionary):
    for key in dictionary:
        if edss in key:
            return key
            break




from sklearn.metrics import plot_confusion_matrix
#
# rf = RandomForestClassifier(n_estimators=25, min_samples_split=25, max_depth=7, max_features='auto')
# predictor_var = ['MRI_lesion_mass', 'primary_EDSS_at_diagnosis','age_at_diagnosis','TIM3_RQ', 'TIGIT_RQ', 'LAG3_RQ', 'PD-1_RQ', 'Male', 'positive_OCB']
# outcome_var = 'diagnosis_RRMS'
# total_tp = 0
# total_tn = 0
# total_fp = 0
# total_fn = 0
#
# # Perform k-fold cross-validation with 10 folds
# kf = KFold(n_splits=10)
# accuracy = []
# for train, test in kf.split(df):
#     # Filter training data
#     train_predictors = (df[predictor_var].iloc[train, :])
#     # The target we're using to train the algorithm.
#     train_target = df[outcome_var].iloc[train]
#
#     test_predictors = (df[predictor_var].iloc[test, :])
#     # The target we're using to train the algorithm.
#     test_target = df[outcome_var].iloc[test]
#
#
#     # Training the algorithm using the predictors and target.
#     rf.fit(train_predictors, train_target)
#     predictions = rf.predict(df[train_predictors]) 
#
#     tn, fp, fn, tp = confusion_matrix(test_target, predictions)
#
#     total_tp += tp
#     total_tn += tn
#     total_fp += fp
#     total_fn += fn
#
#
# return total_tp,total_tn,total_fp,total_fn
#
