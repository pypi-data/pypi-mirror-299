from os import getenv
from typing import Final as Constant
from typing import Self, Tuple, List, Optional, Union, TypeVar, Type
from enum import Enum
from datetime import date, datetime
from abc import ABC

from taxi_data_core import schema

from pydantic import HttpUrl, FilePath, BaseModel
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

Docket = TypeVar("Docket", bound="Docket")
SheetsApp = TypeVar("SheetsApp", bound="SheetsApp")
Voucher = TypeVar("Voucher", bound="Voucher")
CabCharge = TypeVar("CabCharge", bound="CabCharge")
DocketStatement = TypeVar("DocketStatement", bound="DocketStatement")
EftStatement = TypeVar("EftStatement", bound="EftStatement")
DocketStatement = TypeVar("DocketStatement", bound="DocketStatement")
Docket.Status = TypeVar("Docket.Status", bound="Docket.Status")
Voucher.Type = TypeVar("Voucher.Type", bound="Voucher.Type")
Voucher.Status = TypeVar("Voucher.Status", bound="Voucher.Status")
CabCharge.Status = TypeVar("CabCharge.Status", bound="CabCharge.Status")
EftStatement.Type = TypeVar("EftStatement.Type", bound="EftStatement.Type")
DocketStatement.Type = TypeVar("DocketStatement.Type", bound="DocketStatement.Type")
SheetsApp.TransactionStatus = TypeVar("SheetsApp.TransactionStatus", bound="SheetsApp.TransactionStatus")

