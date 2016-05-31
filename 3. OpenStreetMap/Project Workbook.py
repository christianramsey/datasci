
# coding: utf-8

# In[1]:

#!/usr/bin/env python


import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "manchester_england.osm"  # Replace this with your osm file
SAMPLE_FILE = "manchester.sample2.osm"

k = 900# Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')


# In[1]:

# iterative parsing


# In[3]:

#!/usr/bin/env python

"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
        # YOUR CODE HERE
        tags = {'bounds':0, 'member':0,'nd':0,'node':0,
                'osm':0,'relation':0,'tag':0,'way':0}
        for event,elem in ET.iterparse(filename):
            if elem.tag =="bounds":
                tags['bounds'] += 1
            if elem.tag == 'member':
                tags['member'] += 1
            if elem.tag == 'nd':
                tags['nd'] += 1
            if elem.tag =="osm":
                tags['osm'] += 1
            if elem.tag =="node":
                tags['node'] += 1
            if elem.tag =="relation":
                tags['relation'] += 1
            if elem.tag =="tag":
                tags['tag'] += 1
            if elem.tag =="way":
                tags['way'] += 1
                
        return tags
                


def test():

    tags = count_tags('pcharm/manchester_england.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 27148,
                     'nd': 1758747,
                     'node': 1421700,
                     'osm': 1,
                     'relation': 2203,
                     'tag': 805691,
                     'way': 201946}

    

if __name__ == "__main__":
    test()


# In[10]:

# tag types


# In[25]:

#!/usr/bin/env python

import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into your database, you should check the
"k" value for each "<tag>" and see if there are any potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters.

Please complete the function 'key_type', such that we have a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""


