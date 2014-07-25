from get_tweets_by_user import query_twitter_for_histories
from create_classifier import generate_predictions


def make_prediction(names):
    u"""Takes in a list of Twitter user handles. Returns a list of
    single-entry dictionaries, with the keys being the user names
    and the values being the predictions."""
    if isinstance(names, basestring):
        names = [names]
    print "Names: " + str(names)
    histories = query_twitter_for_histories(names, data_collection=False)
    results = []
    get_preds = []
    print "LENGTH: " + str(len(histories))
    for history in histories:
        if len(history) < 100:
            user = {}
            user['name'] = history[0][0]
            user['prediction'] = """Not enough tweeting history to
                                make a prediction."""
            results.append(user)
            print "Not Long enough"
        else:
            print "Long enough"
            get_preds.append(history)
    right, wrong, preds, actual = generate_predictions(get_preds)
    for idx, pred in enumerate(preds):
        user = {}
        user['name'] = pred[0]
        if actual[idx]:
            user['prediction'] = actual[idx]
        else:
            user['prediction'] = pred[2]
        results.append(user)
    # except Exception:
    #     _error = {}
    #     _error['name'] = "Error"
    #     _error['prediction'] = "We couldn't make a prediction for this user."
    #     results.append(_error)
    return results


def serve_predictions(names):
    results = make_prediction(names)
    for result in results:
        yield result

if __name__ == "__main__":
    user_names = ['TrustyJohn']
    results = make_prediction(user_names)
    for result in results:
        print "For the user: ", result['name'], " our predictions are: ", result['prediction']
