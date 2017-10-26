# -*- coding: utf-8 -*- 
# This version adds the code to process the NotAgeAppropriate field.
import pandas as pd
import sys
from Process_Data import Process_Data
import numpy as np
#import pycurl, cStringIO
#import certifi         # lines 7 & 8 are necessary for utilizing REDCap API

p='uploads'         #part of the filepath. Be sure to create your upload folder
dr='mmddyyyy'         #folder destination for the upload file. Name it as the date of the upload, e.g. '06122017'

path = 'C:\\Users\\japese01\\My Documents\\RefugeeHealth\\uploads\\'+p+'\\'+dr+'\\'  # insert filepath here

title = sys.platform.title()
if title == 'linux2':
    pd.options.mode.chained_assignment = None   # to fix a server error when running in vagrant
else:
    pass

form2054=pd.read_csv(path+'DS-2054.txt',sep='|')
form3025vac=pd.read_csv(path+'DS-3025 Vaccinations.txt',sep='|')
predepart=pd.read_csv(path+'Pre-departure Screening.txt',sep='|')
countries=pd.read_csv(path+'country_codes_clean.csv')

pr = Process_Data()
pr.load_countries(path+'../country_codes_clean.csv')

#%%  - select only necessary fields for upload
dtemp=form2054[['AlienNumber','FirstName','MiddleName','LastName',
            'DOB','Sex','Address1','VisaType','DateOfArrival',
            'BirthCountry','PresentCountryOfResidence','PresentAddressOfResidence',
            'PresentCityOfResidence','ClassA','TBActiveClassA',
            'SyphilisClassA','ChancroidClassA','GonorrheaClassA',
            'GranulomaClassA','LymphogranulomaClassA','HansenClassA',
            'AddictionClassA','TBClass','ClassB1Pulmonary',
            'ClassB1Extrapulmonary','ClassB2LTBI','ClassB3Contact',
            'ClassB','ClassBOther','ClassBOtherSpecify','SyphilisClassB',
            'OtherSexTranInfectClassB','PregnancyClassB',
            'NumOfWeeksPregnancy','HansenMultibClassB',
            'HansenMultibClassBTreatment','HansenPaucibClassB',
            'HansenPaucibClassBTreatment','RemissionOfAddictionClassB',
            'MentalDisorderClassA','MentalDisorderClassB']]
d=dtemp.fillna('')  ## did this because I was getting copy error message.
d['name']=map(pr.concat_names,d.FirstName,d.MiddleName,d.LastName)
d.drop(['FirstName','MiddleName','LastName'],inplace=True,axis=1)

#%% - birthdate
d['date_of_birth']=pd.to_datetime(d.DOB)
d.drop(['DOB'],axis=1,inplace=True)
#%% - Sex
d.Sex.replace('M',1,inplace=True)
d.Sex.replace('F',2,inplace=True)
d['gender']=d.Sex
d.drop(['Sex'],axis=1,inplace=True)
#%% - Resettlement Agencies
d['resettlement_agency'] = d.Address1.str.strip()
d['resettlement_agency'] = d.resettlement_agency.str.upper()
d.resettlement_agency.replace('969B CHEROKEE ROAD',1,inplace=True)
d.resettlement_agency.replace('969 CHEROKEE ROAD',1,inplace=True)
d.resettlement_agency.replace('2220 WEST MARKET STREET',2,inplace=True)
d.resettlement_agency.replace('1206 NORTH LIMESTONE',3,inplace=True)
d.resettlement_agency.replace('233 WILLARD STREET',3,inplace=True)
d.resettlement_agency.replace('1710 ALEXANDRIA DRIVE',3,inplace=True)
d.resettlement_agency.replace('1710 ALEXANDRIA DRIVE, SUITE 2',3,inplace=True)
d.resettlement_agency.replace('233 W.  NINTH  STREET,',5,inplace=True)
d.resettlement_agency.replace('806 KENTON STREET',4,inplace=True)
d.resettlement_agency.replace('806 KENTON ST',4,inplace=True)
d.resettlement_agency.replace('',6,inplace=True)
d.drop(['Address1'],axis=1,inplace=True)
#%%
def nullify_addresses(address):
    if address==1:
        return 1
    if address==2:
        return 2
    if address==3:
        return 3
    if address==4:
        return 5
    return 6
    
