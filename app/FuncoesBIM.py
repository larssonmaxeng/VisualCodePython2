import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.file
from enum import Enum
import os
import uuid
import time
import tempfile
O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

class IfcSurfaceSide(Enum):
    POSITIVE ="POSITIVE"
    NEGATIVE = "NEGATIVE"
    BOTH = "BOTH"
    

class ifcFuzzy():
    def __init__(self, arquivoBase):       

        self.filename = "hello_wall.ifc"
        self.timestamp = time.time()
        self.timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(self.timestamp))
        self.creator = "Kianwee Chen"
        self.organization = "NUS"
        self.application = "IfcOpenShell"
        self.application_version = "0.5"
        self.project_globalid=self.create_guid()
        self.project_name = "Hello Wall"

        template = """ISO-10303-21;
            HEADER;
            FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
            FILE_NAME('%(filename)s','%(timestring)s',('%(creator)s'),('%(organization)s'),'%(application)s','%(application)s','');
            FILE_SCHEMA(('IFC4'));
            ENDSEC;
            DATA;
            #1=IFCPERSON($,$,'%(creator)s',$,$,$,$,$);
            #2=IFCORGANIZATION($,'%(organization)s',$,$,$);
            #3=IFCPERSONANDORGANIZATION(#1,#2,$);
            #4=IFCAPPLICATION(#2,'%(application_version)s','%(application)s','');
            #5=IFCOWNERHISTORY(#3,#4,$,.ADDED.,$,#3,#4,%(timestamp)s);
            #6=IFCDIRECTION((1.,0.,0.));
            #7=IFCDIRECTION((0.,0.,1.));
            #8=IFCCARTESIANPOINT((0.,0.,0.));
            #9=IFCAXIS2PLACEMENT3D(#8,#7,#6);
            #10=IFCDIRECTION((0.,1.,0.));
            #11=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#9,#10);
            #12=IFCDIMENSIONALEXPONENTS(0,0,0,0,0,0,0);
            #13=IFCSIUNIT(\*,.LENGTHUNIT.,$,.METRE.);
            #14=IFCSIUNIT(\*,.AREAUNIT.,$,.SQUARE_METRE.);
            #15=IFCSIUNIT(\*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
            #16=IFCSIUNIT(\*,.PLANEANGLEUNIT.,$,.RADIAN.);
            #17=IFCMEASUREWITHUNIT(IFCPLANEANGLEMEASURE(0.017453292519943295),#16);
            #18=IFCCONVERSIONBASEDUNIT(#12,.PLANEANGLEUNIT.,'DEGREE',#17);
            #19=IFCUNITASSIGNMENT((#13,#14,#15,#18));
            #20=IFCPROJECT('%(project_globalid)s',#5,'%(project_name)s',$,$,$,$,(#11),#19);
            ENDSEC;
            END-ISO-10303-21;
            """ % {"filename": self.filename,   
                "timestamp":self.timestamp,
                "timestring":self.timestring,
                "creator":self.creator,
                "organization":self.organization,
                "application":self.application,
                "application_version":self.application_version,
                "project_globalid":self.project_globalid,
                "project_name":self.project_name}
        # Write the template to a temporary file 
        temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
        with open(temp_filename, "wb") as f:
            f.write(template.encode())

        # Obtain references to instances defined in template
        self.ifcfile = ifcopenshell.open(temp_filename)

        self.owner_history = self.ifcfile.by_type("IfcOwnerHistory")[0]
        self.project = self.ifcfile.by_type("IfcProject")[0]
        self.context = self.ifcfile.by_type("IfcGeometricRepresentationContext")[0]
        self.site_placement = self.create_ifclocalplacement(self.ifcfile)
        self.site = self.ifcfile.createIfcSite(self.create_guid(), self.owner_history, "Site", None, None, self.site_placement, None, None, "ELEMENT", None, None, None, None, None)

        self.building_placement = self.create_ifclocalplacement(self.ifcfile, relative_to=self.site_placement)
        self.building = self.ifcfile.createIfcBuilding(self.create_guid(), self.owner_history, 'Building', None, None, self.building_placement, None, None, "ELEMENT", None, None, None)

        self.storey_placement = self.create_ifclocalplacement(self.ifcfile, relative_to=self.building_placement)
        self.elevation = 0.0
        self.building_storey = self.ifcfile.createIfcBuildingStorey(self.create_guid(), self.owner_history, 'Storey', None, None, self.storey_placement, None, None, "ELEMENT", self.elevation)

        self.container_storey = self.ifcfile.createIfcRelAggregates(self.create_guid(), self.owner_history, "Building Container", None, self.building, [self.building_storey])
        self.container_site = self.ifcfile.createIfcRelAggregates(self.create_guid(), self.owner_history, "Site Container", None, self.site, [self.building])
        self.container_project = self.ifcfile.createIfcRelAggregates(self.create_guid(), self.owner_history, "Project Container", None, self.project, [self.site])
        self.material =  self.ifcfile.createIfcMaterial("Representação do canteiro")
        
        #self.ifc = ifcopenshell.file(schema='IFC4')
    def CriarVolumeRetangular(self, base, largura, altura, volume, local):
        
        #142= IFCAXIS2PLACEMENT3D(#140,#20,#12);
        Variavel142 = self.create_ifcaxis2placement(ifcfile=self.ifcfile, point=local)
        #143= IFCCIRCLE(#142,IFCPOSITIVELENGTHMEASURE(100));
        #143= IFCRECTANGLEPROFILEDEF(.AREA.,'Modelos gen\X2\00E9\X0\ricos 1',#142,1992.38939618349,4200.);
        
        point = self.ifcfile.createIfcCartesianPoint((0.,0.))
        dir1 = self.ifcfile.createIfcDirection((1.,0.))
        axis2placement = self.ifcfile.createIfcAxis2Placement2D(point, dir1)
        
        IfcRectangleProfileDef143 = self.ifcfile.createIfcRectangleProfileDef('AREA',None, axis2placement, base, largura)
        
               
        pontoInsercao170 = self.ifcfile.createIfcCartesianPoint(local)
        
        #172= IFCAXIS2PLACEMENT3D(#170,$,$);
        ifcAxisPlacement172 = self.ifcfile.createIfcAxis2Placement3D(pontoInsercao170, None, None)
        #20
        ifcdir20 =  self.ifcfile.createIfcDirection((0.0, 0.0, 1.0))
        
        #173= IFCEXTRUDEDAREASOLID(#167,#172,#20,300.);
        ifcextrudedareasolid173 = self.ifcfile.createIfcExtrudedAreaSolid(IfcRectangleProfileDef143, ifcAxisPlacement172, ifcdir20, altura)
        #174= IFCSHAPEREPRESENTATION(#105,'Body','SweptSolid',(#173));
        
        body_representation = self.ifcfile.createIfcShapeRepresentation(self.context, "Body", "SweptSolid", [ifcextrudedareasolid173])
        

        product_shape = self.ifcfile.createIfcProductDefinitionShape(None, None, [body_representation])
        
        
        #wall_placement = self.create_ifclocalplacement(self.ifcfile, relative_to=self.storey_placement)
        
        """GlobalId	IfcGloballyUniqueId (STRING)	IfcRoot
        OwnerHistory	IfcOwnerHistory (ENTITY)	IfcRoot
        Name	IfcLabel (STRING)	IfcRoot
        Description	IfcText (STRING)	IfcRoot
        ObjectType	IfcLabel (STRING)	IfcObject
        ObjectPlacement	IfcObjectPlacement (ENTITY)	IfcProduct
        Representation	IfcProductRepresentation (ENTITY)	IfcProduct
        TAG	IfcIdentifier (STRING)	IfcElement
        PredefinedType	IfcBuildingElementProxyTypeEnum (ENUM)"""
        data = {"GlobalId": ifcopenshell.guid.new(),#	IfcGloballyUniqueId (STRING)	IfcRoot
                "OwnerHistory": self.owner_history,#	IfcOwnerHistory (ENTITY)	IfcRoot
                "Name": 'Teste canteiro',#	IfcLabel (STRING)	IfcRoot
                "Description": 'Ver se da certo',#	IfcText (STRING)	IfcRoot
                "ObjectType": 'Volume 1',#	IfcLabel (STRING)	IfcObject
                "ObjectPlacement": Variavel142,#	IfcObjectPlacement (ENTITY)	IfcProduct
                "Representation": product_shape ,#	IfcProductRepresentation (ENTITY)	IfcProduct
                #"TAG": 'xxxx',#	IfcIdentifier (STRING)	IfcElement
                "PredefinedType": None#	IfcBuildingElementProxyTypeEnum (ENUM)"""
            
        }       
        elementProxy = self.ifcfile.create_entity('IfcBuildingElementProxy', **data)
       
        #elementProxy = self.ifcfile.createIfcWallStandardCase(self.create_guid(), , "Wall", "An awesome wall", None, wall_placement, product_shape, None)                                    
         
        
        property_values = [
            self.ifcfile.createIfcPropertySingleValue("Reference", "Reference", self.ifcfile.create_entity("IfcText", "Describe the Reference"), None),
            self.ifcfile.createIfcPropertySingleValue("Tipo de instalações", "Qual material", self.ifcfile.create_entity("IfcText", "Hidrossanitário"), None),
            self.ifcfile.createIfcPropertySingleValue("Entregue", "Entregue", self.ifcfile.create_entity("IfcBoolean", False), None),
            
            self.ifcfile.createIfcPropertySingleValue("IsExternal", "IsExternal", self.ifcfile.create_entity("IfcBoolean", True), None),
            self.ifcfile.createIfcPropertySingleValue("ThermalTransmittance", "ThermalTransmittance", self.ifcfile.create_entity("IfcLengthMeasure", 2.569), None),
            self.ifcfile.createIfcPropertySingleValue("Base", "Base", self.ifcfile.create_entity("IfcLengthMeasure", 10), None),
            self.ifcfile.createIfcPropertySingleValue("Altura", "Altura", self.ifcfile.create_entity("IfcLengthMeasure", 20), None),
            
            self.ifcfile.createIfcPropertySingleValue("IntValue", "IntValue", self.ifcfile.create_entity("IfcInteger", 2), None)
        ]
        property_set =self.ifcfile.createIfcPropertySet(self.create_guid(), self.owner_history, "Pset_almoxarifado", None, property_values)
        self.ifcfile.createIfcRelDefinesByProperties(self.create_guid(), self.owner_history, None, None, [elementProxy], property_set)
                

        """Linha 124: #177= IFCMATERIAL('Telhado padr\X2\00E3\X0\o',$,'N\X2\00E3\X0\o atribu\X2\00ED\X0\do');
        Linha 128: #191= IFCMATERIALDEFINITIONREPRESENTATION($,$,(#188),#177);
        Linha 231: #462= IFCRELASSOCIATESMATERIAL('1oXALVbMv3IApHMiluYnwE',#42,$,$,(#173,#215),#177);"""
        #IFCSURFACESTYLERENDERING(#150,0.,$,$,$,$,IFCNORMALISEDRATIOMEASURE(0.5),IFCSPECULAREXPONENT(64.),.NOTDEFINED.);
        """SurfaceColour	IfcColourRgb (ENTITY)	IfcSurfaceStyleShading
           Transparency	IfcNormalisedRatioMeasure (REAL)	IfcSurfaceStyleShading
            DiffuseColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
               TransmissionColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
              DiffuseTransmissionColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
                ReflectionColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
                SpecularColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
                SpecularHighlight	IfcSpecularHighlightSelect (SELECT)	IfcSurfaceStyleRendering
                ReflectanceMethod	IfcReflectanceMethodEnum (ENUM)"""
        cor = self.ifcfile.createIfcColourRgb(None, 0,0,1)
        render = self.ifcfile.createIfcSurfaceStyleRendering(SurfaceColour = cor,
                                                    Transparency=0.,
                                                    SpecularColour = self.ifcfile.createIfcRatioMeasure( 0.5),
                                                    SpecularHighlight = self.ifcfile.createIfcSpecularExponent(64.0))
        ##152= IFCSURFACESTYLE('Telhado padr\X2\00E3\X0\o',.BOTH.,(#151));
        ifcSurfaceStyle = self.ifcfile.createIfcSurfaceStyle("Representação do canteiro", "BOTH", [render])
         #154= IFCPRESENTATIONSTYLEASSIGNMENT((#152));
        IFCPRESENTATIONSTYLEASSIGNMENT = self.ifcfile.createIfcPresentationStyleAssignment([ifcSurfaceStyle])
        
       
        #156= IFCSTYLEDITEM(#149,(#154),$);
        IFCSTYLEDITEM=self.ifcfile.createIfcStyledItem(ifcextrudedareasolid173,[IFCPRESENTATIONSTYLEASSIGNMENT], None) 
        #169= IFCREPRESENTATIONMAP(#168,#159);?
        #173= IFCBUILDINGELEMENTPROXYTYPE('2fHeoK0OX5zfefqRhXROdu',#42,'Modelos gen\X2\00E9\X0\ricos 1',$,$,$,(#169),'2634',$,.NOTDEFINED.);

        self.ifcfile.createIfcMaterialDefinitionRepresentation(None, None,[elementProxy], self.material )
        
        self.ifcfile.createIfcRelAssociatesMaterial(self.create_guid(), self.owner_history, None, None, [elementProxy], self.material )
         
        self.ifcfile.createIfcRelContainedInSpatialStructure(self.create_guid(), self.owner_history, 
                                                             "Building Storey Container", 
                                                             None, 
                                                             [elementProxy], 
                                                             self.building_storey)
    def CriarVolumeCilindrico(self, raio, altura, volume, local):
        """novoVolume = self.ifc.create_entity('IfcBuildingElementProxy', 
                                            GlobalId=ifcopenshell.guid.new(), 
                                            Name='Wall Name')"""
        """#133= IFCAXIS2PLACEMENT3D(#6,$,$);
        #134= IFCLOCALPLACEMENT(#33,#133);
        #136= IFCBUILDINGSTOREY('02NLKuhrH3QRgvXCJuG8f1',#42,'N\X2\00ED\X0\vel 1',$,'N\X2\00ED\X0\vel:N\X2\00ED\X0\vel 1',#134,$,'N\X2\00ED\X0\vel 1',.ELEMENT.,0.);
        #138= IFCAXIS2PLACEMENT3D(#6,$,$);
        #246= IFCRELDEFINESBYTYPE('2V3VIl8tH8Jujkn8i0PQVa',#42,$,$,(#206),#186);
        #140= IFCCARTESIANPOINT((0.,0.,0.));
        #142= IFCAXIS2PLACEMENT3D(#140,#20,#12);
        #143= IFCCIRCLE(#142,IFCPOSITIVELENGTHMEASURE(100));
        #167= IFCARBITRARYCLOSEDPROFILEDEF(.CURVE.,'Modelos gen\X2\00E9\X0\ricos 2',#143);
        #170= IFCCARTESIANPOINT((2814.89635751607,2898.75957998392,280.67807073955));
        #172= IFCAXIS2PLACEMENT3D(#170,$,$);
        #173= IFCEXTRUDEDAREASOLID(#167,#172,#20,300.);
        #174= IFCSHAPEREPRESENTATION(#105,'Body','SweptSolid',(#173));
        #181= IFCAXIS2PLACEMENT3D(#6,$,$);
        #182= IFCREPRESENTATIONMAP(#181,#174);
        #186= IFCBUILDINGELEMENTPROXYTYPE('0tGM3tkTD0aQibt69qB0Pp',#42,'Modelos gen\X2\00E9\X0\ricos 2',$,$,$,(#182),'3224',$,.NOTDEFINED.);
        #190= IFCCLASSIFICATION('http://www.csiorg.net/uniformat','1998',$,'Uniformat',$,$,$);
        #193= IFCCARTESIANTRANSFORMATIONOPERATOR3D($,$,#6,1.,$);
        #194= IFCMAPPEDITEM(#182,#193);
        #196= IFCSHAPEREPRESENTATION(#105,'Body','Ma"""
        
      
        
        
        #142= IFCAXIS2PLACEMENT3D(#140,#20,#12);
        Variavel142 = self.create_ifcaxis2placement(ifcfile=self.ifcfile, point=local)
        #143= IFCCIRCLE(#142,IFCPOSITIVELENGTHMEASURE(100));
        ifccircle143 = self.ifcfile.createIfcCircle(Variavel142, raio)
        #167= IFCARBITRARYCLOSEDPROFILEDEF(.CURVE.,'Modelos gen\X2\00E9\X0\ricos 2',#143);
        ifcclosedprofile167 = self.ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, ifccircle143)
        
        
        #170= IFCCARTESIANPOINT((2814.89635751607,2898.75957998392,280.67807073955));
        
        pontoInsercao170 = self.ifcfile.createIfcCartesianPoint((0.,0.,0.))
        
        #172= IFCAXIS2PLACEMENT3D(#170,$,$);
        ifcAxisPlacement172 = self.ifcfile.createIfcAxis2Placement3D(pontoInsercao170, None, None)
        #20
        ifcdir20 =  self.ifcfile.createIfcDirection((0.0, 0.0, 1.0))
        
        #173= IFCEXTRUDEDAREASOLID(#167,#172,#20,300.);
        ifcextrudedareasolid173 = self.ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile167, ifcAxisPlacement172, ifcdir20, altura)
        #174= IFCSHAPEREPRESENTATION(#105,'Body','SweptSolid',(#173));
        
        body_representation = self.ifcfile.createIfcShapeRepresentation(self.context, "Body", "SweptSolid", [ifcextrudedareasolid173])
        

        product_shape = self.ifcfile.createIfcProductDefinitionShape(None, None, [body_representation])

        """GlobalId	IfcGloballyUniqueId (STRING)	IfcRoot
        OwnerHistory	IfcOwnerHistory (ENTITY)	IfcRoot
        Name	IfcLabel (STRING)	IfcRoot
        Description	IfcText (STRING)	IfcRoot
        ObjectType	IfcLabel (STRING)	IfcObject
        ObjectPlacement	IfcObjectPlacement (ENTITY)	IfcProduct
        Representation	IfcProductRepresentation (ENTITY)	IfcProduct
        TAG	IfcIdentifier (STRING)	IfcElement
        PredefinedType	IfcBuildingElementProxyTypeEnum (ENUM)"""
        data = {"GlobalId": ifcopenshell.guid.new(),#	IfcGloballyUniqueId (STRING)	IfcRoot
                "OwnerHistory": self.owner_history,#	IfcOwnerHistory (ENTITY)	IfcRoot
                "Name": 'Teste canteiro',#	IfcLabel (STRING)	IfcRoot
                "Description": 'Ver se da certo',#	IfcText (STRING)	IfcRoot
                "ObjectType": 'Volume 1',#	IfcLabel (STRING)	IfcObject
                "ObjectPlacement": Variavel142,#	IfcObjectPlacement (ENTITY)	IfcProduct
                "Representation": product_shape ,#	IfcProductRepresentation (ENTITY)	IfcProduct
                #"TAG": 'xxxx',#	IfcIdentifier (STRING)	IfcElement
                "PredefinedType": None#	IfcBuildingElementProxyTypeEnum (ENUM)"""
            
        }       
        elementProxy = self.ifcfile.create_entity('IfcBuildingElementProxy', **data)
       
        #elementProxy = self.ifcfile.createIfcWallStandardCase(self.create_guid(), , "Wall", "An awesome wall", None, wall_placement, product_shape, None)                                    
         
        
        property_values = [
            self.ifcfile.createIfcPropertySingleValue("Reference", "Reference", self.ifcfile.create_entity("IfcText", "Describe the Reference"), None),
            self.ifcfile.createIfcPropertySingleValue("Tipo de instalações", "Qual material", self.ifcfile.create_entity("IfcText", "Hidrossanitário"), None),
            self.ifcfile.createIfcPropertySingleValue("Entregue", "Entregue", self.ifcfile.create_entity("IfcBoolean", False), None),
            
            self.ifcfile.createIfcPropertySingleValue("IsExternal", "IsExternal", self.ifcfile.create_entity("IfcBoolean", True), None),
            self.ifcfile.createIfcPropertySingleValue("ThermalTransmittance", "ThermalTransmittance", self.ifcfile.create_entity("IfcLengthMeasure", 2.569), None),
            self.ifcfile.createIfcPropertySingleValue("Base", "Base", self.ifcfile.create_entity("IfcLengthMeasure", 10), None),
            self.ifcfile.createIfcPropertySingleValue("Altura", "Altura", self.ifcfile.create_entity("IfcLengthMeasure", 20), None),
            
            self.ifcfile.createIfcPropertySingleValue("IntValue", "IntValue", self.ifcfile.create_entity("IfcInteger", 2), None)
        ]
        property_set =self.ifcfile.createIfcPropertySet(self.create_guid(), self.owner_history, "Pset_almoxarifado", None, property_values)
        self.ifcfile.createIfcRelDefinesByProperties(self.create_guid(), self.owner_history, None, None, [elementProxy], property_set)
                

        """Linha 124: #177= IFCMATERIAL('Telhado padr\X2\00E3\X0\o',$,'N\X2\00E3\X0\o atribu\X2\00ED\X0\do');
        Linha 128: #191= IFCMATERIALDEFINITIONREPRESENTATION($,$,(#188),#177);
        Linha 231: #462= IFCRELASSOCIATESMATERIAL('1oXALVbMv3IApHMiluYnwE',#42,$,$,(#173,#215),#177);"""
        #IFCSURFACESTYLERENDERING(#150,0.,$,$,$,$,IFCNORMALISEDRATIOMEASURE(0.5),IFCSPECULAREXPONENT(64.),.NOTDEFINED.);
        """SurfaceColour	IfcColourRgb (ENTITY)	IfcSurfaceStyleShading
           Transparency	IfcNormalisedRatioMeasure (REAL)	IfcSurfaceStyleShading
            DiffuseColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
               TransmissionColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
              DiffuseTransmissionColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
                ReflectionColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
                SpecularColour	IfcColourOrFactor (SELECT)	IfcSurfaceStyleRendering
                SpecularHighlight	IfcSpecularHighlightSelect (SELECT)	IfcSurfaceStyleRendering
                ReflectanceMethod	IfcReflectanceMethodEnum (ENUM)"""
        cor = self.ifcfile.createIfcColourRgb(None, 0,0,1)
        render = self.ifcfile.createIfcSurfaceStyleRendering(SurfaceColour = cor,
                                                    Transparency=0.5,
                                                    SpecularColour = self.ifcfile.createIfcRatioMeasure( 0.5),
                                                    SpecularHighlight = self.ifcfile.createIfcSpecularExponent(64.0))
        ##152= IFCSURFACESTYLE('Telhado padr\X2\00E3\X0\o',.BOTH.,(#151));
        ifcSurfaceStyle = self.ifcfile.createIfcSurfaceStyle("Representação do canteiro", "BOTH", [render])
         #154= IFCPRESENTATIONSTYLEASSIGNMENT((#152));
        IFCPRESENTATIONSTYLEASSIGNMENT = self.ifcfile.createIfcPresentationStyleAssignment([ifcSurfaceStyle])
        
       
        #156= IFCSTYLEDITEM(#149,(#154),$);
        IFCSTYLEDITEM=self.ifcfile.createIfcStyledItem(ifcextrudedareasolid173,[IFCPRESENTATIONSTYLEASSIGNMENT], None) 
        #169= IFCREPRESENTATIONMAP(#168,#159);?
        #173= IFCBUILDINGELEMENTPROXYTYPE('2fHeoK0OX5zfefqRhXROdu',#42,'Modelos gen\X2\00E9\X0\ricos 1',$,$,$,(#169),'2634',$,.NOTDEFINED.);
        #177= IFCMATERIAL('Telhado padr\X2\00E3\X0\o',$,'N\X2\00E3\X0\o atribu\X2\00ED\X0\do');
        #184= IFCPRESENTATIONSTYLEASSIGNMENT((#152));
        #186= IFCSTYLEDITEM($,(#184),$);
        #188= IFCSTYLEDREPRESENTATION(#99,'Style','Material',(#186));
        #191= IFCMATERIALDEFINITIONREPRESENTATION($,$,(#188),#177);
        #197= IFCCLASSIFICATION('http://www.csiorg.net/uniformat','1998',$,'Uniformat',$,$,$);
        #200= IFCCARTESIANTRANSFORMATIONOPERATOR3D($,$,#6,1.,$);
        #201= IFCMAPPEDITEM(#169,#200);
        self.ifcfile.createIfcMaterialDefinitionRepresentation(None, None,[elementProxy], self.material )
        
        self.ifcfile.createIfcRelAssociatesMaterial(self.create_guid(), self.owner_history, None, None, [elementProxy], self.material )
         
        self.ifcfile.createIfcRelContainedInSpatialStructure(self.create_guid(), self.owner_history, 
                                                             "Building Storey Container", 
                                                             None, 
                                                             [elementProxy], 
                                                             self.building_storey)

                                            
    def create_ifcaxis2placement(self, ifcfile, point=O, dir1=Z, dir2=X):
        point = ifcfile.createIfcCartesianPoint(point)
        dir1 = ifcfile.createIfcDirection(dir1)
        dir2 = ifcfile.createIfcDirection(dir2)
        axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
        return axis2placement

    # Creates an IfcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
    def create_ifclocalplacement(self, ifcfile, point=O, dir1=Z, dir2=X, relative_to=None):
        axis2placement = self.create_ifcaxis2placement(ifcfile,point,dir1,dir2)
        ifclocalplacement2 = ifcfile.createIfcLocalPlacement(relative_to,axis2placement)
        return ifclocalplacement2

