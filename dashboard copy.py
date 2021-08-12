import random
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

df_cont = pd.DataFrame(columns=['id','model','creditdebt'])
dek = 0

class Device:
    def __init__(self):
        self.device_model = data.nextDevice()
        self.lifetime = int(data.table.loc[data.table[data.table['Model Name'] == self.device_model].index, 'Life Time'])
        self.purchase_price = int(data.table.loc[data.table[data.table['Model Name'] == self.device_model].index, 'Purchase Price'])
        self.credit_payback_duration = 36
        self.total_credit_debt = self.purchase_price * 1.15   
        self.inventory_value = self.purchase_price
        self.monthly_credit_payback = self.total_credit_debt / 36
        self.constant_lifetime = int(data.table.loc[data.table[data.table['Model Name'] == self.device_model].index, 'Life Time'])
        self.insurance_cost = self.purchase_price * 0.2 / self.constant_lifetime

    def sell (self):
        finance.device_sales += self.purchase_price * 0.35
        data.devices_sold += 1

    def rentalPrice(self, term):
        self.rental_price = int(data.table.loc[data.table[data.table['Model Name'] == self.device_model].index, '{}'.format(term)])

    def reduceLifetime (self):
        if self.lifetime >> 0:
         self.lifetime = self.lifetime -1

    def depreciate (self):
        if self.lifetime == 0:
            self.inventory_value = 0
        else:
            self.inventory_value -= (self.purchase_price * (1/self.constant_lifetime))
        
class User:
    def __init__(self):
        self.term = data.nextTerm()
        self.membership_type = self.term
        self.left_forever = False
        self.canRefer = True

    def reduceTerm (self):
        self.term = self.term -1

#If user brings friend
    def refer (self):
        #one referral per user
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
        new_user_id = self.createUser()

        if len(list(self.inventory)) >> 0: 
            devices_that_match = []

            for device_id in list(self.inventory):
                if self.inventory[device_id] == self.nextDevice() and globals()[device_id].lifetime > 0:
                    devices_that_match.append(device_id)
            
            if len(devices_that_match) >> 0:
                self.id_dictionary[new_user_id] = devices_that_match[0]
                del self.inventory[devices_that_match[0]]
                self.inventory_at_user[devices_that_match[0]] = self.nextDevice()
                finance.delivery_cost += 35
                finance.packaging_cost += 30

            else:     
                new_device_id = self.createDevice()
                self.inventory_at_user[new_device_id] = self.nextDevice()
                self.id_dictionary[new_user_id] = new_device_id
                finance.delivery_cost += 35
                finance.packaging_cost += 30
                        
        else:
            new_device_id = self.createDevice()
            self.inventory_at_user[new_device_id] = self.nextDevice()
            self.id_dictionary[new_user_id] = new_device_id   
            finance.delivery_cost += 35
            finance.packaging_cost += 30      
        
        #print(self.id_dictionary)

    def createUser(self):
        user_id = "user_" + str(self.users_total)
        globals()[user_id] = User()
        self.users_total += 1
        finance.credit_check_cost += 30
        finance.cac += 150
        return user_id


    def createDevice(self):
        device_id = "device_" + str(self.devices_total)
        globals()[device_id] = Device()
        self.devices_total += 1
        return device_id

    def devicesLifetime(self):
        for x in range(self.devices_total):
            device_id = 'device_' + str(x)
            device_instance = globals()[device_id]       

            globals()[device_id].reduceLifetime()
            globals()[device_id].depreciate()

            finance.asset_value += device_instance.inventory_value

            #for control:
            global df_cont
            global dek
            
    #pay per device monthly credit payback, reduce monthly payment from device credit payback, update total credit debt
            if device_instance.credit_payback_duration > 0:
                finance.credit_costs += device_instance.monthly_credit_payback
                device_instance.total_credit_debt -= device_instance.monthly_credit_payback
                #for control
                df_cont.loc[dek] = pd.Series({'id':device_id, 'model':device_instance.device_model, 'creditdebt':device_instance.inventory_value})
                dek +=1
                #print('id{0} !model{1} !creditdebt{2}'.format(device_id, device_instance.device_model, device_instance.total_credit_debt))
                finance.total_credit_debt += device_instance.total_credit_debt
                device_instance.credit_payback_duration -= 1
    
    def inventoryCheck(self):
        for device_id in list(self.inventory):
            device_instance = globals()[device_id]
            if globals()[device_id].lifetime <= 0:
                globals()[device_id].sell()
                del self.inventory[device_id]

#            else:
 #               finance.asset_value += device_instance.inventory_value
  #              device_instance.depreciate()

                
    def userJobs(self):
        for user_id in list(self.id_dictionary):
            device_id = self.id_dictionary[user_id]
            user_instance = globals()[user_id]
            device_instance = globals()[device_id]

            #add user rent income to total rent income, pay payment commission, pay insurance cost for active users
            finance.rent_income += float(self.table.loc[self.table[data.table['Model Name'] == device_instance.device_model].index, '{}'.format(user_instance.membership_type)])
            finance.payment_commission = (finance.rent_income * 0.015)
            finance.insurance_cost += device_instance.insurance_cost

            user_instance.reduceTerm()


            # user term bittiyse
            if user_instance.term <= 0 and user_instance.left_forever == False:
                if random.random() <= 0.5:
                    user_instance.term += user_instance.membership_type
                else:
                    user_instance.left_forever = True
                    self.left_user += 1
                    self.inventory[device_id] = device_instance.device_model
                    finance.delivery_cost += 35
                    finance.maintenance_cost += int(data.table.loc[data.table[data.table['Model Name'] == device_instance.device_model].index, 'Annual Mcost'])
                    del self.inventory_at_user[device_id]
                    del self.id_dictionary[user_id]
    
            if user_instance.canRefer:
                user_instance.refer()