class Docket(schema.Docket):
    '''
    A class to represent a docket.
    
    Attributes:
        docket_date (date): The date of the docket.
        docket_type (str): The type of docket.
        job_number (int): The job number of the docket.
        account_number (str): The account number of the docket.
        passenger_name (str): The name of the passenger.
        pickup_area (str): The pickup area of the docket.
        destination_area (str): The destination area of the docket.
        meter_total (float): The meter total of the docket.
        amount_owing (float): The amount owing on the docket.
        taxi (schema.Taxi | int): The taxi used for the docket.
        driver (schema.Driver | str): The driver of the docket.
        order_number (str): The order number of the docket.
        group_number (str): The group number of the docket.
        start_time (datetime): The start time of the docket.
        finish_time (datetime): The finish time of the docket.
        eft_surcharge (float): The EFT surcharge of the docket.
        extras (float): The extras of the docket.
        paid_by_passenger_tss (float): The amount paid by the passenger using TSS.
        status (Docket.Status): The status of the docket.
        lodgment_date (Optional[datetime | str]): The lodgment date of the docket.
        statement (Optional[str]): The statement of the docket.
        driver_id (Optional[int]): The driver ID of the docket.
        driver_abn (Optional[int]): The driver ABN of the docket.
        row_number (Optional[int]): The row number of the docket.
        '''

    def __init__(self, docket_date: date, docket_type: str, job_number: int, account_number: str, passenger_name: str, pickup_area: str, 
                 destination_area: str, meter_total: float, amount_owing: float, taxi: schema.Taxi | int, driver: schema.Driver | str, order_number: str,
                 group_number: str, start_time: datetime, finish_time: datetime, eft_surcharge: float, extras: float, paid_by_passenger_tss: float,
                     status: SheetsApp.TransactionStatus, lodgment_date: Optional[datetime | str] = None, statement: Optional[str] = None, driver_id: Optional[int] = None, 
                     driver_abn: Optional[int] = None, row_number: Optional[int] = None) -> None:
        super().__init__(docket_date, docket_type, job_number, account_number, passenger_name, pickup_area, destination_area, meter_total, amount_owing,
                         taxi, driver, order_number, group_number, start_time, finish_time, eft_surcharge, extras, paid_by_passenger_tss)
        self.status = status
        self.lodgment_date = lodgment_date
        self.statement = statement
        self.driver_id = driver_id
        self.driver_abn = driver_abn
        self.row_number = row_number

    def __str__(self) -> str:
        return f"{self.job_number} {self.account_number} {self.amount_owing}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.row_number}, {self.job_number}, {self.account_number}, {self.amount_owing})"

    class Structure(BaseModel):
        DATE: Constant[int] = 0
        DOCKET_TYPE: Constant[int] = 1
        JOB_NUMBER: Constant[int] = 2
        ACCOUNT_NUMBER: Constant[int] = 3
        ORDER_NUMBER: Constant[int] = 4
        GROUP_NUMBER: Constant[int] = 5
        START_TIME: Constant[int] = 6
        FINISH_TIME: Constant[int] = 7
        PASSENGER_NAME: Constant[int] = 8
        PICKUP_AREA: Constant[int] = 9
        DESTINATION_AREA: Constant[int] = 10
        METER_TOTAL: Constant[int] = 11
        EFT_SURCHARGE: Constant[int] = 12
        EXTRAS: Constant[int] = 13
        PAID_BY_PASSENGER_TSS: Constant[int] = 14
        AMOUNT_OWING: Constant[int] = 15
        CAR_NUMBER: Constant[int] = 16
        STATUS: Constant[int] = 17
        LODGEMENT_DATE: Constant[int] = 18
        STATEMENT_DATE: Constant[int] = 19
        DRIVER: Constant[int] = 20
        DA: Constant[int] = 21
        ABN: Constant[int] = 22

    def update_status(self, sheets_app: Resource, status: SheetsApp.TransactionStatus) -> None:
        """
        Change the status of the docket in Google Sheets.
        
        Args:
        - sheets_app (Resource): The Google Sheets API resource.
        - status (DocketStatus): The new status of the docket.
        """
        self.status = status
        sheet_name: str = SheetsApp.Structure.DOCKETS_RANGE.split('!')[0]
        range_name = f"{sheet_name}!{chr(64 + self.Structure.STATUS)}{self.row_number}"

        sheets_app.connection.values().update(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=range_name, 
                    valueInputOption="RAW", body={"values": [[self.status]]}).execute()

    @classmethod
    def get(cls: Type[Docket], sheets_app: Resource, job_number: int) -> Self:
        """
        Fetch a docket from Google Sheets by job number.

        Args:
            sheets_app (Resource): The Google Sheets API resource.
            job_number (int): The job number of the docket to retrieve.

        Returns:
            Docket: The docket object populated with data from Google Sheets.
        """
        # Get the data from the specified range in Google Sheets
        SheetsApp.sheet_name = SheetsApp.Structure.DOCKETS_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=SheetsApp.Structure.DOCKETS_RANGE).execute()
        values = sheet_data.get('values', [])
        
        # Create a map from job_number to row data for easy lookup
        job_number_to_row = {row[cls.Structure.JOB_NUMBER]: row for row in values if len(row) > cls.Structure.JOB_NUMBER}

        # Find the row corresponding to the provided job_number
        row = job_number_to_row.get(str(job_number))

        # Iterate over rows and find the matching job_number
        for row_index, row in enumerate(values, start=1):  # `start=1` because Google Sheets rows are 1-indexed
            if len(row) > cls.Structure.JOB_NUMBER and str(row[cls.Structure.JOB_NUMBER]) == str(job_number):
                # Extract values from the row based on the defined structure
                docket_date = datetime.strptime(row[cls.Structure.DATE], SheetsApp.Constants.DEFAULT_DATE_FORMAT).date()  # Assuming date is in 'YYYY-MM-DD' format
                docket_type = cls.Type.from_string(row[cls.Structure.DOCKET_TYPE])
                account_number = row[cls.Structure.ACCOUNT_NUMBER]
                passenger_name = row[cls.Structure.PASSENGER_NAME]
                pickup_area = row[cls.Structure.PICKUP_AREA]
                destination_area = row[cls.Structure.DESTINATION_AREA]
                meter_total = SheetsApp.Actions.string_to_float(row[cls.Structure.METER_TOTAL])
                amount_owing = SheetsApp.Actions.string_to_float(row[cls.Structure.AMOUNT_OWING])
                taxi = int(row[cls.Structure.CAR_NUMBER])  # assuming taxi is stored as an int
                driver = row[cls.Structure.DRIVER]
                order_number = row[cls.Structure.ORDER_NUMBER]
                group_number = row[cls.Structure.GROUP_NUMBER]
                start_time = datetime.strptime(row[cls.Structure.START_TIME], SheetsApp.Constants.DEFAULT_TIME_FORMAT).time()  # ISO 8601 format
                finish_time = datetime.strptime(row[cls.Structure.FINISH_TIME], SheetsApp.Constants.DEFAULT_TIME_FORMAT).time()
                eft_surcharge = SheetsApp.Actions.string_to_float(row[cls.Structure.EFT_SURCHARGE]) if row[cls.Structure.EFT_SURCHARGE] else None
                extras = SheetsApp.Actions.string_to_float(row[cls.Structure.EXTRAS]) if row[cls.Structure.EXTRAS] else None
                paid_by_passenger_tss = SheetsApp.Actions.string_to_float(row[cls.Structure.PAID_BY_PASSENGER_TSS]) if row[cls.Structure.PAID_BY_PASSENGER_TSS] else None
                status = SheetsApp.TransactionStatus.from_string(row[cls.Structure.STATUS])  # Assuming status is stored as a valid Enum value
                lodgment_date = row[cls.Structure.LODGEMENT_DATE] if row[cls.Structure.LODGEMENT_DATE] else None
                statement = row[cls.Structure.STATEMENT_DATE] if row[cls.Structure.STATEMENT_DATE] else None
                driver_id = int(row[cls.Structure.DA].replace(" ", "")) if row[cls.Structure.DA] else None
                driver_abn = int(row[cls.Structure.ABN].replace(" ", "")) if row[cls.Structure.ABN] else None
                # Use the actual row number in Google Sheets (adjusting for the header row)
                row_number = row_index + 1  # +1 if there's a header row, adjust if not

                # Return the docket object populated with the values
                return Docket(
                    docket_date=docket_date,
                    docket_type=docket_type,
                    job_number=job_number,
                    account_number=account_number,
                    passenger_name=passenger_name,
                    pickup_area=pickup_area,
                    destination_area=destination_area,
                    meter_total=meter_total,
                    amount_owing=amount_owing,
                    taxi=taxi,
                    driver=driver,
                    order_number=order_number,
                    group_number=group_number,
                    start_time=start_time,
                    finish_time=finish_time,
                    eft_surcharge=eft_surcharge,
                    extras=extras,
                    paid_by_passenger_tss=paid_by_passenger_tss,
                    status=status,
                    lodgment_date=lodgment_date,
                    statement=statement,
                    driver_id=driver_id,
                    driver_abn=driver_abn,
                    row_number=row_number
                )

        # If no matching job_number is found, raise an exception or handle accordingly
        raise ValueError(f"Docket with job_number {job_number} not found.")

    def update(self, sheets_app: Resource) -> None:
        """
        Update the docket in Google Sheets.
        
        Args:
        - sheets_app (Resource): The Google Sheets API resource.
        """
        SheetsApp.sheet_name = SheetsApp.Structure.DOCKETS_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.spreadsheet_id, range=SheetsApp.Structure.DOCKETS_RANGE).execute()
        values = sheet_data.get('values', [])
        job_number_to_row_index = {row[self.Structure.JOB_NUMBER]: index for index, row in enumerate(values)}

        if str(self.job_number) in job_number_to_row_index:
            row_index = job_number_to_row_index[str(self.job_number)]
        else:
            row_index = len(values)
        
        range_name = f"{SheetsApp.sheet_name}!A{row_index + 2}:W{row_index + 2}"
        sheets_app.connection.values().update(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=range_name, valueInputOption="RAW", 
                                    body={"values": [[self.docket_date, self.docket_type, self.job_number, self.account_number, 
                                                        self.passenger_name, self.pickup_area, self.destination_area, self.meter_total, 
                                                        self.amount_owing, self.taxi, self.status, self.driver, self.order_number, 
                                                        self.group_number, self.start_time, self.finish_time, self.eft_surcharge, self.extras, 
                                                        self.paid_by_passenger_tss, self.lodgment_date, self.statement, self.driver_id, 
                                                        self.driver_abn, self.row_number]]}).execute()
 
    @classmethod
    def bulk_update(cls: Type[Docket], sheets_app: Resource, dockets: List[Docket]) -> None:
        """
        Update multiple dockets in Google Sheets.
        
        Args:
        - sheets_app (Resource): The Google Sheets API resource.
        - dockets (List[Docket]): The list of dockets to update.
        """
        for _ in dockets:
            cls.update(sheets_app)

