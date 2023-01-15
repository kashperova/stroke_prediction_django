from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd
from sklearn import metrics
from django.shortcuts import redirect


def change_lang(request, lang):
    return render(request, 'index.html', {'lang': lang})


def data_processing(filename):
    dataset = pd.read_csv(filename, encoding='latin-1')
    dataset = dataset.rename(columns=lambda x: x.strip().lower())
    dataset.head()

    dataset = dataset.drop(columns=['id'])
    dataset['gender'] = dataset['gender'].apply(lambda x: 1 if x == 'Male' else (2 if x == 'Other' else 0))
    dataset['ever_married'] = dataset['ever_married'].apply(lambda x: 1 if x == 'yes' else 0)
    dataset['residence_type'] = dataset['residence_type'].apply(lambda x: 1 if x == 'Urban' else 0)

    dataset['work_type'].replace(dataset['work_type'].unique(),
                                 [1, 2, 3, 4, 5], inplace=True)
    dataset['smoking_status'].replace(dataset['smoking_status'].unique(),
                                      [1, 2, 3, 4], inplace=True)
    dataset = dataset.dropna()
    dataset['smoking_status'] = dataset['smoking_status'].apply(lambda x: None if x == 4 else x)
    dataset = dataset.dropna()
    return dataset


quest_counter = 10
selected_info = {}


def home_page_return(request):
    return redirect('/')


def home(request):
    return render(request, 'index.html', {'lang': 'eng'})


def predict(request, lang, pk):
    action = request.GET.get('action', 0)
    if action == 'previous':
        pk += 1
    if action == 'next' or action == 'finish':
        pk -= 1
    if pk == 10:
        text_eng = "Please, enter your gender"
        text_ua = "Будь ласка, оберіть свою стать"
        quest_counter = 10
        answers_eng = ['male', 'female']
        answers_ua = ['жіноча', 'чоловіча']
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': answers_eng,
                                              'answers_ua': answers_ua, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 9:
        text_eng = "Please, enter your age"
        text_ua = "Будь ласка, вкажіть свій вік"
        if request.GET['action'] != 'previous' and request.GET['select'] == 'жіноча' or request.GET[
            'select'] == 'female':
            selected_info['gender'] = 0
        elif request.GET['action'] != 'previous' and request.GET['select'] == 'чоловіча' or request.GET[
            'select'] == 'male':
            selected_info['gender'] = 1
        quest_counter = 9
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': {},
                                              'answers_ua': {}, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 8:
        text_eng = "Please indicate if you have high blood pressure"
        text_ua = "Будь ласка, вкажіть, чи є у вас гіпертонія (стійкий підвишений тиск)?"
        if request.GET['action'] != 'previous':
            selected_info['age'] = int(request.GET['select'])
        quest_counter = 8
        answers_eng = ['yes', 'no']
        answers_ua = ['так', 'ні']
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': answers_eng,
                                              'answers_ua': answers_ua, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 7:
        text_eng = "Please indicate if you have heart disease"
        text_ua = "Будь ласка, вкажіть, чи є у вас в анамнезі серцево-судинні захворювання?"
        if request.GET['action'] != 'previous':
            selected_item = request.GET['select']
            if selected_item == 'yes' or selected_item == 'так':
                selected_info['hypertension'] = 1
            else:
                selected_info['hypertension'] = 0
        quest_counter = 7
        answers_eng = ['yes', 'no']
        answers_ua = ['так', 'ні']
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': answers_eng,
                                              'answers_ua': answers_ua, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 6:
        text_eng = "Please indicate if you have ever married"
        text_ua = "Будь ласка, зазначте, чи були ви колись одруженні?"
        if request.GET['action'] != 'previous':
            selected_item = request.GET['select']
            if selected_item == 'yes' or selected_item == 'так':
                selected_info['heart_disease'] = 1
            else:
                selected_info['heart_disease'] = 0
        quest_counter = 6
        answers_eng = ['yes', 'no']
        answers_ua = ['так', 'ні']
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': answers_eng,
                                              'answers_ua': answers_ua, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 5:
        text_eng = "Please select your current work type"
        text_ua = "Будь ласка, зазначте ваш поточний робочий статус"
        if request.GET['action'] != 'previous':
            selected_item = request.GET['select']
            if selected_item == 'yes' or selected_item == 'так':
                selected_info['ever_married'] = 1
            else:
                selected_info['ever_married'] = 0
        quest_counter = 5
        answers_eng = ['private job', 'self employed', 'govt job', 'children', 'never worked']
        answers_ua = ['робота за контрактом', 'приватний підприємець', 'співробітник бюджетної організації',
                      'дитина/підліток', 'ніколи не працював/-ла']
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': answers_eng,
                                              'answers_ua': answers_ua, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 4:
        text_eng = "Please select your current residence type"
        text_ua = "Будь ласка, зазначте, де ви мешкаєте"
        if request.GET['action'] != 'previous':
            selected_item = request.GET['select']
            if selected_item == 'private job' or selected_item == 'робота за контрактом':
                selected_info['work_type'] = 1
            elif selected_item == 'self employed' or selected_item == 'приватний підприємець':
                selected_info['work_type'] = 2
            elif selected_item == 'govt job' or selected_item == 'співробітник бюджетної організації':
                selected_info['work_type'] = 3
            elif selected_item == 'children' or selected_item == 'дитина/підліток':
                selected_info['work_type'] = 4
            elif selected_item == 'never worked' or selected_item == 'ніколи не працював/-ла':
                selected_info['work_type'] = 5
        quest_counter = 4
        answers_eng = ['urban', 'rural']
        answers_ua = ['місто', 'село']
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': answers_eng,
                                              'answers_ua': answers_ua, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 3:
        text_eng = "Please enter your height (sm)"
        text_ua = "Будь ласка, зазначте ваш зріст (см)"
        if request.GET['action'] != 'previous':
            selected_item = request.GET['select']
            if selected_item == 'rural' or selected_item == 'село':
                selected_info['residence_type'] = 1
            else:
                selected_info['residence_type'] = 0
        quest_counter = 3
        answers_eng = []
        answers_ua = []
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': answers_eng,
                                              'answers_ua': answers_ua, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 2:
        text_eng = "Please enter you weight (kg)"
        text_ua = "Будь ласка, зазначте вашу вагу (кг)"
        if request.GET['action'] != 'previous':
            selected_info['height'] = int(request.GET['select'])
        quest_counter = 2
        answers_eng = []
        answers_ua = []
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': answers_eng,
                                              'answers_ua': answers_ua, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 1:
        text_eng = "Please enter you smoking status"
        text_ua = "Будь ласка, оберіть із запропонованих статусів з приводу паління найбільш влучний про вас"
        if request.GET['action'] != 'previous':
            weight = int(request.GET['select'])
            selected_info['bmi'] = (weight / ((selected_info['height'] / 100) * (selected_info['height'] / 100)))
            selected_info.pop('height')
        quest_counter = 1
        answers_eng = ['formerly smoked', 'never smoked', 'smokes']
        answers_ua = ['палив/палила раніше', 'ніколи не палив/палила', 'палю']
        return render(request, 'query.html', {'quest_counter': quest_counter, 'answers_eng': answers_eng,
                                              'answers_ua': answers_ua, 'text_eng': text_eng,
                                              'text_ua': text_ua, 'lang': lang})
    elif pk == 0:
        selected_item = request.GET['select']
        if selected_item == 'formerly smoked' or selected_item == 'палив/палила раніше':
            selected_info['smoking_status'] = 1
        elif selected_item == 'never smoked' or selected_item == 'ніколи не палив/палила':
            selected_info['smoking_status'] = 2
        elif selected_item == 'smokes' or selected_item == 'палю':
            selected_info['smoking_status'] = 3
        return result(request, lang)


