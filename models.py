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
    student_id: int
    student: Optional[Student] = None

@dataclass
class Membership:
    membership_id: Optional[int]
    batch: str
    mem_status: str
    committee: str
    org_id: int
    student_id: int
    organization: Optional[Organization] = None

@dataclass
class Term:
    term_id: Optional[int]
    semester: str
    term_start: date
    term_end: date
    acad_year: int
    fee_amount: float
    fee_due: date
    membership_id: int

@dataclass
class Payment:
    payment_id: Optional[int]
    payment_status: str
    amount: float
    payment_date: date
    term_id: int