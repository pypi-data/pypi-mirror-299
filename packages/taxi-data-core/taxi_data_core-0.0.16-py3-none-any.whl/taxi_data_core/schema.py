from enum import Enum
from typing import Final as Constant, Self, TypeVar, Type, Generator, Optional, Tuple, Dict, List, Any
from platform import system
from shutil import which
from re import match, findall, IGNORECASE
from datetime import datetime, timedelta, date, time
from abc import ABC, abstractmethod
from pydantic.networks import HttpUrl
from pydantic.types import FilePath
from sqlite3 import Error, connect, Cursor
from pydantic import BaseModel

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource, HttpError

from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.edge.service import Service as EdgeService

WebSite = TypeVar("WebSite", bound="WebSite")
DataBase = TypeVar("DataBase", bound="DataBase")
TrackerEvent = TypeVar("TrackerEvent", bound="TrackerEvent")
TrackerEvent.Type = TypeVar("TrackerEvent.Type", bound="TrackerEvent.Type")
SheetsApp = TypeVar("SheetsApp", bound="SheetsApp")
#Driver = TypeVar("Driver", bound="Driver")
#Taxi = TypeVar("Taxi", bound="Taxi")
#Shift = TypeVar("Shift", bound="Shift")
#Job = TypeVar("Job", bound="Job")
#Statement = TypeVar("Statement", bound="Statement")

class Common(ABC):
    """
    A collection of common methods and constants used throughout the Taxi Data Core package.
    """
    class Constants:
        """
        A collection of common constants used throughout the Taxi Data Core package.
        """
        TAG_ANCHOR: Constant[str] = 'a'
        TAG_HREF: Constant[str] = 'href'
        TAG_TABLE: Constant[str] = 'table'
        TAG_ROW: Constant[str] = 'tr'
        TAG_COLUMN: Constant[str] = 'td'
        TAG_ID: Constant[str] = 'id'
        TAG_DIV: Constant[str] = 'div'

        DEFAULT_DATE_FORMAT: Constant[str] = "%d/%m/%Y"
        MONTH_FIRST_DATE_FORMAT: Constant[str] = "%m/%d/%Y"
        DEFAULT_DATE_TIME_FORMAT: Constant[str] = "%d/%m/%Y %H:%M"
        DEFAULT_TIME_FORMAT: Constant[str] = "%H:%M"

        SLICE_REMOVE_HEADER: slice = slice(1, None)
        SLICE_REMOVE_HEADER_FOOTER: slice = slice(1, -1)
        SLICE_REMOVE_FOOTER: slice = slice(None, -1)

        SOUP_HTML_PARSER: Constant[str] = 'html.parser'

        SHORT_TIMEOUT: Constant[int] = 10
        DEFAULT_TIMEOUT: Constant[int] = 30
        LONG_TIMEOUT: Constant[int] = 600
        JUST_FUCKING_WAIT_TIMEOUT: Constant[int] = 6000
        LOOP_LIMIT: Constant[int] = 3

        TIME_WITH_SECONDS: Constant[str] = '%H:%M:%S'
        REVERSE_DATE_FORMAT: Constant[str] = '%Y-%m-%d'

        def __str__(self) -> str:
            self.__class__.__name__

        def __repr__(self) -> str:
            self.__class__.__name__

    class Actions(BaseModel):

        """
        A collection of common actions used throughout the Taxi Data Core package.
        
        Methods:
            date_range_generator(start_date: str, finish_date: str, date_format: str = CommonConstants.DEFAULT_DATE_FORMAT) -> Generator[date, None, None]: Generate a list of dates from start_date to finish_date.
            safe_extract(func, *args, **kwargs): Safely extract a value from a function.
            convert_duration_to_seconds(time_str) -> int: Convert a string like 1 min 30 sec or 1:30 to integer in seconds

        Deprecated Methods:
            timestamp_from_string(string: str) -> time: Replace with datetime.strptime" **
            string_to_float(string: str) -> float: Convert a string to a float value. Replace with float() system function.
            duration_to_seconds(duration: str) -> int: Convert a duration string to seconds. replace with CommonActions.convert_duration_to_seconds
            convert_to_seconds(time_str: str) -> int: Convert a time string to seconds. Replace with CommonActions.convert_duration_to_seconds
        """
        @staticmethod
        def string_to_float(string: str) -> float:
            """
            Convert a string to a float value.
            
            Args:
                string (str): The string to convert.
                
            Returns:
                float: The converted float value.
            """
            # Regular expression to validate the string as a valid dollar amount
            pattern = r'^\$?-?\d{1,3}(,\d{3})*(\.\d{2})?$'

            # Check if the string matches the dollar amount pattern
            if not match(pattern, string):
                raise ValueError("Invalid string. Converstion to float must be a Currency value")
            # Create a translation table that maps '$' and ',' to None
            translation_table = str.maketrans('', '', '$,')

            # Apply the translation table to remove unwanted characters
            cleaned_string = string.translate(translation_table)

            # Convert the cleaned string to a float
            converted_float = float(cleaned_string)

            return converted_float
        
        @staticmethod
        def date_range_generator(start_date: date, finish_date: date) -> Generator[date, None, None]:
            """
            Generates a list of dates from start_date to finish_date using the typing.Generator type hint.

            Args:
                start_date (str): The start date in the format `date_format`.
                finish_date (str): The end date in the format `date_format`.
                date_format (str): The format of the date strings. Default is Common.Constants.DEFAULT_DATE_FORMAT.

            Yields:
                datetime.date: Each date from start_date to finish_date.
            """
            # Generate dates from start to finish
            current_date = start_date.date()
            while current_date <= finish_date.date():
                yield current_date
                current_date += timedelta(days=1)

        @staticmethod
        def safe_extract(func, *args, **kwargs):
            """
            Safely extract a value from a function.
            
            Args:
                func: The function to call.
                *args: The positional arguments to pass to the function.
                **kwargs: The keyword arguments to pass to the function.
            """
            try:
                return func(*args, **kwargs)
            except (IndexError, ValueError):
                return None

        @staticmethod
        def convert_duration_to_seconds(time_str: str) -> int:
            """
            Convert a time string in the format "HH:MM" or patterns like "X Hour Y Minute" to seconds.
            
            Args:
                time_str (str): The time string to convert.
                
            Returns:
                int: The converted time in seconds.
            """
            # Check if the input is in "HH:MM" format
            if match(r'^\d{1,2}:\d{2}$', time_str):
                # Split into hours and minutes
                hours, minutes = map(int, time_str.split(":"))
                return int(timedelta(hours=hours, minutes=minutes).total_seconds())

            # Check for patterns like "X Hour Y Minute" (case-insensitive)
            matches = findall(r'(\d+)\s*(Hour|Minute)', time_str, IGNORECASE)
            
            if matches:
                # Initialize hours and minutes
                hours = minutes = 0
                
                # Process each match and accumulate time
                for value, unit in matches:
                    value = int(value)
                    if unit.lower() == 'hour':
                        hours += value
                    elif unit.lower() == 'minute':
                        minutes += value
                
                # Convert to seconds using timedelta
                return int(timedelta(hours=hours, minutes=minutes).total_seconds())
            
            # If neither pattern matched, raise an error
            raise ValueError("Input string format is not supported.")

        @staticmethod
        def url_from_cell(cell: Tag, url_prefix: str) -> Tuple[HttpUrl, str]:
            """
            Extract both URL and text from the hyperlink in the given table cell.

            Args:
                cell (Tag): A BeautifulSoup Tag object representing a <td> element.

            Returns:
                Tuple[str, str]: A tuple containing the extracted URL and text.
            """
            link_tag = cell.find(Common.Constants.TAG_ANCHOR)  # Find the <a> tag within the column
            if link_tag:  # Ensure the <a> tag is found
                link_url = f"{url_prefix}{link_tag[Common.Constants.TAG_HREF]}"  # Extract the href attribute for the URL
                link_text = link_tag.text.strip()  # Extract the displayed text
            else:
                link_url = f"{url_prefix}"
                link_text = cell.text.strip()
            
            return link_url, link_text

