import pandas as pd

data = pd.read_csv("event.txt", header=None, names=["game", "clip", "index", "x", "y", "event_cls"])

# convert event_cls to int, unknown 0, serve 1, stroke 2
data['event_cls'] = data['event_cls'].map({'unknown': 0, 'serve': 1, 'stroke': 2})


# print(data)
# import pdb; pdb.set_trace()

def to_features(data):
    num = 5
    eps = 1e-15
    data = data.copy()  # Create a copy of the DataFrame to avoid SettingWithCopyWarning
    for i in range(1, num):
        data.loc[:, 'x_lag_{}'.format(i)] = data['x'].shift(i)
        data.loc[:, 'x_lag_inv_{}'.format(i)] = data['x'].shift(-i)
        data.loc[:, 'y_lag_{}'.format(i)] = data['y'].shift(i)
        data.loc[:, 'y_lag_inv_{}'.format(i)] = data['y'].shift(-i) 
        data.loc[:, 'x_diff_{}'.format(i)] = abs(data['x_lag_{}'.format(i)] - data['x'])
        data.loc[:, 'y_diff_{}'.format(i)] = data['y_lag_{}'.format(i)] - data['y']
        data.loc[:, 'x_diff_inv_{}'.format(i)] = abs(data['x_lag_inv_{}'.format(i)] - data['x'])
        data.loc[:, 'y_diff_inv_{}'.format(i)] = data['y_lag_inv_{}'.format(i)] - data['y']
        data.loc[:, 'x_div_{}'.format(i)] = abs(data['x_diff_{}'.format(i)]/(data['x_diff_inv_{}'.format(i)] + eps))
        data.loc[:, 'y_div_{}'.format(i)] = data['y_diff_{}'.format(i)]/(data['y_diff_inv_{}'.format(i)] + eps)
    for i in range(1, num):
        data = data[data['x_lag_{}'.format(i)].notna()]
        data = data[data['x_lag_inv_{}'.format(i)].notna()]
    data = data[data['x'].notna()] 

    colnames_x = ['x_diff_{}'.format(i) for i in range(1, num)] + \
                    ['x_diff_inv_{}'.format(i) for i in range(1, num)] + \
                    ['x_div_{}'.format(i) for i in range(1, num)]
    colnames_y = ['y_diff_{}'.format(i) for i in range(1, num)] + \
                    ['y_diff_inv_{}'.format(i) for i in range(1, num)] + \
                    ['y_div_{}'.format(i) for i in range(1, num)]
    colnames = colnames_x + colnames_y

    features = data[colnames]
    labels = data['event_cls']
    return features, labels


def get_data(data, games=[]):
    game_clips = data[data['game'].isin(games)][['game', 'clip']].drop_duplicates().values
    features = []
    labels = []
    for game, clip in game_clips:
        train_data = data[(data['game'] == game) & (data['clip'] == clip)]
        train_features, train_labels = to_features(train_data)
        features.append(train_features)
        labels.append(train_labels)
    return pd.concat(features, axis=0), pd.concat(labels, axis=0)


train_features, train_labels = get_data(data, ['game1', 'game2', 'game3'])
test_features, test_labels = get_data(data, ['game5'])

from catboost import CatBoostClassifier
catboost_classifier = CatBoostClassifier(iterations=10000, depth=3, learning_rate=0.05, loss_function='MultiClass')
catboost_classifier.fit(train_features, train_labels)

preds = catboost_classifier.predict(test_features)
# Ensure preds is 1D by taking the first column if it's 2D
if preds.ndim > 1:
    preds = preds[:, 0]  # Adjust this line if necessary based on your model's output
# calculate accuracy

val = pd.DataFrame({'pred': preds,'true': test_labels})
val['correct'] = val['pred'] == val['true']
tp = val[((val['pred'] == 2) | (val['pred'] == 1)) & (val['pred'] == val['true'])]
tn = val[(val['pred'] == 0) & (val['pred'] == val['true'])]
fp = val[((val['pred'] == 2) | (val['pred']== 1)) & (val['pred'] != val['true'])]
fn = val[(val['pred'] == 0) & (val['pred'] != val['true'])]
acc = (val['correct']).mean()
recall = len(tp)/(len(tp) + len(fn))
precision = len(tp)/(len(tp) + len(fp))
print(f'tp: {len(tp)}, tn: {len(tn)}, fp: {len(fp)}, fn: {len(fn)}')
print(f'accuracy: {acc}, recall: {recall}, precision: {precision}')
val.to_csv('val.csv')

accuracy = (preds == test_labels).mean()
print(accuracy)
