#!/usr/bin/env python

#
# Generated Wed Mar 30 15:54:07 2011 by generateDS.py version 2.4c.
#

import sys

import ??? as supermod

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = range(3)
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
        if Verbose_import_:
            print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
            if Verbose_import_:
                print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
                if Verbose_import_:
                    print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
                    if Verbose_import_:
                        print("running with ElementTree")
                except ImportError:
                    raise ImportError("Failed to import ElementTree from any known place")

def parsexml_(*args, **kwargs):
    if (XMLParser_import_library == XMLParser_import_lxml and
        'parser' not in kwargs):
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        kwargs['parser'] = etree_.ETCompatXMLParser()
    doc = etree_.parse(*args, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#

class TSchemaSub(supermod.TSchema):
    def __init__(self, Alias=None, Namespace=None, Using=None, Association=None, ComplexType=None, EntityType=None, Function=None, EntityContainer=None):
        super(TSchemaSub, self).__init__(Alias, Namespace, Using, Association, ComplexType, EntityType, Function, EntityContainer, )
supermod.TSchema.subclass = TSchemaSub
# end class TSchemaSub


class TDocumentationSub(supermod.TDocumentation):
    def __init__(self, Summary=None, LongDescription=None):
        super(TDocumentationSub, self).__init__(Summary, LongDescription, )
supermod.TDocumentation.subclass = TDocumentationSub
# end class TDocumentationSub


class TTextSub(supermod.TText):
    def __init__(self, valueOf_=None, mixedclass_=None, content_=None):
        super(TTextSub, self).__init__(valueOf_, mixedclass_, content_, )
supermod.TText.subclass = TTextSub
# end class TTextSub


class TXmlOrTextSub(supermod.TXmlOrText):
    def __init__(self, valueOf_=None, mixedclass_=None, content_=None):
        super(TXmlOrTextSub, self).__init__(valueOf_, mixedclass_, content_, )
supermod.TXmlOrText.subclass = TXmlOrTextSub
# end class TXmlOrTextSub


class TUsingSub(supermod.TUsing):
    def __init__(self, Alias=None, Namespace=None, Documentation=None):
        super(TUsingSub, self).__init__(Alias, Namespace, Documentation, )
supermod.TUsing.subclass = TUsingSub
# end class TUsingSub


class TAssociationSub(supermod.TAssociation):
    def __init__(self, Name=None, Documentation=None, End=None, ReferentialConstraint=None):
        super(TAssociationSub, self).__init__(Name, Documentation, End, ReferentialConstraint, )
supermod.TAssociation.subclass = TAssociationSub
# end class TAssociationSub


class TComplexTypeSub(supermod.TComplexType):
    def __init__(self, TypeAccess=None, Name=None, Documentation=None, Property=None):
        super(TComplexTypeSub, self).__init__(TypeAccess, Name, Documentation, Property, )
supermod.TComplexType.subclass = TComplexTypeSub
# end class TComplexTypeSub


class TConstraintSub(supermod.TConstraint):
    def __init__(self, Documentation=None, Principal=None, Dependent=None):
        super(TConstraintSub, self).__init__(Documentation, Principal, Dependent, )
supermod.TConstraint.subclass = TConstraintSub
# end class TConstraintSub


class TReferentialConstraintRoleElementSub(supermod.TReferentialConstraintRoleElement):
    def __init__(self, Role=None, PropertyRef=None):
        super(TReferentialConstraintRoleElementSub, self).__init__(Role, PropertyRef, )
supermod.TReferentialConstraintRoleElement.subclass = TReferentialConstraintRoleElementSub
# end class TReferentialConstraintRoleElementSub


class TNavigationPropertySub(supermod.TNavigationProperty):
    def __init__(self, Name=None, Relationship=None, ToRole=None, GetterAccess=None, SetterAccess=None, FromRole=None, Documentation=None):
        super(TNavigationPropertySub, self).__init__(Name, Relationship, ToRole, GetterAccess, SetterAccess, FromRole, Documentation, )
supermod.TNavigationProperty.subclass = TNavigationPropertySub
# end class TNavigationPropertySub


class TEntityTypeSub(supermod.TEntityType):
    def __init__(self, TypeAccess=None, Name=None, Documentation=None, Key=None, Property=None, NavigationProperty=None):
        super(TEntityTypeSub, self).__init__(TypeAccess, Name, Documentation, Key, Property, NavigationProperty, )
supermod.TEntityType.subclass = TEntityTypeSub
# end class TEntityTypeSub


class TFunctionSub(supermod.TFunction):
    def __init__(self, FixedLength=None, Scale=None, Name=None, Nullable=None, DefaultValue=None, Precision=None, Collation=None, ReturnType_attr=None, Unicode=None, MaxLength=None, Documentation=None, Parameter=None, DefiningExpression=None, ReturnType=None):
        super(TFunctionSub, self).__init__(FixedLength, Scale, Name, Nullable, DefaultValue, Precision, Collation, ReturnType_attr, Unicode, MaxLength, Documentation, Parameter, DefiningExpression, ReturnType, )
supermod.TFunction.subclass = TFunctionSub
# end class TFunctionSub


class TFunctionParameterSub(supermod.TFunctionParameter):
    def __init__(self, FixedLength=None, Scale=None, Name=None, Nullable=None, DefaultValue=None, Precision=None, Unicode=None, MaxLength=None, Collation=None, Type=None, CollectionType=None, ReferenceType=None, RowType=None):
        super(TFunctionParameterSub, self).__init__(FixedLength, Scale, Name, Nullable, DefaultValue, Precision, Unicode, MaxLength, Collation, Type, CollectionType, ReferenceType, RowType, )
supermod.TFunctionParameter.subclass = TFunctionParameterSub
# end class TFunctionParameterSub


class TCollectionTypeSub(supermod.TCollectionType):
    def __init__(self, FixedLength=None, Scale=None, Nullable=None, DefaultValue=None, Precision=None, Unicode=None, MaxLength=None, Collation=None, ElementType=None, CollectionType=None, ReferenceType=None, RowType=None, TypeRef=None):
        super(TCollectionTypeSub, self).__init__(FixedLength, Scale, Nullable, DefaultValue, Precision, Unicode, MaxLength, Collation, ElementType, CollectionType, ReferenceType, RowType, TypeRef, )
supermod.TCollectionType.subclass = TCollectionTypeSub
# end class TCollectionTypeSub


class TTypeRefSub(supermod.TTypeRef):
    def __init__(self, FixedLength=None, Scale=None, Nullable=None, DefaultValue=None, Precision=None, Unicode=None, MaxLength=None, Collation=None, Type=None, Documentation=None):
        super(TTypeRefSub, self).__init__(FixedLength, Scale, Nullable, DefaultValue, Precision, Unicode, MaxLength, Collation, Type, Documentation, )
supermod.TTypeRef.subclass = TTypeRefSub
# end class TTypeRefSub


class TReferenceTypeSub(supermod.TReferenceType):
    def __init__(self, Type=None, Documentation=None):
        super(TReferenceTypeSub, self).__init__(Type, Documentation, )
supermod.TReferenceType.subclass = TReferenceTypeSub
# end class TReferenceTypeSub


class TRowTypeSub(supermod.TRowType):
    def __init__(self, Property=None):
        super(TRowTypeSub, self).__init__(Property, )
supermod.TRowType.subclass = TRowTypeSub
# end class TRowTypeSub


class TPropertySub(supermod.TProperty):
    def __init__(self, FixedLength=None, Scale=None, Name=None, Nullable=None, DefaultValue=None, Precision=None, Unicode=None, MaxLength=None, Collation=None, Type=None, CollectionType=None, ReferenceType=None, RowType=None):
        super(TPropertySub, self).__init__(FixedLength, Scale, Name, Nullable, DefaultValue, Precision, Unicode, MaxLength, Collation, Type, CollectionType, ReferenceType, RowType, )
supermod.TProperty.subclass = TPropertySub
# end class TPropertySub


class TFunctionReturnTypeSub(supermod.TFunctionReturnType):
    def __init__(self, FixedLength=None, Scale=None, Nullable=None, DefaultValue=None, Precision=None, Unicode=None, MaxLength=None, Collation=None, Type=None, CollectionType=None, ReferenceType=None, RowType=None):
        super(TFunctionReturnTypeSub, self).__init__(FixedLength, Scale, Nullable, DefaultValue, Precision, Unicode, MaxLength, Collation, Type, CollectionType, ReferenceType, RowType, )
supermod.TFunctionReturnType.subclass = TFunctionReturnTypeSub
# end class TFunctionReturnTypeSub


class TEntityKeyElementSub(supermod.TEntityKeyElement):
    def __init__(self, PropertyRef=None):
        super(TEntityKeyElementSub, self).__init__(PropertyRef, )
supermod.TEntityKeyElement.subclass = TEntityKeyElementSub
# end class TEntityKeyElementSub


class TPropertyRefSub(supermod.TPropertyRef):
    def __init__(self, Name=None, valueOf_=None):
        super(TPropertyRefSub, self).__init__(Name, valueOf_, )
supermod.TPropertyRef.subclass = TPropertyRefSub
# end class TPropertyRefSub


class TAssociationEndSub(supermod.TAssociationEnd):
    def __init__(self, Role=None, Type=None, Multiplicity=None, Documentation=None, OnDelete=None):
        super(TAssociationEndSub, self).__init__(Role, Type, Multiplicity, Documentation, OnDelete, )
supermod.TAssociationEnd.subclass = TAssociationEndSub
# end class TAssociationEndSub


class TOnActionSub(supermod.TOnAction):
    def __init__(self, Action=None, Documentation=None):
        super(TOnActionSub, self).__init__(Action, Documentation, )
supermod.TOnAction.subclass = TOnActionSub
# end class TOnActionSub


class TEntityPropertySub(supermod.TEntityProperty):
    def __init__(self, StoreGeneratedPattern=None, Scale=None, Name=None, Nullable=True, DefaultValue=None, MaxLength=None, Precision=None, FixedLength=None, GetterAccess=None, Unicode=None, SetterAccess=None, Collation=None, Type=None, ConcurrencyMode=None, Documentation=None):
        super(TEntityPropertySub, self).__init__(StoreGeneratedPattern, Scale, Name, Nullable, DefaultValue, MaxLength, Precision, FixedLength, GetterAccess, Unicode, SetterAccess, Collation, Type, ConcurrencyMode, Documentation, )
supermod.TEntityProperty.subclass = TEntityPropertySub
# end class TEntityPropertySub


class TComplexTypePropertySub(supermod.TComplexTypeProperty):
    def __init__(self, FixedLength=None, Scale=None, Name=None, Nullable=True, DefaultValue=None, MaxLength=None, Precision=None, GetterAccess=None, Unicode=None, SetterAccess=None, Collation=None, Type=None, ConcurrencyMode=None, Documentation=None):
        super(TComplexTypePropertySub, self).__init__(FixedLength, Scale, Name, Nullable, DefaultValue, MaxLength, Precision, GetterAccess, Unicode, SetterAccess, Collation, Type, ConcurrencyMode, Documentation, )
supermod.TComplexTypeProperty.subclass = TComplexTypePropertySub
# end class TComplexTypePropertySub


class TFunctionImportParameterSub(supermod.TFunctionImportParameter):
    def __init__(self, Scale=None, Name=None, Precision=None, Mode=None, MaxLength=None, Type=None, Documentation=None):
        super(TFunctionImportParameterSub, self).__init__(Scale, Name, Precision, Mode, MaxLength, Type, Documentation, )
supermod.TFunctionImportParameter.subclass = TFunctionImportParameterSub
# end class TFunctionImportParameterSub


class EntityContainerSub(supermod.EntityContainer):
    def __init__(self, TypeAccess=None, LazyLoadingEnabled=None, Extends=None, Name=None, Documentation=None, FunctionImport=None, EntitySet=None, AssociationSet=None):
        super(EntityContainerSub, self).__init__(TypeAccess, LazyLoadingEnabled, Extends, Name, Documentation, FunctionImport, EntitySet, AssociationSet, )
supermod.EntityContainer.subclass = EntityContainerSub
# end class EntityContainerSub


class FunctionImportSub(supermod.FunctionImport):
    def __init__(self, ReturnType=None, MethodAccess=None, EntitySet=None, Name=None, Documentation=None, Parameter=None):
        super(FunctionImportSub, self).__init__(ReturnType, MethodAccess, EntitySet, Name, Documentation, Parameter, )
supermod.FunctionImport.subclass = FunctionImportSub
# end class FunctionImportSub


class EntitySetSub(supermod.EntitySet):
    def __init__(self, GetterAccess=None, EntityType=None, Name=None, GEmptyElementExtensibility=None):
        super(EntitySetSub, self).__init__(GetterAccess, EntityType, Name, GEmptyElementExtensibility, )
supermod.EntitySet.subclass = EntitySetSub
# end class EntitySetSub


class AssociationSetSub(supermod.AssociationSet):
    def __init__(self, Name=None, Association=None, Documentation=None, End=None):
        super(AssociationSetSub, self).__init__(Name, Association, Documentation, End, )
supermod.AssociationSet.subclass = AssociationSetSub
# end class AssociationSetSub


class EndSub(supermod.End):
    def __init__(self, EntitySet=None, Role=None, GEmptyElementExtensibility=None):
        super(EndSub, self).__init__(EntitySet, Role, GEmptyElementExtensibility, )
supermod.End.subclass = EndSub
# end class EndSub



def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    if hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Schema'
        rootClass = supermod.TSchema
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='')
    doc = None
    return rootObj


def parseString(inString):
    from StringIO import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Schema'
        rootClass = supermod.TSchema
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='')
    return rootObj


def parseLiteral(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Schema'
        rootClass = supermod.TSchema
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from ??? import *\n\n')
    sys.stdout.write('import ??? as model_\n\n')
    sys.stdout.write('rootObj = model_.Schema(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="Schema")
    sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

def usage():
    print USAGE_TEXT
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    root = parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()


