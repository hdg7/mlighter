## @package MLighter
#  Documentation for this module.
#
#  More details.

class MLModel:

    def __init__(self,name):
        self.name = name
        
    def predict(self,sample):
        return self.model.predict(sample);

    def predict_proba(self,sample):
        return self.model.predict_proba(sample);
