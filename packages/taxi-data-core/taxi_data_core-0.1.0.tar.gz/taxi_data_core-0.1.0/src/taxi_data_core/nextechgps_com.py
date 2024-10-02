from typing import Final as Constant, Tuple, TypeVar, Self, Optional, Type, List
from os import getenv, rename
from datetime import date, timedelta, datetime
from time import sleep, time
from xml.etree import ElementTree as ET
from pydantic import BaseModel, FilePath

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
from bs4.element import Tag

from taxi_data_core import schema

WebSite = TypeVar('WebSite', bound='WebSite')
TrackerEvent = TypeVar('TrackerEvent', bound='TrackerEvent')
TrackerEntry = TypeVar('TrackerEntry', bound='TrackerEntry')
TrackerEvent.Type = TypeVar('TrackerEvent.Type', bound='TrackerEvent.Type')

class TrackerEvent(schema.TrackerEvent):
    '''
    TrackerEvent class for the GPS tracker events.
    
    This class contains the methods and attributes for storing GPS tracker events.
    
    Attributes:
    
        event_type (str): The type of the GPS tracker event.
        from_time (time): The start time of the GPS tracker event.
        to_time (time): The end time of the GPS tracker event.
        duration (int): The duration of the GPS tracker event.
        
    Methods:
    
        get(row: Tag): Converts a BeautifulSoup row element to a TrackerEvent object.
    '''
    def __init__(self, event_type: TrackerEvent.Type, from_time: time, to_time: time, duration: int):
        super().__init__(event_type, from_time, to_time, duration)

    @classmethod
    def get(cls: Type[TrackerEvent], row: Tag) -> Self:
        '''
        Converts a BeautifulSoup row element to a TrackerEvent object.
        
        Args:
        
            row (Tag): The BeautifulSoup row element.
            
        Returns:
        
            TrackerEvent: The TrackerEvent object.
        ''' 

        cols = row.find_all(WebSite.Constants.TAG_COLUMN)
        
        return cls(event_type=cls.Type.from_string(cols[0].text.strip()),
                        from_time=datetime.strptime(cols[1].text.strip(), WebSite.Structure.DATE_TIME_Y_M_D_H_M_S).time() ,
                        to_time=datetime.strptime(cols[2].text.strip(), WebSite.Structure.DATE_TIME_Y_M_D_H_M_S).time(),
                        duration=WebSite.Actions.convert_duration_to_seconds(cols[3].text.strip()))

class TrackerEntry(schema.TrackerEntry):
    '''
    TrackerEntry class for the GPS tracker data.
    
    This class contains the methods and attributes for storing GPS tracker data.
    
    Attributes:
    
        timestamp (time): The timestamp of the GPS tracker entry.
        distance (float): The distance of the GPS tracker entry.
        latitude (float): The latitude of the GPS tracker entry.
        longitude (float): The longitude of the GPS tracker entry.
        stop_time (Optional[int]): The stop time of the GPS tracker entry.
        direction (Optional[str]): The direction of the GPS tracker entry.
        speed (Optional[float]): The speed of the GPS tracker entry.
        
    Methods:
    
        get(string: str): Converts a string to a TrackerEntry object.
    '''
    def __init__(self, timestamp: time, distance: float, latitude: float, longitude: float, 
                 stop_time: Optional[int] = None, direction: Optional[str] = None, speed: Optional[float] = None):
        super().__init__(timestamp, distance, latitude, longitude)
        self.stop_time = stop_time
        self.direction = direction
        self.speed = speed

    @classmethod
    def get(cls: Type[TrackerEntry], string: str) -> Self:
        '''
        Converts a string to a TrackerEntry object.
        
        Args:
            string (str): The string to convert.
            
        Returns:
        
            TrackerEntry: The TrackerEntry object.
        '''
        lines = string.splitlines()[1:]

        entry: TrackerEntry = TrackerEntry(
            timestamp = datetime.strptime(lines[0], WebSite.Structure.DATE_TIME_Y_M_D_H_M_S).time(),
            distance = WebSite.Actions.safe_extract(lambda: float(lines[1].partition(":")[2].replace("km", ""))),
            latitude = WebSite.Actions.safe_extract(lambda: float(lines[2].partition(":")[2].partition(",")[0])),
            longitude = WebSite.Actions.safe_extract(lambda: float(lines[2].rsplit(":")[2])))
        
        if lines[4].startswith("Stop time:"):
            entry.stop_time = WebSite.Actions.convert_duration_to_seconds(lines[4])
        else:
            entry.direction = WebSite.Actions.safe_extract(lambda: lines[4].split(":")[1].split(",")[0])
            entry.speed = WebSite.Actions.safe_extract(lambda: float(lines[4].split(":")[2].replace("km/h", '')))

        return entry