class Voucher(schema.Voucher):
    '''
    A class to represent a voucher.
    
    Attributes:
        voucher_date (date): The date of the voucher.
        taxi (int): The taxi used for the voucher.
        amount (float): The amount of the voucher.
        voucher_number (int): The voucher number.
        voucher_type (Voucher.Type): The type of the voucher.
        status (Voucher.Status): The status of the voucher.
        lodgment_date (Optional[datetime | str]): The lodgment date of the voucher.
        statement (Optional[str]): The statement of the voucher.
        '''
    def __init__(self, voucher_date: date, taxi: int, amount: float, voucher_number: int, voucher_type: Voucher.Type, status: SheetsApp.TransactionStatus,
                    lodgment_date: Optional[datetime | str] = None, statement: Optional[str] = None, row_number: Optional[int] = None) -> None:
        super().__init__(voucher_date, taxi, amount, voucher_number, voucher_type)
        self.status = status
        self.lodgment_date = lodgment_date
        self.statement = statement
        self.row_number = row_number

    def __str__(self) -> str:
        return f"{self.voucher_type} {self.voucher_number} ${self.amount}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.voucher_number}, {self.voucher_type}, ${self.amount})"
    
    class Structure(BaseModel):
        DATE: Constant[int] = 0
        CAR: Constant[int] = 1
        AMOUNT: Constant[int] = 2
        VOUCHER_NUMBER: Constant[int] = 3
        TYPE: Constant[int] = 4
        STATUS: Constant[int] = 5
        LODGEMENT_DATE: Constant[int] = 6
        STATEMENT_DATE: Constant[int] = 7
        DRIVER: Constant[int] = 8

    def update_status(self, sheets_app: Resource, status: SheetsApp.TransactionStatus) -> None:
        self.status = status
        sheet_name: str = SheetsApp.Structure.VOUCHERS_RANGE.split('!')[0]
        range_name = f"{sheet_name}!{chr(64 + self.Structure.STATUS)}{self.row_number}"

        sheets_app.connection.values().update(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=range_name, 
                    valueInputOption="RAW", body={"values": [[self.status]]}).execute()


    @classmethod
    def get(cls: Type[Voucher], sheets_app: Resource, voucher_number: int) -> Self:
        SheetsApp.sheet_name = SheetsApp.Structure.VOUCHERS_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=SheetsApp.Structure.VOUCHERS_RANGE).execute()
        values = sheet_data.get('values', [])
        
        # Create a map from job_number to row data for easy lookup
        voucher_number_to_row = {row[cls.Structure.VOUCHER_NUMBER]: row for row in values if len(row) > cls.Structure.VOUCHER_NUMBER}

        # Find the row corresponding to the provided job_number
        row = voucher_number_to_row.get(str(voucher_number))

        # Iterate over rows and find the matching job_number
        for row_index, row in enumerate(values, start=1):  # `start=1` because Google Sheets rows are 1-indexed
            if len(row) > cls.Structure.VOUCHER_NUMBER and str(row[cls.Structure.VOUCHER_NUMBER]) == str(voucher_number):
                # Extract values from the row based on the defined structure
                voucher_date = datetime.strptime(row[cls.Structure.DATE], SheetsApp.Constants.DEFAULT_DATE_FORMAT).date()
                taxi = int(row[cls.Structure.CAR])
                amount = SheetsApp.Actions.string_to_float(row[cls.Structure.AMOUNT])
                voucher_number = int(row[cls.Structure.VOUCHER_NUMBER])
                voucher_type = cls.Type.from_string(row[cls.Structure.TYPE])
                status = SheetsApp.TransactionStatus.from_string(row[cls.Structure.STATUS])
                lodgment_date = row[cls.Structure.LODGEMENT_DATE] if row[cls.Structure.LODGEMENT_DATE] else None
                statement = row[cls.Structure.STATEMENT_DATE] if row[cls.Structure.STATEMENT_DATE] else None
                # Use the actual row number in Google Sheets (adjusting for the header row)
                row_number = row_index + 1  # +1 if there's a header row, adjust if not

                # Return the docket object populated with the values
                return Voucher(
                    voucher_date=voucher_date,
                    taxi=taxi,
                    amount=amount,
                    voucher_number=voucher_number,
                    voucher_type=voucher_type,
                    status=status,
                    lodgment_date=lodgment_date,
                    statement=statement,
                    row_number=row_number
                )
            
    def update(self, sheets_app: Resource) -> None:
        SheetsApp.sheet_name = SheetsApp.Structure.VOUCHERS_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.spreadsheet_id, range=SheetsApp.Structure.VOUCHERS_RANGE).execute()
        values = sheet_data.get('values', [])
        voucher_number_to_row_index = {row[self.Structure.VOUCHER_NUMBER]: index for index, row in enumerate(values)}

        if str(self.voucher_number) in voucher_number_to_row_index:
            row_index = voucher_number_to_row_index[str(self.voucher_number)]
        else:
            row_index = len(values)
        
        range_name = f"{SheetsApp.sheet_name}!A{row_index + 2}:W{row_index + 2}"
        sheets_app.connection.values().update(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=range_name, valueInputOption="RAW", 
                                    body={"values": [[self.voucher_date, self.taxi, self.amount, self.voucher_number, 
                                                      self.voucher_type, self.status, self.lodgment_date, self.statement]]}).execute()

    @classmethod
    def bulk_update(cls: Type[Voucher], sheets_app: Resource, vouchers: List[Voucher]) -> None:
        for _ in vouchers:
            cls.update(sheets_app)