class Driver(ABC):
    '''
    Abstract class for Driver objects.
    
    Attributes:
        number (int): The driver's number.
        name (str): The driver's full name.
        prefered_name (str): The driver's preferred name.
        address (str): The driver's address.
        suburb (str): The driver's suburb.
        post_code (int): The driver's post code.
        dob (date): The driver's date of birth.
        mobile (str): The driver's mobile number.
        city (str): The driver's city.
        da_expiry (date): The driver's DA expiry date.
        license_expiry (date): The driver's license expiry date.
        conditions (str): The driver's conditions.
        create_date (datetime): The driver's creation date.
        first_logon (datetime): The driver's first logon date.
        last_logon (datetime): The driver's last logon date.
        first_operator_logon (datetime): The driver's first operator logon date.
        logons_for_operator (int): The number of logons for the operator.
        hours_for_operator (int): The number of hours for the operator.
    '''
    def __init__(self, number: int, name: str, prefered_name: str, address: str, suburb: str, post_code: int, 
                 dob: date, mobile: str, city: str, da_expiry: date, license_expiry: date, conditions: str, 
                create_date: datetime, first_logon: datetime, last_logon: datetime, first_operator_logon: datetime, 
                logons_for_operator: int, hours_for_operator: int, auth_wheelchair: bool, auth_bc: bool, auth_redcliffe: bool, auth_london: bool,
                auth_mandurah: bool, refer_fleet_ops: bool, validation_active: date, validation_until: date, validation_reason: str, active_in_mti: bool) -> None:
        self.number = number
        self.name = name
        self.prefered_name = prefered_name
        self.address = address
        self.suburb = suburb
        self.post_code = post_code
        self.dob = dob
        self.mobile = mobile
        self.city = city
        self.da_expiry = da_expiry
        self.license_expiry = license_expiry
        self.conditions = conditions
        self.create_date = create_date
        self.first_logon = first_logon
        self.last_logon = last_logon
        self.first_operator_logon = first_operator_logon
        self.logons_for_operator = logons_for_operator
        self.hours_for_operator = hours_for_operator
        self.auth_wheelchair = auth_wheelchair
        self.auth_bc = auth_bc
        self.auth_redcliffe = auth_redcliffe
        self.auth_london = auth_london
        self.auth_mandurah = auth_mandurah
        self.refer_fleet_ops = refer_fleet_ops
        self.validation_active = validation_active
        self.validation_until = validation_until
        self.validation_reason = validation_reason
        self.active_in_mti = active_in_mti

    def __str__(self) -> str:
        return f'{self.number} - {self.name}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.number}, {self.name})'

    @abstractmethod
    def get():
        '''
        Abstract method to get the driver object.
        '''
        ...

