import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

class Device(object):
    def __init__(self, id, device_model,user_id):
        #self.lifetime = lifetime
        #self.inventory_value = purchase_price
        #self.purchase_price = purchase_price
        self.device_model = device_model
        self.user_id = user_id
        self.id = id
        self.credit_duration = 36

    def sell (self):
        kasa.device_sales += self.purchase_price * 0.35

    def reduceLifetime (self):
         self.lifetime = self.lifetime -1
    
    def depreciate (self):
        if self.lifetime == 0:
            self.inventory_value = 0
        else:
            self.inventory_value = self.inventory_value * (1-(1/self.lifetime))
        

class User(object):
    def __init__(self, term, model_name):
        self.term = term
        self.membership_type = term
        self.device_id = 0 

    def reduceTerm (self):
        self.term = self.term -1
   
    def pay (self):
        

class Counter():
    def __init__(self):
        self.deneme = 0

deneme = Counter()

class Kasa():
    def __init__(self):
        self.device_sales = 0
        self.rent_income = 0
        self.credit_costs = 0
        self.overheads = 0
        self.gross = self.device_sales + self.rent_income - self.credit_costs - self.overheads
