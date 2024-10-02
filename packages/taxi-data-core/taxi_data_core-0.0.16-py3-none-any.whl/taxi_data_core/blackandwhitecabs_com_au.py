from os import getenv
from typing import Final as Constant, Self, Type, TypeVar, Optional
from datetime import datetime, date, time
from typing import List, Dict

from pydantic import BaseModel, HttpUrl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from bs4.element import Tag
from bs4 import BeautifulSoup
from taxi_data_core import schema
from taxi_data_core.database import BwcDataBase as DataBase

WebSite = TypeVar("WebSite", bound="WebSite")
Job = TypeVar("Job", bound="Job")
GroupStatement = TypeVar("GroupStatement", bound="GroupStatement")
GroupStatement.Transaction = TypeVar("Transaction", bound="GroupStatement.Transaction")
VoucherStatement = TypeVar("VoucherStatement", bound="VoucherStatement")
VoucherStatement.Transaction = TypeVar("Transaction", bound="VoucherStatement.Transaction")
ElectronicJobStatement = TypeVar("ElectronicJobStatement", bound="ElectronicJobStatement")
ElectronicJobStatement.Transaction = TypeVar("Transaction", bound="ElectronicJobStatement.Transaction")
DocketStatement = TypeVar("DocketStatement", bound="DocketStatement")
DocketStatement.Transaction = TypeVar("Transaction", bound="DocketStatement.Transaction")
EftStatement = TypeVar("EftStatement", bound="EftStatement")
EftStatement.Transaction = TypeVar("Transaction", bound="EftStatement.Transaction")
Taxi = TypeVar("Taxi", bound="Taxi")
Driver = TypeVar("Driver", bound="Driver")
Shift = TypeVar("Shift", bound="Shift")

class Taxi(schema.Taxi):
    '''
    Taxi object representing a Taxi.

    Methods:
        get: Get the Taxi object from the website.
    '''
    class Structure(BaseModel):

        FLEET_NUMBER: Constant[int] = 0
        PRIMARY_FLEET: Constant[int] = 1
        REGO: Constant[int] = 2
        REGO_EXPIRY: Constant[int] = 3
        COI_EXPIRY: Constant[int] = 4
        FLEETS: Constant[int] = 5
        CONDITIONS: Constant[int] = 6
        MAKE: Constant[int] = 7
        MODEL: Constant[int] = 8
        BUILD_DATE: Constant[int] = 9
        CAPACITY: Constant[int] = 10
        VALIDATION: Constant[int] = 11
        UNTIL: Constant[int] = 12
        REASON: Constant[int] = 13

    def __init__(self, fleet_number: str, rego: str, rego_expiry: date, coi_expiry: date, make: str, model: str, 
                 build_date: str, capacity: int, primary_fleet: str, fleets: str, conditions: str, validation: str, until: str, reason: str) -> None:
        super().__init__(fleet_number, rego, rego_expiry, coi_expiry, make, model, build_date, capacity, primary_fleet, fleets, conditions,
                         validation, until, reason)


    @classmethod
    def get(cls: Type[Taxi], record: Tag) -> Taxi:

        cols = record.find_all(schema.Common.Constants.TAG_COLUMN)

        return Taxi(fleet_number = cols[cls.Structure.FLEET_NUMBER].text.strip(),
                            primary_fleet = cols[cls.Structure.PRIMARY_FLEET].text.strip(),
                            rego = cols[cls.Structure.REGO].text.strip(),
                            rego_expiry = datetime.strptime(cols[cls.Structure.REGO_EXPIRY].text.strip(), schema.Common.Constants.DEFAULT_DATE_FORMAT),
                            coi_expiry = datetime.strptime(cols[cls.Structure.COI_EXPIRY].text.strip(), schema.Common.Constants.DEFAULT_DATE_FORMAT),
                            fleets = cols[cls.Structure.FLEETS].text.strip(),
                            conditions = cols[cls.Structure.CONDITIONS].text.strip(),
                            make = cols[cls.Structure.MAKE].text.strip(),
                            model = cols[cls.Structure.MODEL].text.strip(),
                            build_date = cols[cls.Structure.BUILD_DATE].text.strip(),
                            capacity = cols[cls.Structure.CAPACITY].text.strip(),
                            validation = cols[cls.Structure.VALIDATION].text.strip() if cols[cls.Structure.VALIDATION] else None,
                            until = cols[cls.Structure.UNTIL].text.strip() if cols[cls.Structure.UNTIL] else None,
                            reason = cols[cls.Structure.REASON].text.strip() if cols[cls.Structure.REASON] else None)

class Driver(schema.Driver):
    '''
    Driver object representing a Driver.
    
    Methods:
        get: Get the Driver object from the website.
    '''

    class Structure(BaseModel):
        NUMBER: Constant[str] = 'Driver number'
        NAME: Constant[str] = 'Driver name'
        GREETING: Constant[str] = 'Greeting'
        ADDRESS: Constant[str] = "Address"
        SUBURB: Constant[str] = 'Suburb'
        POST_CODE: Constant[str] = "Post Code"
        DOB: Constant[str] = "Date of Birth"
        MOBILE: Constant[str] = "Mobile"
        CITY: Constant[str] = "City"
        DA_EXPIRY: Constant[str] = "Authority Expiry"
        LICENSE_EXPIRY: Constant[str] = "License Expiry"
        CONDITIONS: Constant[str] = "Conditions"
        CREATED: Constant[str] = "Created date"
        FIRST_LOGON: Constant[str] = "First log on date"
        LAST_LOGON: Constant[str] = "Last log on date"
        FIRST_OPERATOR_LOGON: Constant[str] = "First log on for operator date"
        LOGON_LAST_180: Constant[str] = "Logons for operator last 180 days"
        HOURS_LAST_180: Constant[str] = "Hours for operator last 180 days"
        AUTH_WHEELCHAIR: Constant[str] = "Wheelchair Authority"
        AUTH_BC: Constant[str] = "Businessclass Authority"
        AUTH_REDFCLIFFE: Constant[str] = "Redcliffe Authority"
        AUTH_LONDON: Constant[str] = "London Cab Authority"
        AUTH_MANDURAH: Constant[str] = "Mandurah Authority"
        REFER_FLEET_OPS: Constant[str] = "Refer Fleet Ops"
        VALIDATION_ACTIVE: Constant[str] = "Validation active"
        VALIDATION_UNTIL: Constant[str] = "Validation until"
        VALIDATION_REASON: Constant[str] = "Validation reason"
        ACTIVE_IN_MTI: Constant[str] = "Active in MTData"

    def __init__(self, number: int, name: str, prefered_name: str, address: str, suburb: str, post_code: int, 
                dob: date, mobile: str, city: str, da_expiry: date, license_expiry: date, conditions: str, 
                create_date: datetime, first_logon: datetime, last_logon: datetime, first_operator_logon: datetime, 
                logons_for_operator: int, hours_for_operator: int, auth_wheelchair: bool, auth_bc: bool, auth_redcliffe: bool, auth_london: bool,
                auth_mandurah: bool, refer_fleet_ops: bool, validation_active: date, validation_until: date, validation_reason: str, active_in_mti: bool) -> None:
        super().__init__(number, name, prefered_name, address,  suburb, post_code, dob, mobile, city, da_expiry, license_expiry,
                         conditions, create_date, first_logon, last_logon, first_operator_logon, logons_for_operator, hours_for_operator, validation_active,
                            validation_until, validation_reason, auth_wheelchair, auth_bc, auth_redcliffe, auth_london, auth_mandurah, refer_fleet_ops, active_in_mti)
    @classmethod
    def get(cls: Type[Driver], website: WebSite) -> Driver:

        WebDriverWait(website.browser, website.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, website.Structure.ID_DRIVER_DETAILS)))

        # Extract the data
        soup = BeautifulSoup(website.browser.page_source, website.Constants.SOUP_HTML_PARSER)
        driver_table = soup.find(website.Constants.TAG_TABLE)

        table_dict: Dict = {}

        for row in driver_table.find_all(website.Constants.TAG_ROW):  # Skip header  & Footer row
            
            cols = row.find_all(website.Constants.TAG_COLUMN)

            key = cols[0].text.strip().replace(":","")
            value = cols[1].text.strip()

            table_dict[key] = value

        return Driver(number = table_dict[cls.Structure.NUMBER],
                        name = table_dict[cls.Structure.NAME],
                        prefered_name = table_dict[cls.Structure.GREETING],
                        address = table_dict[cls.Structure.ADDRESS],
                        suburb = table_dict[cls.Structure.SUBURB],
                        post_code = table_dict[cls.Structure.POST_CODE],
                        dob = datetime.strptime(table_dict[cls.Structure.DOB], website.Constants.DEFAULT_DATE_FORMAT),
                        mobile = table_dict[cls.Structure.MOBILE],
                        city = table_dict[cls.Structure.CITY],
                        da_expiry = datetime.strptime(table_dict[cls.Structure.DA_EXPIRY], website.Constants.DEFAULT_DATE_FORMAT),
                        license_expiry = datetime.strptime(table_dict[cls.Structure.LICENSE_EXPIRY], website.Constants.DEFAULT_DATE_FORMAT),
                        conditions = table_dict[cls.Structure.CONDITIONS],
                        create_date = datetime.strptime(table_dict[cls.Structure.CREATED], website.Constants.DEFAULT_DATE_FORMAT),
                        first_logon = datetime.strptime(table_dict[cls.Structure.FIRST_LOGON], website.Constants.DEFAULT_DATE_FORMAT),
                        last_logon = datetime.strptime(table_dict[cls.Structure.LAST_LOGON], website.Constants.DEFAULT_DATE_FORMAT),
                        first_operator_logon = datetime.strptime(table_dict[cls.Structure.FIRST_OPERATOR_LOGON], website.Constants.DEFAULT_DATE_FORMAT),
                        logons_for_operator = table_dict[cls.Structure.LOGON_LAST_180],
                        hours_for_operator = table_dict[cls.Structure.HOURS_LAST_180],
                        auth_wheelchair = True if table_dict[cls.Structure.AUTH_WHEELCHAIR] else False,
                        auth_bc = True if table_dict[cls.Structure.AUTH_BC] else False,
                        auth_redcliffe = True if table_dict[cls.Structure.AUTH_REDFCLIFFE] else False,
                        auth_london = True if table_dict[cls.Structure.AUTH_LONDON] else False,
                        auth_mandurah = True if table_dict[cls.Structure.AUTH_MANDURAH] else False,
                        refer_fleet_ops = True if table_dict[cls.Structure.REFER_FLEET_OPS] else False,
                        validation_active = datetime.strptime(table_dict[cls.Structure.VALIDATION_ACTIVE], website.Constants.DEFAULT_DATE_FORMAT) if table_dict[cls.Structure.VALIDATION_ACTIVE] else None,
                        validation_until = datetime.strptime(table_dict[cls.Structure.VALIDATION_UNTIL], website.Constants.DEFAULT_DATE_FORMAT) if table_dict[cls.Structure.VALIDATION_UNTIL] else None,
                        validation_reason = table_dict[cls.Structure.VALIDATION_REASON],
                        active_in_mti = True if table_dict[cls.Structure.ACTIVE_IN_MTI] else False)