class Taxi(ABC):
    '''
    Abstract class for Taxi objects.
    
    Attributes:
    
        fleet_number (str): The taxi's fleet number.
        rego (str): The taxi's registration number.
        rego_expiry (date): The taxi's registration expiry date.
        coi_expiry (date): The taxi's COI expiry date.
        make (str): The taxi's make.
        model (str): The taxi's model.
        build_date (str): The taxi's build date.
        capacity (int): The taxi's capacity.
        primary_fleet (str): The taxi's primary fleet.
        fleets (str): The taxi's fleets.
        conditions (str): The taxi's conditions.
    '''
    def __init__(self, fleet_number: str, rego: str, rego_expiry: date, coi_expiry: date, make: str, model: str, build_date: str, 
                 capacity: int, primary_fleet: str, fleets: str, conditions: str, validation: str, until: str, reason: str) -> None:
        self.fleet_number = fleet_number
        self.rego = rego
        self.rego_expiry = rego_expiry
        self.coi_expiry = coi_expiry
        self.make = make
        self.model = model
        self.build_date = build_date
        self.capacity = capacity
        self.primary_fleet = primary_fleet
        self.fleets = fleets
        self.conditions = conditions
        self.validation = validation
        self.until = until
        self.reason = reason

    def __str__(self) -> str:
        return f'{self.fleet_number} - {self.rego}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.fleet_number}, {self.rego})'
    
    @abstractmethod
    def get():
        '''
        Abstract method to get the taxi object.
        '''
        ...

    def update_expiry_dates(self) -> None:
        raise NotImplementedError("update_expiry_dates method not implemented")
    #Update the dates via website scrape of TMR site

class Shift(ABC):
    '''
    Abstract class for Shift objects.
    
    Attributes:
        taxi (Taxi | int): The taxi object or taxi number.
        driver (Driver | int): The driver object or driver number.
        name (str): The shift name.
        log_on (datetime): The shift log on time.
        log_off (datetime): The shift log off time.
        duration (int): The shift duration.
        distance (int): The shift distance.
        offered (int): The number of jobs offered.
        accepted (int): The number of jobs accepted.
        rejected (int): The number of jobs rejected.
        recalled (int): The number of jobs recalled.
        completed (int): The number of jobs completed.
        total_fares (float): The total fares.
        total_tolls (float): The total tolls.
        '''
    def __init__(self, taxi: Taxi | int, driver: Driver | int, name: str, log_on: datetime, log_off: datetime,
                 duration: int, distance: int, offered: int, accepted: int, rejected: int, recalled: int,
                 completed: int, total_fares: float , total_tolls: float) -> None:
        self.taxi = taxi
        self.driver = driver
        self.name = name
        self.log_on = log_on
        self.log_off = log_off
        self.duration = duration
        self.distance = distance
        self.offered = offered
        self.accepted = accepted
        self.rejected = rejected
        self.recalled = recalled
        self.completed = completed
        self.total_fares = total_fares
        self.total_tolls = total_tolls

    def __str__(self) -> str:
        return f'{self.log_on}: {self.taxi} - {self.driver}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.log_on}, {self.taxi}, {self.driver})'
    
    def __append__(self, taxi: Optional[Taxi] = None, driver: Optional[Driver] = None) -> None:
        """
        Append the Taxi and Driver objects to the Shift object.
        
        Args:
            taxi (Optional[Taxi]): The Taxi object to append.
            driver (Optional[Driver]): The Driver object to append.
        """

        if isinstance(self.taxi, int) and isinstance(taxi, Taxi):
            self.taxi = taxi

        if isinstance(self.driver, int) and isinstance(driver, Driver):
            self.driver = driver

    @abstractmethod
    def get():
        '''
        Abstract method to get the shift object.
        '''
        ...