d.resettlement_agency=map(nullify_addresses,d.resettlement_agency)

#d.drop(['resettlement_agency'],axis=1,inplace=True)
#%% Immigration Status
d.VisaType.replace('R',1,inplace=True)
d.VisaType.replace('SIV',4,inplace=True)
d.VisaType.replace('V93',7,inplace=True)
d.VisaType.replace('V92',8,inplace=True)
d.VisaType.replace('P-R',5,inplace=True)
d['immigration_status']=d.VisaType
d.drop(['VisaType'],axis=1,inplace=True)
#%% - US arrival date
d['us_arrival_date']=pd.to_datetime(d.DateOfArrival)
d.drop(['DateOfArrival'],axis=1,inplace=True)
#%% - Country of Origin
"""  Need to Map Country Abbreviations to Country Names """
d['cntry_code_origin']=d.BirthCountry
d.drop(['BirthCountry'],axis=1,inplace=True)
d['cntry_origin']=map(pr.map_countries,d.cntry_code_origin)

#%% - Country of departure
"""  Need to Map Country Abbreviations to Country Names """
d['cntry_code_dept']=d.PresentCountryOfResidence
d.drop(['PresentCountryOfResidence'],axis=1,inplace=True)
d['cntry_dept']=map(pr.map_countries,d.cntry_code_dept)
#%% - Camp/City of Departure
d['camp_city_departure']=map(pr.get_camp,d.PresentCityOfResidence,d.PresentAddressOfResidence)
residences=['PresentCityOfResidence','PresentAddressOfResidence']
d.drop(residences,axis=1,inplace=True)
#%% Class A Conditions
d['ovs_class_a']=d.ClassA
d.drop(['ClassA'],axis=1,inplace=True)
#%%
d['ovs_class_a_list']=map(pr.process_class_A,d.ovs_class_a,
                d.TBActiveClassA,d.SyphilisClassA,d.ChancroidClassA,
                d.GonorrheaClassA,d.GranulomaClassA,d.LymphogranulomaClassA,
                d.HansenClassA,d.AddictionClassA)

d.drop(['TBActiveClassA', 'SyphilisClassA','ChancroidClassA',
       'GonorrheaClassA', 'GranulomaClassA','LymphogranulomaClassA',
       'HansenClassA', 'AddictionClassA'],axis=1,inplace=True) 
       
d['ovs_class_btb']=map(pr.has_tb,d.TBClass) 

d['ovs_class_btb_type']=map(pr.tb_class,d.TBClass,d.ClassB1Pulmonary,
                         d.ClassB1Extrapulmonary,
                         d.ClassB2LTBI,
                         d.ClassB3Contact)
d.drop(['TBClass','ClassB1Pulmonary',
        'ClassB1Extrapulmonary','ClassB2LTBI',
        'ClassB3Contact'],axis=1,inplace=True)


d['ovs_class_b_other']=d.ClassBOther
d['ovs_class_b_oth_list']=map(pr.classb_other,d.ovs_class_b_other,d.ClassBOtherSpecify)
    
d['ovs_class_b_oth_list2']=map(pr.sti,d.ovs_class_b_other,
        d.SyphilisClassB,d.OtherSexTranInfectClassB)    
d['ovs_class_b_oth_list3']=map(pr.pregnant,d.PregnancyClassB,
            d.NumOfWeeksPregnancy)
d['ovs_class_b_oth_list4']=map(pr.hansen,d.HansenMultibClassB,
            d.HansenMultibClassBTreatment,
            d.HansenPaucibClassB,
            d.HansenPaucibClassBTreatment)
d['ovs_class_b_oth_list5']=map(pr.addiction,d.RemissionOfAddictionClassB)
d['ovs_mntl_hlth']=map(pr.mental,d.MentalDisorderClassA,
            d.MentalDisorderClassB)
d.drop(['ClassBOther','ClassBOtherSpecify','SyphilisClassB',
        'OtherSexTranInfectClassB','PregnancyClassB',
        'NumOfWeeksPregnancy','HansenMultibClassB','HansenMultibClassBTreatment',
        'HansenPaucibClassB','HansenPaucibClassBTreatment',
        'RemissionOfAddictionClassB','MentalDisorderClassA',
        'MentalDisorderClassB','ClassB'],axis=1,inplace=True)
        #%% - Prep the pre-departure dataset