class Shift(schema.Shift):
    '''
    Shift object representing a Shift.
    
    Methods:
        get: Get the Shift object from the website.
    '''
    class Structure(BaseModel):

        TAXI: Constant[int] = 0
        DRIVER: Constant[int] = 1
        NAME: Constant[int] = 2
        LOG_ON: Constant[int] = 3
        LOG_OFF: Constant[int] = 4
        DURATION: Constant[int] = 5
        DISTANCE: Constant[int] = 6
        OFFERED: Constant[int] = 7
        ACCEPTED: Constant[int] = 8
        REJECTED: Constant[int] = 9
        RECALLED: Constant[int] = 10
        COMPLETED: Constant[int] = 11
        TOTAL_FARES: Constant[int] = 12
        TOTAL_TOLLS: Constant[int] = 13

    def __init__(self, taxi: Taxi | int, name: str, driver: Driver | int, log_on: datetime, log_off: datetime,
                 duration: int, distance: int, offered: int, accepted: int, rejected: int, recalled: int,
                 completed: int, total_fares: float , total_tolls: float) -> None:
        super().__init__(taxi, driver, name, log_on, log_off, duration, distance, offered, accepted, rejected, recalled, completed, total_fares, total_tolls)

    @classmethod
    def get(cls: Type[Shift], record: Tag) -> Shift:

            cols = record.find_all(schema.Common.Constants.TAG_COLUMN)

            return Shift(taxi = cols[cls.Structure.TAXI].text.strip(),
                            driver = cols[cls.Structure.DRIVER].text.strip(),
                            name = cols[cls.Structure.NAME].text.strip(),
                            log_on = datetime.strptime(cols[cls.Structure.LOG_ON].text.strip(), schema.Common.Constants.DEFAULT_DATE_TIME_FORMAT),
                            log_off = datetime.strptime(cols[cls.Structure.LOG_OFF].text.strip(), schema.Common.Constants.DEFAULT_DATE_TIME_FORMAT),
                            duration = schema.Common.Actions.convert_duration_to_seconds(cols[cls.Structure.DURATION].text.strip()),
                            distance = cols[cls.Structure.DISTANCE].text.strip(),
                            offered = cols[cls.Structure.OFFERED].text.strip(),
                            accepted = cols[cls.Structure.ACCEPTED].text.strip(),
                            rejected = cols[cls.Structure.REJECTED].text.strip(),
                            recalled = cols[cls.Structure.RECALLED].text.strip(),
                            completed = cols[cls.Structure.COMPLETED].text.strip(),
                            total_fares = schema.Common.Actions.string_to_float(cols[cls.Structure.TOTAL_FARES].text.strip()),
                            total_tolls = schema.Common.Actions.string_to_float(cols[cls.Structure.TOTAL_TOLLS].text.strip()))

class Job(schema.Job):
    '''
    Job object representing a Job.
    
    Methods:
        get: Get the Job object from the website.
    '''
    class Structure(BaseModel):
        '''
        Constants for the Job object.
        '''
        BOOKING_ID: Constant[str] = 'Booking ID'
        STATUS: Constant[str] = 'Status'
        ACCEPTED: Constant[str] = 'Accepted date and time'
        METER_ON: Constant[str] = 'Meter On date and time'
        METER_OFF: Constant[str] = 'Meter Off date and time'
        CONDITIONS: Constant[str] = 'Conditions'
        ACCOUNT_NUMBER: Constant[str] = 'Account number'
        CUSTOMER_NAME: Constant[str] = 'Customer name'
        PICKUP_PLACE: Constant[str] = 'Pickup Place'
        PICKUP_ADDRESS: Constant[str] = 'Pickup Address'
        PICKUP_SUBURB: Constant[str] = 'Pickup Suburb'
        PICKUP_REMARKS: Constant[str] = 'Pickup Remark'
        DESTINATION_PLACE: Constant[str] = 'Destination Place'
        DESTINATION_ADDRESS: Constant[str] = 'Destination Address'
        DESTINATION_SUBURB: Constant[str] = 'Destination Suburb'
        DESTINATION_REMARKS: Constant[str] = 'Destination Remark'
        FLAGFALL: Constant[str] = 'Flagfall'
        FARE: Constant[str] = 'Fare'
        EXTRAS: Constant[str] = 'Extras'
        DISCOUNT: Constant[str] = 'Discount'
        TOTAL_WITHOUT_TOLLS: Constant[str] = 'Total without tolls'
        TOLLS: Constant[str] = 'Tolls'
        CAR_NUMBER: Constant[str] = 'Car Number'
        CAR_REGISTRATION: Constant[str] = 'Car Registration'

    def __init__(self, booking_number: int, status: str, accepted: time, meter_on: time, meter_off: time, pick_up_suburb: str, 
                 destination_suburb: str, fare: float, toll: float, taxi_id: schema.Taxi | int,
                 conditions: str, customer_name: str, pickup_place: str, pickup_address: str, destination_place: str,
                 destination_address: str, flagfall: float, extras: float, discount: float, total_without_tolls: float, car_rego: str, 
                 pickup_remarks: Optional[str] = None, destination_remarks: Optional[str] = None, account: Optional[str | schema.Docket] = None) -> None:
        super().__init__(booking_number, meter_on, meter_off, fare, taxi_id)
        self.accepted = accepted
        self.pick_up_suburb = pick_up_suburb
        self.destination_suburb = destination_suburb        
        self.toll = toll
        self.account = account
        self.conditions = conditions
        self.customer_name = customer_name
        self.pickup_place = pickup_place
        self.pickup_address = pickup_address
        self.pickup_remarks = pickup_remarks
        self.destination_place = destination_place
        self.destination_address = destination_address
        self.destination_remarks = destination_remarks
        self.flagfall = flagfall
        self.extras = extras
        self.discount = discount
        self.total_without_tolls = total_without_tolls
        self.car_rego = car_rego
        self.status = status

    @classmethod
    def get(cls: Type[Job], website: WebSite) -> Job:
        '''
        Get the Job object from the website.
        
        Args:
            website (WebSite): The website object to extract the data from.
            
        Returns:
            Job: The Job object.
        '''
        WebDriverWait(website.browser, website.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, website.Structure.ID_MY_FORM)))

        # Extract the data
        soup = BeautifulSoup(website.browser.page_source, website.Constants.SOUP_HTML_PARSER)
        job_table = soup.find(website.Constants.TAG_TABLE)

        table_dict = {
            f'{value}': None for key, value in Job.Structure.__dict__.items()
            if not key.startswith("__") and not callable(value)
        }


        for row in job_table.find_all(website.Constants.TAG_ROW):  # Skip header  & Footer row
            
            cols = row.find_all(website.Constants.TAG_COLUMN)

            key = cols[0].text.strip().replace(":","")
            value = cols[1].text.strip()

            table_dict[key] = value

        return Job(booking_number=int(table_dict[cls.Structure.BOOKING_ID]),
                        status=table_dict[cls.Structure.STATUS],
                        accepted=datetime.strptime(table_dict[cls.Structure.ACCEPTED], f'{website.Constants.DEFAULT_DATE_FORMAT} {website.Constants.DEFAULT_TIME_FORMAT}'),
                        meter_on=datetime.strptime(table_dict[cls.Structure.METER_ON], f'{website.Constants.DEFAULT_DATE_FORMAT} {website.Constants.DEFAULT_TIME_FORMAT}'),
                        meter_off=datetime.strptime(table_dict[cls.Structure.METER_OFF], f'{website.Constants.DEFAULT_DATE_FORMAT} {website.Constants.DEFAULT_TIME_FORMAT}'),
                        pick_up_suburb=table_dict[cls.Structure.PICKUP_SUBURB],
                        destination_suburb=table_dict[cls.Structure.DESTINATION_SUBURB],
                        fare=website.Actions.string_to_float(table_dict[cls.Structure.FARE]),
                        toll=website.Actions.string_to_float(table_dict[cls.Structure.TOLLS]),
                        account=table_dict[cls.Structure.ACCOUNT_NUMBER],
                        taxi_id = table_dict[cls.Structure.CAR_NUMBER],
                        conditions=table_dict[cls.Structure.CONDITIONS],
                        customer_name=table_dict[cls.Structure.CUSTOMER_NAME],
                        pickup_place=table_dict[cls.Structure.PICKUP_PLACE],
                        pickup_address=table_dict[cls.Structure.PICKUP_ADDRESS],
                        pickup_remarks=table_dict[cls.Structure.PICKUP_REMARKS],
                        destination_place=table_dict[cls.Structure.DESTINATION_PLACE],
                        destination_address=table_dict[cls.Structure.DESTINATION_ADDRESS],
                        destination_remarks=table_dict[cls.Structure.DESTINATION_REMARKS],
                        flagfall=website.Actions.string_to_float(table_dict[cls.Structure.FLAGFALL]),
                        extras=website.Actions.string_to_float(table_dict[cls.Structure.EXTRAS]),
                        discount=website.Actions.string_to_float(table_dict[cls.Structure.DISCOUNT]),
                        total_without_tolls=website.Actions.string_to_float(table_dict[cls.Structure.TOTAL_WITHOUT_TOLLS]),
                        car_rego=table_dict[cls.Structure.CAR_REGISTRATION])