class Voucher(ABC):
    '''
    Abstract class for Voucher objects.
    
    Attributes:
        voucher_date (date): The voucher date.
        taxi (int | Taxi): The taxi object or taxi number.
        amount (float): The voucher amount.
        voucher_number (int): The voucher number.
        voucher_type (str | Type): The voucher type.
        '''
    class Type(str, Enum):
        """
        Enum list of Voucher Types for the Black and White Cabs website.

        Attributes:
            PRE_PAID = "pre-paid"
            INTERSTATE_TSS = "Interstate TSS"
            MANUAL_EFT = "manual EFT"
            MANUAL_TSS = "manual TSS"
            
        Methods:
            from_string(docket_type: str) -> Self: Convert a string to a VoucherType object.
        """
        
        PRE_PAID = "pre-paid"
        INTERSTATE_TSS = "Interstate TSS"
        MANUAL_EFT = "manual EFT"
        MANUAL_TSS = "manual TSS"

        def __str__(self) -> str:
            return self.value
        
        def __repr__(self) -> str:
            return self.__class__.__name__ + "." + self.name
        
        @staticmethod
        def from_string(docket_type: str) -> Self:
            """
            Convert a string to a VoucherType object.

            Parameters:

                docket_type: str

            Returns:
                
                    Self: The VoucherType object.
        
                """
            if isinstance(docket_type, str):
                match docket_type:
                    case "pre-paid":
                        return Voucher.Type.PRE_PAID
                    case "Interstate TSS":
                        return Voucher.Type.INTERSTATE_TSS
                    case "manual EFT":
                        return Voucher.Type.MANUAL_EFT
                    case "manual TSS":
                        return Voucher.Type.MANUAL_TSS
                    case _:
                        raise ValueError(f"Invalid voucher type {docket_type}")
            else:
                raise TypeError(f"docket_type must be a string, not {type(docket_type)}")

    def __init__(self, voucher_date: date, taxi: int | Taxi, amount: float, 
                 voucher_number: int, voucher_type: str | Type) -> None:
        self.voucher_date = voucher_date
        self.taxi = taxi
        self.amount = amount
        self.voucher_number = voucher_number
        self.voucher_type = voucher_type

    def __str__(self) -> str:
        return f'{self.voucher_date}: {self.voucher_number}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.voucher_date}, {self.voucher_number})'
    
    def __append__(self, taxi: Optional[Taxi] = None, voucher_type: Optional[Type] = None) -> None:
        """
        Append the Taxi and VoucherType objects to the Voucher object.
        
        Args:
            taxi (Optional[Taxi]): The Taxi object to append.
            voucher_type (Optional[VoucherType]): The VoucherType object to append.
        """

        if isinstance(self.taxi, int) and isinstance(taxi, Taxi):
            self.taxi = taxi

        if isinstance(self.voucher_type, str) and isinstance(voucher_type, Type):
            self.voucher_type = voucher_type

    @abstractmethod
    def get():
        '''
        Abstract method to get the voucher object.
        '''
        ...

class Docket(ABC):
    '''
    Abstract class for Docket objects.
    
    Attributes:
        docket_date (date): The docket date.
        docket_type (str | Type): The docket type.
        job_number (int): The job number.
        account_number (str): The account number.
        passenger_name (str): The passenger name.
        pickup_area (str): The pickup area.
        destination_area (str): The destination area.
        meter_total (float): The meter total.
        amount_owing (float): The amount owing.
        taxi (int | Taxi): The taxi object or taxi number.
        driver (str | Driver): The driver object or driver name.
        order_number (str): The order number.
        group_number (str): The group number.
        start_time (datetime): The start time.
        finish_time (datetime): The finish time.
        eft_surcharge (float): The EFT surcharge.
        extras (float): The extras.
        paid_by_passenger_tss (float): The amount paid by the passenger using TSS.
        '''
    class Type(str, Enum):
        """
        Enum list of Docket Types for the Black and White Cabs website.

        Attributes:
            APP_BOOKING = "App booking"
            ACCOUNT = "BWC Account"
            DVA = "DVA"
            NDIS = "NDIS"
            PRE_PAID = "Pre Paid"
            GROUPS = "Groups"
            INTERNAL = "Internal"

        Methods:
            from_string(docket_type: str) -> Self: Convert a string to a DocketType object.
        """
        APP_BOOKING  = "App booking"
        ACCOUNT = "BWC Account"
        DVA = "DVA"
        NDIS = "NDIS"
        PRE_PAID = "Pre Paid"
        GROUPS = "Groups"
        INTERNAL = "Internal"

        def __str__(self) -> str:
            return self.value
        
        def __repr__(self) -> str:
            return f'{self.__class__.__name__}.{self.name} = {self.value}'
        
        @staticmethod
        def from_string(docket_type: str) -> Self:
            """
            Convert a string to a DocketType object.

            Parameters:

                docket_type: str

            Returns:

                Self: The DocketType object.

            """
            if isinstance(docket_type, str):
                match docket_type:
                    case "App booking":
                        return Docket.Type.APP_BOOKING
                    case "BWC Account":
                        return Docket.Type.ACCOUNT
                    case "DVA":
                        return Docket.Type.DVA
                    case "NDIS":
                        return Docket.Type.NDIS
                    case "Pre Paid":
                        return Docket.Type.PRE_PAID
                    case "Groups":
                        return Docket.Type.GROUPS
                    case "Internal":
                        return Docket.Type.INTERNAL
                    case _:
                        raise ValueError(f"Invalid docket type {docket_type}")
            else:
                raise TypeError(f"docket_type must be a string, not {type(docket_type)}")
        
    def __init__(self, docket_date: date, docket_type: str | Type, job_number: int,
                 account_number: str, passenger_name: str, pickup_area: str, destination_area: str,
                 meter_total: float, amount_owing: float, taxi: int | Taxi,driver: str | Driver, 
                 order_number: Optional[str] = None, group_number: Optional[str ] = None,
                 start_time: Optional[time] = None, finish_time: Optional[time] = None, 
                 eft_surcharge: Optional[float] = None, extras: Optional[float] = None, 
                 paid_by_passenger_tss: Optional[float] = None) -> None:
        self.docket_date = docket_date
        self.docket_type = docket_type
        self.job_number = job_number
        self.account_number = account_number
        self.passenger_name = passenger_name
        self.pickup_area = pickup_area
        self.destination_area = destination_area
        self.meter_total = meter_total
        self.amount_owing = amount_owing
        self.taxi = taxi
        self.driver = driver
        self.order_number = order_number
        self.group_number = group_number
        self.start_time = start_time
        self.finish_time = finish_time
        self.eft_surcharge = eft_surcharge
        self.extras = extras
        self.paid_by_passenger_tss = paid_by_passenger_tss

    def __str__(self) -> str:
        return f'{self.docket_date}: {self.job_number}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.docket_date}, {self.job_number})'
    
    def __append__(self, taxi: Optional[Taxi] = None, 
                   driver: Optional[Driver] = None,
                   docket_type: Optional[Type] = None) -> None:
        """
        Append the Taxi and Driver objects to the Docket object.
        
        Args:
            job (Optional[Job]): The Job object to append.
            taxi (Optional[Taxi]): The Taxi object to append.
            driver (Optional[Driver]): The Driver object to append.
        """

        if isinstance(self.taxi, int) and isinstance(taxi, Taxi):
            self.taxi = taxi

        if isinstance(self.driver, str) and isinstance(driver, Driver):
            self.driver = driver

        if isinstance(self.docket_type, str) and isinstance(docket_type, Type):
            self.docket_type = docket_type

    @abstractmethod
    def get():
        '''
        Abstract method to get the docket object.
        '''
        ...