class GpsRecord(schema.GpsRecord):
    '''
    GpsRecord class for the GPS record data.
    
    This class contains the methods and attributes for storing GPS record data.
    
    Attributes:
    
        record_date (date): The date of the GPS record.
        kml_file (FilePath): The path to the KML file.
        events (Optional[List[TrackerEvent]]): The list of tracker events.
        gps_data (Optional[List[TrackerEntry]]): The list of GPS tracker entries.
        
    Methods:

        coords_in_kml(): Checks if a KML file contains any coordinates.
        '''
    def __init__(self, record_date: date, kml_file: FilePath, events: Optional[List[TrackerEvent]] = None, gps_data: Optional[List[TrackerEntry]] = None):
        super().__init__(record_date, kml_file)
        self.events = events
        self.gps_data = gps_data
    
class WebSite(schema.WebSite, schema.Common):
    '''
    WebSite class for the Nextech GPS website.
    
    This class contains the methods and attributes for interacting with the Nextech GPS website.
    
    Attributes:
    
        url (str): The URL of the Nextech GPS website.
        playback_speed (Optional[str | WebSite.Playback.Speed]): The playback speed setting.
        
    Methods:
    
        find_playback_buttons(): Finds the playback buttons on the GPS tracker page.
        set_playback_speed(): Sets the playback speed on the GPS tracker page.
        login(username: str, password: str): Logs into the Nextech GPS website using the provided username and password.
        switch_to_main_box_iframe(): Switches the browser context to the main box iframe.
        click_on_tracker(): Clicks on the GPS tracker device in the device list.
        nav_to_tracking_report(): Navigates to the tracking report section of the website.
        download_tracking_report(report_date: date, data_dir: FilePath): Downloads the tracking report for the specified date and saves it to the given directory.
        open_playback(): Opens the playback window for the GPS tracker.
        set_playback_date(shift_date: date): Sets the playback start and end dates.
        get_info_pane(): Retrieves the information pane WebElement.
        get_info_pane_text(): Extracts and stores the text from the information pane.
        play_to_end(): Plays the GPS tracker playback to the end.
        setup_playback(shift_date: date): Sets up playback date and speed and finds playback buttons.
        nav_to_playback(): Navigates to the playback section of the application.
        get_gps_data(): Extracts raw data from the tracker information pane.
        wait_for_pin_movement(initial_left: int, initial_top: int): Waits for the location pin to move and returns the new position.
        get_events(): Extracts events from the tracker event list.
    '''
    def __init__(self, url) -> None:
        super().__init__(url)
        self.playback_speed: Optional[str | WebSite.Playback.Speed] = None

    class Structure(BaseModel):
        '''
        Structure class for the Nextech GPS website.
        This class contains the structure elements of the Nextech GPS website, such as IDs, XPaths, and class names.
        '''
        WEB_UI_USERNAME: Constant[str] = getenv("GPS_UI_USERNAME")
        WEB_UI_PASSWORD: Constant[str] = getenv("GPS_UI_PASSWORD")
        WEB_UI_URL: Constant[str] = "http://www.nextechgps.com/"

        FILE_NAME_STRING: Constant[str] = "CC888-63677-"
        DOWNLOADS_FOLDER: Constant[str] = "/home/wayne/Downloads/"

        ID_MAIN_BOX_IFRAME: Constant[str] = 'MainBox'
        ID_DEVICE_LIST: Constant[str] = 'divTabDevice147309'
        ID_REPORT_DOWNLOAD_WINDOW: Constant[str] = 'ifmPage'
        ID_PLAYBACK_START_DATE: Constant[str] = 'txtStartDate'
        ID_PAUSE_BUTTON: Constant[str] = 'btnNext'
        ID_LOGIN_IFRAME: Constant[str] = 'ifm'
        ID_USERNAME_FIELD: Constant[str] = 'txtUserName'
        ID_PASSWORD_FIELD: Constant[str] = 'txtUserPassword'
        ID_LOGIN_BUTTON: Constant[str] = 'accountLoign'
        ID_DOWNLOAD_GO_BUTTON: Constant[str] = 'btnSubmit'
        ID_PLAYBACK_END_DATE: Constant[str] = 'txtEndDate'
        ID_SLIDER: Constant[str] = 'PlaySpeed'
        ID_PLAY_BUTTON: Constant[str] = 'btnPlay'
        ID_EVENT_LIST: Constant[str] = 'tblEvent'
        ID_LOADING_DATA: Constant[str] = 'spanMsg'
        ID_CONTINUE_BUTTON: Constant[str] = 'btnPause'

        XPATH_GPS_TRACKER: Constant[str] = '/html/body/form/div[17]/div[1]/div/div[5]/div[2]/div/div[1]'
        XPATH_MORE_OPTIONS: Constant[str] = '/html/body/form/div[17]/div[1]/div/div[5]/div[2]/div/div[3]/a[3]'
        XPATH_TRACKING_REPORT: Constant[str] = '/html/body/form/div[15]/div/div/div[11]/div[1]/a'
        XPATH_PLAYBACK_BUTTON: Constant[str] = '/html/body/form/div[17]/div[1]/div/div[5]/div[2]/div/div[3]/a[2]'
        XPATH_INFO_PANE: Constant[str] = '/html/body/form/div[3]/div[3]/div[3]/div[4]'
        XPATH_GREEN_LOCATION_PIN: Constant[str] = "/html/body/form/div[3]/div[3]/div[2]"

        CLASS_DOWNLOAD_DATE: Constant[str] = 'Wdate'

        STR_LOADING_DATA: Constant[str] = 'Loading data!'

        DATE_TIME_Y_M_D_H_M_S: Constant[str] = '%Y-%m-%d %H:%M:%S'
        DATE_TIME_YEAR_FIRST: Constant[str] = "%Y-%m-%d"

    class Playback(BaseModel):
        '''
        Playback class for the Nextech GPS website.
        This class contains the playback elements of the Nextech GPS website, such as buttons and playback speed settings.
        '''
        class Buttons():
            '''
            Buttons class for the playback section of the Nextech GPS website.
            This class contains the playback control buttons, such as play, pause, and continue.
            '''
            def __init__(self, Play: WebElement, Pause: WebElement, Continue: WebElement) -> None:
                self.play_button = Play
                self.pause_button = Pause
                self.continue_button = Continue

            def __str__(self) -> str:
                return self.__class__.__name__ + "(Play, Pause, Continue)"
            
            def __repr__(self) -> str:
                return self.__class__.__name__ + "(Play, Pause, Continue)"
            
        class Speed(BaseModel):
            '''
            Speed class for the playback section of the Nextech GPS website.
            This class contains the playback speed settings, such as fast and slow.
            
            Attributes:
            
                FAST (Constant[str]): The fast playback speed setting.
                SLOW (Constant[str]): The slow playback speed setting.
                '''
            FAST: Constant[str] = "FAST"
            SLOW: Constant[str] = "SLOW"

            @staticmethod
            def from_string(speed: str) -> Self:
                """
                Converts a string to a PlaybackSpeed object.

                Args:
                    speed (str): The playback speed.

                Returns:
                    Self: The PlaybackSpeed object.
                """
                if isinstance(speed, str):
                    match speed.upper():
                        case "FAST":
                            return WebSite.Playback.Speed.FAST
                        case "SLOW":
                            return WebSite.Playback.Speed.SLOW
                        case _:
                            raise ValueError(f"Unknown event type: {speed}")
                else:
                    raise TypeError(f"Expected a string, got {type(speed)}")

    def find_playback_buttons(self) -> None:
        """
        Finds the playback buttons on the GPS tracker page.
        
        Args:
            browser (selenium.webdriver): The browser object.
        """

        self.Playback.Buttons = self.Playback.Buttons(
            Play = self.browser.find_element(By.ID, WebSite.Structure.ID_PLAY_BUTTON),
            Pause = self.browser.find_element(By.ID, WebSite.Structure.ID_PAUSE_BUTTON),
            Continue = self.browser.find_element(By.ID, WebSite.Structure.ID_CONTINUE_BUTTON)
        )

    def set_playback_speed(self) -> None:
        """
        Sets the playback speed on the GPS tracker page.

        Args:
            browser (selenium.webdriver): The browser object.
            ID_SLIDER (str): The ID of the slider element.
        """ 
        # Play speed slow
        slider = self.browser.find_element(By.ID, self.Structure.ID_SLIDER)    
        # Initialize ActionChains
        actions = ActionChains(self.browser)

        match self.playback_speed:
            case WebSite.Playback.Speed.FAST:
                offset = -slider.size['width']
            case WebSite.Playback.Speed.SLOW:
                offset = slider.size['width']
            case _:
                raise "Slider offset not correctly set"
        # Move the slider to the right by clicking and dragging
        actions.click_and_hold(slider).move_by_offset(offset, 0).release().perform()

    def login(self, username: str, password: str) -> None:
        '''
        Logs into the Nextech GPS website using the provided username and password.
        
        Args:
            username (str): The username to log in with.
            password (str): The password to log in with.
        '''
        #self.browser: webdriver = CommonActions.set_browser()
        self.username = username
        self.password = password

        # Open the login page
        self.browser.get(self.url)

        iframe = self.browser.find_element(By.ID, self.Structure.ID_LOGIN_IFRAME)
        self.browser.switch_to.frame(iframe)

        # Log in
        username = self.browser.find_element(By.ID, self.Structure.ID_USERNAME_FIELD)
        password = self.browser.find_element(By.ID, self.Structure.ID_PASSWORD_FIELD)

        username.send_keys(self.username)
        password.send_keys(self.password)

        login_button = self.browser.find_element(By.ID, self.Structure.ID_LOGIN_BUTTON)
        login_button.click()

    def switch_to_main_box_iframe(self) -> None:
        '''
        Switches the browser context to the main box iframe.
        '''

        WebDriverWait(self.browser, self.Constants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_MAIN_BOX_IFRAME)))
        iframe = self.browser.find_element(By.ID, self.Structure.ID_MAIN_BOX_IFRAME)
        self.browser.switch_to.frame(iframe)

    def click_on_tracker(self) -> None:
        '''
        Clicks on the GPS tracker device in the device list.
        '''
        #Wait for device list to load
        WebDriverWait(self.browser, self.Constants.LONG_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_DEVICE_LIST)))
        self.tracker: WebElement = self.browser.find_element(By.ID, self.Structure.ID_DEVICE_LIST)

        # Click on device
        element_to_click = self.tracker.find_element(By.XPATH, self.Structure.XPATH_GPS_TRACKER)
        WebDriverWait(self.tracker, self.Constants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, self.Structure.XPATH_GPS_TRACKER)))
        element_to_click.click()

    def nav_to_tracking_report(self) -> None:
        '''
        Navigates to the tracking report section of the website.
        '''
        #Click on more
        element_to_click = self.tracker.find_element(By.XPATH, self.Structure.XPATH_MORE_OPTIONS)
        WebDriverWait(self.tracker, self.Constants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, self.Structure.XPATH_MORE_OPTIONS)))
        element_to_click.click()

        #Click on tracking report
        element_to_click = self.tracker.find_element(By.XPATH, self.Structure.XPATH_TRACKING_REPORT)
        WebDriverWait(self.tracker, self.Constants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, self.Structure.XPATH_TRACKING_REPORT)))
        element_to_click.click()

        # Wait for report download window to load
        WebDriverWait(self.browser, self.Constants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_REPORT_DOWNLOAD_WINDOW)))
        iframe = self.browser.find_element(By.ID, self.Structure.ID_REPORT_DOWNLOAD_WINDOW)
        self.browser.switch_to.frame(iframe)
        
    def download_tracking_report(self, report_date: date, data_dir: FilePath) -> FilePath | None:
        '''
        Downloads the tracking report for the specified date and saves it to the given directory.
        
        Args:
        
            report_date (date): The date of the tracking report.
            data_dir (FilePath): The directory to save the tracking report to.
        '''
        downloads_folder: Constant[str] = f"{getenv('HOME')}/Downloads"
        #parent_dir: Final[str] = f"{getenv('HOME')}/taxi_data"
        file_name: Constant[str] = f"{self.Structure.FILE_NAME_STRING}{report_date.strftime(self.Structure.DATE_TIME_YEAR_FIRST)}.kml"

        old_name: Constant[FilePath] = f"{downloads_folder}/{file_name}"
        new_name: Constant[FilePath] = f"{data_dir}/{file_name}"

        if not FilePath(new_name).exists():
            #Find date field and enter date
            WebDriverWait(self.browser, self.Constants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, self.Structure.CLASS_DOWNLOAD_DATE)))
            date_box = self.browser.find_element(By.CLASS_NAME, self.Structure.CLASS_DOWNLOAD_DATE)
            date_box.clear()
            date_box.send_keys(report_date.strftime(self.Structure.DATE_TIME_YEAR_FIRST))

            self.browser.find_element(By.ID, self.Structure.ID_DOWNLOAD_GO_BUTTON).click()
        

            rename(old_name,new_name)
            return new_name
        else:
            return None

    def open_playback(self) -> None:
            '''
            Opens the playback window for the GPS tracker.
            '''
            # Store the current window handle
            main_window = self.browser.current_window_handle
            #driver.switch_to.default_content()
            iframe = self.browser.find_element(By.ID, self.Structure.ID_MAIN_BOX_IFRAME)
            self.browser.switch_to.frame(iframe)

            # Click Playback
            self.tracker = self.browser.find_element(By.ID, self.Structure.ID_DEVICE_LIST)
            self.tracker.find_element(By.XPATH, self.Structure.XPATH_PLAYBACK_BUTTON).click()

            #Wait for tab to load
            WebDriverWait(self.browser, self.Constants.DEFAULT_TIMEOUT).until(EC.new_window_is_opened([main_window]))

            # Get all window handles (there should be two now)
            window_handles = self.browser.window_handles
            # Switch to the new window handle
            for handle in window_handles:
                if handle != main_window:
                    self.browser.switch_to.window(handle)
                    break
            
            #Wait for playback page to load
            WebDriverWait(self.browser, self.Constants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.ID, self.Structure.ID_PLAYBACK_START_DATE)))

    def set_playback_date(self, shift_date: date) -> None:
        '''
        Sets the playback start and end dates.
        
        Args:
            shift_date (date): The date to set the playback to.
        '''
        #Find date boxes and enter date
        date_box = self.browser.find_element(By.ID, self.Structure.ID_PLAYBACK_START_DATE)
        date_box.clear()
        date_box.send_keys(f"{shift_date} 00:00")   

        date_box = self.browser.find_element(By.ID, self.Structure.ID_PLAYBACK_END_DATE)
        date_box.clear()
        date_box.send_keys(f"{shift_date} 23:59")

    def get_info_pane(self) -> WebElement:
        '''
        Retrieves the information pane WebElement.
        '''
        info_pane: WebElement = self.browser.find_element(By.XPATH, self.Structure.XPATH_INFO_PANE)
    
        if info_pane.text != None:
            return info_pane    

    def get_info_pane_text(self):
        '''
        Extracts and stores the text from the information pane.
        '''
        try:
            text = None
            WebDriverWait(self.browser, self.Constants.DEFAULT_TIMEOUT).until(EC.element_to_be_clickable((By.ID, self.Structure.ID_PAUSE_BUTTON)))
            self.Playback.Buttons.pause_button.click()

            info_pane: WebElement = self.get_info_pane()

        except TimeoutException:
            try:
                self.browser.switch_to.alert.accept()
            except NoAlertPresentException:
                info_pane: WebElement = self.get_info_pane()
                self.info_pane_text = info_pane.text         

        self.info_pane_text = info_pane.text

    def play_to_end(self) -> None:
        '''
        Plays the GPS tracker playback to the end.
        '''
        self.Playback.Buttons.Play.click()
        WebDriverWait(self.browser, self.Constants.JUST_FUCKING_WAIT_TIMEOUT).until(EC.alert_is_present())
        self.browser.switch_to.alert.accept()
        self.browser.switch_to.default_content()

    def setup_playback(self):
        '''
        Sets up playback date and speed and finds playback buttons
        
        Args:
        
            shift_date (date): the date to setup playback for'''
