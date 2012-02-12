class BadGithubObjectException( Exception ):
    pass

class SimpleScalarAttributes:
    class AttributeDefinition:
        def getValueFromRawValue( self, rawValue ):
            return rawValue

    def __init__( self, *attributeNames ):
        self.__attributeNames = attributeNames

    def getAttributeDefinitions( self ):
        return [
            ( attributeName, SimpleScalarAttributes.AttributeDefinition() )
            for attributeName in self.__attributeNames
        ]

def GithubObject( className, *attributePolicies ):
    attributeDefinitions = dict()
    for attributePolicy in attributePolicies:
        for attributeName, attributeDefinition in attributePolicy.getAttributeDefinitions():
            if attributeName in attributeDefinitions:
                raise BadGithubObjectException( "Same attribute defined by two policies" )
            else:
                attributeDefinitions[ attributeName ] = attributeDefinition

    class GithubObject:
        def __init__( self, github, attributes, lazy ):
            self.__attributes = dict()
            self.__updateAttributes( attributes )

        def __getattr__( self, attributeName ):
            if attributeName in attributeDefinitions:
                # if attributeName not in self.__attributes:
                    # self.__fetchAttribute( attributeName )
                return self.__attributes[ attributeName ]
            else:
                raise AttributeError()

        def __updateAttributes( self, attributes ):
            for attributeName, attributeValue in attributes.iteritems():
                attributeDefinition = attributeDefinitions[ attributeName ]
                self.__attributes[ attributeName ] = attributeDefinition.getValueFromRawValue( attributeValue )

    return GithubObject