class Finance:
    def __init__(self):
        self.device_sales = 0
        self.rent_income = 0
        self.credit_costs = 0
        self.insurance_cost = 0
        self.delivery_cost = 0
        self.packaging_cost = 0
        self.asset_value = 0
        self.payment_commission = 0
        self.maintenance_cost = 0
        self.credit_check_cost = 0
        self.cac = 0
        self.total_credit_debt = 0

class Charts:
    def __init__(self):
        self.device_sales = []
        self.rent_income = []
        self.credit_costs = []
        self.delivery_costs = []
        self.balance = []
        self.user_count = []
        self.inventory_count = []
        self.month_count = []
        self.cac = []
        self.insurance_costs = []
        self.packaging_costs = []
        self.POS_costs = []
        self.maintenance_costs = []
        self.findeks_cost = []
        self.left_users = []
        self.asset_value = []
        self.total_credit_debt = []


    def updateCharts (self):
        self.device_sales.append(finance.device_sales)
        self.rent_income.append(finance.rent_income)
        self.credit_costs.append(-finance.credit_costs)
        self.delivery_costs.append(finance.delivery_cost)
        self.POS_costs.append(finance.payment_commission)
        self.cac.append(finance.cac)
        self.findeks_cost.append(finance.credit_check_cost)
        self.maintenance_costs.append(finance.maintenance_cost)
        self.packaging_costs.append(finance.packaging_cost)
        self.insurance_costs.append(finance.insurance_cost)
        self.balance.append(finance.device_sales + finance.rent_income - finance.credit_costs - finance.insurance_cost - finance.delivery_cost - finance.packaging_cost - finance.payment_commission - finance.maintenance_cost - finance.credit_check_cost - finance.cac)
        self.user_count.append(data.users_total)
        self.left_users.append(data.left_user)
        self.inventory_count.append(len(data.inventory))
        self.asset_value.append(finance.asset_value)
        self.total_credit_debt.append(finance.total_credit_debt)

       

finance = Finance()
data = Data()
charts = Charts()

constant_user_monthly = 100

viral_coefficient = 1

for i in range(60):
    charts.month_count.append(i)
    for j in range(constant_user_monthly):
        data.createMembership()    

    data.devicesLifetime()
    data.userJobs()
    data.inventoryCheck()
    charts.updateCharts()



df_device_sales = pd.DataFrame(list(charts.device_sales), index = charts.month_count, columns = ["Device sales income (TRY)"])
df_rent_income = pd.DataFrame(list(charts.rent_income), index = charts.month_count, columns = ["Rent income (TRY)"])
df_credit_costs = pd.DataFrame(list(charts.credit_costs), index = charts.month_count, columns = ["Credit costs (TRY)"])
df_operating_costs = pd.DataFrame(list(zip(charts.cac,charts.delivery_costs,charts.packaging_costs,charts.maintenance_costs,charts.findeks_cost,charts.insurance_costs)),
                        index = charts.month_count, columns = ['CAC','Delivery costs','Packaging costs','Maintenance costs','Findeks costs','Insurance costs'])
df_balance = pd.DataFrame(list(charts.balance), index = charts.month_count, columns = ["Total balance (TRY)"])
df_all = pd.DataFrame(list(zip(charts.device_sales,charts.rent_income,charts.credit_costs)),
                        index = charts.month_count, columns = ['Device sales income','Rent income','Credit costs'])
df_user_count = pd.DataFrame(list(charts.user_count), index = charts.month_count, columns = ["Number of users"])
df_inventory_count = pd.DataFrame(list(charts.inventory_count), index = charts.month_count, columns = ["Number of idle devices"] )
df_mega = pd.DataFrame(list(zip(charts.device_sales,charts.rent_income,charts.credit_costs, charts.user_count,charts.inventory_count,charts.cac,charts.delivery_costs,charts.packaging_costs,charts.maintenance_costs,charts.findeks_cost, charts.left_users, charts.insurance_costs, charts.asset_value, charts.total_credit_debt)),
                        index = charts.month_count, columns = ['Device sales income','Rent income','Credit costs','User count','inventory count','CAC','Delivery costs','Packaging costs','Maintenance costs','Findeks costs','Returned device count','Insurance costs','Asset value','Total Credit debt'])


df_mega.to_csv(r'C:\Users\zeynep.tutengil\Desktop\bazonk\exports\deneme46.csv', index = True)
#df_cont.to_csv(r'C:\Users\zeynep.tutengil\Desktop\bazonk\exports\control7.csv', index = True)