#        self.set_playback_date(shift_date)
        
        # speed: WebSite.Playback.Speed = self.Playback.Speed.SLOW
        # speed.set(self.browser, self.Structure.ID_SLIDER)
        self.playback_speed = self.Playback.Speed.from_string("slow")
        self.set_playback_speed()

        self.find_playback_buttons()

    def nav_to_playback(self) -> None:
        """
        Navigates to the playback section of the application.

        This method performs the following steps:
        1. Logs into the application.
        2. Switches to the default content frame.
        3. Switches to the main box iframe.
        4. Clicks on the tracker element.
        5. Navigates to the tracking report.
        6. Downloads the tracking report.
        7. Switches back to the default content frame.
        8. Opens the playback section.
        """
        self.login()
        self.browser.switch_to.default_content()
        self.switch_to_main_box_iframe()
        self.tracker: WebElement = self.click_on_tracker()
        self.nav_to_tracking_report()
        self.download_tracking_report()
        self.browser.switch_to.default_content()
        self.open_playback()

    def get_gps_data(self) -> List[TrackerEntry]:
        '''
        Extracts raw data from the tracker information pane.
        '''
        gps_data = []

        self.Playback.Buttons.play_button.click()
        # Get First Entry
        self.get_info_pane_text()
        gps_data.append(TrackerEntry.get(self.info_pane_text))

        # Locate the div element 
        location_pin: WebElement = self.browser.find_element(By.XPATH, self.Structure.XPATH_GREEN_LOCATION_PIN)

        # Get the initial position
        initial_left = location_pin.value_of_css_property('left')
        initial_top = location_pin.value_of_css_property('top')

        # Continuous loop
        i = 0
        while True:
            try:
                
                # Check if alert is present
                alert = self.browser.switch_to.alert
                print("Alert is present!")
                return gps_data
                break  # Exit the loop if the alert is found
            except NoAlertPresentException:
                try:
                    print("No alert present yet...")
                    # If continue is disabled break
                    if self.Playback.Buttons.continue_button.is_enabled() == True:
                        self.Playback.Buttons.continue_button.click()  
                        if i > self.Constants.LOOP_LIMIT:
                            return gps_data
                            break 
                    else:
                        return gps_data
                        break

                    current_left = initial_left
                    current_top = initial_top

                    initial_left, initial_top = self.wait_for_pin_movement(initial_left, initial_top)

                    if current_left == initial_left and current_top == initial_top:
                        i += 1               
                    else:
                        i = 0               
                    self.get_info_pane_text()
                    gps_data.append(TrackerEntry.get(self.info_pane_text))

                except UnexpectedAlertPresentException:
                    return gps_data
                    break

    def wait_for_pin_movement(self, initial_left: int, initial_top: int) -> Tuple[int, int]:
        '''
        Waits for the location pin to move and returns the new position.
        
        Args:
            initial_left (int): The initial left position of the location pin.
            initial_top (int): The initial top position of the location pin.
            
        Returns:
        
            Tuple[int, int]: The new left and top positions of the location pin.
        '''
        start_time = time()  # Record the start time

        spinner = ['|', '/', '-', '\\']  # Spinner characters for the animation
        spinner_index = 0  # Initial spinner index

        while True:
            
            try:
                # Check if the timeout has been exceeded
                elapsed_time = time() - start_time
                if elapsed_time > self.Constants.SHORT_TIMEOUT:
                    print(f"\nTimeout reached after {self.Constants.SHORT_TIMEOUT} seconds.")
                    break        
    
                location_pin: WebElement = self.browser.find_element(By.XPATH, self.Structure.XPATH_GREEN_LOCATION_PIN)

                current_left = location_pin.value_of_css_property('left')
                current_top = location_pin.value_of_css_property('top')

                # Check if the position has changed
                if current_left != initial_left or current_top != initial_top:
                    print(f"\nPosition changed! New position: left={current_left}, top={current_top}")
                    # Update initial position to detect further changes
                    initial_left = current_left
                    initial_top = current_top
                    break
                else: 

                    print(f"\rWaiting for position change... {spinner[spinner_index]}", end='')
                    spinner_index = (spinner_index + 1) % len(spinner)  # Update spinner index

                    # Small delay to make the animation visible
                    sleep(0.1)


            except UnexpectedAlertPresentException:
                break

        return initial_left, initial_top

    def get_events(self) -> List[TrackerEvent]:
        '''
        Extracts events from the tracker event list.
        
        Returns:
        
            List[TrackerEvent]: A list of TrackerEvent objects.
        '''
        events = []

        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        events_table = soup.find(self.Constants.TAG_TABLE, {self.Constants.TAG_ID: self.Structure.ID_EVENT_LIST})

        #return [self.get_row(row) for row in events_table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER]]

        return [TrackerEvent.get(row) for row in events_table.find_all(self.Constants.TAG_ROW)[self.Constants.SLICE_REMOVE_HEADER]]


def main() -> None:
    shift_date: date = date.today()-timedelta(days=1)
    try:
        site = WebSite(WebSite.Structure.WEB_UI_URL)
        site.login(WebSite.Structure.WEB_UI_USERNAME, WebSite.Structure.WEB_UI_PASSWORD)

        site.browser.switch_to.default_content()
        site.switch_to_main_box_iframe()
        site.click_on_tracker()
        site.nav_to_tracking_report()

        gps_record: GpsRecord = GpsRecord(shift_date, site.download_tracking_report(shift_date, f'{getenv("HOME")}/test'))

        site.browser.switch_to.default_content()

        site.open_playback()

        site.setup_playback(shift_date)


        gps_record.gps_data = site.get_gps_data()
        gps_record.events = site.get_events()

    finally:
        site.browser.quit()



if __name__ == '__main__':
    main()