class Job(ABC):
    '''
    Abstract class for Job objects.
    
    Attributes:
        booking_number (int): The booking number.
        meter_on (time): The meter on time.
        meter_off (time): The meter off time.
        fare (float): The fare amount.
        taxi_id (Taxi | int): The taxi object or taxi number.
        '''
    def __init__(self, booking_number: int, meter_on: time,
                 meter_off: time, fare: float, taxi_id: Taxi | int) -> None:
        self.booking_number = booking_number
        self.meter_on = meter_on
        self.meter_off = meter_off
        self.fare = fare
        self.taxi_id = taxi_id

    def __str__(self) -> str:
        return str(self.booking_number)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.booking_number}, {self.taxi_id})'

    def __append__(self, docket: Optional[Docket] = None, 
                   taxi: Optional[Taxi] = None, 
                   driver: Optional[Driver] = None, 
                   shift: Optional[Shift] = None) -> None:
        """
        Append the Taxi and Driver objects to the Job object.
        
        Args:
            taxi (Optional[Taxi]): The Taxi object to append.
            driver (Optional[Driver]): The Driver object to append.
            shift (Optional[Shift]): The Shift object to append.
            docket (Docket): The Docket object to append.
        """

        if isinstance(self.taxi_id, int) and isinstance(taxi, Taxi):
            self.taxi_id = taxi

        if isinstance(self.driver_id, int) and isinstance(driver, Driver):
            self.driver_id = driver

        if isinstance(self.shift_id, int) and isinstance(shift, Shift):
            self.shift_id = shift
        
        if isinstance(self.account, str) and isinstance(docket, Docket):
            self.account = docket

    @abstractmethod
    def get():
        '''
        Abstract method to get the job object.
        '''
        ...

