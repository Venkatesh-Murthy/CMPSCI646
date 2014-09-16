#!/usr/bin/python
import pdb
import xml.sax
import glob
import os
class MovieHandler( xml.sax.ContentHandler ):
   def __init__(self,count):
      self.CurrentData = ""
      self.type = ""
      self.format = ""
      self.years=""
      self.year = ""
      self.rating = ""
      self.stars = ""
      self.description = ""
      self.line=""
      self.count=count;
      #count=0;
      #pdb.set_trace()

   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "movie":
         print "*****Movie*****"
         title = attributes["title"]
         print "Title:", title

   # Call when an elements ends
   def endElement(self, tag):
      if self.CurrentData == "type":
         print "Type:", self.type
      elif self.CurrentData == "format":	
         print "Format:", self.format
      elif self.CurrentData == "years":
         print "Years:", self.years
      elif self.CurrentData == "year":
         print "Year:", self.year
      elif self.CurrentData == "rating":
         print "Rating:", self.rating
      elif self.CurrentData == "stars":
         print "Stars:", self.stars
      elif self.CurrentData == "description":
         print "Description:", self.description
      self.CurrentData = ""

   # Call when a character is read
   def characters(self, content):
#      pdb.set_trace();
      if self.CurrentData == "type":
         self.type = content
      elif self.CurrentData == "format":
         self.format = content
      elif self.CurrentData == "years":
         self.years = content   
      elif self.CurrentData == "year":
         self.year = content
      elif self.CurrentData == "rating":
         self.rating = content
      elif self.CurrentData == "stars":
         self.stars = content
      elif self.CurrentData == "description":
         self.description = content
      elif self.CurrentData == "line":
#	 pdb.set_trace()
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
   Handler = MovieHandler(count)
   parser.setContentHandler( Handler )
#   pdb.set_trace()
   #count=0;
   
   for root, dirs, files in os.walk("/home/venk/Documents/Information_Retrieval/books-tiny/"):
     for file in files:
	if file.endswith(".xml"):
     		parser.parse(os.path.join(root, file))
   #parser.parse("sample.xml")i
   print "Word count: ",Handler.count
