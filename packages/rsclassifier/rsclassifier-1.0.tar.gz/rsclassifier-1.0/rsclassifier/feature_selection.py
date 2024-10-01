from sklearn.ensemble import RandomForestClassifier

def feature_importances_using_random_forest(X, y, k = 0):
    rfc = RandomForestClassifier(random_state = 42)
    rfc.fit(X, y)
    importances = rfc.feature_importances_
    feature_names = X.columns
    feature_importances = {}
    for i in range(len(feature_names)):
        feature_importances[feature_names[i]] = importances[i]
    ranked_features = list((dict(sorted(feature_importances.items(), key=lambda item: item[1], reverse = True)).keys()))

    if k < 1:
        return ranked_features
    else:
        return ranked_features[:k]