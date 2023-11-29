import pytest
import saving_utils as su

def test_IDIsValidWhenContainingOnlyCharactersNumbersDashUnderscore():
    assert su.isAlphanumericSpecial("HelloWorld123-_") == True

def test_IDIsValidWhenContainingOnlyCharacters():
    assert su.isAlphanumericSpecial("Hello") == True

def test_IDIsValidWhenContainingOnlyNumbers():
    assert su.isAlphanumericSpecial("123") == True

def test_IDIsValidWhenContainingOnlyDashAndUnderscore():
    assert su.isAlphanumericSpecial("_-_") == True
    
def test_IDIsNotValidWhenContainingOtherSpecialCharacters():
    assert su.isAlphanumericSpecial("$%^&") == False

def test_hashasOnlyDashUnderscoreIsTrueWhenContainingOnlyDashAndUnderscore():
    assert su.hasOnlyDashUnderscore("_-_") == True

def test_hashasOnlyDashUnderscoreIsFalseWhenContainingOtherCharactersWithDashAndUnderscore():
    assert su.hasOnlyDashUnderscore("Hello_-_World") == False

def test_IdIsValidWhenContainingAlphanumeric():
    assert su.idValidation("Hello123")['result'] == True

def test_IdIsValidWhenContainingAlphanumericSpecial():
    assert su.idValidation("Hello123_-_")['result'] == True

def test_IdIsInvalidWhenContainingCharactersOtherThanAlphanumericSpecial():
    assert su.idValidation("Hello123_*&^%")['result'] == False

def test_IDIsNotValidWhenContainingOtherSpecialCharacters():
    assert su.isAlphanumericSpecial("$%^&") == False
