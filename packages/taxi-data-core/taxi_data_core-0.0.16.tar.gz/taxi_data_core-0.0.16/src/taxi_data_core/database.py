from typing import List, TypeVar, Type, Self, Final as Constant, Optional, Tuple, Any
from sqlite3 import Error, Cursor
from argparse import ArgumentParser
from os import getenv
from pathlib import Path
from datetime import date

from taxi_data_core import schema
from pydantic import FilePath, BaseModel

GpsDataBase = TypeVar('GpsDataBase', bound='GpsDataBase')
GpsRecord = TypeVar('GpsRecord', bound='GpsRecord')
TrackerEntry = TypeVar('TrackerEntry', bound='TrackerEntry')
TrackerEvent = TypeVar('TrackerEvent', bound='TrackerEvent')
TrackerEvent.Type = TypeVar('TrackerEvent.Type', bound='TrackerEvent.Type')
BwcDataBase = TypeVar('BwcDataBase', bound='BwcDataBase')

class Driver(schema.Driver):
    def __init__(self, id: int, number: int, name: str, prefered_name: str, address: str, suburb: str, post_code: int, dob: date, mobile: str, city: str, 
                    da_expiry: date, license_expiry: date, auth_wheelchair: bool, auth_bc: bool, auth_redcliffe: bool, auth_london: bool, auth_mandurah: bool, 
                    refer_fleet_ops: bool, conditions: str, create_date: date, first_logon: date, last_logon: date, first_operator_logon: date, 
                    logons_for_operator: int, hours_for_operator: int, validation_active: bool, validation_until: date, validation_reason: str, active_in_mti: bool):
        super().__init__(number, name, prefered_name, address, suburb, post_code, dob, mobile, city, da_expiry, license_expiry, conditions, 
                            create_date, first_logon, last_logon, first_operator_logon, logons_for_operator, hours_for_operator, validation_active,
                            validation_until, validation_reason, active_in_mti, auth_wheelchair, auth_bc, auth_redcliffe, auth_london, auth_mandurah, refer_fleet_ops)
        self.id = id


    class Queries(BaseModel):
        # SQL query to check if a driver exists
        record_id_from_number: Constant[str] = "SELECT id FROM Driver WHERE number = ?"
        driver_number_from_id: Constant[str] = "SELECT number FROM Driver WHERE id = ?"
        # SQL query to insert a new driver
        insert: Constant[str] = '''
        INSERT INTO Driver (
            number, name, greeting, address, suburb, post_code, dob, mobile, city, da_expiry,
            license_expiry, auth_wheelchair, auth_bc, auth_redcliffe, auth_london, auth_mandurah,
            refer_fleet_ops, conditions, create_date, first_logon, last_logon, first_operator_logon,
            logons_for_operator, hours_for_operator, validation_active, validation_until, validation_reason
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # SQL query to update an existing driver
        update: Constant[str] = '''
        UPDATE Driver SET
            name = ?, greeting = ?, address = ?, suburb = ?, post_code = ?, dob = ?, mobile = ?, city = ?,
            da_expiry = ?, license_expiry = ?, auth_wheelchair = ?, auth_bc = ?, auth_redcliffe = ?, auth_london = ?,
            auth_mandurah = ?, refer_fleet_ops = ?, conditions = ?, create_date = ?, first_logon = ?, last_logon = ?,
            first_operator_logon = ?, logons_for_operator = ?, hours_for_operator = ?, validation_active = ?,
            validation_until = ?, validation_reason = ?
        WHERE number = ?
        '''
    def update(self, database: BwcDataBase) -> None:
        database.cursor.execute(Driver.Queries.record_id_from_number, (self.number,))
        result = database.cursor.fetchone()

        if result:
            database.cursor.execute(Driver.Queries.update, (
                self.number, self.name, self.prefered_name, self.address, self.suburb, self.post_code,
                self.dob, self.mobile, self.city, self.da_expiry, self.license_expiry, self.auth_wheelchair,
                self.auth_bc, self.auth_redcliffe, self.auth_london, self.auth_mandurah, self.refer_fleet_ops,
                self.conditions, self.create_date, self.first_logon, self.last_logon, self.first_operator_logon,
                self.logons_for_operator, self.hours_for_operator, self.validation_active, self.validation_until,
                self.validation_reason
            ))
            print(f'Driver {self} updated.')
        else:
            database.cursor.execute(Driver.Queries.insert,(
                self.number, self.name, self.prefered_name, self.address, self.suburb, self.post_code, 
                self.dob, self.mobile, self.city, self.da_expiry, self.license_expiry, 
                self.auth_wheelchair, self.auth_bc, self.auth_redcliffe, self.auth_london, 
                self.auth_mandurah, self.refer_fleet_ops, self.conditions, self.create_date, 
                self.first_logon, self.last_logon, self.first_operator_logon, self.logons_for_operator, 
                self.hours_for_operator, self.validation_active, self.validation_until, self.validation_reason
            ))
            print(f'Driver {self} added.')
        database.connection.commit()

    
    def bulk_update(database: BwcDataBase, drivers: List[Self]) -> None:
        for _ in drivers:
            Driver.update(_, database)

class Taxi(schema.Taxi):
    def __init__(self, id: int, fleet_number: str, rego: str, rego_expiry: date, coi_expiry: date, make: str, model: str, build_date: str, capacity: int, primary_fleet: str, 
                    fleets: str, conditions: str, validation: str, until: date, reason: str):
        super().__init__(fleet_number, rego, rego_expiry, coi_expiry, make, model, build_date, capacity, primary_fleet, fleets, conditions, validation, until, reason)
        self.id = id

    class Queries(BaseModel):
        record_id_from_number: Constant[str] = "SELECT id FROM Taxi WHERE number = ?"
        insert: Constant[str] = '''
            INSERT INTO Taxi (number, primary_fleet, rego, rego_expiry, coi_expiry, fleets, conditions, make, model, build_date, pax, validation, until, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        update: Constant[str] = '''UPDATE Taxi SET primary_fleet = ?, rego = ?, rego_expiry = ?, coi_expiry = ?, fleets = ?, conditions = ?, 
                make = ?, model = ?, build_date = ?, pax = ?, validation = ?, until = ?, reason = ? WHERE number = ?'''
    
    def update(self, database: BwcDataBase) -> None:
        database.cursor.execute(Taxi.Queries.record_id_from_number, (self.fleet_number,))
        result = database.cursor.fetchone()

        if result:
            database.cursor.execute(Taxi.Queries.update, (
                self.primary_fleet, self.rego, self.rego_expiry, self.coi_expiry, self.fleets, self.conditions,
                self.make, self.model, self.build_date, self.capacity, self.validation, self.until, self.reason, self.fleet_number
            ))
            print(f'Taxi {self} updated.')
        else:
            database.cursor.execute(Taxi.Queries.insert, (
                self.fleet_number, self.primary_fleet, self.rego, self.rego_expiry, self.coi_expiry, self.fleets, self.conditions,
                self.make, self.model, self.build_date, self.capacity, self.validation, self.until, self.reason
            ))
            print(f'Taxi {self} added.')
        database.connection.commit()
    
    def bulk_update(database: BwcDataBase, taxis: List[Self]) -> None:
        for _ in taxis:
            Taxi.update(_, database)

class Shift(schema.Shift):
    def __init__(self, id: int, taxi: int, driver: int, name: str, log_on: date, log_off: date, duration: int, distance: int, offered: int, accepted: int, 
                    rejected: int, recalled: int, completed: int, total_fares: float, total_tolls: float):
        super().__init__(taxi, driver, name, log_on, log_off, duration, distance, offered, accepted, rejected, recalled, completed, total_fares, total_tolls)
        self.id = id

    class Queries(BaseModel):
        count_shifts_for_logon: Constant[str] = 'SELECT COUNT(*) FROM Shift WHERE log_on = ?'
        record_id_from_logon: Constant[str] = "SELECT id FROM Shift WHERE log_on = ?"
        get_by_id: Constant[str] = 'SELECT * FROM Shift WHERE id = ?'
        insert: Constant[str] = '''
            INSERT INTO Shift (car_id, driver_id, name, log_on, log_off, duration, distance, offered, accepted, rejected, recalled, completed, total_fares, total_tolls)
            VALUES ((SELECT id FROM Taxi WHERE id = ?), (SELECT id FROM Driver WHERE id = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

    def update(self, database: BwcDataBase) -> None:
        database.cursor.execute(Shift.Queries.count_shifts_for_logon, (self.log_on,))
        result = database.cursor.fetchone()[0]
        car_id: int = database.cursor.execute(Taxi.Queries.record_id_from_number, (self.taxi,)).fetchone()[0]
        driver_id: int = database.cursor.execute(Driver.Queries.record_id_from_number, (self.driver,)).fetchone()[0]

        if result:
            print(f"{self} already exists. Skipping insertion.")
        else:
            database.cursor.execute(Shift.Queries.insert, (
                car_id, driver_id, self.name, self.log_on, self.log_off, self.duration, self.distance, self.offered, self.accepted, 
                self.rejected, self.recalled, self.completed, self.total_fares, self.total_tolls
            ))
            print(f'Shift {self} added.')

        database.connection.commit()
    
    def bulk_update(database: BwcDataBase, taxis: List[Self]) -> None:
        for _ in taxis:
            Shift.update(_, database)

class Job(schema.Job, schema.Common):
    def __init__(self, id: int, booking_number: int, driver_id: int, status: str, accepted: date, meter_on: date, meter_off: date, pick_up_suburb: str, 
                    destination_suburb: str, fare: float, toll: float, account: str, taxi_id: int, shift_id: int):
        super().__init__(booking_number, meter_on, meter_off, fare, taxi_id)
        self.id = id
        self.driver_id = driver_id
        self.status = status
        self.accepted = accepted
        self.pick_up_suburb = pick_up_suburb
        self.destination_suburb = destination_suburb
        self.toll = toll
        self.account = account
        self.shift_id = shift_id

    class Queries(BaseModel):
        count_for_number: Constant[str] = 'SELECT COUNT(*) FROM Job WHERE booking_id = ?'
        find_shift_id: Constant[str] = 'SELECT id FROM Shift WHERE log_on <= ? AND log_off >= ?'
        insert: Constant[str] = '''
                INSERT INTO Job (
                    booking_id, driver_id, status, accepted, meter_on, meter_off,
                    pick_up_suburb, destination_suburb, fare, toll, account, taxi_id, shift_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

    def update(self, database: BwcDataBase) -> None:
        database.cursor.execute(Job.Queries.count_for_number, (self.booking_number,))
        result = database.cursor.fetchone()[0]
        shift_id: int = database.cursor.execute(Job.Queries.find_shift_id, (self.meter_on, self.meter_off)).fetchone()[0]
        shift = database.cursor.execute(Shift.Queries.get_by_id, (shift_id,)).fetchone()
        car_id: int = shift[1]
        driver_id: int = shift[2]


        if result:
            print(f"{self} already exists. Skipping insertion.")
        else:
            database.cursor.execute(Job.Queries.insert, (
                self.booking_number,
                driver_id,
                self.status,
                self.accepted.strftime(Job.Constants.TIME_WITH_SECONDS),
                self.meter_on.strftime(Job.Constants.TIME_WITH_SECONDS),
                self.meter_off.strftime(Job.Constants.TIME_WITH_SECONDS),
                self.pick_up_suburb,
                self.destination_suburb,
                self.fare,
                self.toll,
                self.account,
                car_id,
                shift_id
            ))
            print(f'Job {self} added.')

        database.connection.commit()
    
    def bulk_update(database: BwcDataBase, jobs: List[Self]) -> None:
        for _ in jobs:
            Job.update(_, database)

class TrackerEvent(schema.TrackerEvent):

    def __init__(self, id: int, gps_record_id: int, event_type: Type[TrackerEvent.Type], from_time: date, to_time: date, duration: int) -> None:
        super().__init__(event_type, from_time, to_time, duration)
        self.id = id
        self.gps_record_id = gps_record_id

    class Queries(BaseModel):
        EXISTS: Constant[str] = 'SELECT id FROM TrackerEvent WHERE gps_record_id = ? AND from_time = ?'
        INSERT: Constant[str] = 'INSERT INTO TrackerEvent (gps_record_id, event_type, from_time, to_time, duration) VALUES (?, ?, ?, ?, ?)'

    @classmethod
    def get_related(cls: Type[TrackerEvent], idx: int, cursor: Cursor) -> List[Self]:
        """
        Retrieves related events from the database.

        Args:
            idx (int): The index of the GpsRecord.
            cursor (Cursor): The database cursor.

        Returns:
            List[TrackerEvent]: The list of related events
        """
        try:
            cursor.execute('SELECT * FROM TrackerEvent WHERE gps_record_id = ?', (idx,))
            return [
                cls(
                    id = event[0],
                    gps_record_id = event[1],
                    event_type=TrackerEvent.Type.from_string(event[2]),
                    from_time=event[3],
                    to_time=event[4],
                    duration=event[5]
                ) for event in cursor.fetchall()
            ]

        except Error as e:
            print(f"Error: {e}")
            return None

    def get(self, cursor: Cursor, idx: int) -> Self:
        pass

class TrackerEntry(schema.TrackerEntry):

    def __init__(self, id: int, gps_record_id: int, timestamp: str, distance: float, latitude: float, longitude: float, direction: str, speed: float, stop_time: int):
        super().__init__(timestamp, distance, latitude, longitude)
        self.id = id
        self.gps_record_id = gps_record_id
        self.direction = direction
        self.speed = speed
        self.stop_time = stop_time

    class Queries(BaseModel):
        EXISTS: Constant[str] = 'SELECT id FROM TrackerEntry WHERE gps_record_id = ? AND timestamp = ?'
        INSERT: Constant[str] = 'INSERT INTO TrackerEntry (gps_record_id, timestamp, distance, latitude, longitude, direction, speed, stop_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

    def get(self, cursor: Cursor, idx: int) -> Self:
        pass



    @classmethod
    def get_related(cls: Type[TrackerEntry], idx: int, cursor: Cursor) -> List[Self]:
        """
        Retrieves related tracker entries from the database.

        Args:
            idx (int): The index of the GpsRecord.
            cursor (Cursor): The database cursor.   

        Returns:
            List[Self]: The list of related tracker entries.
        """
        try:
            cursor.execute('SELECT * FROM TrackerEntry WHERE gps_record_id = ?', (idx,))
            return [
                cls(
                    id = event[0],
                    gps_record_id = event[1],
                    timestamp=event[2],
                    distance=event[3],
                    latitude=event[4],
                    longitude=event[5],
                    direction=event[6],
                    speed=event[7],
                    stop_time=event[8]
                ) for event in cursor.fetchall()
            ]

        except Error as e:
            print(f"Error: {e}")
            return None

class GpsRecord(schema.GpsRecord):
    def __init__(self, record_date: date, kml_file: Path, 
                 idx: Optional[int] = None,
                 events: Optional[List[TrackerEvent]] = None, 
                 gps_data: Optional[List[TrackerEntry]] = None):
        super().__init__(record_date, kml_file)
        self.idx = idx
        self.events = events
        self.gps_data = gps_data

    class Queries(BaseModel):
        GET_ALL: Constant[str] = 'SELECT * FROM GpsRecord'
        EXISTS: Constant[str] = 'SELECT id FROM GpsRecord WHERE date = ?'
        INSERT: Constant[str] = 'INSERT INTO GpsRecord (date, kml_file) VALUES (?, ?)'

    @classmethod
    def bulk_update(cls: Type[GpsRecord], records: List[GpsRecord], database: GpsDataBase) -> None:
        """
        Adds a list of GpsRecord objects to the database.
        
        Args:
            records (List[Self]): The list of GpsRecord objects.
            cursor (Cursor): The database cursor.
        """

        for record in records:
            exists: bool | int = database.record_exists(GpsRecord.Queries.EXISTS, (record.record_date.strftime(GpsDataBase.Constants.REVERSE_DATE_FORMAT),))
            if exists is False:

                database.add_record(GpsRecord.Queries.INSERT, (record.record_date.strftime(GpsDataBase.Constants.REVERSE_DATE_FORMAT), str(record.kml_file) if record.kml_file else None))
                
                record.idx = database.cursor.lastrowid  # Get the new ID of the inserted record
            else:
                record.idx = exists

            # Insert or update TrackerEvent entries
            if record.events:
                for event in record.events:
                    
                    if not database.record_exists(TrackerEvent.Queries.EXISTS, (record.idx, event.from_time.strftime(GpsDataBase.Constants.REVERSE_DATE_FORMAT))):
                        database.add_record(TrackerEvent.Queries.INSERT, (record.idx, event.event_type, event.from_time.strftime(GpsDataBase.Constants.TIME_WITH_SECONDS),
                                                                           event.to_time.strftime(GpsDataBase.Constants.TIME_WITH_SECONDS), event.duration))

            # Insert or update TrackerEntry entries
            if record.gps_data:
                for entry in record.gps_data:
                    
                    if not database.record_exists(TrackerEntry.Queries.EXISTS, (record.idx, entry.timestamp.strftime(GpsDataBase.Constants.TIME_WITH_SECONDS))):
                        database.add_record(TrackerEntry.Queries.INSERT, (record.idx, entry.timestamp.strftime(GpsDataBase.Constants.TIME_WITH_SECONDS), entry.distance, entry.latitude, 
                                                                           entry.longitude, entry.direction, entry.speed, entry.stop_time))

    @classmethod
    def get_all(cls: Type[GpsRecord], cursor: Cursor) -> List[Self]:
        """
        Retrieves all GpsRecord objects from the database.

        Args:
            cursor (Cursor): The database cursor.

        Returns:
            List[Self]: The list of GpsRecord objects.
        """

        records: List[cls] = []

        try:
            cursor.execute(GpsRecord.Queries.GET_ALL)
            returned_data = cursor.fetchall()

            for record in returned_data:
                (idx, date, kml_file) = record

                events: List[TrackerEvent] = TrackerEvent.get_related(idx, cursor)
                entries: List[TrackerEntry] = TrackerEntry.get_related(idx, cursor)

                records.append(
                            cls(
                                idx=idx,
                                record_date=date,
                                kml_file=Path(kml_file) if kml_file else None,
                                events=events if events else None,
                                gps_data=entries if entries else None
                            )
                        )         
            return records      
        except Error as e:
            print(f"Error: {e}")
            return None

class BwcDataBase(schema.DataBase):
    
    def __init__(self, db_path: FilePath) -> None:
        super().__init__(db_path)

    def initialize(self) -> None:
        """
        Initialize the database with required tables.
        """
        # Create the Taxi table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Taxi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                primary_fleet TEXT NOT NULL,
                rego TEXT NOT NULL,
                rego_expiry DATE NOT NULL,
                coi_expiry DATE NOT NULL,
                fleets TEXT NOT NULL,
                conditions TEXT NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                build_date TEXT NOT NULL,
                pax INTEGER NOT NULL,
                validation TEXT,
                until DATE,
                reason TEXT
            )
        ''')

        # Create the Driver table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Driver (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL UNIQUE,
                name TEXT NOT NULL,
                greeting TEXT NOT NULL,
                address TEXT NOT NULL,
                suburb TEXT NOT NULL,
                post_code INTEGER NOT NULL,
                dob DATE NOT NULL,
                mobile TEXT NOT NULL,
                city TEXT NOT NULL,
                da_expiry DATE NOT NULL,
                license_expiry DATE NOT NULL,
                auth_wheelchair BOOLEAN,
                auth_bc BOOLEAN,
                auth_redcliffe BOOLEAN,
                auth_london BOOLEAN,
                auth_mandurah BOOLEAN,
                refer_fleet_ops BOOLEAN,
                conditions TEXT NOT NULL,
                create_date DATE NOT NULL,
                first_logon DATE NOT NULL,
                last_logon DATE NOT NULL,
                first_operator_logon DATE NOT NULL,
                logons_for_operator INTEGER NOT NULL,
                hours_for_operator INTEGER NOT NULL,
                validation_active BOOLEAN,
                validation_until DATE,
                validation_reason TEXT
            )
        ''')

        # Create the Shift table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Shift (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER NOT NULL,
                driver_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                log_on DATETIME NOT NULL,
                log_off DATETIME NOT NULL,
                duration INTEGER NOT NULL,  -- Using TEXT to store timedelta as a string
                distance INTEGER NOT NULL,
                offered INTEGER NOT NULL,
                accepted INTEGER NOT NULL,
                rejected INTEGER NOT NULL,
                recalled INTEGER NOT NULL,
                completed INTEGER NOT NULL,
                total_fares REAL NOT NULL,
                total_tolls REAL NOT NULL,
                FOREIGN KEY (car_id) REFERENCES Taxi (id),
                FOREIGN KEY (driver_id) REFERENCES Driver (id)
            )
        ''')

        # Create the Job table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Job (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER NOT NULL,
                driver_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                accepted TIME NOT NULL,
                meter_on TIME NOT NULL,
                meter_off TIME NOT NULL,
                pick_up_suburb TEXT NOT NULL,
                destination_suburb TEXT NOT NULL,
                fare REAL NOT NULL,
                toll REAL NOT NULL,
                account TEXT,
                taxi_id INTEGER NOT NULL,
                shift_id INTEGER NOT NULL,
                FOREIGN KEY (driver_id) REFERENCES Driver (id),
                FOREIGN KEY (taxi_id) REFERENCES Taxi (id),
                FOREIGN KEY (shift_id) REFERENCES Shift (id)
            )
        ''')
        self.connection.commit()
        print(f"Database '{self.file_path.name}' initialized with required tables.")

