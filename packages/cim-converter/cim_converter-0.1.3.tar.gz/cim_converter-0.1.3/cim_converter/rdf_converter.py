from xml.etree.cElementTree import iterparse
from time import time
import re, sys, string

import logging

from traitlets import Unicode

logger = logging.getLogger(__name__)


def xmlns(source):
    """
    Returns a map of prefix to namespace for the given XML file.

    """
    namespaces = {}
    events = ("end", "start-ns", "end-ns")
    for (event, elem) in iterparse(source, events):
        if event == "start-ns":
            prefix, ns = elem
            namespaces[prefix] = ns
        elif event == "end":
            break

    # Reset stream
    if hasattr(source, "seek"):
        source.seek(0)

    return namespaces


def get_rdf_ns(namespaces):
    try:
        ns = namespaces['rdf']
    except KeyError:
        ns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        logger.warn('No rdf namespace found. Using %s' % ns)

    return ns


def get_cim_ns(namespaces):
    """
    Tries to obtain the CIM version from the given map of namespaces and
    returns the appropriate *nsURI* and *packageMap*.

    """
    try:
        ns = namespaces['cim']
        if ns.endswith('#'):
            ns = ns[:-1]
    except KeyError:
        ns = ''
        logger.error('No CIM namespace defined in input file.')

    CIM16nsURI = 'http://iec.ch/TC57/2013/CIM-schema-cim16'

    nsuri = ns

    # import CIM14, CIM15, CIM_EG
    # if ns == CIM14.nsURI:
    #     ns = 'CIM14'
    # elif ns == CIM15.nsURI:
    #     ns = 'CIM15'
    # elif ns == CIM16nsURI:
    #     ns  = 'CIM15'
    # elif ns == CIM_EG.nsURI:
    #     ns = 'CIM_EG'
    # else:
    #     ns = 'CIM15'
    ns = 'cim_converter.CIM_EG'

    cim = __import__(ns, globals(), locals(), ['nsURI', 'packageMap'])

    return nsuri, cim.packageMap


