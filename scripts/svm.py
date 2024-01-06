from construct_corpus import construct_full_corpus_train,construct_full_corpus_test
from extract_data import load_stopwords
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report,confusion_matrix
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Loading stopwords
stopwords=load_stopwords('../utils/stopwords_all.txt')

#Constructing train and test corpus
print('Constructing train corpus...')
x_train,y_train=construct_full_corpus_train()
print('Constructing test corpus...')
x_test,y_test=construct_full_corpus_test()

#Creating pipeline and grid search and fitting
print('Creating pipeline...')
pipeline=Pipeline([('tfidf',TfidfVectorizer(stop_words=stopwords)),
                   ('clf',svm.SVC())])
print('Creating grid search...')
param_grid={'tfidf__max_df':[0.5],#,0.75,1.0],
            'tfidf__ngram_range':[(1,2)],#,(1,1)],
            'clf__C':[1],#,10,0.1],
            'clf__kernel':['linear'],#,'rbf','poly'],
            'clf__decision_function_shape':['ovo']}#,'ovr']}
grid_search=GridSearchCV(pipeline,param_grid,cv=3,n_jobs=1,verbose=2)
print('Fitting...')
grid_search.fit(x_train, y_train)

#Results
result_file=open('../utils/results_svm.txt','w')
result_file.write('Meilleurs paramètres : '+str(grid_search.best_params_))
result_file.write('\nMeilleur score : '+str(grid_search.best_score_))

results=pd.DataFrame(grid_search.cv_results_)
results=results.sort_values(by='rank_test_score')
results.to_csv('../utils/grid_search_results_svm.csv',index=False)

class_names=grid_search.best_estimator_.named_steps['clf'].classes_
y_pred=grid_search.predict(x_test)
result_file.write('\n\n'+str(classification_report(y_test, y_pred)))
conf_matrix=confusion_matrix(y_test, y_pred)
result_file.write('\n\n'+str(conf_matrix))
sns.heatmap(conf_matrix,annot=True,fmt='g',cmap='Blues',xticklabels=class_names,yticklabels=class_names)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()

result_file.close()
print("Done.")