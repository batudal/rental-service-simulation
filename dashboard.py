import random
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

class Device:
    def __init__(self):
        self.device_model = data.nextDevice()
        self.lifetime = int(data.table.loc[data.table[data.table['Model Name'] == self.device_model].index, 'Life Time'])
        self.purchase_price = int(data.table.loc[data.table[data.table['Model Name'] == self.device_model].index, 'Purchase Price'])
        self.credit_payback_duration = 36
        self.total_credit_debt = self.purchase_price * 1.1   
        self.inventory_value = self.purchase_price
        self.monthly_credit_payback = self.total_credit_debt / 36

    def sell (self):
        finance.device_sales += self.purchase_price * 0.35
        data.devices_sold += 1

    def rentalPrice(self, term):
        self.rental_price = int(data.table.loc[data.table[data.table['Model Name'] == self.device_model].index, '{}'.format(term)])

    def reduceLifetime (self):
         self.lifetime = self.lifetime -1
    
    def depreciate (self):
        if self.lifetime == 0:
            self.inventory_value = 0
        else:
            self.inventory_value = self.inventory_value * (1-(1/self.lifetime))
        
class User:
    def __init__(self):
        self.term = data.nextTerm()
        self.membership_type = self.term
        self.left_forever = False
        self.canRefer = True

    def reduceTerm (self):
        self.term = self.term -1

    def refer (self):
        self.canRefer = False
        if viral_coefficient >= 1:
            data.createMembership()
            if random.random() < viral_coefficient-1:
                data.createMembership()
        elif random.random() < viral_coefficient:
            data.createMembership()

class Data:
    def __init__(self):
        self.table = pd.read_csv('Siradaki_Price_List.csv',sep=';')
        self.users_total = 0
        self.devices_total = 0
        self.devices_sold = 0
        self.terms = random.choices([1,3,6,12], weights = [5,5,10,80], k = 100)
        self.devices = random.choices(self.table['Model Name'], weights = self.table['Rental Weight'], k = 100)
        self.id_dictionary = {}
        self.inventory = {}
        self.inventory_at_user = {}
        self.left_user = 0
    
    def nextDevice(self):
        return str(self.devices[self.devices_total % 100])

    def nextTerm(self):
        return int(self.terms[self.users_total % 100])
    
    def createMembership(self):
        user_id = "user_" + str(self.users_total)
        new_device_id = "device_" + str(self.devices_total)

        if len(list(self.inventory)) >> 0: 
            devices_that_match = []

            for device_id in list(self.inventory):
                if self.inventory[device_id] == self.nextDevice() and globals()[device_id].lifetime > 0:
                    devices_that_match.append(device_id)
            
            if len(devices_that_match) >> 0:
                self.id_dictionary[user_id] = devices_that_match[0]
                del self.inventory[devices_that_match[0]]
                self.inventory_at_user[devices_that_match[0]] = self.nextDevice()
                new_device_id = devices_that_match[0]

            else:     
                self.createDevice()
                self.inventory_at_user[new_device_id] = self.nextDevice()
                self.id_dictionary[user_id] = new_device_id
                        
        else:
            self.createDevice()
            self.inventory_at_user[new_device_id] = self.nextDevice()
            self.id_dictionary[user_id] = new_device_id         
        
        self.createUser()

    def createUser(self):
        user_id = "user_" + str(self.users_total)
        globals()[user_id] = User()
        self.users_total += 1

    def createDevice(self):
        device_id = "device_" + str(self.devices_total)
        globals()[device_id] = Device()
        self.devices_total += 1

    def devicesLifetime(self):
        for x in range(self.devices_total):
            device_id = 'device_' + str(x)
            globals()[device_id].reduceLifetime()
    
    def inventoryCheck(self):
        for device_id in list(self.inventory):
            if globals()[device_id].lifetime <= 0:
                globals()[device_id].sell()
                del self.inventory[device_id]
                
    def userJobs(self):
        for user_id in list(self.id_dictionary):
            device_id = self.id_dictionary[user_id]
            user_instance = globals()[user_id]
            device_instance = globals()[device_id]

            finance.rent_income += float(self.table.loc[self.table[data.table['Model Name'] == device_instance.device_model].index, '{}'.format(user_instance.membership_type)])
                
            if device_instance.credit_payback_duration > 0:
                finance.credit_costs += device_instance.monthly_credit_payback
                device_instance.total_credit_debt -= device_instance.monthly_credit_payback
                device_instance.credit_payback_duration -= 1

            user_instance.reduceTerm()

            # user term bittiyse
            if user_instance.term <= 0 and user_instance.left_forever == False:
                if random.random() <= 0.5:
                    user_instance.term += user_instance.membership_type
                else:
                    user_instance.left_forever = True
                    self.left_user += 1
                    self.inventory[device_id] = device_instance.device_model
                    del self.inventory_at_user[device_id]
                    del self.id_dictionary[user_id]

                    #finance.rent_income += device_instance.rentalPrice(user_instance.membership_type)        
            if user_instance.canRefer:
                user_instance.refer()