p=predepart[['AlienNumber','TreatmentType','Treatment','Dosage']]
#%% - Get Parasites Data
p['YN']=1

parasite=p[p['TreatmentType']=='Intest Paras Rx Preventive']
parasite.drop(['TreatmentType','Dosage'],axis=1)
p1=parasite.pivot_table(index='AlienNumber',
                  columns='Treatment',
                  values='YN')
p1 = p1.reset_index()
p1.columns=['AlienNumber','ovs_ip_meds_new___1',
             'ovs_ip_meds_new___2','ovs_ip_meds_new___3']
p1['ovs_intstnl_parasites']=1
p1 = p1[['AlienNumber','ovs_ip_meds_new___1',
         'ovs_intstnl_parasites','ovs_ip_meds_new___2']]          
#%%
malaria=p[p['TreatmentType']=='Malaria Rx Preventive']
m1=malaria.pivot_table(index='AlienNumber',
                  columns='Treatment',
                  values='YN')
m1 = m1.reset_index()
try:    # the m1 variable fluctuates between having 2 and 3 columns
    m1.columns=['AlienNumber','ovs_malaria']
    m1['ovs_malaria']=1
    m1=m1[['AlienNumber','ovs_malaria']]
except:
    m1.columns=['AlienNumber','ovs_malaria', 'ovs_malaria_meds']
    m1['ovs_malaria']=1
    m1=m1[['AlienNumber','ovs_malaria' , 'ovs_malaria_meds']]
#%% placeholder code for the occurrence of ovs_syphilis field
#syphilis=p[p['TreatmentType']=='Syphilis Rx Preventative (replace w/ actual column name)']
#s1=syphilis.pivot_table(index='AlienNumber',
#                        columns='Treatment',
#                        values='YN')
#s1 = s1.reset_index()

#s1.columns=['AlienNumber','ovs_syphilis']
#s1=['ovs_syphilis']=1
#s1=s1[['AlienNumber','ovs_syphilis']]
#%% Merge the sets
t1=p1.merge(m1,how='left',left_on='AlienNumber',right_on='AlienNumber')
#t1=t1.merge(s1,how='left',left_on='AlienNumber',right_on='AlienNumber') #syphilis table merge                 
d=d.merge(t1,how='left')
#%%Finish filling out meds information
d.ovs_intstnl_parasites.fillna(0,inplace=True)
d.ovs_malaria.fillna(0,inplace=True)

#%%  Process the Vaccinations/Immunizations
vac = form3025vac
vac['vacname']=map(pr.drop_x,vac.VaccinationName)

#Drop these from record - we do not record them in REDCap
vac=vac[vac.vacname != 'RotaTeq(RV5)']
vac=vac[vac.vacname != 'Rotarix(RV1)']

#%%
#Drop records in which NotAgeAppropriate is "Y" and all dates are 
#empty
vac['NAP']=map(pr.drop_NAPs,vac['HistoryDate1'],vac['HistoryDate2'], 
    vac['HistoryDate3'],vac['HistoryDate4'],vac['DateByPanelPhy'],
    vac['VaccineGivenByIOM1'],vac['VaccineGivenByIOM2'],
    vac['NotAgeAppropriate'])
    
vac=vac[vac.NAP==0]  
vac.to_csv(path+'temp1.csv',index="False") 
#%%
#Need to add this for the pivot, so a record that applies to a particular
#refugee is marked with 1 - all else will be marked with NaN
vac['YN']=1

v=vac[['AlienNumber','vacname', 
    'HistoryDate1', 'HistoryDate2', 
    'HistoryDate3', 'HistoryDate4','DateByPanelPhy',
    'VaccineGivenByIOM1','VaccineGivenByIOM2','NotAgeAppropriate',
    'YN']]
    
v['HistoryDate1']=pd.to_datetime(v.HistoryDate1)
v['HistoryDate2']=pd.to_datetime(v.HistoryDate2)
v['HistoryDate3']=pd.to_datetime(v.HistoryDate3)
v['HistoryDate4']=pd.to_datetime(v.HistoryDate4)
v['DateByPanelPhy']=pd.to_datetime(v.DateByPanelPhy)
v['VaccineGivenByIOM1']=pd.to_datetime(v.VaccineGivenByIOM1)
v['VaccineGivenByIOM2']=pd.to_datetime(v.VaccineGivenByIOM2)


