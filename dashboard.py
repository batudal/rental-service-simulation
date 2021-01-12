import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

#total debt, total profit asas

#Sidebar
st.sidebar.header("Sidebar")
st.sidebar.subheader("Growth parameters:")
initial_users = st.sidebar.slider('Initial number of users', 0, 1000, 100)
virality = st.sidebar.slider('Virality coefficient', 0.00,1.30,1.00)
user_continues_rent = st.sidebar.slider('Retention rate', 0.00,1.00, 0.50)

st.sidebar.subheader("Graph parameters:")
length_in_months = st.sidebar.slider('Time period in months', 0, 120, 36)

#Mainpage
st.image('./siradaki.png')
st.text("Welcome to Siradaki Dashboard.\n\nConfigure the chart by changing parameters on the sidepanel.")
st.subheader("Users vs Time")

terms = [1,3,6,12]
percentage = random.choices(terms, weights=(5,5,10,80), k=100)

devices_table = pd.read_csv('Siradaki_Price_List.csv',sep=';')
model_list = devices_table['Model Name']
model_list_length = len(model_list)

percentage_devices = random.choices(model_list, weights=(devices_table['Rental Weight']), k=100)

usernames = []
inventory = []
asset_list = []
left_users = []
chart_totalUsers = []
chart_months = []
chart_newUsers = []
chart_revenue = []
sales_revenue = 0

matching_dict = {}

class Device(object):
    def __init__(self, model, lifetime, purchase_price,user_id,id):
        self.lifetime = lifetime
        self.inventory_value = purchase_price
        self.purchase_price = purchase_price
        self.model = model
        self.user_id = user_id
        self.id = id

    def sell (self):
        global sales_revenue
        sales_revenue += self.purchase_price / 2

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
        self.type = term
        self.didRefer = False
        self.model_name = model_name
        self.checkedRefer = False
        self.leftForever = False
        self.device_id = 0 

    def reduceTerm (self):
        self.term = self.term -1
   
    def pay (self):
        return int(devices_table.loc[devices_table[devices_table['Model Name']==self.model_name].index, str(self.type)])

class Counter():
    def __init__(self):
        self.userCounter = 0
        self.kasa = 0
        self.inventory = []
        self.deviceCounter = 0
        self.termCounter = 0

counter = Counter()

def create_user_instance(class_name,instance_name):
    while True:
        name = instance_name + str(counter.userCounter)

        model_modulo = counter.deviceCounter % 100
        term_modulo = counter.userCounter % 100
        term = percentage[term_modulo]
        model_name = percentage_devices[model_modulo]
        globals()[name] = class_name(term,model_name)
        usernames.append(name)
        counter.userCounter += 1
        availables = []
        
        if len(inventory) != 0:
            for i in inventory:
                #print('inventory' + i)
                if globals()[i].model == model_name and globals()[i].lifetime >= term:
                   globals()[i].user_id = name
        else:
            initiate_device(1,model_name,name)
            globals()[name].device_id = asset_list[-1]
            #print('assets' + asset_list[-1])
        yield True

def create_device_instance(class_name,device_name,model_name, user_id):
    while True:
        device_id = device_name + str(counter.deviceCounter)
        lifetime = int(devices_table.loc[devices_table[devices_table['Model Name']== model_name].index, 'Life Time'])
        purchase_price = int(devices_table.loc[devices_table[devices_table['Model Name']== model_name].index, 'Purchase Price']) 

        globals()[device_id] = class_name(model_name,lifetime,purchase_price,user_id,device_id)
        asset_list.append(device_id)
        counter.deviceCounter += 1
        yield True

def initiate (user_count):

    generator_instance = create_user_instance(User,'user_')
    for i in range(user_count):
        next(generator_instance)

def initiate_device (device_count,model_name,user_id):

    generator_instance = create_device_instance(Device,'device_', model_name, user_id)
    for i in range(device_count):
        next(generator_instance)
        
def firstMonth (user_count):
    initiate(user_count)

def monthForward(month):

    global inventory
    global asset_list

    active_users = 0
    churn_count = 0
    referrals = 0
    revenue = 0

    # iterate over assets and take action
    for x in asset_list:
        #print(len(globals()))
        #print(x)
        device = globals()[x]
        

        if device.lifetime <= 0 and device.user_id == 0:
            inventory.remove(x)
            asset_list.remove(x)
            device.sell()
        else:
            device.reduceLifetime()
            device.depreciate()

    # iterate over users and take action
    for i in range(len(usernames)):
        user = globals()[usernames[i]]

        # user subscription devam ediyorsa
        if user.term > 0:
            user.reduceTerm()
            revenue += user.pay()
            active_users += 1

            # user brings a friend
            if user.didRefer == False and user.checkedRefer == False and random.random() <= virality:
                user.didRefer = True
                referrals += 1
                initiate(user_count=1)

                # extra virality
                if random.random() <= virality-1:
                    initiate(user_count=1)

            user.checkedRefer = True

        # userin subscriptioni bittiyse             
        elif user.device_id != 0:
            # user devam eder
            if random.random() <= user_continues_rent and user.leftForever == False:
                user.term = random.choice([1,3,6,12])
            # user sistemden cikar
            else:
                churn_count += 1
                active_users -= 1
                if user.leftForever == False:
                    inventory.append(user.device_id)
                    user.leftForever = True

                    asdf = globals()[user.device_id]
                    asdf.user_id = 0
                    user.device_id = 0

                #left_users.append(usernames[i])
            
    counter.inventory.append(inventory)
    chart_months.append(month)
    chart_totalUsers.append(active_users)
    chart_newUsers.append(referrals)
    chart_revenue.append(revenue)

firstMonth(initial_users)
for i in range(length_in_months):
    monthForward(i)
    #print(i)
    #print(asset_list)
 
df = pd.DataFrame(list(zip(chart_totalUsers, chart_newUsers)),
               index = chart_months,
               columns =['Total Users', 'New Users']) 

df2 = pd.DataFrame(list(chart_revenue),
               index = chart_months,
               columns =['Revenue in TRY']) 

st.line_chart(df)
st.subheader("Revenue in TRY")
st.line_chart(df2)