# sigorta + bakim eklenecek
class Finance:
    def __init__(self):
        self.device_sales = 0
        self.rent_income = 0
        self.credit_costs = 0

class Charts:
    def __init__(self):
        self.device_sales = []
        self.rent_income = []
        self.credit_costs = []
        self.balance = []
        self.user_count = []
        self.inventory_count = []
        self.month_count = []

    def updateCharts (self):
        self.device_sales.append(finance.device_sales)
        self.rent_income.append(finance.rent_income)
        self.credit_costs.append(-finance.credit_costs)
        self.balance.append(finance.device_sales + finance.rent_income - finance.credit_costs)
        self.user_count.append(data.users_total)
        self.inventory_count.append(len(data.inventory))

finance = Finance()
data = Data()
charts = Charts()

st.sidebar.subheader('Parameters')
constant_user_monthly = st.sidebar.slider('Monthly users added:', 0,10,1)
viral_coefficient = st.sidebar.slider('Viral coefficient:', 0.00,1.50,0.8)

for i in range(48):
    charts.month_count.append(i)
    charts.updateCharts()
    data.devicesLifetime()
    data.userJobs()
    data.inventoryCheck()
    for j in range(constant_user_monthly):
        data.createMembership()

st.image('./siradaki.png')
st.text("Welcome to Siradaki Dashboard.\n\nConfigure the chart by changing parameters on the sidepanel.")

df_device_sales = pd.DataFrame(list(charts.device_sales), index = charts.month_count, columns = ["Device sales income (TRY)"])
df_rent_income = pd.DataFrame(list(charts.rent_income), index = charts.month_count, columns = ["Rent income (TRY)"])
df_credit_costs = pd.DataFrame(list(charts.credit_costs), index = charts.month_count, columns = ["Credit costs (TRY)"])
df_balance = pd.DataFrame(list(charts.balance), index = charts.month_count, columns = ["Total balance (TRY)"])
df_all = pd.DataFrame(list(zip(charts.device_sales,charts.rent_income,charts.credit_costs)),
                        columns = ['Device sales income','Rent income','Credit costs'])
df_user_count = pd.DataFrame(list(charts.user_count), columns = ["Number of users"])
df_inventory_count = pd.DataFrame(list(charts.inventory_count), columns = ["Number of idle devices"] )

st.header("Accounting")
col1, col2, col3 = st.beta_columns(3)
col4, col5 = st.beta_columns(2)

st.header("Counters")
col6, col7 = st.beta_columns(2)

with col1:
    st.subheader("Cumulative Income from Rents")
    st.line_chart(df_rent_income)
    
with col2:
    st.subheader("Cumulative Credit Costs")
    st.line_chart(df_credit_costs)

with col3:
    st.subheader("Cumulative Device Sales")
    st.line_chart(df_device_sales)

with col4:
    st.subheader("Cumulative Balance")
    st.line_chart(df_balance)    

with col5:
    st.subheader("Cumulative Balance Sheet")
    st.bar_chart(df_all)

with col6:
    st.subheader("Cumulative User count")
    st.bar_chart(df_user_count)

with col7:
    st.subheader("Cumulative Inventory ")
    st.bar_chart(df_inventory_count)