class CabCharge(schema.Statement.Transaction):
    '''
    A class to represent a Cabcharge.
    
    Attributes:
    
        date (date): The date of the Cabcharge.
        taxi (int): The taxi used for the Cabcharge.
        amount (float): The amount of the Cabcharge.
        reference (int): The reference number of the Cabcharge.
        status (CabCharge.Status): The status of the Cabcharge.
        statement (Optional[int]): The statement of the Cabcharge.
        '''
    def __init__(self, date: date, taxi: int, amount: float, reference: int, status: CabCharge.Status, 
                 statement: Optional[int] = None, row_number: Optional[int] = None) -> None:
        super().__init__(date, amount)
        self.statement = statement
        self.taxi = taxi
        self.reference = reference
        self.status = status
        self.row_number = row_number

    def __str__(self) -> str:
        return f"{self.reference} ${self.amount}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.reference}, ${self.amount})"

    class Structure(BaseModel):
        DATE: Constant[int] = 0
        CAR: Constant[int] = 1
        AMOUNT: Constant[int] = 2
        REFERENCE: Constant[int] = 3
        STATUS: Constant[int] = 4
        STATEMENT: Constant[int] = 5

    def update_status(self, sheets_app: Resource, status: SheetsApp.TransactionStatus) -> None:
        self.status = status
        sheet_name: str = SheetsApp.Structure.CABCHARGE_RANGE.split('!')[0]
        range_name = f"{sheet_name}!{chr(64 + self.Structure.STATUS)}{self.row_number}"

        sheets_app.connection.values().update(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=range_name, 
                    valueInputOption="RAW", body={"values": [[self.status]]}).execute()

    @classmethod
    def get(cls: Type[CabCharge], sheets_app: Resource, reference_number: int) -> Self:
        SheetsApp.sheet_name = SheetsApp.Structure.CABCHARGE_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=SheetsApp.Structure.CABCHARGE_RANGE).execute()
        values = sheet_data.get('values', [])
        
        # Create a map from job_number to row data for easy lookup
        ref_number_to_row = {row[cls.Structure.REFERENCE]: row for row in values if len(row) > cls.Structure.REFERENCE}

        # Find the row corresponding to the provided job_number
        row = ref_number_to_row.get(str(reference_number))

        # Iterate over rows and find the matching job_number
        for row_index, row in enumerate(values, start=1):  # `start=1` because Google Sheets rows are 1-indexed
            if len(row) > cls.Structure.REFERENCE and str(row[cls.Structure.REFERENCE]) == str(reference_number):
                # Extract values from the row based on the defined structure
                date = datetime.strptime(row[cls.Structure.DATE], SheetsApp.Constants.DEFAULT_DATE_FORMAT).date()
                taxi = int(row[cls.Structure.CAR])
                amount = SheetsApp.Actions.string_to_float(row[cls.Structure.AMOUNT])
                reference = int(row[cls.Structure.REFERENCE])
                status = SheetsApp.TransactionStatus.from_string(row[cls.Structure.STATUS])
                statement = int(row[cls.Structure.STATEMENT]) if row[cls.Structure.STATEMENT] else None
                # Use the actual row number in Google Sheets (adjusting for the header row)
                row_number = row_index + 1  # +1 if there's a header row, adjust if not

                # Return the docket object populated with the values
                return CabCharge(
                    date=date,
                    taxi=taxi,
                    amount=amount,
                    reference=reference,
                    status=status,
                    statement=statement,
                    row_number=row_number
                )

    
    def update(self, sheets_app: Resource) -> None:
        SheetsApp.sheet_name = SheetsApp.Structure.CABCHARGE_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.spreadsheet_id, range=SheetsApp.Structure.CABCHARGE_RANGE).execute()
        values = sheet_data.get('values', [])
        ref_number_to_row_index = {row[self.Structure.REFERENCE]: index for index, row in enumerate(values)}

        if str(self.reference) in ref_number_to_row_index:
            row_index = ref_number_to_row_index[str(self.reference)]
        else:
            row_index = len(values)
        
        range_name = f"{SheetsApp.sheet_name}!A{row_index + 2}:W{row_index + 2}"
        sheets_app.connection.values().update(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=range_name, valueInputOption="RAW", 
                                    body={"values": [[self.date, self.taxi, self.amount, self.reference, self.status, self.statement]]}).execute()

    @classmethod
    def bulk_update(cls: Type[CabCharge], sheets_app: Resource, cab_charges: List[CabCharge]) -> None:
        for _ in cab_charges:
            cls.update(sheets_app)



