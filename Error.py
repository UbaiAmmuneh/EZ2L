class Error(Exception):
    pass


class IdentifierDoesntMatchValue(Error):
    pass


def IdentifierDoesntMatchValueRaiser(identifier, value):
    error_end = {
        'null': 'The only allowed value is: null',
        'boolean': 'Allowed values are: true / false',
        'number': 'Allowed values are: any number including floating points and negatives.',
        'string': 'Make sure to have matching quotes at start and end of string',
        'array': 'Make sure to include array elements between [ and ]',
        'map': 'Make sure to include map elements between { and }',
    }

    message = 'Type of %s doesn\'t match %s identifier. %s' % (identifier, value, error_end.get(identifier))
    return IdentifierDoesntMatchValue(message)


class UnknownIdentifier(Error):
    pass


def UnknownIdentifierRaiser(value):
    message = 'Uknown identifier for value %s.' % value
    return IdentifierDoesntMatchValue(message)


class EmptyValue(Error):
    pass


def EmptyValueRaiser(value, identifier):
    def place_of_empty_valu(v):
        i = v.index('')
        if i == 0:
            return 'The first value in the array is empty.'
        elif i == len(v) - 1:
            return 'The last value in the array is empty.'
        else:
            return 'Empty value is between %s and %s at index %s' % (i - 1, i + 1, i)

    errors = {
        'array': 'Can\'t declare an array with an empty value. %s' % place_of_empty_valu(value),
        'map': 'Can\'t declare an map with an empty value. %s' % place_of_empty_valu(value),
        'map-key': 'Can\'t create a key,value pair with empty key',
        'map-value': 'Can\'t create a key,value pair with empty value, '
                     'you can use null as map value if you need an empty map value',
    }

    return EmptyValue(errors.get(identifier))


class InvalidKeyValuePairStructure(Error):
    pass


def InvalidKeyValuePairStructureRaiser(value):
    message = 'Make sure to have one value for every key, got %s values for the same key.' % value.count(':')
    return InvalidKeyValuePairStructure(message)


class UsageOfReservedWord(Error):
    pass


def UsageOfReservedWordRaiser(reserved_word):
    return UsageOfReservedWord('Can\'t use a reserved word as a name or value.')


class BadVariableName(Error):
    pass


def BadVariableNameRaiser(name, letter_index):
    if letter_index == 0:
        message = 'Variable name must start with a letter or underscore, got -%s- %s.' % (name[0], name[1:])
    else:
        message = 'Variable name may contain letters, numbers and underscore, got %s -%s- %s' % \
                  (name[:letter_index], name[letter_index], name[letter_index+1:])
    return BadVariableName(message)
