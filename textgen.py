import os, sys, random
from unicodedata import category

def listdir_nohidden(path):
    lst = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            lst.append(f)
    return lst

class Grammar:
    def __init__(self, message, gram_en, gram_ru, category):
        self.gram_en = gram_en; self.gram_ru = gram_ru; self.category = category; self.message = message
        self.variations = None; self.valid = True
        if(not self.GrammarIsValid(self.gram_en)): self.valid = False
        if(not self.GrammarIsValid(self.gram_ru)): self.valid = False

    def GrammarIsValid(self, grammar):
        if(grammar.count("[") != grammar.count("]")):
            print("[WARNING] Ignoring a grammar [ != ].")
            print(grammar, "\n\n") #Debugging
            return False
        return True

    def RenderVariation(self, lang="ru"):
        gram = self.gram_ru
        if(lang == "en"):
            gram = self.gram_en
        self.variations = 1
        while "[" in gram:         
            #Parse the options of the first brackets
            options = gram[gram.index("[")+1:gram.index("]")].split(",")

            #Remove empty options (grammar mistake)
            try: 
                options.remove("")
            except: 
                pass

            #Make sure there is no space at the beginning of an option
            options = [o if(o[0] != " ") else o[1:] for o in options]
            self.variations *= len(options)

            #Select a random option and replace the first brackets with this option
            gram = gram[:gram.index("[")]+""+random.choice(options)+""+gram[gram.index("]")+1:]
        return gram

    def GetVariations(self, lang="ru"):
        self.RenderVariation(lang)
        return self.variations

class SubjectGenerator:
    def __init__(self, grammarpath="subjects/"):
        self.grammars = []; self.grammarpath = grammarpath
        for file in listdir_nohidden(self.grammarpath):
            self.LoadGrammar(os.path.join(self.grammarpath, file))
    
    def LoadGrammar(self, file):
        f = open(file, encoding='UTF-8')
        csvlines = f.readlines()[1:] #Crop Title-Row
        for g in csvlines:
            if(len(g.split("\t")) < 1):
                print("> Grammar", file, "has empty cells. Please fix.")
                continue
            g_en, g_ru = g.split("\t")[:2]
            g = Grammar("", g_en, g_ru, "subject")
            if(g.valid):
                self.grammars.append(g) #key is category, value is list of grammars
        return True

    def GenerateSubject(self):
        g = random.choice(self.grammars)
        return g.RenderVariation()

class TextGenerator:
    def __init__(self, grammarpath="grammars/", max_words=350):
        self.max_words = int(max_words); self.grammars = {}; self.grammarpath = grammarpath
        files = listdir_nohidden(self.grammarpath)
        if(len(files) == 0):
            print("[CRITICAL ERROR] You do not have any grammar files in your grammar directory. Please read the manual...")
            exit(1)
        for file in files:
            self.LoadGrammar(os.path.join(self.grammarpath, file))

    def LoadGrammar(self, file):
        f = open(file, encoding='UTF-8')
        csvlines = f.readlines()[1:] #Crop Title-Row
        for g in csvlines:
            if(len(g.split("\t")) < 4):
                print("> Grammar", file, "has empty cells. Please fix.")
                continue
            message, g_en, g_ru, category = g.split("\t")[:4]
            g = Grammar(message, g_en, g_ru, category)
            if(g.valid):
                if(category in self.grammars.keys()):
                    self.grammars[category].append(g) #key is category, value is list of grammars
                else:
                    self.grammars[category] = [g]
        return True

    # Function just cleans artifacts of wrong grammar. Like double spaces, <space><comma>, Missing spaces behind commas, ....
    def Clean(self, text):
        text = text.replace("\n ", "\n")                            # Remove spaces after linebreaks
        while text[0] == " " or text[0] == "\n": text = text[1:]    # Remove spaces at beginning
        while text[-1] == "\n": text = text[:-1]                    # Remove newline at end

        text = text.replace("?", ". ") # Make sure every . got a space after it
        text = text.replace("!", ". ") # Make sure every . got a space after it
        text = text.replace(".", ". ") # Make sure every . got a space after it
        text = text.replace(". \n", ".\n") # Except last line

        text = text.replace(",", ", ") # Make sure every comma got a space
        text = text.replace(" ,", ", ") # Make sure there is never a space before a comma

        while("  " in text):
            text = text.replace("  ", " ")
        
        return text

    def GenerateText(self, lang="ru"):
        used_grams = [] # avoid doubles
        texts = {} # Store texts in dictionary based on category so we can sort it based on category lateron
        msg = "" # Basically the translation of the russian text

        # Fill dictionary with rendered grammars
        failed = 0
        while(len("".join(sum(([l[0] for l in i] for i in texts.values()), [])).split(" ")) < self.max_words):  # As long as max_words not reached
            category, grammarlist = random.choice(list(self.grammars.items()))                                  # Select random category
            g = random.choice(grammarlist)                                                                      # Select grammar 
            if(category not in used_grams):                                                                     # Check that the grammar is not used yet
                used_grams.append(g.message)                                                          
                if(category in texts.keys()):                                                                   # Render and add
                    texts[category].append((g.RenderVariation(lang), g.RenderVariation("en")))
                else:
                    texts[category] = [(g.RenderVariation(lang), g.RenderVariation("en"))]
                failed = 0
            else: 
                failed += 1
            if(failed == 200): # Avoid stuck in loop
                break

        # Sort dictionary by category and merge texts
        text = ""
        for category, textlist in texts.items():
            # Merge texts from a category
            for t, m in textlist: text += t; msg += m
            #Add random amount of linebreaks
            for i in range(random.randint(0,2)):text += "\n"; msg += "\n"

        return (self.Clean(text), self.Clean(msg))

import time
if __name__ == "__main__":
    if(len(sys.argv) == 3): # folder      max_wordcount
        tg = TextGenerator(sys.argv[1], sys.argv[2])
    else: #default
        tg = TextGenerator()
        
    while True:
        text, msg = tg.GenerateText()
        print(msg+"\n\n########################## NEW MAIL ##################################\n\n")
        time.sleep(0.1)