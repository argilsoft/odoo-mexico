#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2014 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#
#    Coded by: vauxoo consultores (info@vauxoo.com)
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

'''
Enter address (path_local) and Url of file to download
'''

import os
from os.path import basename
import xml
from xml.dom import minidom
import urllib
import urllib2
from urlparse import urlsplit
import sys
from urllib2 import Request, urlopen, URLError, HTTPError
import ConfigParser

# Read file.conf
if len(sys.argv)==2:
    if os.path.exists(sys.argv[1]):
        file_conf = sys.argv[1]
        if file_conf:
            config = ConfigParser.RawConfigParser()
            config.read(file_conf)
            url = config.get('options', 'url')
            path_local = config.get('options', 'path_local')
            urls_list =  url.split(',')
    else:
        sys.exit('ERROR: File %s was not found!' % sys.argv[1])
# End Read file.conf
else:
    print "Example of path_local:\n\n /home/carlos/instancias/7/addons_all/openerp-mexico-localization70/l10n_mx_facturae/SAT/cadenaoriginal_3_2/"
    path_local = raw_input('\nEnter the address (path_local): ')
    print "\nExample of URL:\r"
    print "http://www.sat.gob.mx/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt\n"
    print "http://www.sat.gob.mx/sitio_internet/cfd/nomina/nomina11.xsd"
    url = raw_input('Enter Url of file to download: ')
    urls_list =  url.split(',')
    #~url = "http://www.sat.gob.mx/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt"
    #~url = "http://www.sat.gob.mx/sitio_internet/cfd/nomina/nomina11.xsd"
path_local_current = os.getcwd() # Knowing the current directory

if path_local:
    if not os.path.exists(path_local):
        os.mkdir(path_local)
else:
    path_local = path_local_current
for url in urls_list:
    name_file = basename(urlsplit(url)[2])
    # Generate Path local for Linux and Windows
    if path_local:
        path_local_file = os.path.join(path_local, name_file)
    else:
        path_local_file = os.path.join(path_local_current, name_file)
        path_local = path_local_current
    # End Generate Path local
    # Abrir URL
    try:
        f = urllib2.urlopen(url)
    except HTTPError, e:
        print "HTTP Error:",e.code , url
    except URLError, e:
        print "URL Error:",e.reason , url
        #~sys.exit(0)
    # Update file
    content_file = f.read()
    with open(path_local_file, "wb") as code:
        code.write(content_file)
    code.close()
    print "Downloaded ", name_file
    # End file update
    doc_xml = xml.dom.minidom.parseString(content_file) # Convert content to doc
    node_stylesheet = doc_xml.getElementsByTagName("xsl:stylesheet") # Read node xsl:stylesheet of doc_xml
    if node_stylesheet:
        node_stylesheet[0].setAttribute("version", '1.0') # Replace version from 2.0 to 1.0 for library xsltproc
        node_include = doc_xml.getElementsByTagName("xsl:include")  # Read node xsl:include of doc_xml
        for include in node_include:
            # Read links
            url = include.getAttribute("href")
            url = str(url)
            name_file_child = basename(urlsplit(url)[2])
            include.setAttribute("href", name_file_child) # Replace version from 2.0 to 1.0 for library xsltproc
            # End Read links
            path_local_file2 = os.path.join(path_local, name_file_child) # Generate Path local
            # Download childs nodes
            f = urllib2.urlopen(url)
            content = f.read()
            doc = xml.dom.minidom.parseString(content)
            node_stylesheet2 = doc.getElementsByTagName("xsl:stylesheet")
            if node_stylesheet2:
                node_stylesheet2[0].setAttribute("version", '1.0') # Replace version from 2.0 to 1.0 for library xsltproc
            content = doc.toxml().encode('utf-8')
            with open(path_local_file2, "wb") as c:
                c.write(content)
            c.close()
            print "Downloaded ",name_file_child
            # End Download childs nodes
        # Duplicated file downloaded with suffix "_l"
        new_content = doc_xml.toxml().encode('utf-8')
        name_file_split = os.path.splitext(name_file)
        text_name = name_file_split[0]
        extension = name_file_split[1]
        name_file = text_name + '_l' + extension
        path_local_file3 = os.path.join(path_local, name_file) # Generate Path local for local file
        with open(path_local_file3, "wb") as c:
            c.write(new_content)
        c.close()
        print "Was created ", name_file
    

