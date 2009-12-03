"""
Geo code various items in the database.

"""
from optparse import OptionParser
import urllib
import connection
import time
import json
import countryCodes
import re

def geocode(text, country_code=None):
    url = 'http://maps.google.com/maps/geo?q=' + urllib.quote(text)
    url +='&key=ABQIAAAAbEHSuXgpf-u5fGdCit8dwRT2yXp_ZAY8_ufC3CFXhHIE1NvwkxQs4GalmejOnVxM2GgcZ1AkId8BXw'
    if country_code:
        url += '&gl=%s' % country_code['code']
    print url
    resp = json.loads(urllib.urlopen(url).read())
    lat,lng = 0.0,0.0
    try:
        lat,lng = resp['Placemark'][0]['Point']['coordinates'][:2]
        print lat,lng
        time.sleep(1)
        return lng,lat
    except:
        return None

def locations(country=None, reparse=False):
    conn,c = connection.connect()
    country_code =  countryCodes.country_codes(code=country)
    extra_and = ""
    
    if country:
        extra_and += " AND country='%s'" % country
    if not reparse:
        extra_and += " AND latlng = ''"
    sql = """
    SELECT * FROM data_locations
    WHERE name IS NOT NULL
    %(extra_and)s
    ORDER BY parent_name DESC
    """ % locals()
    c.execute(sql)
    conn.commit() 
    rows = c.fetchall()
    while rows:
        row = rows.pop()
        text = row[3].split('/')
        text.reverse()
        text = "%s, %s, %s" % (", ".join(text),row[2], country_code['name'])
        parent_name = re.sub("'", "\\'", row[3])
        name = re.sub("'", "\\'", row[2])
        latlng = geocode(text, country_code)
        if latlng:
            latlng = str(latlng)
            c.execute("""
                UPDATE data_locations
                SET latlng=%(latlng)s
                WHERE parent_name=%(parent_name)s
                AND name=%(name)s
            """, locals())
            conn.commit() 
            latlng = None
        # text = c1.fetchone()[3]
    



if __name__ == '__main__':
    
    parse_types = ['locations']
    
    parser = OptionParser()
    parser.add_option("-t", "--type", type='choice', choices=parse_types, dest="parse_type",
                      help="[locations]", metavar="parse type")
    parser.add_option("-r", "--reparse", action="store_true", dest="reparse",
                      help="Reparse existing parsed items", metavar="Reparse")
    parser.add_option("-c", "--country", dest="country",
                      help="Country to parse", metavar="country")

    (options, args) = parser.parse_args()

    if options.parse_type == 'locations':
        locations(options.country, options.reparse)