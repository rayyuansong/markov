#
# textmodel.py
#
# TextModel project!
#
# Name(s): Ray Song
#
from porter import create_stem
import math

class TextModel(object):
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        #
        # Create another of your own
        #
        self.punct = {}     # For counting punctuations

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = 'Words:\n' + str(self.words) + '\n\n'
        s += 'Word lengths:\n' + str(self.wordlengths) + '\n\n'
        s += 'Stems:\n' + str(self.stems) + '\n\n'
        s += 'Sentence lengths:\n' + str(self.sentencelengths) + '\n\n'
        s += 'Punctuation:\n' + str(self.punct)
        return s

    # Include other functions here.
    # In particular, you'll need functions that add to the model.
    def readTextFromFile(self,filename):
        """This method reads a text and stores it in the self.text"""
        f=open(filename)
        text=f.read()
        f.close()
        self.text=text

    def makeSentenceLengths(self):
        """This method creates a dictionary of numbers of
           different lengths of sentences and stores in
           self.sentencelengths
        """
        LoW=self.text.split()
        d={}
        count=0
        for w in LoW:
            if not (w[-1]=="." or w[-1]=="?" or w[-1]=="!"):
                count+=1
            elif count==0:
                pass
            elif count+1 not in d:
                d[count+1]=1
                count=0
            else:
                d[count+1]+=1  
                count=0 
        self.sentencelengths=d
    
    def cleanString(self,s):
        """This method returns the text without upper case 
           letters and punctuations
        """
        text=s.lower()
        new_text=""
        for i in text:
            if i=="," or i==";" or i=="?" or i=="." or i=="!" or i=="'" :
                pass
            else:
                new_text+=i
        self.text=new_text
        return new_text
    
    def makeWordLengths(self):
        """This method creates a dictionary of numbers of
           word lengths of sentences and stores in
           self.wordlengths
        """
        LoW=self.text.split()
        d={}
        for w in LoW:
            if len(w) in d:
                d[len(w)]+=1
            else:
                d[len(w)]=1
        self.wordlengths=d

    def makeWords(self):
        """This method creates a dictionary of numbers of
           word of sentences and stores in self.words
        """
        LoW=self.text.split()
        d={}
        for w in LoW:
            if w in d:
                d[w]+=1
            else:
                d[w]=1
        self.words=d
    
    def makeStems(self):
        """This method creates a dictionary of numbers of
           word lengths of sentences and stores in
           self.wordlengths
        """
        LoW=self.text.split()
        d={}
        for w in LoW:
            if create_stem(w) in d:
                d[create_stem(w)]+=1
            else:
                d[create_stem(w)]=1
        self.stems=d

    def isPunct(self,w):
        """This boolean method returns when a string is
           a punctuation mark
        """
        return w=="!" or w=="." or w=="," or w==":" or w=="'"\
        or w=="?"
    
    def makePunctuation(self):
        """This method creates a dictionary of numbers of
           word lengths of sentences and stores in
           self.punct
        """
        d={}
        for w in self.text:
            if self.isPunct(w):
                if w in d:
                    d[w]+=1
                else:
                    d[w]=1
        self.punct=d
    
    def normalizeDictionary(self,d):
        """This method should accept any single one of the model 
        dictionaries d and return a normalized version
        """
        total=sum(d.values())
        nd={}
        for k in d:
            nd[k]=d[k]/total
        return nd
    
    def smallestValue(self, nd1, nd2):
        """This method should accept any two model dictionaries 
        d1 and nd2 and should return the smallest positive (that 
        is, non-zero) value across them both.
        """
        small=sum(nd2.values())+sum(nd1.values())
        for k in nd1:
            if nd1[k]<small:
                small=nd1[k]

        for k in nd2:
            if nd2[k]<small:
                small=nd2[k]
        return small
    

    def compareDictionaries(self, d, nd1, nd2):
        """This method computes and returns The log-probability that
        the dictionary d arose from the distribution of data in the 
        normalized dictionary nd1 and The log-probability that 
        dictionary d arose from the distribution of data in normalized 
        dictionary nd2
        """
        
        total_log_prob1=0.0
        total_log_prob2=0.0
        epsilon=self.smallestValue(nd1,nd2)/2
        for k in d:
            if k not in nd1:
                total_log_prob1+=math.log(epsilon)
            else:
                total_log_prob1+=d[k]*math.log(nd1[k])
            
            if k not in nd2:
                total_log_prob2+=math.log(epsilon)
            else:
                total_log_prob2+=d[k]*math.log(nd2[k])
        return [total_log_prob1,total_log_prob2]
    
    def createAllDictionaries(self):
        """Create out all five of self's
           dictionaries in full.
        """
        self.makeSentenceLengths()
        self.makeWords()
        self.makeStems()
        self.makePunctuation()
        self.makeWordLengths()
    

    def compareTextWithTwoModels(self, model1, model2):
        """Print out the comparative results of the log-probabilities 
           for all five dictionaries
        """
        self.createAllDictionaries()
        model1.createAllDictionaries()
        model2.createAllDictionaries()
        sL=self.compareDictionaries(self.sentencelengths,\
        self.normalizeDictionary(model1.sentencelengths),\
        self.normalizeDictionary(model2.sentencelengths))
        mW=self.compareDictionaries(self.words,\
        self.normalizeDictionary(model1.words),\
        self.normalizeDictionary(model2.words))
        mS=self.compareDictionaries(self.stems,\
        self.normalizeDictionary(model1.stems),\
        self.normalizeDictionary(model2.stems))
        mP=self.compareDictionaries(self.punct,\
        self.normalizeDictionary(model1.punct),\
        self.normalizeDictionary(model2.punct))
        mL=self.compareDictionaries(self.wordlengths,\
        self.normalizeDictionary(model1.wordlengths),\
        self.normalizeDictionary(model2.wordlengths))
        


        names=["model1","model2"]
        tot=[]
        tot.append(names)
        tot.append(sL)
        tot.append(mW)
        tot.append(mS)
        tot.append(mP)
        tot.append(mL)

        points1=0
        points2=0
        for i in range(1,6):
            if tot[i][0]>tot[i][1]:
                points1+=1
            elif tot[i][0]<tot[i][1]:
                points2+=1

        tot.append([points1,points2])

        columns=["name","sentencelengths","words","stems","punctuation","wordlengths","total"]
        for i in range(len(columns)):
            print("%-15s %-15s %-15s" %(columns[i],tot[i][0],tot[i][1]))

        if points1>points2:
            print ("Model1 has a larger total possibility. Model1 wins")
        else:
            print ("Model2 has a larger total possibility. Model2 wins")
        




