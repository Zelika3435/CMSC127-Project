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
    term_id: Optional[int]
    semester: str
    payment_status: str = "unpaid"
    role: str = ""
    term_start: date = None
    term_end: date = None
    acad_year: str = ""
    fee_amount: float = 0.0
    fee_due: date = None
    balance: float = 0.0
    membership_id: int = None

@dataclass
class Payment:
    payment_id: Optional[int]
    amount: float
    payment_date: date
    term_id: int