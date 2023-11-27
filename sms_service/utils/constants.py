from enum import Enum


class SMSBodyTypes(Enum):
    VISITOR = """Dear {visitor},\n\nWelcome to aamarPay. Your visiting number is {otp_code}. Please show this code to the front desk when you check-out.\n\nThanks, \nVPass-aamarPay"""
    VISITING_PERSON = """Dear {visiting_person},\n\nA visitor named {visitor} has come to visit you for {purpose} purpose.\n\nThanks, \nVPass-aamarPay"""