def getPredictions(gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, bmi,
                   smoking_status):
    model = pickle.load(open('data_and_model/model.sav', 'rb'))
    scaled = pickle.load(open('data_and_model/scaler.sav', 'rb'))

    dataset = data_processing('data_and_model/test.csv')
    numerical_features_list = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']

    dataset[numerical_features_list] = scaled.transform(dataset[numerical_features_list])

    X_test = dataset.drop(['stroke'], axis=1)
    y_test = dataset['stroke']

    y_pred_proba = model.predict_proba(X_test)[::, 1]
    auc = round(metrics.roc_auc_score(y_test, y_pred_proba), 4) * 100

    column_size = 10
    values = [gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, None, bmi,
              smoking_status]

    # start fuzzy exploration method
    dists = []  # distances between
    sum_d = 0  # variable for saving reversed sum of distances
    membs_levels = []  # list of membership levels
    all_avg_gl_levels = []

    # start iterate though all rows of dataframe to count distances
    for row in dataset.itertuples():
        d = 0
        # initialize variable for saving distance
        # add value of feature "avg_glucose_level" to list that contains all average glucose levels
        all_avg_gl_levels.append(row[8])
        for index in range(column_size):
            if index != 7:
                d += np.abs(row[index + 1] - values[index])  # sum absolute value between values of user data and other

        d = d / 9
        sum_d += (1 / d)  # reverse distances
        dists.append(d)
        # count = 0

    for d in dists:
        membs_levels.append(round((1 / d) / sum_d, 3))  # calculation of membership levels

    avg_glucose_level = 0

    for i in range(len(all_avg_gl_levels)):
        avg_glucose_level += (all_avg_gl_levels[i] * membs_levels[i])

    avg_glucose_level = round(avg_glucose_level, 3)

    new_values = scaled.transform([[age, hypertension, heart_disease, avg_glucose_level, bmi]])
    age = new_values[0][0]
    hypertension = new_values[0][1]
    heart_disease = new_values[0][2]
    avg_glucose_level = new_values[0][3]
    bmi = new_values[0][4]

    new_values = np.array([[gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi,
         smoking_status]])

    prediction = model.predict(new_values)
    proba = model.predict_proba(new_values)
    if prediction == 0:
        proba = round(proba[0][0], 4) * 100
        return 'no stroke', proba
    elif prediction == 1:
        proba = round(proba[0][1], 4) * 100
        return 'stroke', proba
    else:
        return 'error', proba


def result(request, lang):
    gender = selected_info['gender']
    age = selected_info['age']
    hypertension = selected_info['hypertension']
    heart_disease = selected_info['heart_disease']
    ever_married = selected_info['ever_married']
    work_type = selected_info['work_type']
    residence_type = selected_info['residence_type']
    bmi = selected_info['bmi']
    smoking_status = selected_info['smoking_status']
    result_prediction, proba = getPredictions(gender, age, hypertension, heart_disease,
                                              ever_married, work_type, residence_type, bmi, smoking_status)
    proba = round(proba, 4)
    if lang == 'ua':
        if result_prediction == 'no stroke':
            result_prediction = 'низький ризик винекнення інсульту'
        elif result_prediction == 'stroke':
            result_prediction = 'високий ризик винекнення інсульту'
    return render(request, 'result.html', {'result_prediction': result_prediction, 'proba': proba, 'lang': lang})