#%%
'''
The original code assumed there was row in v for each possible
polio, pneumo and mcv vaccines.  However, after the NotAgeAppropriates
are dropped, this is no longer the case. This code searches the 
list do determine which vaccinations are in the list and adds those
that are not so there is a column for each possible series vaccine.
'''
#pivot the table 
try:
    vac_yn=v.pivot('AlienNumber','vacname','YN')
except:    # added on 7/13/2017 due to a 'duplicate index' error in the 3025-Vacc dataset; repeats for all v.pivot occurrences
    v.drop_duplicates(inplace=True)
    vac_yn=v.pivot('AlienNumber','vacname','YN')

#%%
series_vacs=['IPV','OPV','PCV10','PCV13','PCV7',
                 'PPSV23','Other MCV conjugate','MCV4','Other']
                 
for vacs in series_vacs:
    if vacs not in vac_yn.columns:
       vac_yn[vacs]=np.NaN
             
#%%
vac_yn['Polio']=map(pr.set_polio, vac_yn.IPV, vac_yn.OPV)
vac_yn['Pneumo']=map(pr.set_pneumo,vac_yn.PCV10,vac_yn.PCV13,
            vac_yn.PCV7,vac_yn.PPSV23)
vac_yn['Mcv']=map(pr.set_mcv,vac_yn['Other MCV conjugate'],vac_yn.MCV4)
vac_yn.drop(series_vacs,axis=1,inplace=True)   
         
#%%          
vac_yn.columns=pr.make_columns(vac_yn.columns)
vac_yn = vac_yn.reset_index()

#%%
def add_empty_columns(df,vacs):
    for vac in vacs:
        if vac not in df.columns:
            df[vac]=np.NaN
    return df
 
vac_h1=v.pivot('AlienNumber','vacname','HistoryDate1')
vac_hd1=add_empty_columns(vac_h1,series_vacs)
vac_h2=v.pivot('AlienNumber','vacname','HistoryDate2')
vac_hd2=add_empty_columns(vac_h2,series_vacs)
vac_h3=v.pivot('AlienNumber','vacname','HistoryDate3')
vac_hd3=add_empty_columns(vac_h3,series_vacs)
vac_h4=v.pivot('AlienNumber','vacname','HistoryDate4')
vac_hd4=add_empty_columns(vac_h4,series_vacs)
vac_p=v.pivot('AlienNumber','vacname','DateByPanelPhy')
vac_panel=add_empty_columns(vac_p,series_vacs)
vac_i1=v.pivot('AlienNumber','vacname','VaccineGivenByIOM1')
vac_iom1=add_empty_columns(vac_i1,series_vacs)
vac_i2=v.pivot('AlienNumber','vacname','VaccineGivenByIOM2')
vac_iom2=add_empty_columns(vac_i2,series_vacs)

#%%
vac_hd1=pr.prep_columns(vac_hd1,vac_yn.columns,'_date1')
vac_hd2=pr.prep_columns(vac_hd2,vac_yn.columns,'_date2')
vac_hd3=pr.prep_columns(vac_hd3,vac_yn.columns,'_date3') 
vac_hd4=pr.prep_columns(vac_hd4,vac_yn.columns,'_date4')
vac_panel=pr.prep_columns(vac_panel,vac_yn.columns,'_panel') 
vac_iom1=pr.prep_columns(vac_iom1,vac_yn.columns,'_iom1') 
vac_iom2=pr.prep_columns(vac_iom2,vac_yn.columns,'_iom2')

#%%
#Merge the vaccinations
vaccinations=vac_yn.merge(vac_hd1,how='left', left_on='AlienNumber', right_on='AlienNumber')
vaccinations=vaccinations.merge(vac_hd2,how='left', left_on='AlienNumber', right_on='AlienNumber')
vaccinations=vaccinations.merge(vac_hd3,how='left', left_on='AlienNumber', right_on='AlienNumber')
vaccinations=vaccinations.merge(vac_hd4,how='left', left_on='AlienNumber', right_on='AlienNumber')

