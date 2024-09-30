from enum import Enum
import json
import importlib
import os

# Pobierz katalog, w którym znajduje się ten plik
current_directory = os.path.dirname(__file__)
#Variables
intrepunctions = [".", ",", ":", ";", "?", "!", "\""]
whiteSigns = [" ", "  ", "\n", "\f"]
with open(f'{current_directory}/matchmaker.json', 'r') as file:
    global data
    data = json.load(file)
    if data['name'] != "match_maker":
      print("An library error: \"match maker\"")
      quit()
# Enums
class FilterType(Enum):
    Filter = "10294857630"
    Count = "85250958238"
class NormalizeType(Enum):
   DeleteInterpunctions = "023402839502938"
   LowText = "03950-1938509"
   DeleteWhiteSigns = "49582938598208745"
   ReplaceSignsToNumber = "3098925802989540"
# Classes
class Math():
  def Mean(analisysData:list):
    srednia = 0
    srednia = sum(analisysData)
    return srednia/len(analisysData)
  def Difference(a, b):
    difference = b/a
    difference = difference*100
    return difference-100
  def Normalize(analisysData:list, normalizeNumber:int):
    najwieksza = 0
    for element in analisysData:
      if element > najwieksza:
        najwieksza = element
    position = 0
    for position in range(len(analisysData)):
      analisysData[position] = analisysData[position]/(najwieksza/normalizeNumber)
    return analisysData
  def MakeInt(value:float, divideNumber:int):
    return round(value-divideNumber,0)
  def AbsoluteDifference(a,b):
    return abs(a-b)
  def AbsoluteIntPercentDifference(a, b):
    return abs(Math.MakeInt(Math.Difference(a,b)))
  def WeightedAverage(analisysData=[],weights=[]):
    score=[]
    for position in range(len(analisysData)):
      for weight in range(weights[position]):
        analisysData.insert(analisysData[position]+weight, analisysData[position])
    return sum(analisysData)/len(analisysData)
  def NumberRepeat(numbers:list) -> dict:
        nums = {}
        for liczba in range(len(numbers)):
            if numbers[liczba] in nums:
                nums[numbers[liczba]] +=1
            else:
               nums[numbers[liczba]] = 1
        

        return nums
  def PercentNumberChance(numbers:list) -> dict:
        chance = {}
        repeats = Math.NumberRepeat(numbers)
        suma = sum(repeats.values())
        for i in range(len(numbers)):
           if numbers[i] not in chance:
            chance[numbers[i]] = (repeats.get(numbers[i])/suma)*100
        return chance
#class Finance():
    
    # def FinancialAngle(amounts:list, max_change:int):
    #     angles = []
    #     for i in range(1, len(amounts)):
    #         start_amount = amounts[i - 1]
    #         end_amount = amounts[i]
    #         angle = 180 * ((end_amount - start_amount) / max_change)
    #         angles.append(max(0, min(angle, 180)))
    #     return angles
    

class Text():


  def CountInrerpunctions(text:str) -> dict:
      data = {}
      for i in range(len(intrepunctions)):
         if intrepunctions[i] in text:
            data[intrepunctions[i]] = text.count(intrepunctions[i])
      return data
  def CountSigns(text:str, lowerSigns:bool) -> dict:
    data = {}
    signs = []
    if lowerSigns:
      for i in range(len(text.lower())):
          if text[i].lower() not in signs:
            data[text[i].lower()] = 1
            signs.append(text[i].lower())
          else:
            data[text[i].lower()] += 1
      return data
    else:
      for i in range(len(text)):
        if text[i] not in signs:
          data[text[i]] = 1
          signs.append(text[i])
        else:
          data[text[i]] += 1
      return data
  def CountWord(text:str,word:str) -> int:
  
     text = text.lower()
     word = word.lower()
     return text.count(word)
  def FilterWordsWithSign(text:str, sign:str,filterType:FilterType) -> dict:
    result = {}
    if filterType == FilterType.Count:
      result["count"] = Text.CountWord(sign)
      return result
    elif filterType == FilterType.Filter:
       newText = text.lower().replace(sign.lower(), "")
       result["filter"]  = newText
       return result
    else:
      return ValueError
  #def GetWordFrequency(text:str) -> dict:
  def NormalizeText(text:str, normalizeType:NormalizeType):
    result = ""
    if normalizeType == NormalizeType.DeleteInterpunctions:
      for i in range(len(intrepunctions)):
        text = text.replace(intrepunctions[i], '')
      result = text

    elif normalizeType == NormalizeType.LowText:
      result = text.lower()
    elif normalizeType == NormalizeType.DeleteWhiteSigns:
      for i in range(len(whiteSigns)):
        text = text.replace(whiteSigns[i], '')
      result = text
    elif normalizeType == NormalizeType.ReplaceSignsToNumber:
       alphabet = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
       text = text.lower()
       text = text.strip()
       for i in range(len(text)):
          index = i
          if text[i] not in alphabet or text[i] == '':
            if text[i] not in whiteSigns:
              result += text[i] + "|"
            else:
               result += " |"
            continue
          else:
             letter = text[i]
             index = alphabet.index(letter)
             print(index)
             result += str(index) + "|"
    return result
  def GetWordsFromText(text:str) -> list:
    result = text.split()
    return result
