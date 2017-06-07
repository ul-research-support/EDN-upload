# -*- coding: utf-8 -*-
import pandas as pd
import pycurl, cStringIO
import certifi

class Process_Data(object):
    """
    Main Process Data object.

    Example::

        pr = Process_Data()

    """
    def __init__(self):
        self.description='Class to Process Data'
    
    
    def concat_names(self,f,m,l):
        """
        :synopsis: Concatenate the names of the input into a single variable.
        :param f: First Name
        :param m: Middle name
        :param l: Last Name
        :returns: Concatenated string --> REDCap Variable:  **[name]**
        
        Example::

            d['name']=map(pr.concat_names,d.FirstName,d.MiddleName,d.LastName)

        """

        if m=='':
            return l+", "+f
        return l+", "+f+", "+m
    
    def load_countries(self,c):
        """
        :synopis: Load the countries into a dataframe for country/code look up table.
        :param c:  Path to csv file with country names
        :returns:   Reference to file with country names/codes
        :note: This file is country_codes_clean.csv  

        Example::

            pr.load_countries(path+'country_codes_clean.csv')

        """
        self.countries=pd.read_csv(c)
        
        
    def map_countries(self,c):
        """
        :synopsis: Map the country codes provided by EDN to the country names provided by country_codes_clean.csv file.
        :param c:   Country code to map
        :returns:   Country name-->REDCAP Variable:  **[cntry_origin], [cntry_dept]**
        :note: This module is used to map codes-->countries for both origin and departure

        Example::

                   d['cntry_origin']=map(pr.map_countries,d.cntry_code_origin)
                   d['cntry_dept']=map(pr.map_countries,d.cntry_code_dept)

        """
        for index, country in self.countries.iterrows():
            if c==country['country_codes']:
                return country['country']
    
    
    def get_camp(self,city,camp):
        """
        :synopsis: Map the country codes provided by EDN to the country names provided by country_codes_clean.csv file.
        :param c:  City of Residence, Camp of Residence
        :returns:  Camp or City-->REDCAP Variable:  **[camp_city_departure]**
        :note: This module is used to fill camp name/city name

        Example::

                  d['camp_city_departure']=map(pr.get_camp,d.PresentCityOfResidence,d.PresentAddressOfResidence)
        """
        if pd.isnull(camp):
            return city
        else:
            return camp
    
    def  process_class_A(self,cla,tb,syph,chanc,gon,gran,lymph,hansen,addict):
        """
        :synopsis:      Checks variables to determine if the refugee has any Class A Conditions.
        :param cla:     Class A Conditions (1/0)
        :param tb:      Tuberculosis (1/0)
        :param syph:    Syphillis (1/0)
        :param chanc:   Chancroid (1/0)
        :param gon:     Gonorrhea (1/0)
        :param gran:    Granuloma (1/0)
        :param lymph:   Lymphogranuloma (1/0)
        :param hansen:  Hansen's Diseases (1/0)
        :param addict:  Addiction (1/0)
        :returns:   List of Class A Conditions-->REDCap Variable: **[ovs_class_a_list]**

        Example::

            d['ovs_class_a_list']=map(pr.process_class_A,d.ovs_class_a,
                d.TBActiveClassA,d.SyphilisClassA,d.ChancroidClassA,
                d.GonorrheaClassA,d.GranulomaClassA,d.LymphogranulomaClassA,
                d.HansenClassA,d.AddictionClassA)
        
        .. todo::  

            No Class A conditions were present in the sample data. Still need to finish the code
            to check every variable that has been passed into the function.

        """
             
        if cla==0:
            return ''
        
        classa = ''
        if tb==1:
            classa=classa+'TB\n'
        if syph==1:
            classa=classa+'Syphillis\n'
        
        return classa
        
    def has_tb(self,tb):
        """
        :synopsis: Check for Class B Tuberculosis
        :param tb:  Tuberculosis (1/0)
        :returns:   (int) 1/0 --> REDCap Variable: **[ovs_class_btb]**   

        Example::

            d['ovs_class_btb']=map(pr.has_tb,d.TBClass) 
      
        """
        if tb=='None':
            return 0
        else:
            return 1
            
    def tb_class(self,tb,b1,b1ex,b2,b3):
        """
        :synopsis: Check for Class B Tuberculosis
        :param tb:      Tuberculosis (1/0)
        :param b1:      Class B1 Pulmonary (1/0)
        :param b1ex:    Class B1 Extrapulmonary (1/0)
        :param b2:      Class B2 LTBI (1/0)
        :param b3:      Class B3 Contact (1/0) 
        :returns:       TB Class-->REDCap Variable: **[ovs_class_btb_type]**
        
        Example::

            d['ovs_class_btb']=map(pr.has_tb,d.TBClass)
      
        """
        if tb==0:
            return ''
        if b1==1 or b1ex==1:
            return 1
        if b2==1:
            return 2
        if b3==1:
            return 3
        
        return ''
    

    def classb_other(self,classb,l):
        """
        :synopsis: Set variable to indicate there is an unlisted Class B conditions to process.
        :param classb:  Class B Conditions (1/0)
        :param l:       List of Class B Conditions
        :returns:   List of Class B Conditions to write to dataset-->REDCap Variable: **[ovs_class_b_other_list]**
        
        Example::

            d['ovs_class_b_oth_list']=map(pr.classb_other,d.ovs_class_b_other,d.ClassBOtherSpecify
      
        """
        if classb==1:
            return l
      
    def sti(self,classb,syph,ost):
        """
        :synopsis:      Set variable to indicate there is an Sexually Transmitted Class B conditions to process.
        :param classb:  Class B Conditions (1/0)
        :param syph:    Syphilis (1/0)
        :param ost:     Other Sexually Transmitted Condition (string)
        :returns:       List of Sexually Transmitted Class B Conditions to write to dataset-->REDCap Variable: **[ovs_class_b_other_list2]**

        Example::

            d['ovs_class_b_oth_list2']=map(pr.sti,d.ovs_class_b_other,
            d.SyphilisClassB,d.OtherSexTranInfectClassB) 
            
        """
        l = ''     
        if syph==1:
            l = l + 'Syphilis\n'
        if ost==1:
            l = l + 'Other STI'
        
        return l
    
    def pregnant(self,p,num):
        """
        :synopsis:      Set variable to indicate there a Pregnant Class B conditions to process.
        :param p:       Pregnant (1/0)
        :param num:     Number of Weeks (string)
        :returns:       Class B Pregnancy Conditions to write to dataset-->REDCap Variable: **[ovs_class_b_other_list3]**

        Example::

            d['ovs_class_b_oth_list3']=map(pr.pregnant,d.PregnancyClassB,
                d.NumOfWeeksPregnancy) 
            
        """
        l = ''
        if p==1:
            l = l+'Pregnant '+str(num)
        return l


    def hansen(self,hmcb,hmcbt,hpcb,hpcbt):
        """
        :synopsis:      Set variable to indicate there Class B conditions (Hansens' Disease) to process.
        :param hmcb:    Hansen MultiClass B 
        :param hmcbt:   Hansen MultiClass B Treatment
        :param hpcb:    Hansen PaucibClass B
        :param hpcbt:   Hansen PaucibClass B Treatment
        :returns:       Class B Hansen Conditions to write to dataset-->REDCap Variable: **[ovs_class_b_other_list4]**

        Example::

            d['ovs_class_b_oth_list4']=map(pr.hansen,d.HansenMultibClassB,
                d.HansenMultibClassBTreatment,
                d.HansenPaucibClassB,
                d.HansenPaucibClassBTreatment) 
            
        """
        l = ''
        if hmcb==1:
            l = l + hmcbt +'\n'
        if hpcb==1:
            l = l +hpcbt
        return l

    def addiction(self,a):
        """
        :synopsis:      Set variable to indicate there a  Class B Addiction condition to process.
        :param a:       Addiction (1/0)
        :returns:       Class B Addiction Condition to write to dataset-->REDCap Variable: **[ovs_class_b_other_list5]**

        Example::

            d['ovs_class_b_oth_list5']=map(pr.addiction,d.RemissionOfAddictionClassB) 
            
        """
        if a==1:
            return 'Remission of Addiction'

    def mental(self,ma,mb):
        """
        :synopsis:      Set variable to indicate there a mental disorder
        :param ma:      Class A Mental Disorder (1/0)
        :param mb:      Class B Mental Disorder (1/0)  
        :returns:       Mental Disorder to write to dataset-->REDCap Variable: **['ovs_mntl_hlth']**

        Example::

            d['ovs_mntl_hlth']=map(pr.mental,d.MentalDisorderClassA,
                d.MentalDisorderClassB) 
            
        """
        if ma==1 or mb==1:
            return 1
        else:
            return 0
    
    def checknull(self,d):
        if pd.isnull(d):
            return 0
        else:
            return 1

    def drop_NAPs(self,d1,d2,d3,d4,d5,d6,d7,nap):
        no_dates = 0;
        no_dates = no_dates+self.checknull(d1)
        no_dates = no_dates+self.checknull(d2)
        no_dates = no_dates+self.checknull(d3)
        no_dates = no_dates+self.checknull(d4)
        no_dates = no_dates+self.checknull(d5)
        no_dates = no_dates+self.checknull(d6)
        no_dates = no_dates+self.checknull(d7)
        
        if no_dates==0:
            return 1
        else:
            return 0  
            
    def drop_x(self,vaccine):
        """
        :synopsis:          Clean the vaccine data to strip out leading [Xx]
        :param vaccine:     Vaccine entry
        :returns:           Cleaned Vaccine String-->REDCap Variable: **None - temp variable**

        Example::

           vac['vacname']=map(pr.drop_x,vac.VaccinationName) 
            
        """
        to_strip='Specify (check) vaccine:'        
        if vaccine.startswith(to_strip):
            vaccine=vaccine.lstrip(to_strip)
            print vaccine
        if vaccine.startswith('[X]Td'):
            return 'Td'
        if vaccine.startswith('[X]Polio-OPV'):
            return 'OPV' 
        if vaccine.startswith('MMR (Measles'):
            return 'MMR'        
        if vaccine.startswith('[x]'):
            return vaccine.lstrip('[x]')
        if vaccine.startswith('[ ]'):
            return vaccine.lstrip('[ ]')

        
            
        return vaccine
        
    def set_polio(self,i,o):
        """
        :synopsis:      Evaluate if Polio vaccination has been received
        :param i:       IPV vaccination received (1/0)
        :param o:       OPV vaccination received (1/0)
        :returns:       Polio Vaccine (1/0)-->REDCap Variable: **['Polio']**

        Example::

           vac_yn['Polio']=map(pr.set_polio, vac_yn.IPV, vac_yn.OPV) 
            
        """
        if i==1 or o==1:    
            return 1
    
    def set_pneumo(self,p10,p13,p7,p23):
        """
        :synopsis:      Evaluate if Pneumococcal vaccination has been received
        :param p10:     Pneumococcal PCV10 vaccination received (1/0)
        :param p13:     Pneumococcal PCV13 vaccination received (1/0)  
        :param p7:      Pneumococcal PCV7 vaccination received (1/0) 
        :param p23:     Pneumococcal PPSV23 vaccination received (1/0)
        :returns:       Pneumo Vaccine (1/0)-->REDCap Variable: **['Pneumo']**

        Example::

           vac_yn['Pneumo']=map(pr.set_pneumo,vac_yn.PCV10,vac_yn.PCV13,
                vac_yn.PCV7,vac_yn.PPSV23) 
            
        """
        if p10==1 or p13==1 or p7==1 or p23==1:
            return 1
                
    def set_mcv(self,m1,m2):
        """
        :synopsis:      Evaluate if Meningococcal vaccination has been received
        :param m1:      MCV4 vaccination received (1/0)
        :param m2:      Other MC vaccination received (1/0)
        :returns:       MCV Vaccine (1/0)-->REDCap Variable: **['Polio']**

        Example::

           vac_yn['Mcv']=map(pr.set_mcv,vac_yn['Other MCV conjugate'],vac_yn.MCV4) 
            
        """
        if m1==1 or m2==1:
            return 1
    
    def make_columns(self,cols):
        """
        :synopsis:      Change the column names from EDN format to REDCap Format
        :param cols:    List of column names from EDN
        :returns:       List of columns names for-->REDCap Variable: **None - temp variable**

        Example::

           vac_yn.columns=pr.make_columns(vac_yn.columns) 
            
        """
        columns=list()    
        for col in cols:
            if col=='DT, DTP, DTaP':
                columns.append('oi_dtap_dtp_dt')
            elif col=='Hepatitis A':
                columns.append('oi_hepa')
            elif col=='Hepatitis B':
                columns.append('oi_hbv')
            elif col=='Hib':
                columns.append('oi_hib')
            elif col=='Influenza':
                columns.append('oi_influenza')
            elif col=='MMR':
                columns.append('oi_mmr')
            elif col=='Mcv':
                columns.append('oi_mcv')
            elif col=='Measles':
                columns.append('oi_measles')
            elif col=='Mumps':
                columns.append('oi_mumps')
            elif col=='Pneumo':
                columns.append('oi_pneumococcal')
            elif col=='Polio':
                columns.append('oi_polio')
            elif col=='Rubella':
                columns.append('oi_rubella')
            elif col=='Td':
                columns.append('oi_td')
            elif col=='Tdap':
                columns.append('oi_tdap')
            else:
                columns.append('oi_varicella')
    
        return columns

    def set_polio_dates(self,i,o):
        """
        :synopsis:      REDCap contains only 1 polio variable,this module gets the date of whichever polio vaccine the refugee received 
        :param i:       IPV Vaccination date
        :param o:       OPV Vaccination date
        :returns:       Dataframe with vaccination dates-->REDCap Variable: **None - temp variable**

        Example::

           df['Polio']=map(self.set_polio_dates, df.IPV, df.OPV)
            
        """
        if pd.notnull(i):
            return i
        else:
            return o
    
    def set_pneumo_dates(self,p10,p13,p7,p23):
        """
        :synopsis:      Gets the date of each PCV vaccine the refugee received
        :param p10:     Pneumococcal PCV10 vaccination date
        :param p13:     Pneumococcal PCV13 vaccination date  
        :param p7:      Pneumococcal PCV7 vaccination date 
        :param p23:     Pneumococcal PPSV23 vaccination date
        :returns:       Dataframe with vaccination dates-->REDCap Variable: **None - temp variable**

        Example::

           df['Pneumo']=map(self.set_pneumo_dates,df.PCV10,df.PCV13,
                df.PCV7,df.PPSV23) 
            
        """
        if pd.notnull(p10):
            return p10
        elif pd.notnull(p13):
            return p13
        elif pd.notnull(p7):
            return p7
        else:
            return p23
                
    def set_mcv_dates(self,m1,m2):
        """
        :synopsis:      REDCap contains only 1 MCV variable, \
        this module gets the date of whichever MCV vaccine the refugee received 
        :param m1:       MCV4 Vaccination date
        :param m2:       MCV Other Vaccination date
        :returns:        Dataframe with vaccination dates-->REDCap Variable: **None - temp variable**

        Example::

           df['Mcv']=map(self.set_mcv_dates,df['Other MCV conjugate'],
                df.MCV4)
            
        """
        if pd.notnull(m1):
            return m1
        else:
            return m2
    
    def prep_columns(self,df,cols,suffix):
        """
        :synopsis:       Set up 4 columns for past vaccination dates \
        and 3 columns for departure vaccination dates  
        :param cols:     Columns to process
        :param suffix:   Date suffix to append to column name
        :returns:        Dataframe with vaccination dates-->REDCap Variable: **None - temp variable**

        Example::

           vac_hd1=pr.prep_columns(vac_hd1,vac_yn.columns,'_date1')
            
        """
        df['Polio']=map(self.set_polio_dates, df.IPV, df.OPV)
        df['Pneumo']=map(self.set_pneumo_dates,df.PCV10,df.PCV13,
                df.PCV7,df.PPSV23)
        df['Mcv']=map(self.set_mcv_dates,df['Other MCV conjugate'],
                df.MCV4)
        df.drop(['IPV','OPV','PCV10','PCV13','PCV7',
                     'PPSV23','Other MCV conjugate','MCV4','Other'],
                axis=1,inplace=True)
        df_cols = [col+suffix for col in cols if col !='AlienNumber']  
        df.columns=df_cols
        df=df.reset_index()
        return df
    
    def upload_data(self,d):
        """
        :synopsis: Upload the data using the REDCap API
        :param d:   JSON data to post to REDCap Server
        :returns:   Null
        
        .. todo::  

            Need to make sure all fields are present in REDCap database \
            each vaccine should have at least four dates to match EDN.

     
        """
        buf = cStringIO.StringIO()
        data = {
            'token': 'C63575A754CB3DFDAB9B9E4AD1B36A5A',
            'content': 'project',
            'format': 'json',
            'returnFormat': 'json'
        }
        ch = pycurl.Curl()
        ch.setopt(pycurl.CAINFO, certifi.where())  ### PYTHON will fail without this reference
        ch.setopt(ch.URL, 'https://refugeehealth.louisville.edu/api/')
        ch.setopt(ch.HTTPPOST, data.items())
        ch.setopt(ch.WRITEFUNCTION, buf.write)
        ch.perform()
        ch.close()
        print buf.getvalue()
        buf.close()
