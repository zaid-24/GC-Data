import json
import pandas as pd
import ast

def get_services(risk, zipcode, cluster = None):
    services = []
    if risk == 'Transportation Risk':
        data_dict = json.load(open('transportation_services.json'))
        services = data_dict[str(int(zipcode))]
    if risk == 'Transportation Risk' and cluster == 1:
        data_dict = json.load(open('telehealth_providers.json'))
        services = data_dict[str(int(zipcode))]

    if risk == 'Healthcare Access Risk':
        data_dict = json.load(open('telehealth_providers.json'))
        services = data_dict[str(int(zipcode))]
    if risk == 'Healthcare Access Risk' and cluster == 0:
        data_dict = json.load(open('Home_Health_physical_therapy.json'))
        services = data_dict[str(int(zipcode))]
    if risk == 'Healthcare Access Risk' and cluster == 3:
        data_dict = json.load(open('hospitals_with_emergency_services.json'))
        services = data_dict[str(int(zipcode))]
    
    if risk == 'Food Security':
        data_dict = json.load(open('food_services.json'))
        services = data_dict[str(int(zipcode))]
    if risk == 'Food Security' and cluster == 2:
        data_dict = json.load(open('transportation_services.json'))
        services = data_dict[str(int(zipcode))]
    
    if risk == 'Financial Risk':
        data_dict = json.load(open('medicare_providers.json'))
        services = data_dict[str(int(zipcode))]
        
    if risk == 'Technology Access Risk':
        data_dict = json.load(open('telehealth_providers.json'))
        services = data_dict[str(int(zipcode))]
    
    if not services or not len(services):
        return None
    
    return services

def get_suggested_actions(risk, risk_clusters, risk_actions_df, zipcode):
    
    risk_clusters_actions = risk_actions_df[risk_actions_df['Risk Title'] == risk]['Suggested Actions'].values[0]
    risk_clusters_actions = ast.literal_eval(risk_clusters_actions)
    suggested_actions_dict = {}
    services = {}

    suggested_actions_dict = {key: value for key, value in risk_clusters_actions.items() if key in risk_clusters}

    services = {}

    if risk == 'Transportation Risk':
        if not ('Public Commute Services' in risk_clusters or 'Private Transport Conditions' in risk_clusters):
            services['Tranportation Services'] = get_services(risk, zipcode)
        services['Telehealth Service Providers'] = get_services(risk, zipcode, 1)

    if risk == 'Food Security':
        if 'Food Service Providers' not in risk_clusters:
            services['Food Service Providers'] = get_services(risk, zipcode)
        if 'Accessibility to Supermarkets' in risk_clusters:
            services['Tranportation Services'] = get_services(risk, zipcode, 2)

    if risk == 'Healthcare Access Risk':
        if len(risk_clusters):
            services['Telehealth Service Providers'] = get_services(risk, zipcode) #home health services and physical therapy services
        if 'Rehab Centers' in risk_clusters:
            services['Home Health Physical Therapy Providers'] = get_services(risk, zipcode, 0) #home health services and physical therapy services
        if 'Hospital Count' in risk_clusters[3]:
            services['Hospitals With Emergency Services'] = get_services(risk, zipcode, 3) #home health services and physical therapy services

    if risk == 'Financial Risk' and (('Medicare/ Medicaid Beneficiaries' not in risk_clusters) and ('Medicare Utilization' not in risk_clusters)):
        services['Medicare Service Providers'] = get_services(risk, zipcode)

    if risk == 'Technology Access Risk' and ('Internet/Cellular Data Unavailability' in risk_clusters and 'Electronic Device Unavailability' not in risk_clusters):#internet risk and no electronic device risk
        services['Tranportation Services'] = get_services(risk, zipcode)


    
    
    return suggested_actions_dict, services