class Statement(ABC):
    '''
    Abstract class for Statement objects.
    
    Attributes:
        statement_date (date): The statement date.
        statement_amount (float): The statement amount.
        '''
    Transaction = TypeVar('Transaction', bound='Statement.Transaction')
    class Transaction(ABC):
        '''
        Abstract class for Transaction objects.
        
        Attributes:
            amount (float): The transaction amount.
            date (date): The transaction date.
            '''
        def __init__(self, amount: float, date: date) -> None:
            self.amount = amount
            self.date = date
        
        def __str__(self) -> str:
            return f'{self.date.strftime(Common.Constants.DEFAULT_DATE_FORMAT)} ${self.amount:,.2f}'
        
        def __repr__(self) -> str:
            return f'{self.date.strftime(Common.Constants.DEFAULT_DATE_FORMAT)} ${self.amount:,.2f}'

        @abstractmethod
        def get():
            '''
            Abstract method to get the transaction object.
            '''
            ...

    class Type(str, Enum):
        """
        Enum list of Statement Types for the Black and White Cabs website.

        Attributes:
        -----------
        ACCOUNT = "AC"
            Represents an account statement.
        DVA = "DV2"
            Represents a DVA statement.
        NDIS = "NDI"
            Represents an NDIS statement.

        Methods:
            from_string(statement_type: str) -> Self: Convert a string to a StatementType object.
        """
        ACCOUNT = "AC"
        DVA = "DV2"
        NDIS = "NDI"

        def __str__(self) -> str:
            return self.value
        
        def __repr__(self) -> str:
            return self.__class__.__name__ + "." + self.name

        def from_string(statement_type: str) -> Self:
            """
            Convert a string to a StatementType object.

            Parameters:
                statement_type: str

            Returns:
                Self: The StatementType object.
            """
            if isinstance(statement_type, str):
                match statement_type:
                    case "AC":
                        return Statement.Type.ACCOUNT
                    case "DV2":
                        return Statement.Type.DVA
                    case "NDI":
                        return Statement.Type.NDIS
                    case _:
                        raise ValueError(f"Invalid Statement Type: {statement_type}")
            else:
                raise TypeError(f"statement_type must be a string, not {type(statement_type)}")

    class Status(str, Enum):
        '''
        Enum list of Statement Status for the Black and White Cabs website.
        
        Attributes:
        
        PENDING = "Pending"
            Represents a pending statement.
        POSTED = "Posted"
            Represents a posted statement.
            '''
        PENDING  = "Pending"
        POSTED = "Posted"

        def __str__(self) -> str:
            return self.value
        
        def __repr__(self) -> str:
            return f'{self.__class__.__name__}.{self.name} = {self.value}'

        @staticmethod
        def from_string(status: str) -> Self:
            '''
            Convert a string to a StatementStatus object.
            
            Parameters:
                status: str - The status string to convert.
            '''
            if isinstance(status, str):
                match status:
                    case "Pending":
                        return Statement.Status.PENDING
                    case "Posted":
                        return Statement.Status.POSTED
                    case _:
                        raise ValueError(f"Invalid status {status}")
            else:
                raise TypeError(f"docket_type must be a string, not {type(status)}")
                
    def __init__(self, statement_date: date, statement_amount: float) -> None:
        self.statement_date = statement_date
        self.statement_amount = statement_amount
    
    def __str__(self) -> str:
        return f'{self.statement_date}: {self.statement_amount}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.statement_date}, {self.statement_amount})'
    
    @abstractmethod
    def get():
        '''
        Abstract method to get the statement object.
        '''
        ...

class WebSite(ABC):
    '''
    Abstract class for Website objects.
    
    Attributes:
    
        url (str): The website URL.
        browser (WebDriver): The WebDriver object.
        '''
    _instance = None

    def __new__(cls: Type[WebSite], *args, **kwargs):
        if cls._instance is None:
            # Call the parent's __new__ to create a new instance if none exists
            cls._instance = super(WebSite, cls).__new__(cls)
        else:
            raise Exception(f"An instance of website connection for {cls} already exists.")
        return cls._instance
    
    def __init__(self, url: HttpUrl) -> None:
        self.url = url
        self.initialize()

    def __str__(self) -> str:
        return self.url
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.url})'
    
    def initialize(self):
        """
        Initialize a WebDriver object based on the available browsers.
        
        Returns:
            WebDriver: The WebDriver object.
        """
        # Detect the operating system
        os_name = system().lower()
        
        # Initialize a list to check available browsers in priority order
        available_browsers = []

        # Check for Firefox
        if which("firefox"):
            available_browsers.append('firefox')
        
        # Check for Chrome/Chromium
        if which("chrome") or which("chromium"):
            available_browsers.append('chrome')
        
        # Check for Safari (only available on macOS)
        if os_name == "darwin" and which("safaridriver"):
            available_browsers.append('safari')
        
        # Check for Microsoft Edge (only available on Windows)
        if os_name == "windows" and which("msedge"):
            available_browsers.append('edge')

        # Initialize WebDriver in priority order: Firefox > Chrome > Safari > Edge
        if 'firefox' in available_browsers:
            self.browser =  webdriver.Firefox(service=FirefoxService())
        elif 'chrome' in available_browsers:
            self.browser =  webdriver.Chrome(service=ChromeService())
        elif 'safari' in available_browsers:
            self.browser =  webdriver.Safari(service=SafariService())
        elif 'edge' in available_browsers:
            self.browser =  webdriver.Edge(service=EdgeService())
        else:
            raise EnvironmentError("No supported browsers found on the system. Please install Firefox, Chrome, Safari, or Edge.")
        
    @abstractmethod
    def login(self) -> None:
        '''
        Abstract method to login to the website.
        '''
        ...