print(" +++++++++++ Model1 +++++++++++ ")
TM1 = TextModel()
TM1.readTextFromFile("train1.txt")
TM1.createAllDictionaries()  # provided in hw description
print(TM1)

print(" +++++++++++ Model2 +++++++++++ ")
TM2 = TextModel()
TM2.readTextFromFile("train2.txt")
TM2.createAllDictionaries()  # provided in hw description
print(TM2)


print(" +++++++++++ Unknown text +++++++++++ ")
TM_Unk = TextModel()
TM_Unk.readTextFromFile("unknown.txt")
TM_Unk.createAllDictionaries()  # provided in hw description
print(TM_Unk)

TM = TextModel()
d1 = {'a': 5, 'b':1, 'c':2}
nd1 = TM.normalizeDictionary(d1)
d2 = {'a': 15, 'd':1}
nd2 = TM.normalizeDictionary(d2)
print("The normalized dictionaries are:")
print(nd1)
print(nd2)
sm_va = TM.smallestValue(nd1, nd2)
print("and the smallest value between them is", sm_va)

TM1 = TextModel()
TM1.readTextFromFile("train1.txt")
TM2 = TextModel()
TM2.readTextFromFile("train2.txt")
TM_Unk = TextModel()
TM_Unk.readTextFromFile("unknown.txt")
TM_Unk.compareTextWithTwoModels(TM1,TM2)

print(" ++++++++++++++++++++++++++++++++++++++++++++ ")
print(" +++++++++++ My Own Training Sets +++++++++++ ")
print(" ++++++++++++++++++++++++++++++++++++++++++++ ")

print("First text is from Part1, Chapter 1 from 1984 by George Orwell. ")
TMa = TextModel()
TMa.readTextFromFile("train_orwell.txt")


print("Second text is from A Very Short Story by Ernest Hemingway.")
TMb = TextModel()
TMb.readTextFromFile("train_avst.txt")



print(" We have Unknown text A ") #a snippet from Hemingway's the Old Man of the Sea
TM_Unka = TextModel()
TM_Unka.readTextFromFile("unka.txt")


print(" We have Unknown text B ") #a snippet from Orwell's Animal farm
TM_Unkb = TextModel()
TM_Unkb.readTextFromFile("unkb.txt")


print(" We have Unknown text C ") #a snippet from Orwell's letter to Fitzgerald
TM_Unkc = TextModel()
TM_Unkc.readTextFromFile("unkc.txt")

print(" We have Unknown text D ") #a snippet from Orwell's letter to Fitzgerald
TM_Unkd = TextModel()
TM_Unkd.readTextFromFile("unkd.txt")

print(" +++++++++++ Unknown text A Results +++++++++++ ")
TM_Unka.compareTextWithTwoModels(TMa,TMb)



print(" +++++++++++ Unknown text B Results +++++++++++ ")
TM_Unkb.compareTextWithTwoModels(TMa,TMb)

print(" +++++++++++ Unknown text C Results +++++++++++ ")
TM_Unkc.compareTextWithTwoModels(TMa,TMb)

print(" +++++++++++ Unknown text D Results +++++++++++ ")
TM_Unkd.compareTextWithTwoModels(TMa,TMb)