def cimread(source, packageMap=None, nsURI=None, start_dict=None):
    """ CIM RDF/XML parser.

    @type source: File-like object or a path to a file.
    @param source: CIM RDF/XML file.
    @type profile: dict
    @param packageMap: Map of class name to PyCIM package name. All CIM
    classes are under the one namespace, but are arranged into sub-packages
    so a map from class name to package name is required. Defaults to the
    latest CIM version, but may be set to a map from a profile to return
    a profile model.
    @type profile: string
    @param nsURI: CIM namespace URI used in the RDF/XML file. For example:
    http://iec.ch/TC57/2010/CIM-schema-cim15
    @rtype: dict
    @return: Map of UUID to CIM object.

    @author: Richard Lincoln <r.w.lincoln@gmail.com>
    """
    # Start the clock.
    t0 = time()

    #logger.info('##########################################################################')
    logger.info('START of parsing file \"%s\"', source)
    logger_errors_grouped = {}

    # A map of uuids to CIM objects to be returned.
    d = start_dict if start_dict is not None else {}

    # Obtain the namespaces from the input file
    namespaces = xmlns(source)
    ns_rdf = get_rdf_ns(namespaces)
    if bool(nsURI) != bool(packageMap):
        raise ValueError(
            'Either pass "packageMap" AND "nsURI" or none of them.')
    elif (nsURI is None) and (packageMap is None):
        nsURI, packageMap = get_cim_ns(namespaces)

    # CIM element tag base (e.g. {http://iec.ch/TC57/2009/CIM-schema-cim14#}).
    base = "{%s#}" % nsURI
    # Length of element tag base.
    m = len(base)

    # First pass instantiates the classes.
    context = iterparse(source, ("start", "end"))

    # Turn it into an iterator (required for cElementTree).
    context = iter(context)

    # Get the root element ({http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF).
    _, root = next(context)

    for event, elem in context:
        # Process 'end' elements in the CIM namespace.
        if event == "end" and elem.tag[:m] == base:

            # Unique resource identifier for the CIM object.
            uuid = elem.get("{%s}ID" % ns_rdf)
            if uuid is not None:  # class
                # Element tag without namespace (e.g. VoltageLevel).
                tag = elem.tag[m:]
                try:
                    mname = packageMap[tag] + '.' + tag
                except KeyError:
                    logger.error("Unable to locate module for: %s (%s)", tag,
                                 uuid)
                    root.clear()
                    continue
                # Import the module for the CIM object.
                module = __import__(mname, globals(), locals(), [tag], 0)
                # Get the CIM class from the module.
                klass = getattr(module, tag)
                # print(klass.__dict__)
                # Instantiate the class and map it to the uuid.
                d[uuid] = klass(UUID=uuid)

        # Clear children of the root element to minimise memory usage.
        root.clear()
    # Reset stream
    if hasattr(source, "seek"):
        source.seek(0)

    ## Second pass sets attributes and references.
    context = iter(iterparse(source, ("start", "end")))

    # Get the root element ({http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF).
    _, root = next(context)

    for event, elem in context:
        # Process 'start' elements in the CIM namespace.
        if event == "start" and elem.tag[:m] == base:
            uuid = elem.get("{%s}ID" % ns_rdf)
            if uuid is None:
                uuid = elem.get("{%s}about" % ns_rdf)
                if uuid is not None:
                    uuid = uuid[1:]
            if uuid is not None:
                # Locate the CIM object using the uuid.
                try:
                    obj = d[uuid]
                except KeyError:
                    logger.error("Missing '%s' object with uuid: %s",
                                 elem.tag[m:], uuid)
                    root.clear()
                    continue

                # Iterate over attributes/references.
                for event, elem in context:
                    # Process end events with elements in the CIM namespace.
                    if event == "end" and elem.tag[:m] == base:
                        # Break if class closing element (e.g. </cim:Terminal>).
                        if elem.get("{%s}ID" % ns_rdf) is None and \
                                elem.get("{%s}about" % ns_rdf) is None:
                            # Get the attribute/reference name.
                            attr = elem.tag[m:].rsplit(".")[-1]

                            if not hasattr(obj, attr):
                                error_msg = "'%s' has not attribute '%s'" % (
                                    obj.__class__.__name__, attr)
                                try:
                                    logger_errors_grouped[error_msg] += 1
                                except KeyError:
                                    logger_errors_grouped[error_msg] = 1
                                logger.error("'%s' has not attribute '%s'",
                                             obj.__class__.__name__, attr)
                                continue

                            # Use the rdf:resource attribute to distinguish
                            # between attributes and references/enums.
                            uuid2 = elem.get("{%s}resource" % ns_rdf)

                            if uuid2 is None:  # attribute

                                # Convert value type using the default value.
                                try:
                                    typ = type(getattr(obj, attr))
                                    if typ == type(
                                            True
                                    ):  # KKG: Test if it is boolean value
                                        # KKG: NB: The function bool("false") returns True, because it is called upon non-empty string!
                                        # This means that it wrongly reads "false" value as boolean True and this is why this special case testing is necessary
                                        if str.title(elem.text) == 'True':
                                            setattr(obj, attr, True)
                                        else:
                                            setattr(obj, attr, False)
                                    else:
                                        # print(obj.__class__.__name__)
                                        # print(source)
                                        setattr(obj, attr, typ(elem.text))
                                except TypeError:
                                    pass
                            else:  # reference or enum
                                # Use the '#' prefix to distinguish between
                                # references and enumerations.
                                if uuid2[0] == "#":  # reference
                                    try:
                                        val = d[uuid2[1:]]  # remove '#' prefix
                                    except KeyError:
                                        # logger.error(
                                        #     "Referenced '%s' [%s] "
                                        #     "object missing.",
                                        #     obj.__class__.__name__, uuid2[1:])
                                        continue

                                    default = getattr(obj, attr)

                                    if default == None:  # 1..1 or 1..n
                                        # Rely on properties to set any
                                        # bi-directional references.
                                        setattr(obj, attr, val)
                                    elif isinstance(default, list):
                                        # Use 'add*' method to set reference.
                                        getattr(obj, ("add%s" % attr))(val)

                                else:  # enum
                                    val = uuid2.rsplit(".", 1)[1]
                                    setattr(obj, attr, val)

                        else:
                            # Finished setting object attributes.
                            break

        # Clear children of the root element to minimise memory usage.
        root.clear()

    if logger_errors_grouped:
        for error, count in logger_errors_grouped.items():
            logging_message = '%s : %d times' % (error, count)
            logger.warn(logging_message)

    # logging_message = 'Created totally %d CIM objects in %.2fs.' %(len(d), time() - t0)
    logger.info('Created totally %d CIM objects in %.2fs.' %
                (len(d), time() - t0))
    # logging_message = 'END of parsing file \"%s\"\n' % source
    logger.info('END of parsing file \"%s\"\n' % source)

    return d

