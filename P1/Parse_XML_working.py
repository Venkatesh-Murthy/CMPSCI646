#!/usr/bin/python
import pdb
import xml.sax
import glob
import os
import operator
class DocHandler( xml.sax.ContentHandler ):
   def __init__(self,count,book_count,uniq_count,page_count,inv_index):
      self.CurrentData = ""
      self.CurrentPage=""
      self.OldPage=-1;
      self.line=""
      self.region=""
      self.section=""
      self.page=""
      self.page_tmp=""
      self.pag_cont=""
      self.count=count;
      self.page_count=page_count;
      self.uniq_count=uniq_count;
      self.book_count=str(book_count);
      self.inv_index=inv_index;
#      if(book_count==0):
#	self.Book=[{}];
 #     else:
  #    	self.Book.append({});
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
                self.page_count=self.page_count+1;
		#self.pag_cont=self.page_tmp;
		self.page_tmp=""
      
   def stp_word_chk(self,word):
#	if(word=="the"):
#		pdb.set_trace()
	if word in self.stp_dict:
		self.valid=0;
	else:
		self.valid=1;
   # Call when an elements ends
   def endElement(self, tag):
      #pdb.set_trace()
      #self.pag_cont=self.page_tmp;
      #self.page_tmp="";
      if (tag == 'page'):
	self.pag_cont=self.page_tmp;                                                                                                                               
        self.page_tmp="";
	if(self.pag_cont!=""):    
#	 pdb.set_trace()                                                                                                                                                                                                                           
         self.line=self.pag_cont;                                                                                                                                                                                                                           
         self.pag_cont=""                                                                                                                                                                                                                                   
         self.special_characters(self.line);                                                                                                                                                                                                                
         word=self.line.split(' ')   
	 special_words=['powerful', 'strong', 'butter', 'salt'];                                                                                                                                                                                                                       
        # pdb.set_trace()                                                                                                                                                                                                                                   
         for i in range(len(word)):                                                                                                                                                                                                                         
             self.valid=1;#self.stp_word_chk(word[i]);                                                                                                                                                                                                      
             if (self.valid==1 and word[i]!=""):                                                                                                                                                                                                            
#               print word[i]                                                                                                                                                                                                                               
                self.count=self.count+1;                                                                                                                                                                                                                    
                if word[i] in self.inv_index:                                                                                                                                                                                                               
                   if self.book_count in self.inv_index[word[i]]:                                                                                                                                                                                           
                      if self.CurrentPage in self.inv_index[word[i]][self.book_count]:                                                                                                                                                                      
                        self.inv_index[word[i]][self.book_count][self.CurrentPage] += 1;                                                                                                                                                                    
                        self.inv_index[word[i]]['total']+=1;                                                                                                                                                                                                
                      else:                                                                                                                                                                                                                                 
                        self.inv_index[word[i]][self.book_count][self.CurrentPage] =1;                                                                                                                                                                      
                        self.inv_index[word[i]]['total']+=1;                                                                                                                                                                                                
        #               self.uniq_count=self.uniq_count+1;                                                                                                                                                                                                  
                   else:                                                                                                                                                                                                                                    
                        self.inv_index[word[i]][self.book_count]={}                                                                                                                                                                                         
                        self.inv_index[word[i]]['total']+=1;                                                                                                                                                                                                
                        self.inv_index[word[i]][self.book_count][self.CurrentPage]=1;                                                                                                                                                                       
        #               self.uniq_count=self.uniq_count+1;                                                                                                                                                                                                  
                else:                                                                                                                                                                                                                                       
                        self.inv_index[word[i]]={};                                                                                                                                                                                                         
                        self.inv_index[word[i]][self.book_count]={}                                                                                                                                                                                         
                        self.inv_index[word[i]]['total']=1;                                                                                                                                                                                                 
                        self.inv_index[word[i]][self.book_count][self.CurrentPage]=1;                                                                                                                                                                       
                        self.uniq_count=self.uniq_count+1; 
	
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
	#pdb.set_trace()
	for i in range(len(word)):
		if(word[i].isupper()==True):
			new_str=new_str+word[i].lower();
		elif(word[i]=='-' and word[i]=='\''):
			new_str=new_str+word[i]
		elif(word[i].islower()==True):
			new_str=new_str+word[i]
        	elif(word[i].isnumeric()==True):                                                                                                                                                                                                              
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
      #elif self.CurrentData == "line" or self.CurrentData =="marker":
      elif self.CurrentData == "line":  
       self.line = content
       #pdb.set_trace()
       self.page_tmp=self.page_tmp +" "+ self.line;
       if(self.pag_cont!=""): 
         self.line=self.pag_cont;
         self.pag_cont=""
	 self.special_characters(self.line);
	 word=self.line.split(' ')
	 pdb.set_trace()
	 for i in range(len(word)):
	     self.valid=1;#self.stp_word_chk(word[i]);
	     if (self.valid==1 and word[i]!=""):
#		print word[i]
		
		self.count=self.count+1;
	 	if word[i] in self.inv_index:
		   if self.book_count in self.inv_index[word[i]]:
	              if self.CurrentPage in self.inv_index[word[i]][self.book_count]:	
        		self.inv_index[word[i]][self.book_count][self.CurrentPage] += 1;
			self.inv_index[word[i]]['total']+=1;
		      else:
			self.inv_index[word[i]][self.book_count][self.CurrentPage] =1;
			self.inv_index[word[i]]['total']+=1;
	#		self.uniq_count=self.uniq_count+1;
		   else:
			self.inv_index[word[i]][self.book_count]={}
			self.inv_index[word[i]]['total']+=1;
			self.inv_index[word[i]][self.book_count][self.CurrentPage]=1;
	#		self.uniq_count=self.uniq_count+1;
		else:
			self.inv_index[word[i]]={};
			self.inv_index[word[i]][self.book_count]={}
 			self.inv_index[word[i]]['total']=1;
			self.inv_index[word[i]]['word_pair']={}
			self.inv_index[word[i]]['word_pair']['powerful']=[0,0,0];
			self.inv_index[word[i]]['word_pair']['strong']=[0,0,0];
			self.inv_index[word[i]]['word_pair']['salt']=[0,0,0];
			self.inv_index[word[i]]['word_pair']['butter']=[0,0,0];
			self.inv_index[word[i]][self.book_count][self.CurrentPage]=1;
                        self.uniq_count=self.uniq_count+1;
