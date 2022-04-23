import pickle
import pandas as pd

with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
    
data.to_csv('data.csv', index=False)