try:
    unicode("")
except NameError:
    def encode(s, encoding):
        return s
    _escape = re.compile(r"[&<>\"\x80-\xff]+")
else:
    def encode(s, encoding):
        return s.encode(encoding)
    _escape = re.compile(eval(r'u"[&<>\"\u0080-\uffff]+"'))

def encode_entity(text, pattern=_escape):
    def escape_entities(m):
        out = []
        for char in m.group():
            out.append("&#%d;" % ord(char))
        return "".join(out)
    return encode(pattern.sub(escape_entities, text), "ascii")

del _escape

def escape_cdata(s, encoding=None):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if encoding:
        try:
            return encode(s, encoding)
        except UnicodeError:
            return encode_entity(s)
    return s

def escape_attrib(s, encoding=None):
    s = s.replace("&", "&amp;")
    s = s.replace("'", "&apos;")
    s = s.replace("\"", "&quot;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if encoding:
        try:
            return encode(s, encoding)
        except UnicodeError:
            return encode_entity(s)
    return s

class XMLWriter:

    def __init__(self, file, encoding="us-ascii"):
        if not hasattr(file, "write"):
            file = open(file, "w")
        self.__write = file.write
        if hasattr(file, "flush"):
            self.flush = file.flush
        self.__open = 0
        self.__tags = []
        self.__data = []
        self.__encoding = encoding

    def __flush(self):
        if self.__open:
            self.__write(">")
            self.__open = 0
        if self.__data:
            data = "".join(self.__data)
            self.__write(escape_cdata(data, self.__encoding))
            self.__data = []

    def declaration(self):
        encoding = self.__encoding
        if encoding == "us-ascii" or encoding == "utf-8":
            self.__write("<?xml version='1.0'?>\n")
        else:
            self.__write("<?xml version='1.0' encoding='%s'?>\n" % encoding)

    def start(self, tag, attrib={}, **extra):
        self.__flush()
        tag = escape_cdata(tag, self.__encoding)
        self.__data = []
        self.__tags.append(tag)
        self.__write("<%s" % tag)
        if attrib or extra:
            combined_attrib = attrib.copy()
            combined_attrib.update(extra)
            for k, v in sorted(attrib.items()):
                k = escape_cdata(k, self.__encoding)
                v = escape_attrib(v, self.__encoding)
                self.__write(" %s=\"%s\"" % (k, v))
        self.__open = 1
        return len(self.__tags)-1

    def comment(self, comment):
        self.__flush()
        self.__write("<!-- %s -->\n" % escape_cdata(comment, self.__encoding))

    def data(self, text):
        self.__data.append(text)

    def end(self, tag=None):
        if tag:
            assert self.__tags, "unbalanced end(%s)" % tag
            assert escape_cdata(tag, self.__encoding) == self.__tags[-1],\
                   "expected end(%s), got %s" % (self.__tags[-1], tag)
        else:
            assert self.__tags, "unbalanced end()"
        tag = self.__tags.pop()
        if self.__data:
            self.__flush()
        elif self.__open:
            self.__open = 0
            self.__write(" />")
            return
        self.__write("</%s>" % tag)

    def close(self, id):
        while len(self.__tags) > id:
            self.end()

    def element(self, tag, text=None, attrib={}, **extra):
        self.start(tag, attrib, **extra)
        if text:
            self.data(text)
        self.end()

    def flush(self):
        pass


def cimwrite(d, source, encoding="utf-8"):
    logger = logging.getLogger(__name__)
    nsPrefixRDF = "rdf"
    nsRDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    nsURI = "http://www.elektro-gorenjska.si/CIM/Profiles/NetworkModel"
    nsPrefix = "cim"
    """CIM RDF/XML serializer.

    @type d: dict
    @param d: Map of URIs to CIM objects.
    @type source: File or file-like object.
    @param source: This object must implement a C{write} method
    that takes an 8-bit string.
    @type encoding: string
    @param encoding: Character encoding defaults to "utf-8", but can also
    be set to "us-ascii".
    @rtype: bool
    @return: Write success.
    """
    # Start the clock
    t0 = time()

    w = XMLWriter(source, encoding)

    # Write the XML declaration.
    w.declaration()

    # Add a '#' suffix to the CIM namespace URI if not present.
    nsCIM = nsURI if nsURI[-1] == "#" else nsURI + "#"

    # Start the root RDF element and declare namespaces.
    xmlns = {u"xmlns:%s" % nsPrefixRDF: nsRDF, u"xmlns:%s" % nsPrefix: nsCIM}
    rdf = w.start(u"%s:RDF" % nsPrefixRDF, xmlns)


    # Iterate over all UUID, CIM object pairs in the given dictionary.
    for uuid, obj in d.items():
        w.start(u"%s:%s" % (nsPrefix, obj.__class__.__name__),
                {u"%s:ID" % nsPrefixRDF: obj.UUID})

        mro = obj.__class__.mro()
        mro.reverse()
        

        # Serialise attributes.
        for klass in mro[2:]: # skip 'object' and 'Element'
            attrs = [a for a in klass._attrs if a not in klass._enums]
            for attr in attrs:
                val = getattr(obj, attr)
                if val != klass._defaults[attr]:
                    w.element(u"%s:%s.%s" % (nsPrefix, klass.__name__, attr),
                              str(val))
                    

        # Serialise enumeration data-types.
        for klass in mro[2:]: # skip 'object' and 'Element'
            enums = [a for a in klass._attrs if a in klass._enums]
            for enum in enums:
                val = getattr(obj, enum)
                dt = klass._enums[enum]
                w.element(u"%s:%s.%s" % (nsPrefix, klass.__name__, enum),
                          attrib={u"%s:resource" % nsPrefixRDF:
                                  u"%s%s.%s" % (nsCIM, dt, val)})

        # Serialise references.
        for klass in mro[2:]: # skip 'object' and 'Element'
            # FIXME: serialise 'many' references.
            refs = [r for r in klass._refs if r not in klass._many_refs]
            for ref in refs:

                val = getattr(obj, ref)
                if val is not None:
                    w.element(u"%s:%s.%s" % (nsPrefix, klass.__name__, ref),
                        attrib={u"%s:resource" % nsPrefixRDF:
                                u"#%s" % val.UUID})
                        
        # Serialise 'many' references.
        for klass in mro[2:]:
            many_refs = [r for r in klass._refs if r in klass._many_refs]
            for many_ref in many_refs:
                vals = getattr(obj, many_ref)
                if isinstance(vals, list):
                    for val in vals:
                        w.element(u"%s:%s.%s" % (nsPrefix, klass.__name__, many_ref),
                                attrib={u"%s:resource" % nsPrefixRDF:
                                        u"#%s" % val.UUID})
                else:
                    w.element(u"%s:%s.%s" % (nsPrefix, klass.__name__, many_ref),
                                attrib={u"%s:resource" % nsPrefixRDF:
                                        u"#%s" % vals.UUID})
            

        w.end()

    # Close the root RDF element.
    w.close(rdf)

    # Flush the output stream.
    w.flush()

    logger.info("%d CIM objects serialised in %.2fs.", len(d), time() - t0)