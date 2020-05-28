import pandas as pd 

class NerMeasurement:
    
    def __init__(self, l_true, l_pred):
        self.s_true = set(l_true)
        self.s_pred = set(l_pred)
        
        self.intersection = self.s_true.intersection(self.s_pred)
        self.union = self.s_true.union(self.s_pred)
        
        self.mis = self.s_true - self.s_pred
        self.spu = self.s_pred - self.s_true
        self.cor = self.intersection
        self.inc = 0
        self.par = 0
        
        self.pos = len(self.cor) + self.inc + self.par + len(self.mis)
        self.act = len(self.cor) + self.inc + self.par + len(self.spu)
        
    def jaccard_simmilarity(self):
        return len(self.intersection) / len(self.union)
    
    def precision(self):
        return len(self.cor) / self.act
    
    def recall(self):
        return len(self.cor) / self.pos
    
    def f1_score(self):
        p = self.precision()
        r = self.recall()
        if 0 == p + r:
            return 0
        else:
            return (2 * p * r)/(p + r)
        
