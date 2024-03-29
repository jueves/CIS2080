import pandas as pd
import json

'''
Labels data, sets pd.NA and creates UBE variable
Decisions made are documented in codebook.md
'''

def get_preprocessed_data(data_file_name="../data/cis2080.csv", labels_file_name="../metadata/descriptive_var_names.json"):
  data = pd.read_csv(data_file_name, sep=";", na_values=[" ", " "*2, "-8"], decimal=",")
  data = get_labeled_data(data, labels_file_name)
  data["UBE"] = data.apply(get_ube, axis=1, args=get_drink_variables(labels_file_name))
  data["UBEplus"] = get_ube_plus(data, labels_file_name)
  data['drinking_pattern'] = get_drink_pattern(data)
  return(data)



def get_labeled_data(data, labels_file_name):
  with open(labels_file_name) as f:
    var_names = json.load(f)

  # Rename selected variables
  new_names = []
  for code in data.columns:
    if (code in var_names.keys() and var_names[code]["description"] != "incomplete"):
      new_names.append(var_names[code]["name"])
    else:
      new_names.append(code)

  data.columns = new_names

  # Set NAs
  def set_NAs(var_dict):
    for key, value in var_dict.items():
      data[key] = data[key].replace(value, pd.NA)
      
  set_NAs({
    #"cigarettes": 99,
    #"cigars": 99,
    "drink_loc1": [0, 9],
    "drink_loc2": [0, 9],
    "political_espectrum": [98, 99],
    "income": 99,
    #"occupation": 98,
    #"socioeconomic_condition": 12,
    "sex": 9,
    #"sector": 9,
    #"status": 9
  })


  def get_numeric_dict(dictionary):
    # Gets a dictionary with string keys and returns
    # a similar dictionary with integer keys.
    new_dic = {}
    for key, value in dictionary.items():
      new_dic[int(key)] = value
    return(new_dic)

  # Assign labels
  for metadata in var_names.values():
    if (metadata["description"] != "incomplete" and "values" in metadata.keys()):
      # Convert dictionary keys from string to numeric
      numeric_dict = get_numeric_dict(metadata['values'])

      # Set values
      data[metadata['name']] = data[metadata['name']].map(numeric_dict)

      # Check if all values are strings.
      if all(isinstance(value, str) for value in metadata["values"].values()):
        # Apply categorical
        is_ordered = metadata["ordered"] == "True"
        data[metadata['name']] = pd.Categorical(data[metadata["name"]],
                                            categories=list(metadata["values"].values()),
                                            ordered=is_ordered).remove_unused_categories()
  return(data)

def get_drink_variables(labels_file_name):            
  # Get var names for all drinking variables
  with open(labels_file_name) as f:
    var_names = json.load(f)
  drink_type_vars = []
  drink_amount_vars = []
  for key, value in var_names.items():
    if value["name"][:10] == "drink_type":
        drink_type_vars.append(key)
    elif value["name"][:12] == "drink_amount":
        drink_amount_vars.append(key)
  return((drink_type_vars, drink_amount_vars))
  
def get_ube(row, drink_amount_vars, drink_type_vars):
  '''
  Takes one row of a Pandas Dataframe and returns the amount of  UBE (int),
  which means "Unidades de Bebida Estándar" = Stantard Drinks.
  '''
  
  def get_ube_per_drinktype(drink):
    '''
    Returns the number of UBEs corresponding to the given type of drink (number as a str).
    '''
    if (pd.isna(drink)):
      ube = 0
    elif (int(drink) in [1, 2, 6]): # Low alcohol drink types
      ube = 1
    elif (int(drink) in [3, 4, 5, 7, 8]): # High alcochol drink types
      ube = 2
    else:
      ube = 0
    return(ube)
  
  def get_drink_amount(raw_amount):
    if (pd.isna(raw_amount)):
      amount = 0
    else:
      amount = int(raw_amount)
    
    return(amount)

  drink_type_ubes = [get_ube_per_drinktype(x) for x in row[drink_type_vars]]
  drink_amounts = [get_drink_amount(x) for x in row[drink_amount_vars]]
  ube = sum([drink_type_ubes[i] * drink_amounts[i] for i in range(len(drink_type_ubes))])
  return(ube)
  
def get_ube_plus(data, labels_file_name):
  '''
  drink_amount_data: 
    pandas.DataFrame of all variables regarding drinking amounts.
    8 is used to code an amount of 8 or more drinks.
  Returns:
    pandas.Series with the number of ocasions in which this amount
    is reached for each person.
  '''
  _, drink_amount_vars = get_drink_variables(labels_file_name)
  subdata = data[drink_amount_vars]

  ube_plus = subdata.apply(lambda x: sum(x == 8), axis=1)

  return(ube_plus)

def get_drink_pattern(data):
  '''
  Returns a pandas.Series with 3 categories:
    - "nondrinker"
    - "drinker"
    - "heavy_drinker"
  '''
  if "UBEplus" not in data.columns:
    raise Exception("An UBEplus variable is needed in order to compute heavy drinkers.")
  
  my_cat = pd.api.types.CategoricalDtype(categories=["nondrinker", "drinker",
                                                     "heavy_drinker"], ordered=True)
  
  drinking_pattern = pd.Series(["drinker"]*len(data), dtype=my_cat)

  drinking_pattern[data.UBE == 0] = "nondrinker"
  
  drinking_pattern[data.UBEplus > 0] = "heavy_drinker"

  return(drinking_pattern)