class GroupStatement(schema.Statement):
    Transaction = TypeVar("Transaction", bound="Transaction")
    '''
    GroupStatement object representing a Group statement.
    
    Methods:
        get: Get the GroupStatement object from the website.
    '''
    class Structure(BaseModel):
        '''
        Constants for the GroupStatement object.
        '''
        DATE: Constant[int] = 0
        VEHICLE: Constant[int] = 1
        REFERENCE: Constant[int] = 2
        AMOUNT: Constant[int] = 3
        BATCH: Constant[int] = 4
        STATUS: Constant[int] = 5

    class Transaction(schema.Statement.Transaction):
        '''
        GroupStatement.Transaction object representing a transaction in the GroupStatement object.
        
        Methods:
            get: Get the GroupStatement.Transaction object from the website.
        '''
        class Structure(BaseModel):
            '''
            Constants for the GroupStatement.Transaction object.
            '''
            GROUP: Constant[int] = 0
            DOCKET: Constant[int] = 1
            AMOUNT: Constant[int] = 2
            DATE: Constant[int] = 3

        def __init__(self, group: str, docket: int, amount: float, date: date) -> None:
            super().__init__(date, amount)
            self.group = group
            self.docket = docket
        
        def __str__(self) -> str:
            return f'{self.date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} Job: {self.docket} ${self.amount:,.2f} {self.group}'
        
        def __repr__(self) -> str:
            return f'{self.date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} Job: {self.docket} ${self.amount:,.2f} {self.group}'

        @classmethod
        def get(cls: Type[GroupStatement.Transaction], row: Tag) -> Self:
            '''
            Get the GroupStatement.Transaction object from the website.
            
            Args:
                row (Tag): The row of the table to extract the data from.
                
            Returns:
                GroupStatement.Transaction: The GroupStatement.Transaction object.
            '''
            cols = row.find_all(WebSite.Constants.TAG_COLUMN)

            return GroupStatement.Transaction(group=cols[GroupStatement.Transaction.Structure.GROUP].text.strip(),
                            docket=int(cols[GroupStatement.Transaction.Structure.DOCKET].text.strip()),
                            amount=WebSite.Actions.string_to_float(cols[GroupStatement.Transaction.Structure.AMOUNT].text.strip()),
                            date=datetime.strptime(cols[GroupStatement.Transaction.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT))



    def __init__(self, statement_date: date, statement_amount: float, url: HttpUrl, vehicle: int, reference: int, batch: int, status: str) -> None:
        super().__init__(statement_date, statement_amount)
        self.url: HttpUrl = url
        self.vehicle: int = vehicle
        self.reference: int = reference
        self.batch: int = batch
        self.status: str = status

    @classmethod
    def get(cls: Type[GroupStatement], row: Tag) -> GroupStatement:
        '''
        Get the GroupStatement object from the website.
        
        Args:
            row (Tag): The row of the table to extract the data from.
            
        Returns:
            GroupStatement: The GroupStatement object.
        '''
        cols = row.find_all(WebSite.Constants.TAG_COLUMN)

        return GroupStatement(statement_date=datetime.strptime(cols[cls.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT),
                              statement_amount=WebSite.Actions.string_to_float(cols[cls.Structure.AMOUNT].text.strip()),
                              url=cols[cls.Structure.DATE].find("a").get("href"),
                              vehicle=int(cols[cls.Structure.VEHICLE].text.strip()),
                              reference=int(cols[cls.Structure.REFERENCE].text.strip()),
                              batch=int(cols[cls.Structure.BATCH].text.strip()),
                              status=cols[cls.Structure.STATUS].text.strip())
    
class VoucherStatement(schema.Statement):
    Transaction = TypeVar("Transaction", bound="Transaction")
    '''
    VoucherStatement object representing a Voucher statement.
    
    
    Methods:
        get: Get the VoucherStatement object from the website.
    '''
    class Structure(BaseModel):
        '''
        Constants for the VoucherStatement object.
        '''
        DATE: Constant[int] = 0
        VEHICLE: Constant[int] = 1
        REFERENCE: Constant[int] = 2
        CROSS_REFERENCE: Constant[int] = 3
        COUNT: Constant[int] = 4
        AMOUNT: Constant[int] = 5
        BATCH: Constant[int] = 6
        STATUS: Constant[int] = 7

    class Transaction(schema.Statement.Transaction):
        '''
        VoucherStatement.Transaction object representing a transaction in the VoucherStatement object.
        
        Methods:
            get: Get the VoucherStatement.Transaction object from the website.
        '''
        class Structure(BaseModel):
            '''
            Constants for the VoucherStatement.Transaction object.
            '''
            TYPE: Constant[int] = 0
            DOCKET: Constant[int] = 1
            EXTENDED: Constant[int] = 2
            AMOUNT: Constant[int] = 3
            DATE: Constant[int] = 4

        def __init__(self, transaction_type: int, docket: int, extended: str, amount: float, date: date) -> None:
            super().__init__(amount, date)
            self.transaction_type = transaction_type
            self.docket = docket
            self.extended = extended
        
        def __str__(self) -> str:
            return f'{self.date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} Job: {self.docket} ${self.amount:,.2f} {self.group}'
        
        def __repr__(self) -> str:
            return f'{self.date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} Job: {self.docket} ${self.amount:,.2f} {self.group}'

        @classmethod
        def get(cls: Type[VoucherStatement.Transaction], row: Tag) -> Self:
            '''
            Get the VoucherStatement.Transaction object from the website.
            
            Args:
                row (Tag): The row of the table to extract the data from.
                
            Returns:
                VoucherStatement.Transaction: The VoucherStatement.Transaction object.
            '''
            cols = row.find_all(WebSite.Constants.TAG_COLUMN)

            return VoucherStatement.Transaction(transaction_type=int(cols[VoucherStatement.Transaction.Structure.TYPE].text.strip()),
                            docket=int(cols[VoucherStatement.Transaction.Structure.DOCKET].text.strip()),
                            extended=cols[VoucherStatement.Transaction.Structure.EXTENDED].text.strip(),
                            amount=WebSite.Actions.string_to_float(cols[VoucherStatement.Transaction.Structure.AMOUNT].text.strip()),
                            date=datetime.strptime(cols[VoucherStatement.Transaction.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT))



    def __init__(self, statement_date: date, statement_amount: float, url: HttpUrl, vehicle: int, reference: int, batch: int, status: str, cross_reference: str, count: int) -> None:
        super().__init__(statement_date, statement_amount)
        self.url: HttpUrl = url
        self.vehicle: int = vehicle
        self.reference: int = reference
        self.cross_reference: str = cross_reference
        self.count: int = count
        self.batch: int = batch
        self.status: str = status

    @classmethod
    def get(cls: Type[VoucherStatement], row: Tag) -> VoucherStatement:
        '''
        Get the VoucherStatement object from the website.
        
        Args:
            row (Tag): The row of the table to extract the data from.
            
        Returns:
            VoucherStatement: The VoucherStatement object.
        '''
        cols = row.find_all(WebSite.Constants.TAG_COLUMN)

        return VoucherStatement(statement_date=datetime.strptime(cols[cls.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT),
                              statement_amount=WebSite.Actions.string_to_float(cols[cls.Structure.AMOUNT].text.strip()),
                              url=cols[cls.Structure.DATE].find("a").get("href"),
                              vehicle=int(cols[cls.Structure.VEHICLE].text.strip()),
                              reference=int(cols[cls.Structure.REFERENCE].text.strip()),
                              batch=int(cols[cls.Structure.BATCH].text.strip()),
                              status=cols[cls.Structure.STATUS].text.strip(),
                              cross_reference=cols[cls.Structure.CROSS_REFERENCE].text.strip(),
                              count=int(cols[cls.Structure.COUNT].text.strip()))
    
class ElectronicJobStatement(schema.Statement):
    Transaction = TypeVar("Transaction", bound="Transaction")
    '''
    ElectronicJobStatement object representing a Electronic Job statement.
    
    Methods:
        get: Get the ElectronicJobStatement object from the website.
    '''
    class Structure(BaseModel):
        '''
        Constants for the ElectronicJobStatement object.
        '''
        DATE: Constant[int] = 0
        COUNT: Constant[int] = 1
        AMOUNT: Constant[int] = 2

    class Transaction(schema.Job):
        '''
        ElectronicJobStatement.Transaction object representing a transaction in the ElectronicJobStatement object.
        
        Methods:
            get: Get the ElectronicJobStatement.Transaction object from the website.
        '''
        class Structure(BaseModel):
            '''
            Constants for the ElectronicJobStatement.Transaction object.
            '''
            TYPE: Constant[int] = 0
            BOOKING_NUMBER: Constant[int] = 1
            DATE: Constant[int] = 2
            TIME: Constant[int] = 3
            VEHICLE: Constant[int] = 4
            DRIVER: Constant[int] = 5
            AMOUNT: Constant[int] = 6
            METER_ON: Constant[int] = 7
            METER_OFF: Constant[int] = 8
            DISTANCE: Constant[int] = 9
            STATUS: Constant[int] = 10

        def __init__(self, transaction_type: str, booking_number: int, accepted_time: time,fare: float, booking_date: date,
                     taxi_id: int, driver_id: str, meter_on: time, meter_off: time, distance: float,
                     status: str) -> None:
            super().__init__(booking_number, meter_on, meter_off, taxi_id, fare)
            self.transaction_type = transaction_type
            self.accepted_time = accepted_time
            self.driver_id = driver_id
            self.distance = distance
            self.status = status
            self.booking_date = booking_date

        def __str__(self) -> str:
            return f'{self.booking_date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} Job: {self.booking_number} ${self.fare:,.2f}'
        
        def __repr__(self) -> str:
            return f'{self.booking_date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} Job: {self.booking_number} ${self.fare:,.2f}'

        @classmethod
        def get(cls: Type[VoucherStatement.Transaction], row: Tag) -> Self:
            '''
            Get the ElectronicJobStatement.Transaction object from the website.
            
            Args:
                row (Tag): The row of the table to extract the data from.
                
            Returns:
                ElectronicJobStatement.Transaction: The ElectronicJobStatement.Transaction object.
            '''
            cols = row.find_all(WebSite.Constants.TAG_COLUMN)

            return ElectronicJobStatement.Transaction(
                            transaction_type=cols[ElectronicJobStatement.Transaction.Structure.TYPE].text.strip(),
                            booking_number=int(cols[ElectronicJobStatement.Transaction.Structure.BOOKING_NUMBER].text.strip()),
                            accepted_time=datetime.strptime(cols[ElectronicJobStatement.Transaction.Structure.TIME].text.strip(), WebSite.Constants.DEFAULT_TIME_FORMAT),
                            fare=WebSite.Actions.string_to_float(cols[ElectronicJobStatement.Transaction.Structure.AMOUNT].text.strip()),
                            booking_date=datetime.strptime(cols[ElectronicJobStatement.Transaction.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT),
                            taxi_id=int(WebSite.Actions.string_to_float(cols[ElectronicJobStatement.Transaction.Structure.VEHICLE].text.strip())),
                            driver_id=cols[ElectronicJobStatement.Transaction.Structure.DRIVER].text.strip(),
                            meter_on=datetime.strptime(cols[ElectronicJobStatement.Transaction.Structure.METER_ON].text.strip(), WebSite.Constants.DEFAULT_TIME_FORMAT),
                            meter_off=datetime.strptime(cols[ElectronicJobStatement.Transaction.Structure.METER_OFF].text.strip(), WebSite.Constants.DEFAULT_TIME_FORMAT),
                            distance=WebSite.Actions.string_to_float(cols[ElectronicJobStatement.Transaction.Structure.DISTANCE].text.strip()),
                            status=cols[ElectronicJobStatement.Transaction.Structure.STATUS].text.strip()
            )



    def __init__(self, statement_date: date, statement_amount: float, url: HttpUrl, count: int) -> None:
        super().__init__(statement_date, statement_amount)
        self.url: HttpUrl = url
        self.count: int = count

    @classmethod
    def get(cls: Type[ElectronicJobStatement], row: Tag) -> ElectronicJobStatement:
        '''
        Get the ElectronicJobStatement object from the website.
        
        Args:
            row (Tag): The row of the table to extract the data from.
            
        Returns:
            ElectronicJobStatement: The ElectronicJobStatement object.
        '''
        cols = row.find_all(WebSite.Constants.TAG_COLUMN)

        return ElectronicJobStatement(
                                statement_date=datetime.strptime(cols[cls.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT),
                                statement_amount=WebSite.Actions.string_to_float(cols[cls.Structure.AMOUNT].text.strip()),
                                url=cols[cls.Structure.DATE].find("a").get("href"),
                                count=int(cols[cls.Structure.COUNT].text.strip()))

class DocketStatement(schema.Statement):
    Transaction = TypeVar("Transaction", bound="Transaction")
    '''
    DocketStatement object representing a Docket statement.
    
    Methods:
        get: Get the DocketStatement object from the website.
    '''
    class Structure(BaseModel):
        '''
        Constants for the DocketStatement object.
        '''
        DATE: Constant[int] = 0
        TYPE: Constant[int] = 1
        AMOUNT: Constant[int] = 2

    class Transaction(schema.Job):
        '''
        DocketStatement.Transaction object representing a transaction in the DocketStatement object.
        
        Methods:
            get: Get the DocketStatement.Transaction object from the website.
        '''
        class Structure(BaseModel):
            '''
            Constants for the DocketStatement.Transaction object.
            '''
            TYPE: Constant[int] = 0
            BOOKING_NUMBER: Constant[int] = 1
            DATE: Constant[int] = 2
            TIME: Constant[int] = 3
            VEHICLE: Constant[int] = 4
            AMOUNT: Constant[int] = 5
            METER_ON: Constant[int] = 6
            METER_OFF: Constant[int] = 7
            DISTANCE: Constant[int] = 8

        def __init__(self, booking_type: str, booking_number: int, booking_date: date, accepted_time: time, taxi_id: int, fare: float, meter_on: time, meter_off: time, distance: float) -> None:
            super().__init__(booking_number, meter_on, meter_off, taxi_id, fare)
            self.booking_type = booking_type
            self.accepted_time = accepted_time
            self.booking_date = booking_date
            self.distance = distance
        
        def __str__(self) -> str:
            return f'{self.booking_date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} Job: {self.booking_number} ${self.fare:,.2f}'
        
        def __repr__(self) -> str:
            return f'{self.booking_date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} Job: {self.booking_number} ${self.fare:,.2f}'

        @classmethod
        def get(cls: Type[GroupStatement.Transaction], row: Tag) -> Self:
            '''
            Get the DocketStatement.Transaction object from the website.
            
            Args:
                row (Tag): The row of the table to extract the data from.
                
            Returns:
                DocketStatement.Transaction: The DocketStatement.Transaction object.
            '''
            cols = row.find_all(WebSite.Constants.TAG_COLUMN)

            return DocketStatement.Transaction(
                            booking_type=cols[DocketStatement.Transaction.Structure.TYPE].text.strip(),
                            booking_number=int(cols[DocketStatement.Transaction.Structure.BOOKING_NUMBER].text.strip()),
                            booking_date=datetime.strptime(cols[DocketStatement.Transaction.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT),
                            accepted_time=datetime.strptime(cols[DocketStatement.Transaction.Structure.TIME].text.strip(), WebSite.Constants.DEFAULT_TIME_FORMAT),
                            taxi_id=int(WebSite.Actions.string_to_float(cols[DocketStatement.Transaction.Structure.VEHICLE].text.strip())),
                            fare=WebSite.Actions.string_to_float(cols[DocketStatement.Transaction.Structure.AMOUNT].text.strip()),
                            meter_on=datetime.strptime(cols[DocketStatement.Transaction.Structure.METER_ON].text.strip(), WebSite.Constants.DEFAULT_TIME_FORMAT),
                            meter_off=datetime.strptime(cols[DocketStatement.Transaction.Structure.METER_OFF].text.strip(), WebSite.Constants.DEFAULT_TIME_FORMAT),
                            distance=WebSite.Actions.string_to_float(cols[DocketStatement.Transaction.Structure.DISTANCE].text.strip())
            )

    def __init__(self, statement_date: date, statement_amount: float, url: HttpUrl, statement_type: str) -> None:
        super().__init__(statement_date, statement_amount)
        self.url: HttpUrl = url
        self.statement_type: str = statement_type

    @classmethod
    def get(cls: Type[GroupStatement], row: Tag) -> GroupStatement:
        '''
        Get the GroupStatement object from the website.
        
        Args:
            row (Tag): The row of the table to extract the data from.
            
        Returns:
            GroupStatement: The GroupStatement object.
        '''
        cols = row.find_all(WebSite.Constants.TAG_COLUMN)

        return DocketStatement(
                                statement_date=datetime.strptime(cols[cls.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT),
                                statement_amount=WebSite.Actions.string_to_float(cols[cls.Structure.AMOUNT].text.strip()),
                                url=cols[cls.Structure.DATE].find("a").get("href"),
                                statement_type=cols[cls.Structure.TYPE].text.strip()
        )
        
class EftStatement(schema.Statement):
    Transaction = TypeVar("Transaction", bound="Transaction")
    '''
    EftStatement object representing a Eft statement.
    
    Methods:
        get: Get the EftStatement object from the website.
    '''
    class Structure(BaseModel):
        '''
        Constants for the EftStatement object.
        '''
        STATEMENT: Constant[int] = 0
        DATE: Constant[int] = 1
        AMOUNT: Constant[int] = 2

    class Transaction(schema.Statement.Transaction):
        '''
        EftStatement.Transaction object representing a transaction in the EftStatement object.
        
        Methods:
            get: Get the EftStatement.Transaction object from the website.
        '''
        class Structure(BaseModel):
            '''
            Constants for the EftStatement.Transaction object.
            '''
            TAXI: Constant[int] = 0
            DATE: Constant[int] = 1
            TIME: Constant[int] = 2
            TYPE: Constant[int] = 3
            TRANSACTION_ID: Constant[int] = 4
            AMOUNT: Constant[int] = 5

        def __init__(self, taxi_id: int, transaction_date: date, amount: float, transaction_time: time, 
                    transaction_type: str, transaction_id: int) -> None:
            super().__init__(amount, transaction_date)
            self.taxi_id = taxi_id
            self.transaction_time = transaction_time
            self.transaction_type = transaction_type
            self.transaction_id = transaction_id
        
        def __str__(self) -> str:
            return f'{self.transaction_date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} {self.transaction_id} ${self.amount:,.2f}'
        
        def __repr__(self) -> str:
            return f'{self.transaction_date.strftime(WebSite.Constants.DEFAULT_DATE_FORMAT)} {self.transaction_id} ${self.amount:,.2f}'

        @classmethod
        def get(cls: Type[EftStatement.Transaction], row: Tag) -> Self:
            '''
            Get the EftStatement.Transaction object from the website.
            
            Args:
                row (Tag): The row of the table to extract the data from.
                
            Returns:
                EftStatement.Transaction: The EftStatement.Transaction object.
            '''
            cols = row.find_all(WebSite.Constants.TAG_COLUMN)

            return EftStatement.Transaction(
                            taxi_id=int(cols[EftStatement.Transaction.Structure.TAXI].text.strip()),
                            transaction_date=datetime.strptime(cols[EftStatement.Transaction.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT),
                            amount=WebSite.Actions.string_to_float(cols[EftStatement.Transaction.Structure.AMOUNT].text.strip()),
                            transaction_time=datetime.strptime(cols[EftStatement.Transaction.Structure.TIME].text.strip(), WebSite.Constants.DEFAULT_TIME_FORMAT),
                            transaction_type=cols[EftStatement.Transaction.Structure.TYPE].text.strip(),
                            transaction_id=int(cols[EftStatement.Transaction.Structure.TRANSACTION_ID].text.strip())
            )

    def __init__(self, statement_date: date, statement_amount: float, url: HttpUrl, reference: int) -> None:
        super().__init__(statement_date, statement_amount)
        self.url: HttpUrl = url
        self.reference: int = reference

    @classmethod
    def get(cls: Type[EftStatement], row: Tag) -> Self:
        '''
        Get the EftStatement object from the website.
        
        Args:
            row (Tag): The row of the table to extract the data from.
            
        Returns:
            EftStatement: The EftStatement object.
        '''
        cols = row.find_all(WebSite.Constants.TAG_COLUMN)

        return EftStatement(
                statement_date=datetime.strptime(cols[cls.Structure.DATE].text.strip(), WebSite.Constants.DEFAULT_DATE_FORMAT),
                statement_amount=WebSite.Actions.string_to_float(cols[cls.Structure.AMOUNT].text.strip()),
                url=cols[cls.Structure.STATEMENT].find("a").get("href"),
                reference=int(cols[cls.Structure.STATEMENT].text.strip())
        )
    
class WebSite(schema.WebSite, schema.Common):
    '''
    WebSite object representing Black and white cabs website.
    
    Methods:
        login: Log in to the website.
        close_last_login_window: Close the last login window.
        select_operator: Select the operator.
        shifts_for_vehicle_set_date_range: Set the date range for the shifts for a vehicle.
        use_nav_menu: Use the navigation menu to select a link.
        get_driver_list: Get a list of drivers from the website.
        get_taxi_list: Get a list of vehicles from the website.
        nav_vehicle_shifts: Navigate to the shifts for a vehicle page.
        get_shift_list: Get a list of shifts from the website.
        get_job_list: Get a list of jobs from the website.
        find_driver: Find a driver by number.
        find_taxi: Find a taxi by fleet number.
        find_shift: Find a shift by taxi and date.
        find_job: Find a job by booking number.
        get_group_statements: Get a list of group statements from the website.
        find_group_statement: Find a group statement by date.
        get_voucher_statements: Get a list of voucher statements from the website.
        find_voucher_statement: Find a voucher statement by date.
        get_electronic_job_statements: Get a list of electronic job statements from the website.
        find_electronic_job_statement: Find an electronic job statement by date.
        get_docket_statements: Get a list of docket statements from the website.
        find_docket_statement: Find a docket statement by date.
        get_eft_statements: Get a list of eft statements from the website.
        find_eft_statement: Find an eft statement by date.
        get_account_balance: Get the account balance from the website.
    '''
    class Structure(BaseModel):
        '''
        Constants for the website.
        '''
        WEB_UI_USERNAME: Constant[str] = getenv("BWC_UI_USERNAME")
        WEB_UI_PASSWORD: Constant[str] = getenv("BWC_UI_PASSWORD")
        WEB_UI_URL: Constant[str] = "https://operators.blackandwhitecabs.com.au/"

        ID_USERNAME_FIELD: Constant[str] = 'userName'
        ID_PASSWORD_FIELD: Constant[str] = 'userPassword'
        ID_LOGON_BUTTON: Constant[str] = 'logon-button'
        ID_OPERATOR: Constant[str] = 'operator'
        ID_VEHICLES_LIST: Constant[str] = 'VehiclesForOperatorList'
        ID_SHIFTS_FOR_VEHICLE: Constant[str] = 'shiftsForVehicle'
        ID_FROM_DATE: Constant[str] = 'fromDate'
        ID_TO_DATE: Constant[str] = 'toDate'
        ID_JOBS_FOR_SHIFT: Constant[str] = 'jobsForShift'
        ID_DRIVER_DETAILS: Constant[str] = "mainContent"
        ID_GROUP_DOCKETS_LODGED_TABLE: Constant[str] = 'GroupDocketsLodgedList'
        ID_DOCKETS_LODGED_TABLE: Constant[str] = 'DocketsLodgedList'
        ID_ELECTRONIC_JOBS: Constant[str] = 'ElectronicJobsList'
        ID_MY_FORM: Constant[str] = 'myForm'
        ID_ELECTRONIC_JOBS_LIST: Constant[str] = 'electronicJobsList'
        ID_BOOKING_NUMBER: Constant[str] = 'bookingNumber'
        ID_DOCKETS_LODGED_LIST: Constant[str] = 'docketsLodgedList'

        CLASS_LAST_LOGIN_MSG_CLOSE: Constant[str] = 'dijitDialogCloseIcon'

        LINK_TEXT_VEHICLES_FOR_OPERATOR: Constant[str] = 'Vehicles for Operator'
        LINK_TEXT_CAR_NUMBER: Constant[str] = 'G6609'
        LINK_TEXT_DRIVERS_FOR_OPERATOR: Constant[str] = 'Drivers for Operator'
        LINK_TEXT_GROUP_DOCKETS_LODGED: Constant[str] = 'Group Dockets Lodged'
        LINK_TEXT_DOCKETS_LODGED: Constant[str] = 'Dockets Lodged'
        LINK_TEXT_ELECTRONIC_JOBS: Constant[str] = 'Electronic Jobs'
        LINK_TEXT_DOCKET_STATEMENTS: Constant[str] = 'Docket Statements'
        LINK_TEXT_EFTPOS_STATEMENTS: Constant[str] = 'Eftpos Statements'
        LINK_TEXT_MY_ACCOUNT: Constant[str] = 'My Accounts'
        LINK_TEXT_BOOKING_LOOKUP: Constant[str] = 'Booking Lookup'

        TEXT_WAYNE_BENNETT: Constant[str] = 'Wayne Bennett'

        XPATH_GO_BUTTON: Constant[str] = "//*[contains(text(), 'Go')]"
        XPATH_SEARCH_BUTTON: Constant[str] = "//*[contains(text(), 'Search')]"
        XPATH_SHIFT_ROW: Constant[str] = '//*[@id="shiftsForVehicle"]/tbody/tr'
        XPATH_DRIVER_ROW: Constant[str] = '//*[@id="driversForOperatorList"]/tbody/tr'
        XPATH_VEHICLE_ROW: Constant[str] = '//*[@id="VehiclesForOperatorList"]/tbody/tr'
        XPATH_DRIVER_DETAILS: Constant[str] = "/html/body/div[4]/form/table"
        XPATH_DOCKET_STATEMENT: Constant[str] = '/html/body/div[4]/form/table'
        XPATH_ELECTRONIC_JOB_ROW: Constant[str] = '//*[@id="ElectronicJobsList"]/tbody/tr'
        XPATH_JOBS_FOR_SHIFT: Constant[str] = '//*[@id="jobsForShift"]/tbody/tr'
        XPATH_GROUP_DOCKETS_LIST: Constant[str] = '//*[@id="GroupDocketsLodgedList"]/tbody/tr'
        XPATH_DOCKETS_LODGED_LIST: Constant[str] = '//*[@id="DocketsLodgedList"]/tbody/tr'
        XPATH_TABLE_ROW: Constant[str] = '//*/tbody/tr'

    def login(self, username: str, password: str) -> None:
        
        """
        Log in to the website.

        Args:
            username (str): The username to log in with.
            password (str): The password to log in with.
        """
        self.username = username
        self.password = password
        # Open the login page
        self.browser.get(self.url)

        # Log in
        username = self.browser.find_element(By.ID, self.Structure.ID_USERNAME_FIELD)
        password = self.browser.find_element(By.ID, self.Structure.ID_PASSWORD_FIELD)

        username.send_keys(self.username)
        password.send_keys(self.password)

        login_button = self.browser.find_element(By.ID, self.Structure.ID_LOGON_BUTTON)
        login_button.click()

    def close_last_login_window(self) -> None:
        """
        Close the last login window.
        """
        # Wait for the page to load and close last login dialog
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, self.Structure.CLASS_LAST_LOGIN_MSG_CLOSE)))
        last_login_close = self.browser.find_element(By.CLASS_NAME, self.Structure.CLASS_LAST_LOGIN_MSG_CLOSE)
        last_login_close.click()

    def select_operator(self) -> None:
        """
        Select the operator.
        """
        # Wait for operator page to load then select operator and click on car
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_OPERATOR)))
        operator_menu = Select(self.browser.find_element(By.ID, self.Structure.ID_OPERATOR))
        operator_menu.select_by_visible_text(self.Structure.TEXT_WAYNE_BENNETT)

    def shifts_for_vehicle_set_date_range(self, from_date: date, to_date: date) -> None:
        """
        Set the date range for the shifts for a vehicle.
        
        Args:
            from_date (datetime): The start date for the date range.
            to_date (datetime): The end date for the date range.
        """
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_SHIFTS_FOR_VEHICLE)))
        from_date_field = self.browser.find_element(By.ID, self.Structure.ID_FROM_DATE)
        from_date_field.clear()
        from_date_field.send_keys(from_date.strftime(self.Constants.MONTH_FIRST_DATE_FORMAT))
        to_date_field = self.browser.find_element(By.ID, self.Structure.ID_TO_DATE)
        to_date_field.clear()
        to_date_field.send_keys(to_date.strftime(self.Constants.MONTH_FIRST_DATE_FORMAT))
        go_button = self.browser.find_element(By.XPATH, self.Structure.XPATH_GO_BUTTON)
        go_button.click()

        #Wait for filtered list to load and click on shift
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_SHIFTS_FOR_VEHICLE)))

    def use_nav_menu(self, link_text: str) -> None:
        """
        Use the navigation menu to select a link.
        
        Args:
            link_text (str): The text of the link to select.
        """
        # Go to Vehicle for operator page
        jobs_link = self.browser.find_element(By.LINK_TEXT, link_text)
        jobs_link.click()

    def get_driver_list(self) -> List[Driver]:
        """
        Get a list of drivers from the website.
        
        Returns:
            list[Driver]: A list of drivers from the website.
        """
        self.use_nav_menu(link_text=self.Structure.LINK_TEXT_DRIVERS_FOR_OPERATOR)
        self.select_operator()

        driver_list = []

        table_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_DRIVER_ROW)
        for i in range(0, len(table_rows)):
            table_rows[i].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
            
            driver_list.append(Driver.get(self))
            
            
        return driver_list

    def get_taxi_list(self) -> List[Taxi]:
        """
        Get a list of vehicles from the website.
        
        Returns:
            list[Taxi]: A list of vehicles from the website.
        """
        self.use_nav_menu(link_text=self.Structure.LINK_TEXT_VEHICLES_FOR_OPERATOR)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_MY_FORM)))
        self.select_operator()
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_VEHICLES_LIST)))
        vehicle_list: List[Taxi] = []

        soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
        car_table = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_VEHICLES_LIST})

        for row in car_table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER]:

            vehicle_list.append(Taxi.get(row))

        return vehicle_list

    def nav_vehicle_shifts(self, taxi_number: str) -> None:
        '''
        Navigate to the shifts for a vehicle page.
        
        Args:
            taxi_number (str): The taxi number to search for.
        '''
        # Iterate over each shift and extract job data
        self.use_nav_menu(link_text=self.Structure.LINK_TEXT_VEHICLES_FOR_OPERATOR)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_MY_FORM)))
        self.select_operator()
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_OPERATOR)))
        
        try:
            car_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_VEHICLE_ROW)

            for i in range(0, len(car_rows)):
                if car_rows[i].text.startswith(taxi_number):
                    car_rows[i].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
                    break
                

        except NoSuchElementException:
            raise f'No vehicle found with number {taxi_number}'

    def get_shift_list(self, taxi_number: str, from_date: date, to_date: date) -> List[Shift]:
        """
        Get a list of shifts from the website.
        
        Args:
            from_date (str): The start date for the date range.
            to_date (str): The end date for the date range.
            
        Returns:
            list[Shift]: A list of shifts from the website.
        """
        shift_list: List[Shift] = []
        try:
            self.nav_vehicle_shifts(taxi_number)    
            WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_SHIFTS_FOR_VEHICLE)))
            self.shifts_for_vehicle_set_date_range(from_date, to_date)
            
            soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
            shifts_table = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_SHIFTS_FOR_VEHICLE})

            for row in shifts_table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:  # Skip header  & Footer row
                shift_list.append(Shift.get(row))

            return shift_list
        except NoSuchElementException:
            return None

    def get_job_list(self, taxi_number: str, from_date: date, to_date: date) -> List[Job]:
        """
        Get a list of jobs from the website.
        
        Args:

            taxi_number (str): The taxi number to search for.
            from_date (str): The start date for the date range.
            to_date (str): The end date for the date range.
            
        Returns:
            list[Job]: A list of jobs from the website.
        """
        self.nav_vehicle_shifts(taxi_number)    
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_SHIFTS_FOR_VEHICLE)))
        self.shifts_for_vehicle_set_date_range(from_date, to_date)
        # Iterate over each shift and extract job data
        jobs_data = []
        shift_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_SHIFT_ROW)
    
        for i in range(0, len(shift_rows)):
            # Click on the browser ID link for each shift
            self.car_number: str = shift_rows[i].text.split(" ")[0]
            self.shift_logon = datetime.strptime(f'{shift_rows[i].text.split(" ")[5]} {shift_rows[i].text.split(" ")[6]}', self.Constants.DEFAULT_DATE_TIME_FORMAT)
            shift_rows[i].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
            
                        
            # Wait for job list to load
            WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_JOBS_FOR_SHIFT)))

            job_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_JOBS_FOR_SHIFT)

            for j in range(0, len(job_rows)):

                job_rows[j].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
                WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_MY_FORM)))
                
                jobs_data.append(Job.get(self))

                self.browser.back()
                WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_JOBS_FOR_SHIFT)))
                job_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_JOBS_FOR_SHIFT)

            # Go back to the shift list page to process the next shift
            self.browser.back()
            WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_SHIFTS_FOR_VEHICLE)))
            shift_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_SHIFT_ROW)
        return jobs_data

    def find_driver(self, driver_number: int) -> Driver | None:
        """
        Get a list of drivers from the website.
        
        Args:
            driver_number (int): The driver number to search for.

        Returns:
            list[Driver]: A list of drivers from the website.
        """
        self.use_nav_menu(link_text=self.Structure.LINK_TEXT_DRIVERS_FOR_OPERATOR)
        self.select_operator()
        try:
            self.browser.find_element(By.LINK_TEXT, str(driver_number)).click()

            return Driver.get(self)
        except NoSuchElementException:
            return None
        
    def find_taxi(self, taxi_number: str) -> Taxi | None:
        """
        Get a list of drivers from the website.
        
        Args:
            taxi_number (str): The taxi number to search for.

        Returns:
            list[Driver]: A list of drivers from the website.
        """
        self.use_nav_menu(link_text=self.Structure.LINK_TEXT_VEHICLES_FOR_OPERATOR)
        self.select_operator()
        try:

            soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
            car_table = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_VEHICLES_LIST})

            for row in car_table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER]:
                if row.text.startswith(taxi_number):
                    return Taxi.get(row)

        except NoSuchElementException:
            return None

    def find_shift(self, logon: datetime, taxi_number: str) -> Shift | None:
        '''
        Find a shift for a vehicle on a specific date.
        
        Args:
            logon (datetime): The logon date to search for.
            taxi_number (str): The taxi number to search for.
            
        Returns:
            Shift: The shift for the vehicle on the date.
        '''
        self.nav_vehicle_shifts(taxi_number)
        self.shifts_for_vehicle_set_date_range(logon.date(), logon.date())

        try:
            soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
            shift_table = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_SHIFTS_FOR_VEHICLE})
            for row in shift_table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER]:
                if logon.strftime(self.Constants.DEFAULT_DATE_TIME_FORMAT) in row.text:
                    return Shift.get(row)
            

        except NoSuchElementException:
            return None

    def find_job(self, booking_number: int) -> Job | None:
        '''
        Find a job by booking number.
        
        Args:
            booking_number (int): The booking number to search for.
            
        Returns:
            Job: The job for the booking number.
        '''
        try:
            self.use_nav_menu(self.Structure.LINK_TEXT_BOOKING_LOOKUP)
            WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_BOOKING_NUMBER)))
            self.select_operator()
            booking_number_field = self.browser.find_element(By.ID, self.Structure.ID_BOOKING_NUMBER)
            booking_number_field.send_keys(booking_number)
            self.browser.find_element(By.XPATH, self.Structure.XPATH_SEARCH_BUTTON).click()
            WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_MY_FORM)))

            return Job.get(self)
        except NoSuchElementException:
            return None

    def get_group_statements(self) -> List[GroupStatement]:
        '''
        Get a list of group statements from the website.
        
        Returns:
            list[GroupStatement]: A list of group statements from the website.
        '''
        self.use_nav_menu(self.Structure.LINK_TEXT_GROUP_DOCKETS_LODGED)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_GROUP_DOCKETS_LODGED_TABLE)))
        group_statements: List[GroupStatement] = []

        soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
        group_table = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_GROUP_DOCKETS_LODGED_TABLE})

        for row in group_table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:  # Skip header  & Footer row
            group_statements.append(GroupStatement.get(row))

        return group_statements

    def find_group_statement(self, statement_date: date) -> GroupStatement | None:
        '''
        Find a group statement by date.
        
        Args:
            statement_date (date): The date of the statement to search for.
            
        Returns:
            GroupStatement: The group statement for the date.
        '''
        transactions: List[GroupStatement.Transaction] = []
        self.use_nav_menu(self.Structure.LINK_TEXT_GROUP_DOCKETS_LODGED)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_GROUP_DOCKETS_LODGED_TABLE)))

        try:

            statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_GROUP_DOCKETS_LIST)
        
            for i in range(0, len(statement_rows)):

                if statement_date.strftime(self.Constants.DEFAULT_DATE_FORMAT) in statement_rows[i].text:
                    statement_rows[i].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DOCKETS_LODGED_LIST)))

                    soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
                    groups_lodged = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_DOCKETS_LODGED_LIST})

                    for row in groups_lodged.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:

                        transactions.append(GroupStatement.Transaction.get(row))
                    self.browser.back()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_GROUP_DOCKETS_LODGED_TABLE)))
                    statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_GROUP_DOCKETS_LIST)

            return transactions
        
        except NoSuchElementException:
            return None                                                                        

    def get_voucher_statements(self) -> List[VoucherStatement] | None:
        '''
        Get a list of voucher statements from the website.
        
        Returns:
            list[VoucherStatement]: A list of voucher statements from the website.
        '''
        self.use_nav_menu(self.Structure.LINK_TEXT_DOCKETS_LODGED)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DOCKETS_LODGED_TABLE)))
        voucher_statements: List[VoucherStatement] = []

        soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
        voucher_table = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_DOCKETS_LODGED_TABLE})

        for row in voucher_table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:  # Skip header  & Footer row
            voucher_statements.append(VoucherStatement.get(row))

        return voucher_statements

    def find_voucher_statement(self, statement_date: date) -> List[VoucherStatement.Transaction] | None:
        '''
        Find a voucher statement by date.
        
        Args:
            statement_date (date): The date of the statement to search for.
            
        Returns:
            VoucherStatement: The voucher statement for the date.
        '''
        transactions: List[GroupStatement.Transaction] = []
        self.use_nav_menu(self.Structure.LINK_TEXT_DOCKETS_LODGED)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DOCKETS_LODGED_TABLE)))

        try:

            statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_DOCKETS_LODGED_LIST)
        
            for i in range(0, len(statement_rows)):

                if statement_date.strftime(self.Constants.DEFAULT_DATE_FORMAT) in statement_rows[i].text:
                    statement_rows[i].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DOCKETS_LODGED_LIST)))

                    soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
                    groups_lodged = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_DOCKETS_LODGED_LIST})

                    for row in groups_lodged.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:

                        transactions.append(VoucherStatement.Transaction.get(row))
                    self.browser.back()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DOCKETS_LODGED_TABLE)))
                    statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_DOCKETS_LODGED_LIST)

            return transactions
        
        except NoSuchElementException:
            return None    

    def get_electronic_job_statements(self) -> List[ElectronicJobStatement] | None:
        '''
        Get a list of electronic job statements from the website.
        
        Returns:
            list[ElectronicJobStatement]: A list of electronic job statements from the website.
        '''

        self.use_nav_menu(self.Structure.LINK_TEXT_ELECTRONIC_JOBS)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_ELECTRONIC_JOBS)))
        statements: List[VoucherStatement] = []

        soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
        table = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_ELECTRONIC_JOBS})

        for row in table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:  # Skip header  & Footer row
            statements.append(ElectronicJobStatement.get(row))

        return statements

    def find_electronic_job_statement(self, statement_date: date) -> List[ElectronicJobStatement.Transaction] | None:
        '''
        Find an electronic job statement by date.
        
        Args:
            statement_date (date): The date of the statement to search for.
            
        Returns:
            ElectronicJobStatement: The electronic job statement for the date.
        '''
        transactions: List[GroupStatement.Transaction] = []
        self.use_nav_menu(self.Structure.LINK_TEXT_ELECTRONIC_JOBS)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_ELECTRONIC_JOBS)))

        try:

            statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_ELECTRONIC_JOB_ROW)
        
            for i in range(0, len(statement_rows)):

                if statement_date.strftime(self.Constants.DEFAULT_DATE_FORMAT) in statement_rows[i].text:
                    statement_rows[i].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_ELECTRONIC_JOBS_LIST)))

                    soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
                    groups_lodged = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_ELECTRONIC_JOBS_LIST})

                    for row in groups_lodged.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:

                        transactions.append(ElectronicJobStatement.Transaction.get(row))
                    self.browser.back()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_ELECTRONIC_JOBS)))
                    statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_ELECTRONIC_JOB_ROW)

            return transactions
        
        except NoSuchElementException:
            return None    

    def get_docket_statements(self) -> List[DocketStatement] | None:
        '''
        Get a list of docket statements from the website.
        
        Returns:
            list[DocketStatement]: A list of docket statements from the website.
        '''
        self.use_nav_menu(self.Structure.LINK_TEXT_DOCKET_STATEMENTS)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_MY_FORM)))
        statements: List[VoucherStatement] = []

        soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
        table = soup.find(self.Constants.TAG_TABLE)

        for row in table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:  # Skip header  & Footer row
            statements.append(DocketStatement.get(row))

        return statements

    def find_docket_statement(self, statement_date: date, statement_type: DocketStatement.Type) -> List[DocketStatement.Transaction] | None:
        '''
        Find a docket statement by date.
        
        Args:
            statement_date (date): The date of the statement to search for.
            statement_type (DocketStatement.Type): The type of statement to search for.
            
        Returns:
            DocketStatement: The docket statement for the date.
        '''
        transactions: List[GroupStatement.Transaction] = []
        self.use_nav_menu(self.Structure.LINK_TEXT_DOCKET_STATEMENTS)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_MY_FORM)))

        try:

            statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_TABLE_ROW)
        
            for i in range(0, len(statement_rows)):

                if statement_date.strftime(self.Constants.DEFAULT_DATE_FORMAT) in statement_rows[i].text and statement_type.value in statement_rows[i].text:
                    statement_rows[i].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DRIVER_DETAILS)))

                    soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
                    groups_lodged = soup.find(self.Constants.TAG_TABLE)

                    for row in groups_lodged.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:

                        transactions.append(DocketStatement.Transaction.get(row))
                    self.browser.back()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DRIVER_DETAILS)))
                    statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_TABLE_ROW)

            return transactions
        
        except NoSuchElementException:
            return None    

    def get_eft_statements(self) -> List[EftStatement] | None:
        '''
        Get a list of eft statements from the website.
        
        Returns:
            list[EftStatement]: A list of eft statements from the website.
        '''

        self.use_nav_menu(self.Structure.LINK_TEXT_EFTPOS_STATEMENTS)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_MY_FORM)))
        statements: List[VoucherStatement] = []

        soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
        table = soup.find(self.Constants.TAG_TABLE)

        for row in table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:  # Skip header  & Footer row
            statements.append(EftStatement.get(row))

        return statements

    def find_eft_statement(self, statement_date: date, reference: int) -> List[EftStatement.Transaction] | None:
        '''
        Find an eft statement by date.
        
        Args:
            statement_date (date): The date of the statement to search for.
            reference (int): The reference number to search for.
            
        Returns:
            EftStatement: The eft statement for the date.
        '''
        transactions: List[GroupStatement.Transaction] = []
        self.use_nav_menu(self.Structure.LINK_TEXT_EFTPOS_STATEMENTS)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_MY_FORM)))

        try:

            statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_TABLE_ROW)
        
            for i in range(0, len(statement_rows)):

                if statement_date.strftime(self.Constants.DEFAULT_DATE_FORMAT) in statement_rows[i].text and str(reference) in statement_rows[i].text:
                    statement_rows[i].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DRIVER_DETAILS)))

                    temp_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_TABLE_ROW)
                    temp_rows[0].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DRIVER_DETAILS)))
                    day_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_TABLE_ROW)
                    for i in range(0, len(day_rows)):
                        day_rows[i].find_element(By.TAG_NAME, self.Constants.TAG_ANCHOR).click()
                        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DRIVER_DETAILS)))

                        soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
                        groups_lodged = soup.find(self.Constants.TAG_TABLE)

                        for row in groups_lodged.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER_FOOTER]:

                            transactions.append(EftStatement.Transaction.get(row))
                        self.browser.back()
                        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DRIVER_DETAILS)))
                        day_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_TABLE_ROW)
                    self.browser.back()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DRIVER_DETAILS)))
                    self.browser.back()
                    WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DRIVER_DETAILS)))
                    statement_rows = self.browser.find_elements(By.XPATH, self.Structure.XPATH_TABLE_ROW)

            return transactions
        
        except NoSuchElementException:
            return None    
    
    def get_account_balance(self) -> float:
        '''
        Get the account balance from the website.
        
        Returns:
            float: The account balance from the website.
        '''
        self.use_nav_menu(self.Structure.LINK_TEXT_MY_ACCOUNT)
        WebDriverWait(self.browser, self.Constants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DRIVER_DETAILS)))
        soup = BeautifulSoup(self.browser.page_source, self.Constants.SOUP_HTML_PARSER)
        table = soup.find(self.Constants.TAG_TABLE)
        return WebSite.Actions.string_to_float(table.find_all(self.Constants.TAG_ROW)[1].find_all(self.Constants.TAG_COLUMN)[2].text.strip())