# Creates an IfcPolyLine from a list of points, specified as Python tuples
    def create_ifcpolyline(self, ifcfile, point_list):
        ifcpts = []
        for point in point_list:
            point = ifcfile.createIfcCartesianPoint(point)
            ifcpts.append(point)
        polyline = ifcfile.createIfcPolyLine(ifcpts)
        return polyline

# Creates an IfcExtrudedAreaSolid from a list of points, specified as Python tuples
    def create_ifcextrudedareasolid(self, ifcfile, point_list, ifcaxis2placement, extrude_dir, extrusion):
        polyline = self.create_ifcpolyline(ifcfile, point_list)
        ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
        ifcdir = ifcfile.createIfcDirection(extrude_dir)
        ifcextrudedareasolid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile, ifcaxis2placement, ifcdir, extrusion)
        return ifcextrudedareasolid

    def create_guid(self):
        return  uuid.uuid4().hex # ifcopenshell.guid.compress(uuid.uuid1().hex)    
    def Salvar(self):
        self.ifcfile.write(self.filename)   
        print(self.ifcfile)  
        print(self.ifcfile)  
        
ifc1 = ifcFuzzy(arquivoBase="")
ifc1.CriarVolumeCilindrico(altura=2, raio=0.5, volume=0, local=(1.,3.,0.))
ifc1.CriarVolumeCilindrico(altura=2, raio=1, volume=0, local=(3.,3.,6.))
ifc1.CriarVolumeRetangular(base=2, largura=6, volume=0, altura=2, local=(3.,3.,6.))
ifc1.CriarVolumeRetangular(base=2, largura=6, volume=0, altura=2, local=(5.5,3.,6.))
ifc1.CriarVolumeRetangular(base=2, largura=6, volume=0, altura=2, local=(7.5,3.,6.))
ifc1.CriarVolumeRetangular(base=2, largura=6, volume=0, altura=2, local=(9.5,3.,6.))
ifc1.Salvar()        