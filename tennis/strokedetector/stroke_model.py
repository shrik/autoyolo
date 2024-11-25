import pandas as pd

data = pd.read_csv("event.txt", header=None, names=["game", "clip", "index", "x", "y", "event_cls"])

# convert event_cls to int, unknown 0, serve 1, stroke 2
data['event_cls'] = data['event_cls'].map({'unknown': 0, 'serve': 1, 'stroke': 1})

FEATURE_WINDOW_NUM = 5
# print(data)
# import pdb; pdb.set_trace()


def get_feature_cols(num = FEATURE_WINDOW_NUM):
    colnames_x = ['x_diff_{}'.format(i) for i in range(1, num)] + \
                ['x_diff_inv_{}'.format(i) for i in range(1, num)] + \
                ['x_div_{}'.format(i) for i in range(1, num)]
    colnames_y = ['y_diff_{}'.format(i) for i in range(1, num)] + \
                    ['y_diff_inv_{}'.format(i) for i in range(1, num)] + \
                    ['y_div_{}'.format(i) for i in range(1, num)]
    # colnames_xy = ['x_diff_div_y_diff_{}'.format(i) for i in range(1, num)]
    colnames = colnames_x + colnames_y 
    return colnames

def to_features(data, num=FEATURE_WINDOW_NUM):
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
        # by mayuchao
        # data.loc[:, 'x_diff_div_y_diff_{}'.format(i)] = data['x_diff_{}'.format(i)]/(data['y_diff_{}'.format(i)] + eps)
    for i in range(1, num):
        data = data[data['x_lag_{}'.format(i)].notna()]
        data = data[data['x_lag_inv_{}'.format(i)].notna()]
    data = data[data['x'].notna()] 
    return data

def get_data(data, games=[]):
    game_clips = data[data['game'].isin(games)][['game', 'clip']].drop_duplicates().values
    res  = []
    for game, clip in game_clips:
        filtered = data[(data['game'] == game) & (data['clip'] == clip)]
        res.append(to_features(filtered))
    return pd.concat(res, axis=0)


train_data = get_data(data, ['game1', 'game2', 'game3'])
test_data = get_data(data, ['game5'])

from catboost import CatBoostRegressor
catboost_regressor = CatBoostRegressor(iterations=1000, depth=2, learning_rate=0.05, loss_function='RMSE')
catboost_regressor.fit(train_data[get_feature_cols(FEATURE_WINDOW_NUM)], train_data['event_cls'])

test_data["pred"] = catboost_regressor.predict(test_data[get_feature_cols(FEATURE_WINDOW_NUM)])

import numpy as np
for threshold in np.arange(0.1, 1, 0.1):
    print(f'===> threshold: {threshold}')

    preds_threshold = (test_data["pred"] > threshold).astype(int)
    # calculate accuracy
    val = pd.DataFrame({'pred': preds_threshold,'true': test_data['event_cls']})
    val['correct'] = val['pred'] == val['true']
    tp = val[(val['pred'] == 1) & (val['pred'] == val['true'])]
    tn = val[(val['pred'] == 0) & (val['pred'] == val['true'])]
    fp = val[(val['pred'] == 1) & (val['pred'] != val['true'])]
    fn = val[(val['pred'] == 0) & (val['pred'] != val['true'])]
    acc = (val['correct']).mean()
    recall = len(tp)/(len(tp) + len(fn))
    precision = len(tp)/(len(tp) + len(fp))
    print(f'tp: {len(tp)}, tn: {len(tn)}, fp: {len(fp)}, fn: {len(fn)}')
    print(f'accuracy: {acc}, recall: {recall}, precision: {precision}')

# export cbm model
catboost_regressor.save_model('stroke_model.cbm')

test_data["pred_cls"] = (test_data["pred"] > 0.1).astype(int)
test_data["correct"] = test_data["pred_cls"] == test_data["event_cls"]
test_data[["game", "clip", "index", "pred_cls", "event_cls", "correct", "pred"]].to_csv('val.csv')