class EftStatement(schema.Statement):
    '''
    A class to represent an EFT statement.
    
    Attributes:
        statement (int): The statement number.
        statement_date (date): The date of the statement.
        statement_amount (float): The amount of the statement.
        amount_allocated (float): The amount allocated to the statement.
        '''
    def __init__(self, statement: int, statement_date: date, statement_amount: float, amount_allocated: float, url: HttpUrl) -> None:
        super().__init__(statement_date, statement_amount)
        self.statement = statement
        self.amount_allocated = amount_allocated
        self.url = url

    def __str__(self) -> str:
        return f"{self.statement} ${self.statement_amount}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.statement}, ${self.statement_amount})"

    class Structure(BaseModel):
        STATEMENT: Constant[int] = 0
        DATE: Constant[int] = 1
        AMOUNT: Constant[int] = 2
        ALLOCATED_AMOUNT: Constant[int] = 3
        URL: Constant[int] = 4

    @classmethod
    def get(cls: Type[EftStatement], sheets_app: Resource, batch_number: int) -> Self:
        SheetsApp.sheet_name = SheetsApp.Structure.EFT_STATEMENT_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=SheetsApp.Structure.EFT_STATEMENT_RANGE).execute()
        values = sheet_data.get('values', [])
        
        # Create a map from job_number to row data for easy lookup
        ref_number_to_row = {row[cls.Structure.STATEMENT]: row for row in values if len(row) > cls.Structure.STATEMENT}

        # Find the row corresponding to the provided job_number
        row = ref_number_to_row.get(str(batch_number))

        # Iterate over rows and find the matching job_number
        for row_index, row in enumerate(values, start=1):  # `start=1` because Google Sheets rows are 1-indexed
            if len(row) > cls.Structure.STATEMENT and str(row[cls.Structure.STATEMENT]) == str(batch_number):
                # Extract values from the row based on the defined structure
                statement = int(row[cls.Structure.STATEMENT])
                statement_date = datetime.strptime(row[cls.Structure.DATE], SheetsApp.Constants.DEFAULT_DATE_FORMAT).date()
                statement_amount = SheetsApp.Actions.string_to_float(row[cls.Structure.AMOUNT])
                amount_allocated = SheetsApp.Actions.string_to_float(row[cls.Structure.ALLOCATED_AMOUNT])
                url = row[cls.Structure.URL]
                # Use the actual row number in Google Sheets (adjusting for the header row)
                row_number = row_index + 1

                # Return the docket object populated with the values
                return EftStatement(
                    statement=statement,
                    statement_date=statement_date,
                    statement_amount=statement_amount,
                    amount_allocated=amount_allocated,
                    url=url
                )

    def update(self, sheets_app: Resource) -> None:
        SheetsApp.sheet_name = SheetsApp.Structure.EFT_STATEMENT_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.spreadsheet_id, range=SheetsApp.Structure.EFT_STATEMENT_RANGE).execute()
        values = sheet_data.get('values', [])
        ref_number_to_row_index = {row[self.Structure.DATE]: index for index, row in enumerate(values)}

        if str(self.statement) in ref_number_to_row_index:
            row_index = ref_number_to_row_index[str(self.statement)]
        else:
            row_index = len(values)
        
        range_name = f"{SheetsApp.sheet_name}!A{row_index + 2}:W{row_index + 2}"
        sheets_app.connection.values().update(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=range_name, valueInputOption="RAW", 
                                    body={"values": [[self.statement, self.statement_date,  self.statement_amount, self.amount_allocated]]}).execute()

    @classmethod
    def bulk_update(cls: Type[EftStatement], sheets_app: Resource, eft_statements: List[EftStatement]) -> None:
        for _ in eft_statements:
            cls.update(sheets_app)