class GpsDataBase(schema.DataBase, schema.Common):

    def __init__(self, db_path: FilePath) -> None:
        super().__init__(db_path)

    def initialize(self) -> None:
        """
        Initialize the database with required tables.
        """
        # Create the Taxi table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS GpsRecord (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                kml_file TEXT
            )
        ''')

        # Create the TrackerEvent table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TrackerEvent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gps_record_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                from_time TIME NOT NULL,
                to_time TIME NOT NULL,
                duration INTEGER NOT NULL,
                FOREIGN KEY (gps_record_id) REFERENCES GpsRecord (id)
            )
        ''')

        # Create the TrackerEntry table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TrackerEntry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gps_record_id INTEGER NOT NULL,
                timestamp TIME NOT NULL,
                distance REAL NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                direction TEXT,
                speed REAL,
                stop_time INTEGER,
                FOREIGN KEY (gps_record_id) REFERENCES GpsRecord (id)
            )
        ''')

        self.connection.commit()
        print(f"Database '{self.file_path.name}' initialized with required tables.")

    def record_exists(self, QUERY: str, PARAMETERS: Tuple[Any, Any]) -> bool | None:
        """
        Checks if the GpsRecord already exists in the database.

        Args:
            cursor (Cursor): The database cursor.

        Returns:
            bool: True if the record exists, False otherwise.
        """
        try:
            # Check if the GpsRecord already exists in the database based on the 'date' field
            self.cursor.execute(QUERY, PARAMETERS)
            idx: bool | int = self.cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
            return None
        if idx:
            return idx[0]
        else:
            return False

    def add_record(self, QUERY: str, PARAMETERS: Tuple[Any, Any]) -> None:
        """
        Adds the GpsRecord to the database.
        
        Args:
            cursor (Cursor): The database cursor.
        """
        try:
            self.cursor.execute(QUERY , PARAMETERS)
            self.cursor.connection.commit()
            print(f"Query: {QUERY} run on database with parameters {PARAMETERS}")
        except Error as e:
            print(f"Error: {e}")

def main() -> None:
    ...

    parser = ArgumentParser(description='Initializes database')
    parser.add_argument('--destination',type=str,required=False,help="destination folder for downloaded data",default=f"{getenv('HOME')}/test")
    args, unknown = parser.parse_known_args()

    bwc_db: Path = Path(f"{args.destination}/bwc_data.db")
    gps_db: Path = Path(f"{args.destination}/gps_data.db")

    
    try:

        bwc_data_base: BwcDataBase = BwcDataBase(bwc_db)
        gps_data_base: GpsDataBase = GpsDataBase(gps_db)

    except Error as e:
        print(f"An error occurred: {e}")
    finally:
        bwc_data_base.connection.close()
        gps_data_base.connection.close()



#     driver_list: List[Driver] = Driver.get_all(bwc_data_base.cursor)
#     taxi_list: List[Taxi] = Taxi.get_all(bwc_data_base.cursor)
#     shift_list: List[Shift] = Shift.get_all(bwc_data_base.cursor)
#     job_list: List[Job] = Job.get_all(bwc_data_base.cursor)
#     gps_records: List[GpsRecord] = GpsRecord.get_all(gps_data_base.cursor)

#     print(driver_list)
#     print(taxi_list)
#     print(shift_list)
#     print(job_list)
#     print(gps_records)

if __name__ == '__main__':
    main()