lower = re.compile(r'^([a-z]|_)*$')
higher = re.compile(r'^([A-Z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
naptan = re.compile(r'^([naptan]|_)*:')


def key_type(element, keys):
    if element.tag == "tag":
        
        l = re.search(lower, element.attrib['k'])
        h = re.search(higher, element.attrib['k'])
        lc = re.search(lower_colon, element.attrib['k'])
        pc = re.search(problemchars, element.attrib['k'])
        np = re.search(naptan, element.attrib['k'])
        if np:
            keys['naptan']  += 1 
        if l:
            keys['lower']  += 1 
        if h:
            keys['higher']  += 1             
        if lc:
            keys['lower_colon']  += 1 
         
        if pc:
            keys['problemchars']  += 1 
        if  not (l or lc or pc or h or np):
            keys['other'] += 1               
    return keys



def process_map(filename):
    keys = {"naptan":0, "lower": 0, 'higher':0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.

    keys = process_map('pcharm/manchester_england.osm')
    pprint.pprint(keys)
    assert keys == {'higher': 280,
                     'lower': 608844,
                     'lower_colon': 74340,
                     'naptan': 135348,
                     'other': 769,
                     'problemchars': 2}


if __name__ == "__main__":
    test()



# exploring users


import xml.etree.cElementTree as ET
import pprint as pp
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""
def get_user(element):

    if 'changeset' in element.attrib:
        if 'uid' in element.attrib:
            return element.attrib['uid']
    
    



def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        uid = get_user(element)
        if uid:
            users.add(uid)
        
    print(len(users))
    return users
    


def test():

    users = process_map('pcharm/manchester_england.osm')
    len(users)
    assert len(users) == 1919



if __name__ == "__main__":
    test()

# Improving Street Names

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "P3/manchester.sample2.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Pleasent", "Walk", "Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Close", "Crescent", "Garden", "Grove", "Saint", "Terrace", "Junction", "Gardens"]

# UPDATE THIS VARIABLE
mapping = { 
            "St.": "Street",
            "St": "Street",
            "Rd.": "Road",
            "RD": "Road"
            "N.":"North",
            "Ave":"Avenue",
            "Gr":"Grove",
            "Gn": "Green",
            "Pk": "Park"
            
            
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street" or elem.attrib['k'] == 'naptan:Street')


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
#                 pprint.pprint(tag.attrib)
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    m = street_type_re.search(name)
    for key, value in mapping.iteritems():
        match = re.search(key, name)
        if match:
            name = name.replace(key, value)
            return name
        
    return name




def test():
    st_types = audit(OSMFILE)
    for st_type, ways in st_types.iteritems():
        print("")
        print(st_type)
        print(ways)
        print("")
        for name in ways:
            better_name = update_name(name, mapping)
            print (name, "=>", better_name)
            if name == "Derbyshire Caving Club":
                assert better_name == "Derbyshire Caving Cb"
            if name == "Catalan Rd.":
                assert better_name == "Catalan Road"


if __name__ == '__main__':
    test()


# Preparing for Database



from __future__ import print_function

"""
After auditing is complete the next step is to prepare the data to be inserted into a SQL database.
To do so you will parse the elements in the OSM XML file, transforming them from document format to
tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
imported to a SQL database as tables.

The process for this transformation is as follows:
- Use iterparse to iteratively step through each top level element in the XML
- Shape each element into several data structures using a custom function
- Utilize a schema and validation library to ensure the transformed data is in the correct format
- Write each data structure to the appropriate .csv files

We've already provided the code needed to load the data, perform iterative parsing and write the
output to csv files. Your task is to complete the shape_element function that will transform each
element into the correct format. To make this process easier we've already defined a schema (see
the schema.py file in the last code tab) for the .csv files and the eventual tables. Using the
cerberus library we can validate the output against this schema to ensure it is correct.

## Shape Element Function
The function should take as input an iterparse Element object and return a dictionary.

### If the element top level tag is "node":
The dictionary returned should have the format {"node": .., "node_tags": ...}

The "node" field should hold a dictionary of the following top level node attributes:
- id
- user
- uid
- version
- lat
- lon
- timestamp
- changeset
All other attributes can be ignored

The "node_tags" field should hold a list of dictionaries, one per secondary tag. Secondary tags are
child tags of node which have the tag name/type: "tag". Each dictionary should have the following
fields from the secondary tag attributes:
- id: the top level node id attribute value
- key: the full tag "k" attribute value if no colon is present or the characters after the colon if one is.
- value: the tag "v" attribute value
- type: either the characters before the colon in the tag "k" value or "regular" if a colon
        is not present.

Additionally,

- if the tag "k" value contains problematic characters, the tag should be ignored
- if the tag "k" value contains a ":" the characters before the ":" should be set as the tag type
  and characters after the ":" should be set as the tag key
- if there are additional ":" in the "k" value they and they should be ignored and kept as part of
  the tag key. For example:

  <tag k="addr:street:name" v="Lincoln"/>
  should be turned into
  {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}

- If a node has no secondary tags then the "node_tags" field should just contain an empty list.

The final return value for a "node" element should look something like:

{'node': {'id': 757860928,
          'user': 'uboot',
          'uid': 26299,
       'version': '2',
          'lat': 41.9747374,
          'lon': -87.6920102,
          'timestamp': '2010-07-22T16:16:51Z',
      'changeset': 5288876},
 'node_tags': [{'id': 757860928,
                'key': 'amenity',
                'value': 'fast_food',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'cuisine',
                'value': 'sausage',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'name',
                'value': "Shelly's Tasty Freeze",
                'type': 'regular'}]}

### If the element top level tag is "way":
The dictionary should have the format {"way": ..., "way_tags": ..., "way_nodes": ...}

The "way" field should hold a dictionary of the following top level way attributes:
- id
-  user
- uid
- version
- timestamp
- changeset

All other attributes can be ignored

The "way_tags" field should again hold a list of dictionaries, following the exact same rules as
for "node_tags".

Additionally, the dictionary should have a field "way_nodes". "way_nodes" should hold a list of
dictionaries, one for each nd child tag.  Each dictionary should have the fields:
- id: the top level element (way) id
- node_id: the ref attribute value of the nd tag
- position: the index starting at 0 of the nd tag i.e. what order the nd tag appears within
            the way element

The final return value for a "way" element should look something like:

{'way': {'id': 209809850,
         'user': 'chicago-buildings',
         'uid': 674454,
         'version': '1',
         'timestamp': '2013-03-13T15:58:04Z',
         'changeset': 15353317},
 'way_nodes': [{'id': 209809850, 'node_id': 2199822281, 'position': 0},
               {'id': 209809850, 'node_id': 2199822390, 'position': 1},
               {'id': 209809850, 'node_id': 2199822392, 'position': 2},
               {'id': 209809850, 'node_id': 2199822369, 'position': 3},
               {'id': 209809850, 'node_id': 2199822370, 'position': 4},
               {'id': 209809850, 'node_id': 2199822284, 'position': 5},
               {'id': 209809850, 'node_id': 2199822281, 'position': 6}],
 'way_tags': [{'id': 209809850,
               'key': 'housenumber',
               'type': 'addr',
               'value': '1412'},
              {'id': 209809850,
               'key': 'street',
               'type': 'addr',
               'value': 'West Lexington St.'},
              {'id': 209809850,
               'key': 'street:name',
               'type': 'addr',
               'value': 'Lexington'},
              {'id': '209809850',
               'key': 'street:prefix',
               'type': 'addr',
               'value': 'West'},
              {'id': 209809850,
               'key': 'street:type',
               'type': 'addr',
               'value': 'Street'},
              {'id': 209809850,
               'key': 'building',
               'type': 'regular',
               'value': 'yes'},
              {'id': 209809850,
               'key': 'levels',
               'type': 'building',
               'value': '1'},
              {'id': 209809850,
               'key': 'building_id',
               'type': 'chicago',
               'value': '366409'}]}
"""

import csv
import codecs
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "pcharm/manchester_england.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

import pprint as pp
# - if the tag "k" value contains problematic characters, the tag should be ignored
def handle_tag(tag):
    tag_dict = {}
    problem_cars = re.search(PROBLEMCHARS, tag.attrib['k'])

#     replacing addr
    if tag.attrib['k'] == 'naptan:Street'
        


#  <tag k="addr:street:name" v="Lincoln"/>
# 209809850,name,Lexington,addr:street
# for example, the grader is looking for:
# 209809850,street:name,Lexington,addr
# {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}"


    if problem_cars is None:
        split_keys = tag.attrib['k'].split(':',1)
        if len(split_keys) > 1:
            tag_dict['type'] = split_keys[0]
        else:
            tag_dict['type'] = 'regular'

        tag_dict['key'] = split_keys[-1]
        print("TYPE: ", split_keys[0])
        print("KEY: ", split_keys[-1])
        tag_dict['value'] = tag.attrib['v']
        # pp.pprint(tag_dict)
        return tag_dict


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':
        for tag, tagvalue in element.attrib.iteritems():
            if tag != 'visible':
                node_attribs[tag] = tagvalue

        for x in element.iter():
            if x.tag == 'tag':
                tag_s = handle_tag(x)
                tag_s['id'] = element.attrib['id']
                tags.append(tag_s)

        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        for tag, tagvalue in element.attrib.iteritems():
            if tag != 'visible':
                way_attribs[tag] = tagvalue

        wn_count = 0
        wn_dict = {}
        wn_tags_dict = {}
        for x in element.iter():
            if x.tag == 'nd':
                wn_dict = {}
                print("X ATTRIB:")
                pp.pprint(x.attrib)
                wn_dict['node_id'] = int(x.attrib['ref'])
                wn_dict['position'] = wn_count
                wn_dict['id'] = int(element.attrib['id'])
                wn_count += 1
                print("The result from X attrib converted:")
                pp.pprint(wn_dict)
                way_nodes.append(wn_dict)
            if x.tag == 'tag':
                tag_s = handle_tag(x)
                tag_s['id'] = int(element.attrib['id'])
                tags.append(tag_s)
                tags
        print(" ")
        print("RESULT: ")
        print(" ")
        pp.pprint({'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags})
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)




# 
# ### Exploring the data

"""
sqlite commands to create the db

.import ways.csv way
.import ways_nodes.csv way_nodes
.import ways_tags.csv way_tags
.import nodes_tags.csv node_tags
.import nodes.csv node

"""

import sqlite3
import pandas as pd  
import pprint as pp
get_ipython().magic(u'matplotlib inline')

db = sqlite3.connect("pcharm/manchester.db")
c = db.cursor()

# Cities
cities = '''SELECT tags.value, COUNT(*) as count 
           FROM (SELECT * FROM node_tags UNION ALL 
           SELECT * FROM way_tags) tags
           WHERE tags.key LIKE '%city'
           GROUP BY tags.value
           ORDER BY count DESC;
        '''

##Number of Nodes
nn = 'SELECT COUNT(*) FROM node';
##Number of ways
nw = 'SELECT COUNT(*) FROM way';
##Number of users
nu = 'SELECT COUNT(DISTINCT(e.uid)) FROM (SELECT uid FROM node UNION ALL SELECT uid FROM way) e;'
nnt = 'SELECT COUNT(*) FROM node_tags'
nwt = 'SELECT COUNT(*) FROM way_tags'

node_tag_types = 'SELECT key, COUNT(*) as Amt FROM node_tags GROUP BY key ORDER BY Amt DESC '
way_tag_types = 'SELECT key, COUNT(*) as Amt FROM way_tags GROUP BY key ORDER BY Amt DESC '



religious_tags = 'SELECT value, count(*) as num FROM way_tags WHERE key = "religion" GROUP BY value ORDER BY num DESC;'

bicycle = 'SELECT value, count(*) as num FROM way_tags WHERE key = "bicycle" Group By value Order by num ;'

food = 'SELECT value, Count(*) as num FROM node_tags WHERE key = "cuisine" GROUP BY value ORDER BY num DESC ;'

amenity = 'SELECT value, count(*) as num FROM node_tags WHERE key="amenity" GROUP BY value ORDER BY num DESC;'

schools = 'SELECT value, count(*) as num FROM way_tags WHERE key="school" GROUP BY value ORDER BY num DESC;'

naptan = 'SELECT * FROM node_tags WHERE key="street" ;'



c.execute(bicycle)
rows = c.fetchall()

'''Uncomment to see your query in python'''
print ("Row data:")

'''Uncomment to print your query by row'''
print ("your output:")

'''Uncomment to see your query as a pandas dataframe.
This is similar to the output you've been seeing throughout this course
You can learn more about pandas dataframes in our Intro to Data Analysis course!'''
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd    


df = pd.DataFrame(rows)
db.close()
df