#	 self.count=self.count+len(word)

#         print self.Book 
	 #print "Word Count:", self.counter
   def ignorableWhitespace(self, whitespace):
	print whitespace
def tokenPF_calc(u):
	 page_count=0;
	 for v in u.itervalues():                                                                                                                                                                                                                           
            if type(v) is dict:                                                                                                                                                                                                                             
#                print v                                                                                                                                                                                                                                     
                #pdb.set_trace()                                                                                                                                                                                                                            
                #for w in v.itervalues():                                                                                                                                                                                                                    
                 #    tmp2+=w                                                                                                                                                                                                                                
                page_count+=len(v);  
	 return page_count                                                                                                                                                                                                                              
          
if ( __name__ == "__main__"):
   
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
   count=0;
   page_count=0;
   uniq_count=0; 
   book_count=0;
   inv_index={};
   # override the default ContextHandler
   Handler = DocHandler(count,book_count,uniq_count,page_count,inv_index)
   Handler.count=0;
   
   
   parser.setContentHandler( Handler )
#   pdb.set_trace()
   #count=0;
   
   #for root, dirs, files in os.walk("/home/venk/Documents/Information_Retrieval/sample_python/P1/data/"):
   for root, dirs, files in os.walk("/home/venk/Documents/Information_Retrieval/books-tiny/"):
     for file in files:
	if file.endswith(".xml"):
		print "Processing... ",file
               # source=open(os.path.join(root, file));

	        #pdb.set_trace()	
		Handler = DocHandler(Handler.count,(book_count),Handler.uniq_count,Handler.page_count,inv_index)    
		parser.setContentHandler( Handler ) 
		#book_count=book_count+1;                                                                                                                                                                                                                         
   	#	parser.setContentHandler( Handler )
     		parser.parse(os.path.join(root, file))
#		Handler.Book[book_count]=sorted((Handler.Book[book_count]).iteritems(), key=operator.itemgetter(1),reverse=True);
		#print Handler.Book
		#print "Word count: ",Handler.counter
		book_count=book_count+1; 
                #xml.sax.parse(source, DocHandler(count))
   #parser.parse("sample.xml")i
   #print "Word count: ",Handler.count
   #print "Page: ", Handler.page
   #prin:170
#Handler.inv_index;
  
  # print "VNM tiny N " + str(book_count) + ' ' + str(Handler.page_count)
 #  print "VNM tiny TO " + str(Handler.count) 
#   print "VNM tiny TU " + str(Handler.uniq_count)
   #book_count=[];page_count=[]; word_count=[];diction={};
  # for u in inv_index.itervalues():
	 #print u
	 #book_count.append((len(u)))
	 #tmp=0;
	 #tmp2=0;
	 
	 #for v in u.itervalues():
	 #   if type(v) is dict:	
	#	print v
		#pdb.set_trace()
	#	for w in v.itervalues():
         #            tmp2+=w
	#	tmp+=len(v);
	# page_count.append(tmp)
	# word_count.append(tmp2)
	 
#print word_count
#print page_count
#print book_count
#print Handler.inv_index
n=sorted(inv_index, key=lambda x: (inv_index[x]['total']),reverse=True)
print "VNM tiny N " + str(book_count) + ' ' + str(Handler.page_count)                                                                                                                                                                                    
print "VNM tiny TO " + str(Handler.count)                                                                                                                                                                                                                
print "VNM tiny TU " + str(Handler.uniq_count)
for i in range(50):
	u=Handler.inv_index[n[i]];
	tokenString=n[i];
	tokenBF=(len(u)-1);
	tokenPF=(tokenPF_calc(u));
	tokenTF=(inv_index[n[i]]['total'])
	tokenP=float(tokenTF)/len(n);
	tokenPR=float(tokenP)*(i+1);
	print "VNM " + str(i+1) + ' ' + tokenString + ' ' + str(tokenBF) + ' ' + str(tokenPF) + ' ' + str(tokenTF)+ ' ' + str(tokenP) + ' ' + str(tokenPR);
	#for x in n: inv_index[x]
new_list=['powerful','strong','butter','salt','washington','james', 'church'];
for i in range(7):                                                                                                                                                                                                                                         
        u=Handler.inv_index[new_list[i]];                                                                                                                                                                                                                          
        tokenString=new_list[i];                                                                                                                                                                                                                                   
        tokenBF=(len(u)-2);                                                                                                                                                                                                                                 
        tokenPF=(tokenPF_calc(u));                                                                                                                                                                                                                          
        tokenTF=(inv_index[new_list[i]]['total'])                                                                                                                                                                                                                  
        tokenP=float(tokenTF)/len(n);                                                                                                                                                                                                                           
        tokenPR=float(tokenP)*(i+1); 
	                                                                                                                                                                                                           
        print "VNM " + str(n.index(new_list[i])+1) + ' ' + tokenString + ' ' + str(tokenBF) + ' ' + str(tokenPF) + ' ' + str(tokenTF)+ ' ' + str(tokenP) + ' ' + str(tokenPR);
#pdb.set_trace()
#print Handler.inv_index['powerful']
