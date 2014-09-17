#!/usr/bin/python
import pdb
import xml.sax
import glob
import os
class DocHandler( xml.sax.ContentHandler ):
   def __init__(self,count):
      self.CurrentData = ""
      self.line=""
      self.region=""
      self.section=""
      self.page=""
      self.count=count;
      

   # Call when an element starts
   def startElement(self, tag, attributes):
      
      self.CurrentData = tag
      

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
     

   # Call when a character is read
   def characters(self, content):
#      print "Characters: ", content
      #pdb.set_trace();
      
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
	 word=self.line.split(' ')
	 self.count=self.count+len(word)
         
	 #print "Word Count:", self.count
   def ignorableWhitespace(self, whitespace):
	print whitespace
  
if ( __name__ == "__main__"):
   
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
   count=0;
   # override the default ContextHandler
   Handler = DocHandler(count)
   parser.setContentHandler( Handler )
#   pdb.set_trace()
   #count=0;
   
   for root, dirs, files in os.walk("/home/venk/Documents/Information_Retrieval/books-medium/"):
     for file in files:
	if file.endswith(".xml"):
		print "Processing... ",file
               # source=open(os.path.join(root, file));
     		parser.parse(os.path.join(root, file))
                #xml.sax.parse(source, DocHandler(count))
   #parser.parse("sample.xml")i
   print "Word count: ",Handler.count
