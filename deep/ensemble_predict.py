import xgboost as xgb
import numpy as np
import argparse

from params import *
import util

def predict_ensemble(model, activations_test, best_iteration):
	concat_test = np.concatenate(activations_test, axis = 1)

	dtest = xgb.DMatrix(concat_test)

	return model.predict(dtest, ntree_limit = best_iteration)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Predict ensemble using XGBoost.')
	parser.add_argument('ensemble_model', metavar='ensemble_model', type=str, help = 'file to use as ensemble model.')
	parser.add_argument('model_ids', metavar='model_ids', type=str, nargs='+', help = 'list of models to ensemble.')

	args = parser.parse_args()

	m_test = []

	# Load all models
	for m in args.model_ids:
		t = np.load(params.SAVE_URL + "/" + m + "/raw_predictions_test.npy")
		m_test.append(t)

	model = xgb.Booster(model_file='ensembles/' + args.ensemble_model)
	best_iteration = np.load('ensembles/' + args.ensemble_model + '_best_iteration.npy')

	y = util.load_sample_submission()
	keys = y.index.values

	preds = predict_ensemble(model, m_test, best_iteration)
	preds = np.round(preds[:, np.newaxis])

	y.loc[keys] = preds

	y.to_csv('ensembles/' + args.ensemble_model + '.csv')
