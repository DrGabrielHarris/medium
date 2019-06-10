import pandas as pd
from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
import graphviz as gv

# read data from csv
df = pd.read_csv('AudienceChurn.dataSample.csv', encoding='latin1', index_col='customer_no')
df.info()

# split data
y = df['churned']
X = df.drop('churned', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# build pipelines for attributes
num_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(categories='auto',
                             sparse=False,
                             handle_unknown='ignore'))])

# compose pipelines into one using column transformer
num_attrs = X.columns[X.dtypes != object].tolist()
cat_attrs = X.columns[X.dtypes == object].tolist()

preprocessor = ColumnTransformer(transformers=[
    ('num', num_transformer, num_attrs),
    ('cat', cat_transformer, cat_attrs)],
    remainder='drop')

# build full pipeline
tree = DecisionTreeClassifier(presort=True, random_state=42)
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', tree)])

# create a grid search and fit model
params = {'classifier__criterion': ['entropy', 'gini'],
          'classifier__max_depth': [5, 6, 7],
          'classifier__min_samples_leaf': [4, 5, 6]}

classifier_gs = GridSearchCV(pipeline, params, scoring='roc_auc', cv=5, verbose=1)
classifier_gs.fit(X_train, y_train)

# access model results
print(f'Best CV evaluation score:\n{round(classifier_gs.best_score_, 3)} mean', end=' ')
print(f'Best parameters:\n{classifier_gs.best_params_}\n')
print(f'Best estimator:\n{classifier_gs.best_estimator_}\n')

# get encoded features names
onehot_attrs = classifier_gs.best_estimator_.named_steps[
    'preprocessor'].named_transformers_['cat'].named_steps[
    'onehot'].get_feature_names(input_features=cat_attrs).tolist()

# plot tree using graphviz
export_graphviz(decision_tree=classifier_gs.best_estimator_.named_steps['classifier'],
                out_file='tree.dot',
                feature_names=num_attrs + onehot_attrs,
                class_names=['non-churned', 'churned'],
                rounded=True,
                filled=True)

# convert image from dot to png
gv.Source.from_file('tree.dot', format="png")