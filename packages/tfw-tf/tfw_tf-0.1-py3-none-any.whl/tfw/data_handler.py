# tfw/tfw.py
# tfw/data_handler.py
class tf:
    def __init__(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
    
    def X_val(self):
        return self.X_train
    
    def y_val(self):
        return self.y_train
    
    def X_test(self):
        return self.X_train
    
    def y_test(self):
        return self.y_train
