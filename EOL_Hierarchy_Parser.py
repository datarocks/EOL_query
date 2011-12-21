__author__ = 'Jim'

import urllib2 # for calling API URLs


from lxml import etree #for EOL_hierarchy

def EOL_hierarchy(search_term):

    #This function depends heavily on this stackoverflow thread:
    #http://stackoverflow.com/questions/3785629/good-python-xml-parser-to-work-with-namespace-heavy-documents

    #base URL for Encyclopedia of Life Hierarchy API
    SEARCH_URL = 'http://eol.org/api/hierarchy_entries/1.0/%s'

    #search_term is an EOL identifier
    str_search_term = str(search_term) #make sure the search term is a string
    url = (SEARCH_URL % str_search_term) #build the URL to call the API

    #print url #trouble shooting print statement

    socket = urllib2.urlopen(url) #call the api and load the XML response into memory
    et = etree.parse(socket)  #parse the XML into a tree that Python knows what to do with

    #declare namespaces, crucial to success, you have to look at the XML document you are going to parse and
    #pull out the namespaces.  You might be able to do this with regexes, but namespaces are often weird, and
    #many times XML is poorly constructed.
    ns = {
        'dcterms':"http://purl.org/dc/terms/",
        'dwc': "http://rs.tdwg.org/dwc/terms/",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'dwr': "http://rs.tdwg.org/dwc/dwcrecord/",
        'dc' : "http://purl.org/dc/elements/1.1/",

    }


    #This counts the number of levels in the taxonomic hierarchy by counting the number of <dwc:taxon> elements
    #it is crucial to use the lxml version of etree, since it is the only one that is XML namespace aware

    recordcount = len(et.xpath("dwc:Taxon", namespaces=ns))
    #print "Number of records:", recordcount #trouble shooting print statement

    # according to docs, .xpath returns always lists when querying for elements
    # .find returns one element, but only supports a subset of XPath

    #this iterates through the hierarchy and pulls the correct
    hierarchy = []
    for i in range(recordcount):
        record = et.xpath("dwc:Taxon", namespaces=ns)[i]
        taxonRank = record.xpath("dwc:taxonRank", namespaces=ns)[0].text
        taxonName = record.xpath("dwc:scientificName", namespaces=ns)[0].text
        taxtuple = (taxonRank,taxonName)
        hierarchy.append(taxtuple)
        #print "level", i, ":", hierarchy[i] #troubleshooting print statement

    return hierarchy #returns an ordered list from highest (e.g. kingdom) to lowest (e.g. species)

#Test Query  Uncomment the next two lines to harvest Hierarchy data about Dame's Violet!
#list = EOL_hierarchy(36432213) #
#print list
