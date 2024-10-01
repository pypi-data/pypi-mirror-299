import pandas as pd
import re
import numpy as np
from typing import Union, Literal,Optional
from fuzzywuzzy import process



class POC_matching:
    """
    Args:
    --------
    comp: str
        The survey number that needs to be looked for a match.
    to_check_list: list
        List containing survey number from our database for POC
            
    .. note::

        Make sure it is a :code:`list` and not a :code:`string list`. Import :code:`ast` and use :code:`ast.literal_eval(<list>)` to convert :code:`string-list` to :code:`list`.
    """ 
    

    replace_dict_tel = {'అ': 'A', 'ఆ': 'AA', 'ఇ': 'I', 'ఈ': 'EE', 'ఉ': 'U', 'ఊ': 'OO', 'ఋ': 'RU', 'ज': 'JA', 'ౠ': 'RUU', 'ర': 'R',
                         'ు': 'U', 'మ': 'M', 'ా': 'AA', 'ద': 'DHA', 'గ': 'G', 'ి': 'I', 'ం': 'M', 'డ': 'DA', 'ల': 'LA', 'ఎ': 'E', 'ఏ': 'E',
                        'ఓ': 'O', 'ఐ': 'AI', 'ఔ': 'AU', 'చ': 'CHA', 'ె': 'E', 'వ': 'VA', 'క': 'KA', 'ప': 'PA', 'ో': 'O', 'ూ': 'U', 'ై': 'AI',
                        'బ': 'B', 'జ': 'JA', 'ట': 'TA', 'ే': 'E', 'న': 'NA', 'ఒ': 'O', 'య': 'YA', 'ః': 'AH', 'ఖ': 'K', 'భ': 'B', 'స': 'SA',
                        'ఫ': 'PHA', 'ఘ': 'GHA', 'ఝ': 'JAA', 'ఛ': 'CHA', 'ఞ': 'INI', 'ఠ': 'TAA', 'ఢ': 'DAA', 'ణ': 'NA', 'త': 'THA', 'థ': 'THAA',
                        'ధ': 'DHA', 'ష': 'SHA', 'ఙ': 'GNA', 'ఁ': 'RA', 'హ': 'HA', 'శ': 'SHA', '౦': 'O', 'ొ': 'O', 'ఌ': 'RU', 'à': 'AA', 'ౌ': 'AU',
                        'ళ': 'LA', 'ఱ': 'RA', 'ృ': 'RU', 'ీ': 'EE', 'ड़': 'DAA', 'ౡ': 'RUU', 'ఝూ': 'JHU', 'అే': 'AE', 'ो': 'AE', 'म': 'M',
                        'ु': 'U', 'द': 'D', 'ग': 'G'}
    
    replace_dict_kar = {'ಅ': 'A', 'ಬ': 'B', 'ಕ': 'K', 'ಡ': 'D', 'ಇ': 'E', 'ಆ': 'A', 'ಬಿ': 'B', 'ಫ': 'P', 'ಎ': 'E', 'ಈ': 'E',
                         'ಗ': 'G', 'ಸಿ': 'C', 'ಹ': 'H', 'ಜಿ': 'G','ಡಿ': 'D', 'ಜೆ': 'G', 'ಉ': 'A', 'ಆಯ್': 'I'
                        ,'ಎಚ್': 'H', 'ಪಿ': 'P', 'ಕೆ': 'K', 'ಪಾ': 'P', 'ಪ': 'P',
                        'ರಸ್ತೆ': 'ROAD', 'ರ': 'R', 'ಐ': 'E', 'ಶೇ': 'C', 'ಓ': 'O', 'ಸೇ': 'C', 'ಎನ್': 'N', 'ಬಿನ್': 'B'}
    
    replace_dict_Hin = {'अ': 'A', 'आ': 'AA', 'इ': 'E', 'ई': 'I', 'उ': 'U', 'ऊ': 'OO', 'ए': 'A', 'ऐ': 'AE', 'ओ': 'O', 'औ': 'AO', 'अं': 'AM', 'अः': 'A:',
                        'ऋ': 'RI', 'ॠ': 'RR', 'ा': 'AA', 'ि': 'I', 'ी': 'II', 'ु': 'U', 'ू': 'UU', 'ृ': 'R', 'ॄ': 'RR', 'ॅ': 'E', 'ॆ': 'E', 'े': 'E', 'ै': 'AI',
                        'ॉ': 'O', 'ॊ': 'O', 'ो': 'O', 'ौ': 'AU', 'क': 'K', 'ख': 'KHA', 'ग': 'G', 'घ': 'GHA', 'ङ': 'NGA', 'च': 'CA', 'छ': 'CHHA', 'ज': 'JA',
                        'झ': 'JHA', 'ञ': 'NYA', 'ट': 'TA', 'ठ': 'THH', 'ड': 'DA', 'ढ': 'DH', 'ण': 'N', 'त': 'T', 'थ': 'THA', 'द': 'D', 'ध': 'DHA', 'न': 'NA',
                        'प': 'P', 'फ': 'FA', 'ब': 'B', 'भ': 'BHA', 'म': 'MA', 'य': 'Y', 'र': 'R', 'ल': 'LA', 'व': 'V', 'श': 'SHA', 'ष': 'SHHA', 'स': 'SA',
                        'ह': 'HA', 'क्ष': 'KSH', 'त्र': 'TRA', 'ज्ञ': 'GYA', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7',
                         '८': '8', '९': '9'}
    
    replace_dict_Od = {'ଅ': 'A', 'ଆ': 'AA', 'ଇ': 'I', 'ଈ': 'II', 'ଉ': 'U', 'ଊ': 'UU', 'ଋ': 'R', 'ଌ': 'L', 'ଏ': 'E', 'ଐ': 'AI', 'ଓ': 'O', 'ଔ': 'AU',
                       'ା': 'AA', 'ି': 'I', 'ୀ': 'II', 'ୁ': 'U', 'ୂ': 'UU', 'ୃ': 'R', 'ୄ': 'RR', 'େ': 'E', 'ୈ': 'AI', 'ୋ': 'O', 'ୌ': 'AU', 'କ': 'KA',
                       'ଖ': 'GA', 'ଘ': 'GHA', 'ଙ': 'NGA', 'ଚ': 'CA', 'ଛ': 'CHA', 'ଜ': 'JA', 'ଝ': 'JHA', 'ଞ': 'NYA', 'ଟ': 'TTA', 'ଠ': 'TTHA', 'ଡ': 'DDA',
                       'ଢ': 'DDHA', 'ଣ': 'NNA', 'ତ': 'TA', 'ଥ': 'THA', 'ଦ': 'DA', 'ଧ': 'DHA', 'ନ': 'NA', 'ପ': 'PA', 'ଫ': 'PHA', 'ବ': 'BA', 'ଭ': 'BHA',
                       'ମ': 'MA', 'ଯ': 'YA', 'ର': 'RA', 'ଲ': 'LA', 'ଳ': 'LLA', 'ଵ': 'VA', 'ଶ': 'SHA', 'ଷ': 'SSA', 'ସ': 'SA', 'ହ': 'HA', 'ଡ଼': 'RRA',
                       'ଢ଼': 'RHA', 'ୟ': 'YYA', '୧': '1', '୨': '2', '୩': '3', '୪': '4', '୫': '5', '୬': '6', '୭': '7', '୮': '8','୯': '9'}
                      
    """
    patterns for string updation method
    """
    pattern_eng = r'(\d[a-zA-Z]+)|([a-zA-Z]\d+)'
    pattern_hi = r'(\d[a-zA-Z\u0900-\u097F\u200d]+)|([a-zA-Z\u0900-\u097F\u200d]\d+)'
    pattern_tel = r'(\d[a-zA-Z\u0C00-\u0C7F]+)|([a-zA-Z\u0C00-\u0C7F]\d+)'
    pattern_kan = r'(\d[a-zA-Z\u0C80-\u0CFF]+)|([a-zA-Z\u0C80-\u0CFF]\d+)'
    pattern_od = r'(\d[a-zA-Z\u0B00-\u0B7F]+)|([a-zA-Z\u0B00-\u0B7F]\d+)'
    

    def __init__(self,comp:str,check_list:list[str]):
        """

        Args:
        --------
        comp: The survey number that needs to be looked for a match.
        to_check_list: List containing survey number from our database for POC
                
        .. note::

           Make sure it is a `list` and not a `string list`. Import ast and use ast.literal_eval(<list>) to convert `string list` to `list`.
        """ 
        
        self.compare = comp
        self.to_check_list =check_list

    
    def D1D2_cold(self):
        """
        This method prevents one-to-many matches (one-D1 and many-D2) in D1-D2 matching

        Return:
        -------------
        :code:`list` containing the index of the correct survey number

        Example:
        -------------
        >>> string = '13/1'
        >>> comparing_list = ['13 (s)','14/1 (s)','13/2 (p)','13/1/1 (p)','13/1/2 (p)']
            # correct index is [0] i.e ['13 (s)']
        >>> print(POC_matching(string,comparing_list).D1D2_cold())
            [0]
        """

        new_compare = self.clean_bandit(self.compare)
        correct_index = []
        for i, sur in enumerate(self.to_check_list):
            if not pd.notna(sur):
                continue
            updated_sur = self.clean_bandit(sur)
            split_val =[re.sub(r'^0+','',numb).strip() for numb in new_compare.split('/')]
            split_val2 = [re.sub(r'^0+','',numb).strip() for numb in updated_sur.split('/')]
            if len(split_val)<len(split_val2):
                continue
            min_len = min(len(split_val),len(split_val2))
            if (np.array(split_val[:min_len])==np.array(split_val2[:min_len])).all()==True:
                # print('correct')
                correct_index.append(i)
            
            else:
                # print('Not correct')
                pass

        return correct_index
    
    
    def right_choice(self):
        r"""  
        Applicabe to states like :code:`MP`, :code:`MH`, :code:`OD`, and :code:`RJ` if survey number does not have regional/english alphabet. Here the survey number is split based on :code:`/`.
        but if you find **'-'** or **'\\'** as a split, go for :code:`right_choice_AP`.

        Return:
        -------------
        :code:`list` containing the index of the correct survey number

        .. note::

           This method is used for states that do not have regional language issues and the client data format matches the DB format of the survey number

        Example:
        -------------
        >>> string = '13/1'
        >>> comparing_list = ['13/1 (s)','14/1 (s)','13/2 (p)','13/1/1 (p)']
            # correct index is [0,3] i.e ['13/1 (s)','13/1/1 (p)']
        >>> print(POC_matching(string,comparing_list).right_choice())
            [0,3]
        """

        new_compare = self.clean_bandit(self.compare.strip())
        correct_index = []
        for i, sur in enumerate(self.to_check_list):
            if not pd.notna(sur):
                continue
            updated_sur = self.clean_bandit(sur.strip())
            split_val =[re.sub(r'^0+','',numb).strip() for numb in new_compare.split('/')]
            split_val2 = [re.sub(r'^0+','',numb).strip() for numb in updated_sur.split('/')]
            min_len = min(len(split_val),len(split_val2))
            if (np.array(split_val[:min_len])==np.array(split_val2[:min_len])).all()==True:
                # print('correct')
                correct_index.append(i)
            
            else:
                # print('Not correct')
                pass

        return correct_index
    

    def right_choice_AP(self,include:Literal['normal','both']='normal',state:Optional[Literal['TS','AP','MH','KA','RJ','OD']]=None, split_pat: str = r"\/|\-"):
        r"""
        Used for matching states that have regional/english alphabet in survey_no. This can also be used if the survey_number has different pattern for spliting.

        Args:
        --------------------- 
        include: str
            It includes :code:`normal (default)` which is used when you want to match without changing the characters i.e the english alphabet will not be converted to Regional character for matching and `both`, which is first matched without changing 
            alphabets and then matched by changing alphabets.
         
        state: str
            The state you are working with. By default state is :code:`None`. The :code:`state` can be anything if :code:`include` is :code:`normal`, but if include is :code:`both`, the :code:`state` has to be mentioned. It takes :code:`TS`, :code:`AP`, :code:`MH`, :code:`RJ`, :code:`OD` or :code:`KA`
           
        split_pat: str
            The pattern (regex prefered) based on which the text has to split. The default is :code:`\/|\-` i.e. split is based on either **'/'** or **'-'**.
                    

        Return:
        -------------
        :code:`list` containing the index of the correct survey number
        
        Example:
        -------------------  
        >>> string = '13/A1'
        >>> comparing_list = ['13/A1','14/A/1','12/A/1','13/అ','13-అ/1']
            #correct matching is [0,3,4] index i.e. '13/A1','13/అ','13-అ/1' 
        >>> print(POC_matching(string,comparing_list).right_choice_AP(include='normal'))
            [0]
        >>> print(POC_matching(string,comparing_list).right_choice_AP(include='both',state='AP'))
            [0, 3, 4]
        
        """
        if state is None:
            ref = 'En'

        elif state in ['TS','AP']:
            ref = 'Tel'

        elif state in ['RJ','MH']:
            ref = 'Hi'

        elif state == 'KA':
            ref = 'Ka'

        elif state == 'OD':
            ref = 'Od'

        else:
            raise ValueError("Please enter valid argument. It supports 'TS','AP','MH','KA', 'OD', and 'RJ'")
        
        new_compare = self.clean_bandit(POC_matching.string_updation(self.compare.strip(),ref).strip())
        correct_index = []
        pattern = split_pat
        for i, sur in enumerate(self.to_check_list):
            if not pd.notna(sur):
                continue
            updated_sur = self.clean_bandit(POC_matching.string_updation(sur.strip()).strip())
            split_val =[re.sub(r'^0+','',numb).strip() for numb in re.split(pattern,new_compare)]
            split_val2 = [re.sub(r'^0+','',numb).strip() for numb in re.split(pattern,updated_sur)]
            min_len = min(len(split_val),len(split_val2))
            if (np.array(split_val[:min_len])==np.array(split_val2[:min_len])).all()==True:
                # print('correct')
                correct_index.append(i)
            
            else:
                # print('Not correct')
                pass
        if include=='both':
            correct_index_up = self.change_char_match(self.compare,self.to_check_list,correct_index,ref,pattern)

        else:
            correct_index_up = correct_index.copy()

        return list(set(correct_index_up))
    

    def change_char_match(self,comparing:str,to_check_list:list[str],index_correct:list[int],refer,pattern_spliting):
        """
        This method is called by the method 'right_choice_AP' if 'both' is mentioned as an args.

        Return:
        -------------
        :code:`list` containing the index of the correct survey number
        """
        
        compare = POC_matching.char_assasin(comparing,refer)
        
        new_compare = self.clean_bandit(POC_matching.string_updation(compare.strip(),refer).strip())
        
        pattern = pattern_spliting
        for i, row in enumerate(to_check_list):
            if not pd.notna(row):
                continue
            sur = POC_matching.char_assasin(row,refer)
            updated_sur = self.clean_bandit(POC_matching.string_updation(sur.strip(),refer).strip())
            split_val =[re.sub(r'^0+','',numb).strip() for numb in re.split(pattern,new_compare)]
            
            split_val2 = [re.sub(r'^0+','',numb).strip() for numb in re.split(pattern,updated_sur)]
            
            min_len = min(len(split_val),len(split_val2))
            if (np.array(split_val[:min_len])==np.array(split_val2[:min_len])).all()==True:
                # print('correct')
                index_correct.append(i)
            
            else:
                # print('Not correct')
                pass

        return index_correct



    def clean_bandit(self,str_name:str):
        """
        This method removes alpahbets present within the brackets at the end

        Args:
        ------------
        str_name: str
            parse the string that has (S)/(P) in the brackets at the end of the survey number

        Return:
        ---------
            :code:`string`
        
        """
        pattern_comparing = r'\([a-zA-Z]\)*$'
        new_d1 = re.sub(pattern_comparing,'',str_name).strip().lower() #converted to lower for matching states that have alphabets and can be either in upper or lower case
        return new_d1
    


    @staticmethod
    def char_assasin(eng_name:str,region:Literal['Hi','Tel','Ka','Od']='Tel'):
        r"""
        converts the village names with regional character to english.

        Args:
        ------
        eng_name: str
            The name (regional) that needs to be converted to english.
        region: str
            the char to be replaced with. Supports :code:`Hi`, :code:`Tel (default)`, :code:`Ka`, and :code:`Od`.

        Return:
        --------
            :code:`string`

        Example:
        ------------
        >>> string = '12/अ/1'
        >>> print(POC_matching.char_assasin(string,'Hi'))
            '12/A/1'
        """
        if region=='Tel':
            dict_ref = POC_matching.replace_dict_tel
            patter_ref = r'([\u0C00-\u0C7F]+)'

        elif region=='Ka':
            dict_ref = POC_matching.replace_dict_kar
            patter_ref = r'([\u0C80-\u0CFF]+)'

        elif region=='Hi':
            dict_ref = POC_matching.replace_dict_Hin
            patter_ref = r'([\u0900-\u097F\u200d]+)'

        elif region=='Od':
            dict_ref = POC_matching.replace_dict_Od
            patter_ref = r'([\u0B00-\u0B7F]+)'

        else:
            raise ValueError("Supports only 'Hi', 'Tel', 'Ka' or 'Od'")

        sub_value = re.sub(patter_ref,lambda x:  dict_ref.get(x.group().lower()) if dict_ref.get(x.group().lower()) else x.group(),eng_name)
        return sub_value
    

    @staticmethod
    def string_updation(string:str,pattern:Literal['En','Hi','Tel','Ka','Od']= 'En'):
        r"""
        This method adds **'/'** inbetween an alphabet and a digit, if alphabet is preceded or succeeded by a digit.
    
        Args:
        -----------
        string: str
            string you want to change
        pattern: str
            the string you are passing has to refer which pattern; supports :code:`En (default)`, :code:`Hi`, :code:`Tel`, :code:`Ka`, and :code:`Od`

        Return:
        -----------
        :code:`string`

        Example:
        ----------------
            
        >>> data = '13/1AA/BB1/E'
        >>> updated_data = string_updation(data,'En')
        >>> print(updated_data)
            '13/1/AA/BB/1/E'
        """
        if pattern=='En':
            pattern_ref = POC_matching.pattern_eng

        elif pattern=='Hi':
            pattern_ref = POC_matching.pattern_hi

        elif pattern=='Tel':
            pattern_ref = POC_matching.pattern_tel

        elif pattern=='Ka':
            pattern_ref = POC_matching.pattern_kan

        elif pattern=='Od':
            pattern_ref = POC_matching.pattern_od
        
        else:
            raise ValueError("The pattern did not match. Pattern supports 'En','Hi',and 'Tel' ")

        new_string=string
        ser = re.search(pattern_ref,new_string)
        while re.search(pattern_ref,new_string):
            ser = re.search(pattern_ref,new_string)
            new_string = new_string[:ser.start()+1]+'/'+new_string[ser.start()+1:]

        return new_string




    @staticmethod
    def best_val(actual_val:str,group_val:list,region:Literal['Hi','Tel','Ka','Od']='Tel',split_pat: str = r"\/|\-"):
        r"""
        If you have one-to-many matches and want to select the first bigger parcel (survey number)
        amongst the list

        Args:
        ---------
        actual_val: str
            The survey number (provided by the client) based on which parcel needs to be selected

        group_val: list
            The list of survey number amongst which you want to know the best parcel to retain

        region: str
            the char to be replaced with. Supports :code:`Hi`, :code:`Tel (default)`, :code:`Ka`, and :code:`Od`. If survey_number is in english than use :code:`Hi`.

        split_pat: str
            The pattern (regex prefered) based on which the text has to split. The default is :code:`\/|\-` i.e. split is based on either **'/'** or **'-'**.

        Return:
        ------------
        The function will return the :code:`index` of the best parcel from the list
        """
        actual_val = POC_matching.char_assasin(actual_val,region)
        group_val = [POC_matching.char_assasin(i,region) for i in group_val]
        # print(group_val)
        if actual_val.strip() in [i.strip() for i in group_val]:
            temp_ind = [i.strip() for i in group_val].index(actual_val)
            return temp_ind

        elif len(re.split(split_pat,actual_val))>1:
            if any(len(re.split(split_pat,actual_val)) >= len(re.split(split_pat,matching))for matching in group_val):
                for i in range(len(re.split(split_pat,actual_val)),0,-1):
                    rem = [match for match in group_val if len(re.split(split_pat,match))==i] 
                    if rem:
                        best_ind = group_val.index(process.extractOne(actual_val,rem)[0])
                        # print(best_ind)
                        return best_ind
            else:
                rem_ind = group_val.index(process.extractOne(actual_val,group_val)[0])
                return rem_ind
        else:
            rem_ind = group_val.index(process.extractOne(actual_val,group_val)[0])
            return rem_ind
        



    
    