class MatchMaker():
  def __init_():
     def __init__(self):
        self.plugins = {}
        self.plugins_manager = self.Plugins(self)
  @staticmethod
  def MMSplitText(text:str):
    if data["extracts"]['splitText']['enabled']:
        result = []
        myData = Text.GetWordsFromText(text)

        # Zmienna klucz podziału
        split_key = data["extracts"]['splitText']['key']

        # Zmienna do przechowywania aktualnego fragmentu
        current_segment = []

        # Przechodzimy przez słowa w myData
        for word in myData:
            if word != split_key:  # Sprawdzamy, czy słowo nie jest kluczem podziału
                current_segment.append(word)  # Dodajemy słowo do aktualnego segmentu
            else:
                # Dodajemy aktualny segment do wyników, jeśli nie jest pusty
                if current_segment:
                    result.append(' '.join(current_segment))  # Dołączamy złączony segment
                    current_segment = []  # Resetujemy aktualny segment

        # Dodajemy ostatni segment, jeśli istnieje
        if current_segment:
            result.append(' '.join(current_segment))

        return result  # Zwracamy przetworzoną listę
    else:
        return []  # Jeśli splitText nie jest włączone, zwracamy pustą listę
  @staticmethod
  def MMHiddenText(text:str) -> str:

    start = data["extracts"]['HiddenData']['key_s']
    end = data["extracts"]['HiddenData']['key_e']
    if data["extracts"]['HiddenData']['enabled']:
      while start in text and end in text:
        start_index = text.find(start)
        end_index = text.find(end) + len(end)
        text = text[:start_index] + text[end_index:]
        
      return text
    else:
       return None
  @staticmethod
  def MMPasswordText(text:str) -> str:
    start = data["extracts"]['PasswordData']['key_s']
    end = data["extracts"]['PasswordData']['key_e']
    if data["extracts"]['PasswordData']['enabled']:
      while start in text and end in text:
        start_index = text.find(start) + len(start)
        end_index = text.find(end)
        hidden_part = '*' * (end_index - start_index)
        text = text[:start_index-len(start)] + hidden_part + text[end_index+len(end):]
        
      return text
    else:
       return None
  class Plugins():
      def __init__(self, matchmaker_instance):
            self.matchmaker_instance = matchmaker_instance
      def InstallPlugin(name):
            if data['Plugins']['can_be_installed']:
              try:
                  # Spróbuj zaimportować bibliotekę
                  globals()["lib"] = importlib.import_module(f"HintlyDataAnalisys.plugins.{name}")
                  # Sprawdzenie czy ścieżka `Plugins -> plugins` istnieje, jeśli nie, to ją tworzymy
                  if 'Plugins' not in data:
                      data['Plugins'] = {}
                  if name not in data['Plugins']['installed_plugins']:
                    print(f"Succesfully installed {name}")
                    data['Plugins']['installed_plugins'].append(name)
                  # Zapiszmy zmodyfikowane dane z powrotem do pliku JSON
                  current_directory = os.path.dirname(__file__)
                  with open(f'{current_directory}/matchmaker.json', 'w') as file:
                    json.dump(data, file, indent=4)
              except ImportError as e:
                  print(f"Error installing \"plugin\" {name}: {e}")
  class timeLib():
      def Detect(text:str):
          try:
            if "timeLib" in data['Plugins']['installed_plugins']:
              globals()["lib"] = importlib.import_module(f"HintlyDataAnalisys.plugins.timeLib")
              return lib.replace_time_tags(text)
            else:
              print("You must install the timeLib plugin.")
          except:
             return
          