class DocketStatement(schema.Statement):
    '''
    A class to represent a docket statement.
    
    Attributes:
        statement_date (date): The date of the statement.
        statement_type (DocketStatement.Type): The type of the statement.
        statement_amount (float): The amount of the statement.
        allocated_amount (float): The amount allocated to the statement.
        reference (str): The reference number of the statement.
        '''
    def __init__(self, statement_date: date, statement_type: DocketStatement.Type, statement_amount: float , allocated_amount: float, reference: str) -> None:
        super().__init__(statement_date, statement_amount)
        self.statement_type = statement_type
        self.reference = reference
        self.allocated_amount = allocated_amount

    def __str__(self) -> str:
        return f"{self.statement_type} {self.reference} ${self.statement_amount}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.statement_type} {self.reference} ${self.statement_amount})"
    
    class Structure(BaseModel):
        DATE: Constant[int] = 0
        TYPE: Constant[int] = 1
        AMOUNT: Constant[int] = 2
        ALLOCATED_AMOUNT: Constant[int] = 3
        REFERENCE: Constant[int] = 4

    @classmethod
    def get(cls: Type[DocketStatement], sheets_app: Resource, batch_date: date, batch_type: DocketStatement.Type) -> Self:
        SheetsApp.sheet_name = SheetsApp.Structure.DOCKET_STATEMENT_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=SheetsApp.Structure.DOCKET_STATEMENT_RANGE).execute()
        values = sheet_data.get('values', [])
        
        batch_string: str = f'{batch_date.strftime(SheetsApp.Constants.DEFAULT_DATE_FORMAT)} {batch_type.value}'
        # Create a map from job_number to row data for easy lookup
        ref_number_to_row = {f'{row[cls.Structure.DATE]} {row[cls.Structure.TYPE]}': row for row in values if len(row) > cls.Structure.DATE}

        # Find the row corresponding to the provided job_number
        row = ref_number_to_row.get(str(batch_string))

        # Iterate over rows and find the matching job_number
        for row_index, row in enumerate(values, start=1):  # `start=1` because Google Sheets rows are 1-indexed
            if len(row) > cls.Structure.DATE and str(f'{row[cls.Structure.DATE]} {row[cls.Structure.TYPE]}') == str(batch_string):
                date = datetime.strptime(row[cls.Structure.DATE], SheetsApp.Constants.DEFAULT_DATE_FORMAT).date()
                statement_type = cls.Type.from_string(row[cls.Structure.TYPE])
                statement_amount = SheetsApp.Actions.string_to_float(row[cls.Structure.AMOUNT])
                allocated_amount = SheetsApp.Actions.string_to_float(row[cls.Structure.ALLOCATED_AMOUNT])
                reference = row[cls.Structure.REFERENCE]
                # Use the actual row number in Google Sheets (adjusting for the header row)
                row_number = row_index + 1  # +1 if there's a header row, adjust if not

                # Return the docket object populated with the values
                return DocketStatement(
                    statement_date=date,
                    statement_type=statement_type,
                    statement_amount=statement_amount,
                    allocated_amount=allocated_amount,
                    reference=reference
                )

    def update(self, sheets_app: Resource) -> None:
        SheetsApp.sheet_name = SheetsApp.Structure.DOCKET_STATEMENT_RANGE.split('!')[0]
        sheet_data = sheets_app.connection.values().get(spreadsheetId=SheetsApp.spreadsheet_id, range=SheetsApp.Structure.DOCKET_STATEMENT_RANGE).execute()
        values = sheet_data.get('values', [])
        ref_number_to_row_index = {row[self.Structure.REFERENCE]: index for index, row in enumerate(values)}

        if str(self.statement) in ref_number_to_row_index:
            row_index = ref_number_to_row_index[str(self.statement)]
        else:
            row_index = len(values)
        
        range_name = f"{SheetsApp.sheet_name}!A{row_index + 2}:W{row_index + 2}"
        sheets_app.connection.values().update(spreadsheetId=SheetsApp.Structure.SPREADSHEET_ID, range=range_name, valueInputOption="RAW", 
                                    body={"values": [[self.statement, self.statement_date,  self.statement_amount, self.amount_allocated]]}).execute()

    @classmethod
    def bulk_update(cls: Type[DocketStatement], sheets_app: Resource, docket_statements: List[DocketStatement]) -> None:
        for _ in docket_statements:
            cls.update(sheets_app)