#Merge Panel/IOM vaccinations
depart_vac=vac_panel.merge(vac_iom1,how='left', left_on='AlienNumber', right_on='AlienNumber')
depart_vac=depart_vac.merge(vac_iom2,how='left', left_on='AlienNumber', right_on='AlienNumber')
depart_vac.to_csv(path+'departure_vaccinations.csv',index=False) 

#%%  Merge Vaccinations with data
d=d.merge(vaccinations,how='left', left_on='AlienNumber', right_on='AlienNumber')

#%% - AlienNumber - reformat the alien_no so it matches our storage format
d['alien_no']=['A'+str(row) for row in d['AlienNumber']]  #list comprehension approach
d.drop(['AlienNumber'],inplace=True,axis=1)

#%%
d1=d.dropna(axis='columns',how='all')

#%%
data_cols = [col for col in d1.columns if 'date' in col]
for col in data_cols:
    d1[col]=d1[col].dt.strftime('%Y-%m-%d')
    d1[col].replace('NaT','',inplace=True,axis=1)
d2=d1.copy()
d2.to_csv(path+'column_error.csv',index=False)

#%% - legacy code
#d3 = d2[['alien_no','name','date_of_birth','gender',
#        'resettlement_agency','immigration_status','us_arrival_date',
#        'cntry_code_origin','cntry_code_dept', 
#        'ovs_class_a','ovs_class_a_list',
#        'ovs_class_btb','ovs_class_btb_type','ovs_class_b_other',
#        'ovs_class_b_oth_list','ovs_class_b_oth_list2',
#        'ovs_class_b_oth_list3',
#        'ovs_mntl_hlth','ovs_ip_meds_new___1',
#        'ovs_ip_meds_new___2','ovs_ip_meds_new___4',
#        'ovs_malaria_meds',
#        'oi_dtap_dtp_dt','oi_hepa','oi_hbv',
#        'oi_hib','oi_influenza','oi_mmr','oi_measles','oi_mumps',
#        'oi_td','oi_tdap','oi_varicella','oi_polio', 'oi_pneumococcal',
#        'oi_dtap_dtp_dt_date1','oi_hepa_date1','oi_hbv_date1',
#        'oi_hib_date1','oi_mmr_date1','oi_measles_date1',
#        'oi_mumps_date1','oi_td_date1','oi_tdap_date1',
#        'oi_varicella_date1','oi_polio_date1','oi_pneumococcal_date1',
#        'oi_dtap_dtp_dt_date2','oi_hepa_date2','oi_hbv_date2',
#        'oi_hib_date2','oi_mmr_date2','oi_measles_date2','oi_td_date2',
#        'oi_polio_date2','oi_pneumococcal_date2',
#        'oi_dtap_dtp_dt_date3','oi_hepa_date3','oi_hbv_date3',
#        'oi_hib_date3','oi_polio_date3','oi_pneumococcal_date3',
#        'oi_dtap_dtp_dt_date4','oi_hbv_date4','oi_hib_date4',
#        'oi_polio_date4']]

#%%
d2 = d2.T.groupby(level=0).first().T # added to remove duplicate columns
data = d2.to_json(orient='records',double_precision=0)

d2.cntry_code_dept.loc[d2.cntry_code_dept == 'UP'] = 'UA'
d2.cntry_code_dept.loc[d2.cntry_code_dept == 'ZA'] = 'SF'
d2.cntry_code_dept.loc[d2.cntry_code_dept == 'GV'] = 'GN'
d2.cntry_code_dept.loc[d2.cntry_code_dept == 'HO'] = ''
d2.cntry_code_origin.loc[d2.cntry_code_origin == 'UP'] = 'UA'
d2.cntry_code_origin.loc[d2.cntry_code_origin == 'ZA'] = 'SF'
d2.cntry_code_origin.loc[d2.cntry_code_origin == 'GV'] = 'GN'
d2.cntry_code_origin.loc[d2.cntry_code_origin == 'HO'] = ''

d2.replace('NaT', '', inplace=True, axis=1)  # added to remove NaT values from csv file

#%% - Create CSV file for upload purposes
d2=d2.fillna(value='', axis=1)
d2.to_csv(path+'EDNupload_'+dr+'.csv', index=False, date_format='%Y-%m-%d')    # create CSV file for manual import

#%% - Alternatively, perform upload using REDCap API 
# pr.upload_data(data)