class DataBase(ABC):
    '''
    Abstract class for Database objects.
    
    Attributes:
    
        file_path (FilePath): The database file path.
        connection (Connection): The database connection.
        cursor (Cursor): The database cursor.
        '''
    _instance = None

    def __new__(cls: Type[DataBase], *args, **kwargs):
        if cls._instance is None:
            # Call the parent's __new__ to create a new instance if none exists
            cls._instance = super(DataBase, cls).__new__(cls)
        else:
            raise Exception(f"An instance of DB connection for {cls} already exists.")
        return cls._instance
    
    def __init__(self, file_path: FilePath) -> None:
        self.file_path = FilePath(file_path)
        if self.file_path.exists():
            self.open()
        else:
            self.open()
            self.initialize()

    def __str__(self) -> str:
        return self.file_path.name
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.file_path.name})'
    
    @abstractmethod
    def initialize(self) -> None:
        '''
        Abstract method to initialize the database.
        '''
        ...

    def open(self) -> None:
        """
        Open the database connection.
        """
        try:
            self.connection = connect(self.file_path)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"DB Connection Error: {e}")

class GpsRecord(ABC):
    '''
    Abstract class for GPS Record objects.
    
    Attributes:
    
        record_date (date): The record date.
        kml_file (FilePath): The KML file path.
        '''
    def __init__(self, record_date: date, kml_file: FilePath) -> None:
        self.record_date = record_date
        self.kml_file = kml_file
    
    def __str__(self) -> str:
        return f'{self.record_date}: {self.kml_file}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.record_date}, {self.kml_file})'

    def kml_is_valid(self) -> bool:
        """
        Checks if a KML file contains any coordinates.
        
        Args:
            kml_file_path (str): The path to the KML file to be checked.
        
        Returns:
            bool: True if coordinates are found, False otherwise.
        """
        try:
            tree = ET.parse(self.kml_file)
            root = tree.getroot()

            # KML files often use the 'http://www.opengis.net/kml/2.2' namespace
            ns = {'kml': 'http://www.opengis.net/kml/2.2'}

            # Find all 'coordinates' elements in the KML
            coordinates_elements = root.findall('.//kml:coordinates', ns)

            for coordinates in coordinates_elements:
                # Split by space to check if there are valid coordinate sets (longitude,latitude[,altitude])
                if coordinates.text and any(coord.strip() for coord in coordinates.text.strip().split()):
                    return True

            return False
        except ET.ParseError as e:
            print(f"Error parsing KML file: {e}")
            return False
        except FileNotFoundError:
            print(f"KML file not found: {self.kml_file}")
            return False

class TrackerEntry(ABC):
    '''
    Abstract class for Tracker Entry objects.
    
    Attributes:
    
        timestamp (time): The timestamp.
        distance (float): The distance.
        latitude (float): The latitude.
        longitude (float): The longitude.
        '''
    def __init__(self, timestamp: time, distance: float, latitude: float, 
                 longitude: float) -> None:
        self.timestamp = timestamp
        self.distance = distance
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return f'{self.timestamp}: {self.distance}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.timestamp}, {self.distance})'

    @abstractmethod
    def get():
        '''
        Abstract method to get the tracker entry object.
        '''
        ...



class TrackerEvent(ABC):
    '''
    Abstract class for Tracker Event objects.
    
    Attributes:
    
        event_type (Type): The event type.
        from_time (time): The from time.
        to_time (time): The to time.
        duration (int): The duration.
        '''
    def __init__(self, event_type: TrackerEvent.Type, from_time: time, to_time: time, duration: int) -> None:
        self.event_type = event_type
        self.from_time = from_time
        self.to_time = to_time
        self.duration = duration
    
    def __str__(self) -> str:
        return f"{self.event_type}: {self.from_time} to {self.to_time} ({self.duration} seconds)"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.event_type}, {self.from_time}, {self.to_time}, {self.duration})"


    class Type(str,Enum):
        """
        Enum class to represent the different types of GPS tracker events.
        
        Attributes:
            STAY: Constant[str] = "Stay": Represents the event where the vehicle is stationary.

        Methods:
            from_string(event_type: str) -> Self: Converts a string to a GpsTrackerEvent object.
            
        """
        STAY: Constant[str] = "Stay"

        def __str__(self) -> str:
            return self.value
        
        def __repr__(self) -> str:
            return self.__class__.__name__ + "." + self.name
        
        @classmethod
        def from_string(cls: Type[TrackerEvent.Type], event_type: str) -> Self:
            """
            Converts a string to a GpsTrackerEvent object.

            Args:
                event_type (str): The event type.

            Returns:
                Self: The GpsTrackerEvent object.
            """
            if isinstance(event_type, str):
                match event_type.capitalize():
                    case "Stay":
                        return cls.STAY
                    case _:
                        raise ValueError(f"Unknown event type: {event_type}")
            else:
                raise TypeError(f"Expected a string, got {type(event_type)}")

    @abstractmethod
    def get():
        '''
        Abstract method to get the tracker event object.
        '''
        ...

