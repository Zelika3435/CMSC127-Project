from dataclasses import dataclass
from datetime import date
from typing import Optional, List

@dataclass
class Student:
    student_id: Optional[int]
    first_name: str
    last_name: str
    gender: str
    degree_program: str
    standing: str

@dataclass
class Organization:
    org_id: Optional[int]
    org_name: str

@dataclass
class Member:
    member_id: Optional[int]
    student_id: int
    student: Optional[Student] = None

@dataclass
class Membership:
    membership_id: int
    batch: str
    mem_status: str
    committee: str
    org_id: int
    student_id: int

@dataclass
class HasMembership:
    student_id: int
    membership_id: int
    student: Optional[Student] = None
    membership: Optional[Membership] = None

@dataclass
class Term:
    def __init__(self, term_id, semester, payment_status, role, term_start, term_end, acad_year, fee_amount, fee_due, balance, membership_id):
        self.term_id = term_id
        self.semester = semester
        self.payment_status = payment_status
        self.role = role
        self.term_start = term_start
        self.term_end = term_end
        self.acad_year = acad_year
        self.fee_amount = fee_amount
        self.fee_due = fee_due
        self.balance = balance
        self.membership_id = membership_id

@dataclass
class Payment:
    payment_id: Optional[int]
    amount: float
    payment_date: date
    term_id: int