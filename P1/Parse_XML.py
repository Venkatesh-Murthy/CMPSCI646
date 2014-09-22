#!/usr/bin/python
import pdb
import xml.sax
import glob
import os
import operator
class DocHandler( xml.sax.ContentHandler ):
   def __init__(self,count,book_count):
      self.CurrentData = ""
      self.CurrentPage=""
      self.line=""
      self.region=""
      self.section=""
      self.page=""
      self.counter=count;
      if(book_count==0):
	self.Book=[{}];
      else:
      	self.Book.append({});
      self.stp_dict={};
      with open('stop_words.txt') as fp:
	for line in fp:
      #f=open('stop_words.txt','r');
      #self.stp_dict={};
      #for line in f.readline():
#		pdb.set_trace()
		self.stp_dict[line[:-1]]=1;
      #f.close()

      
      

   # Call when an element starts
   def startElement(self, tag, attributes):
      
      self.CurrentData = tag
      if(tag=='page'):
		self.CurrentPage=attributes['id'];
      
   def stp_word_chk(self,word):
#	if(word=="the"):
#		pdb.set_trace()
	if word in self.stp_dict:
		self.valid=0;
	else:
		self.valid=1;
   # Call when an elements ends
   #def endElement(self, tag):
    #  if self.CurrentData == "region":
     #    print "Region:", self.region
#      elif self.CurrentData == "section":	
 #        print "Section:", self.section
  #    elif self.CurrentData == "page":
   #      print "Page:", self.page
    #  elif self.CurrentData == "line":
     #    print "Year:", self.line
   def special_characters(self, word):
	new_str="";
#	print word
#	pdb.set_trace()
	for i in range(len(word)):
		if(word[i].isupper()==True):
			new_str=new_str+word[i].lower();
		elif(word[i]=='-' and word[i]=='\''):
			new_str=new_str+word[i]
		elif(word[i].islower()==True):
			new_str=new_str+word[i]
		else:
			new_str=new_str+" "
	self.line=new_str

   

   # Call when a character is read
   def characters(self, content):
#      print "Characters: ", content
#      pdb.set_trace();
      
      if self.CurrentData == "region":
         self.region = content
	 word=self.region.split(' ')
       #  pdb.set_trace()
         #self.count=self.count+len(word)

      elif self.CurrentData == "section":
         self.section = content
	 word=self.section.split(' ')
         #self.count=self.count+len(word)

      elif self.CurrentData == "page":
         self.page = content
	 word=self.page.split(' ')
         self.count=self.count+len(word)
      elif self.CurrentData == "line":
	  
         self.line = content
	 self.special_characters(self.line);
	 word=self.line.split(' ')
#	 pdb.set_trace()
	 for i in range(len(word)):
	     self.stp_word_chk(word[i]);
	     if (self.valid==1 and word[i]!=""):   
	 	if word[i] in self.Book[book_count]:
        		self.Book[book_count][word[i]] += 1
		else:
			self.Book[book_count][word[i]]=0;
	 self.counter=self.counter+len(word)

#         print self.Book 
	 #print "Word Count:", self.counter
   def ignorableWhitespace(self, whitespace):
	print whitespace
  
if ( __name__ == "__main__"):
   
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
   count=0;
   book_count=0;
   # override the default ContextHandler
   Handler = DocHandler(count,book_count)
   parser.setContentHandler( Handler )
#   pdb.set_trace()
   #count=0;
   
   for root, dirs, files in os.walk("/home/venk/Documents/Information_Retrieval/sample_python/P1/data/"):
     for file in files:
	if file.endswith(".xml"):
		print "Processing... ",file
               # source=open(os.path.join(root, file));

		
		Handler = DocHandler(count,(book_count))    
		parser.setContentHandler( Handler ) 
		#book_count=book_count+1;                                                                                                                                                                                                                         
   	#	parser.setContentHandler( Handler )
     		parser.parse(os.path.join(root, file))
		Handler.Book[book_count]=sorted((Handler.Book[book_count]).iteritems(), key=operator.itemgetter(1),reverse=True);
		#print Handler.Book
		#print "Word count: ",Handler.counter
		book_count=book_count+1; 
                #xml.sax.parse(source, DocHandler(count))
   #parser.parse("sample.xml")i
   print "Word count: ",Handler.counter
   print "Page: ", Handler.page
   
   print Handler.Book