class SheetsApp(ABC):
    '''
    Abstract class for Google Sheets objects.
    
    Attributes:
    
        SCOPES (Tuple[HttpUrl]): The Google Sheets API scopes.
        credentials_file (FilePath): The credentials file path.
        spreadsheet_id (str): The spreadsheet ID.
        connection (Resource): The Google Sheets connection.
        sheet_name (str): The sheet name.
        '''
    _instance = None

    def __new__(cls: Type[SheetsApp], *args, **kwargs):
        if cls._instance is None:
            # Call the parent's __new__ to create a new instance if none exists
            cls._instance = super(SheetsApp, cls).__new__(cls)
        else:
            raise Exception(f"An instance of google sheets for {cls} already exists.")
        return cls._instance
    
    def __init__(self, SCOPES: Tuple[HttpUrl], credentials_file: FilePath, spreadsheet_id: str) -> None:
        self.initialize(SCOPES, credentials_file)
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name: str = None

    def __str__(self) -> str:
        return self.__class__.__name__
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'

    class TransactionStatus(str, Enum):
        """
        Enum list of Docket Statuses for the Black and White Cabs website.

        Attributes:
            COMPLETED: Constant[str] = "Completed"
            LODGED: Constant[str] = "Lodged"
            LOGGED: Constant[str] = "Logged"
            PAID: Constant[str] = "Paid"
            DISPUTED: Constant[str] = "Disputed"
            FINALISED: Constant[str] = "Finalised"
        
        Methods:
            from_string(docket_status: str) -> Self: Convert a string to a DocketStatus object.
        """

        # def __init__(self) -> None:
        #     self.COMPLETED: Constant[str] = "Completed"
        #     self.LODGED: Constant[str] = "Lodged"
        #     self.LOGGED: Constant[str] = "Logged"
        #     self.PAID: Constant[str] = "Paid"
        #     self.DISPUTED: Constant[str] = "Disputed"
        #     self.FINALISED: Constant[str] = "Finalised"

        def __str__(self) -> str:
            return self.value
        
        def __repr__(self) -> str:
            return self.__class__.__name__ + "." + self.name
        
        COMPLETED: Constant[str] = "Completed"
        LODGED: Constant[str] = "Lodged"
        LOGGED: Constant[str] = "Logged"
        PAID: Constant[str] = "Paid"
        DISPUTED: Constant[str] = "Disputed"
        FINALISED: Constant[str] = "Finalised"

        @staticmethod
        def from_string(docket_status: str) -> Self:
            """
            Convert a string to a DocketStatus object.

            Parameters:

                docket_status: str

            Returns:
                
                    Self: The DocketStatus object.
        
                """
            if isinstance(docket_status, str):
                match docket_status:
                    case "Completed":
                        return SheetsApp.TransactionStatus.COMPLETED
                    case "Lodged":
                        return SheetsApp.TransactionStatus.LODGED
                    case "Logged":
                        return SheetsApp.TransactionStatus.LOGGED
                    case "Paid":
                        return SheetsApp.TransactionStatus.PAID
                    case "Disputed":
                        return SheetsApp.TransactionStatus.DISPUTED
                    case "Finalised":
                        return SheetsApp.TransactionStatus.FINALISED
                    case _:
                        raise ValueError(f"Invalid docket status {docket_status}")
            else:
                raise TypeError(f"docket_status must be a string, not {type(docket_status)}")

    def initialize(self, SCOPES: Tuple[HttpUrl], credentials_file: FilePath) -> None:
        '''
        Initialize the Google Sheets connection.
        
        Args:
        
            SCOPES (Tuple[HttpUrl]): The Google Sheets API scopes.
            credentials_file (FilePath): The credentials file path.
            '''
        creds = None
        try:
            # Try to load existing credentials
            creds = Credentials.from_authorized_user_file(credentials_file, SCOPES)
        except (ValueError, FileNotFoundError):
            # If credentials file does not exist or is in the wrong format, create new credentials
            pass

        # If there are no valid credentials available, initiate the authorization flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh the credentials if expired
                creds.refresh(Request())
            else:
                # Run the OAuth flow to get new credentials
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

                # Save the newly authorized credentials to the credentials file
                with open(credentials_file, "w") as token:
                    token.write(creds.to_json())

        try:
            # Build the service object
            service = build("sheets", "v4", credentials=creds)
            self.connection: Resource = service.spreadsheets()
        except HttpError as err:
            print(f"An error occurred: {err}")
            self.connection = None

    def get_range(self, range: str) -> List[List[str]]:
        '''
        Get the values from a specified range in the Google Sheet.
        
        Args:
        
            range (str): The range to retrieve values from.
            
        Returns:
        
            List[List[str]]: The values from the specified range.
            '''
        result = self.connection.values().get(spreadsheetId=self.spreadsheet_id, range=range).execute()
        return result.get("values", [])
    
def main() -> None:
    doc = Docket(date(2021, 1, 1), Docket.Type.APP_BOOKING, 123456, "123456", "John Doe", "Brisbane", "Gold Coast", 100.00, 0.00, 1, 1, datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 11, 0), 0.00, 0.00, 0.00)

    print(doc.docket_type)

    for _ in Common.Actions.date_range_generator("01/01/2021", "31/01/2021"):
        print(_)

    class test(Common, WebSite):
        def __init__(self, url: HttpUrl) -> None:
            super().__init__(url)

        def login(self):
            pass


    new_test = test("https://www.google.com")

    print(new_test)


if __name__ == "__main__":
    pass