def main() -> None:
    db_path: str = f'{getenv("HOME")}/test/bwc_data.db'
    my_id: int = 87872331
    my_taxi: str = "G6609"
    from_date: date = date(2024, 9, 1)
    to_date: date = date(2024, 9, 19)
    logon: datetime = datetime(2024, 9, 2, 7, 16)
    job_number: int = 9275252

    try:
        database: DataBase = DataBase(db_path)
        site = WebSite(WebSite.Structure.WEB_UI_URL)
    
        site.login(WebSite.Structure.WEB_UI_USERNAME, WebSite.Structure.WEB_UI_PASSWORD)
        site.close_last_login_window()

        drivers: List[Driver] = site.get_driver_list()
        me: Driver = site.find_driver(my_id)
        cars: List[Taxi] = site.get_taxi_list()
        my_car: Taxi = site.find_taxi(my_taxi)
        shifts: List[Shift] = site.get_shift_list(my_taxi, from_date, to_date)
        my_shift: Shift = site.find_shift(logon, my_taxi)
        job_list: List[Job] = site.get_job_list(my_taxi, from_date, to_date)
        my_job: Job = site.find_job(job_number)
        group_statements: List[GroupStatement] = site.get_group_statements()
        group_transactions: List[GroupStatement.Transaction] = site.find_group_statement(group_statements[0].statement_date)

        voucher_statements: List[VoucherStatement] = site.get_voucher_statements()
        voucher_transactions: List[VoucherStatement.Transaction] = site.find_voucher_statement(voucher_statements[0].statement_date)

        electronic_job_statements: List[ElectronicJobStatement] = site.get_electronic_job_statements()
        electronic_job_transactions: List[ElectronicJobStatement.Transaction] = site.find_electronic_job_statement(electronic_job_statements[0].statement_date)

        docket_statements: List[DocketStatement] = site.get_docket_statements()
        docket_transactions: List[DocketStatement.Transaction] = site.find_docket_statement(docket_statements[0].statement_date, DocketStatement.Type.from_string(docket_statements[0].statement_type))

        eft_statements: List[EftStatement] = site.get_eft_statements()
        eft_transactions: List[EftStatement.Transaction] = site.find_eft_statement(eft_statements[0].statement_date, eft_statements[0].reference)

        balance: float = site.get_account_balance()

    finally :
        site.browser.quit()
        database.connection.close()


    print(site)





if __name__ == "__main__":
    main()