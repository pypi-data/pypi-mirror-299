from matclassification.methods import MDT

class MoveletDT(MDT):
    def __init__(self, 
                 n_jobs=-1,
                 verbose=2,
                 random_state=42,
                 filterwarnings='ignore'):
        
        super().__init__('MDT', n_jobs=n_jobs, verbose=verbose, random_state=random_state, filterwarnings=filterwarnings)
        
    def prepare_input(self,
                      ls_movs,
                      
                      tid_col='tid', class_col='label',
#                      space_geohash=False, # For future implementation
                      geo_precision=30,
                      validate=False):
        
        X, y, nattr, num_classes = super().prepare_input(train, test,
                                                         tid_col=tid_col, class_col=class_col, 
#                                                         geo_precision=geo_precision,
                                                         validate=validate)
        
        self.config['features'] = list(filter(lambda c: c not in [tid_col, class_col, 'class'], train.columns))
        
        return X, y, nattr, num_classes
        
    def fit(self, 
            X_train, 
            y_train, 
            X_val,
            y_val):
        
        self.model = self.create()
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_val)
        return y_pred
        
#        y_val1 = argmax(y_val, axis = 1)
#        self.report = self.score(y_val1, y_pred)       
#        return self.report

def render(movelets, attribute=None, title='Movelets Markov Tree', concat_edges=True): 