class SheetsApp(schema.SheetsApp, schema.Common):
    '''
    A class to represent a Google Sheets application.
    
    Attributes:
        SCOPES (Tuple[HttpUrl]): The Google Sheets API scopes.
        credentials_file (FilePath): The path to the credentials file.
        spreadsheet_id (str): The ID of the spreadsheet.
        '''
    def __init__(self, SCOPES: Tuple[HttpUrl], credentials_file: FilePath, spreadsheet_id: str) -> None:
        super().__init__(SCOPES, credentials_file, spreadsheet_id)
        
    class Structure(BaseModel):
        '''
        A class to represent the structure of the Google Sheets application.
        '''
        READ_ONLY_SCOPE: Constant[HttpUrl] = "https://www.googleapis.com/auth/spreadsheets.readonly"
        READ_WRITE_SCOPE: Constant[HttpUrl] = 'https://www.googleapis.com/auth/spreadsheets'

        SPREADSHEET_ID: Constant[str] = '148J47DO_RZe-bbCbN_1yyqHB6MWS9JNKjvjPsg_5wlA'
        CREDENTIALS_FILE: Constant[FilePath] = FilePath(f'{getenv("HOME")}/sheets-api-credentials.json')

        TOTALS_RANGE: Constant[str] = 'Totals!B5:G5'
        DOCKETS_RANGE: Constant[str] = 'Copy of Dockets!A2:W'
        VOUCHERS_RANGE: Constant[str] = 'Vouchers!A2:I'
        CABCHARGE_RANGE: Constant[str] = 'Cabcharge!A2:G'
        EFT_STATEMENT_RANGE: Constant[str] = 'EFTPOS Statements!A2:D'
        DOCKET_STATEMENT_RANGE: Constant[str] = 'Docket Statements!A2:E'

        # INDEX_DATE: Constant[int] = 0  # Assuming Job Number is in column A (0-based index)
        # INDEX_STATEMENT_TYPE: Constant[int] = 1
        # INDEX_STATEMENT_AMOUNT: Constant[int] = 2
        # INDEX_ALLOCATED_AMOUNT: Constant[int] = 3
        # INDEX_REFERENCE: Constant[int] = 4
        # INDEX_DOCKET_STATUS: Constant[int] = 18

        SHEET_ID_DOCKET_STATEMENTS: Constant[int] = 1428866035
        SHEET_ID_DOCKETS: Constant[int] = 1053745662

        ROW_ITERATOR_START: Constant[int] = 2

        DF_COLUMN_JOB_NUMBER: Constant[str] = 'job_number'
        DF_COLUMN_STATUS: Constant[str] = 'status'
        DF_COLUMN_DOCKET_DATE: Constant[str] = 'docket_date'
        DF_COLUMN_ROW_NUMBER: Constant[str] = 'row_number'
        DATE_FORMAT: Constant[str] = '%Y-%m-%d'

    def parse_date_or_string(self, value: Optional[Union[str, datetime]]) -> Optional[Union[str, datetime]]:
        """
        Parses a value to return a datetime object if the string is a valid date,
        otherwise returns the string or None if it's empty.
        
        Args:
        - value (Optional[Union[str, datetime]]): The value to be parsed.
        - date_format (str): The format to use for date parsing.
        
        Returns:
        - Optional[Union[str, datetime]]: Parsed datetime object, original string, or None.
        """
        if not value:  # None or empty string case
            return None
        if isinstance(value, datetime):  # Already a datetime
            return value
        try:
            # Try to parse it as a datetime
            return datetime.strptime(value, self.Structure.DF_DATE_FORMAT)
        except (ValueError, TypeError):
            # If parsing fails, return it as a string
            return value
        

def main() -> None:

    JOB_NUMBER: Constant[int] = 81785392

    try:

        sheets_app: SheetsApp = SheetsApp(SCOPES = [SheetsApp.Structure.READ_ONLY_SCOPE], credentials_file = SheetsApp.Structure.CREDENTIALS_FILE, spreadsheet_id = SheetsApp.Structure.SPREADSHEET_ID)

        docket: Docket = Docket.get(sheets_app, JOB_NUMBER)

    finally:
        sheets_app.connection.close()

if __name__ == "__main__":
    main()