"""CQ World Wide DX CW plugin"""

# CQ Worldwide DX Contest, RTTY
# Status:	        Active
# Geographic Focus:	Worldwide
# Participation:	Worldwide
# Awards:	        Worldwide
# Mode:	            RTTY
# Bands:	        80, 40, 20, 15, 10m
# Classes:	        Single Op All Band (High/Low/QRP)
#                   Single Op Single Band (High/Low/QRP)
#                   Single Op Assisted All Band (High/Low/QRP)
#                   Single Op Assisted Single Band (High/Low/QRP)
#                   Single Op Overlays: (Classic/Rookie/Youth)
#                   Multi-Single (High/Low)
#                   Multi-Two
#                   Multi-Multi
#                   Explorer
# Max power:	    HP: 1500 watts
#                   LP: 100 watts
#                   QRP: 5 watts
# Exchange:	        48 States/Canada: RST + CQ Zone + (state/VE area)
#                   All Others:       RST + CQ Zone
# Work stations:	Once per band
# QSO Points:	    1 point per QSO with same country
#                   2 points per QSO with same continent
#                   3 points per QSO with different continent
# Multipliers:	    W/VE Stations: Each US state/VE area once per band
#                   Each DXCC/WAE country once per band
#                   Each CQ zone once per band
# Score Calculation:	Total score = total QSO points x total mults
# E-mail logs to:	(none)
# Upload log at:	https://www.cqwwrtty.com/logcheck/
# Mail logs to:	    (see rules)
# Find rules at:	https://www.cqwwrtty.com/
# Cabrillo name:	CQ-WW-RTTY


# pylint: disable=invalid-name, unused-argument, unused-variable, c-extension-no-member, unused-import

import datetime
import logging

from pathlib import Path

from PyQt6 import QtWidgets

from not1mm.lib.ham_utility import get_logged_band
from not1mm.lib.plugin_common import gen_adif, get_points
from not1mm.lib.version import __version__

logger = logging.getLogger(__name__)

ALTEREGO = None

EXCHANGE_HINT = "RST + CQ Zone + (state/VE area)"

name = "CQ WW RTTY"
cabrillo_name = "CQ-WW-RTTY"
mode = "RTTY"  # CW SSB BOTH RTTY
# columns = [0, 1, 2, 3, 4, 5, 6, 15]
columns = [
    "YYYY-MM-DD HH:MM:SS",
    "Call",
    "Freq",
    "Snt",
    "Rcv",
    "SentNr",
    "ZN",
    "Exchange1",
    "PTS",
]

advance_on_space = [True, True, True, True, True]

# 1 once per contest, 2 work each band, 3 each band/mode, 4 no dupe checking
dupe_type = 2


def init_contest(self):
    """setup plugin"""
    set_tab_next(self)
    set_tab_prev(self)
    interface(self)
    self.next_field = self.other_1


def interface(self):
    """Setup user interface"""
    self.field1.show()
    self.field2.show()
    self.field3.show()
    self.field4.show()
    self.snt_label.setText("SNT")
    self.field1.setAccessibleName("RST Sent")
    label = self.field3.findChild(QtWidgets.QLabel)
    label.setText("CQ Zone")
    self.field3.setAccessibleName("C Q Zone")
    label = self.field4.findChild(QtWidgets.QLabel)
    label.setText("State/Prov")
    self.field4.setAccessibleName("U S State or Providence")


def reset_label(self):
    """reset label after field cleared"""


def set_tab_next(self):
    """Set TAB Advances"""
    self.tab_next = {
        self.callsign: self.field1.findChild(QtWidgets.QLineEdit),
        self.field1.findChild(QtWidgets.QLineEdit): self.field2.findChild(
            QtWidgets.QLineEdit
        ),
        self.field2.findChild(QtWidgets.QLineEdit): self.field3.findChild(
            QtWidgets.QLineEdit
        ),
        self.field3.findChild(QtWidgets.QLineEdit): self.field4.findChild(
            QtWidgets.QLineEdit
        ),
        self.field4.findChild(QtWidgets.QLineEdit): self.callsign,
    }


def set_tab_prev(self):
    """Set TAB Advances"""
    self.tab_prev = {
        self.callsign: self.field4.findChild(QtWidgets.QLineEdit),
        self.field1.findChild(QtWidgets.QLineEdit): self.callsign,
        self.field2.findChild(QtWidgets.QLineEdit): self.field1.findChild(
            QtWidgets.QLineEdit
        ),
        self.field3.findChild(QtWidgets.QLineEdit): self.field2.findChild(
            QtWidgets.QLineEdit
        ),
        self.field4.findChild(QtWidgets.QLineEdit): self.field3.findChild(
            QtWidgets.QLineEdit
        ),
    }


def set_contact_vars(self):
    """Contest Specific"""
    self.contact["SNT"] = self.sent.text()
    self.contact["RCV"] = self.receive.text()
    self.contact["ZN"] = self.other_1.text()
    self.contact["Exchange1"] = self.other_2.text()
    self.contact["SentNr"] = self.contest_settings.get("SentExchange", 0)
    

def predupe(self):
    """called after callsign entered"""


def prefill(self):
    """Fill CQ Zone"""
    if len(self.other_1.text()) == 0:
        self.other_1.setText(str(self.contact.get("ZN", "")))


def points(self):
    """Calc point"""
    # QSO Points:	    1 point per QSO with same country
    #                   2 points per QSO with same continent
    #                   3 points per QSO with different continent

    result = self.cty_lookup(self.station.get("Call", ""))
    if result:
        for item in result.items():
            mycountry = item[1].get("entity", "")
            mycontinent = item[1].get("continent", "")
    result = self.cty_lookup(self.contact.get("Call", ""))
    if result:
        for item in result.items():
            entity = item[1].get("entity", "")
            continent = item[1].get("continent", "")
            if mycountry.upper() == entity.upper():
                return 1
            if mycontinent == continent:
                return 2
            else:
                return 3
    return 0


def show_mults(self):
    """Return display string for mults"""

    # Multipliers:	    W/VE Stations: Each US state/VE area once per band
    #                   Each DXCC/WAE country once per band
    #                   Each CQ zone once per band

    result1 = self.database.fetch_zn_band_count()
    result2 = self.database.fetch_country_band_count()
    res3_query = f"select count(DISTINCT(Exchange1 || ':' || Band)) as spc_count from dxlog where ContestNR = {self.database.current_contest};"
    result3 = self.database.exec_sql(res3_query)
    if result1 and result2 and result3:
        return int(result1.get("zb_count", 0)) + int(result2.get("cb_count", 0)) + int(result3.get("spc_count", 0))
    return 0


def show_qso(self):
    """Return qso count"""
    result = self.database.fetch_qso_count()
    if result:
        return int(result.get("qsos", 0))
    return 0


def calc_score(self):
    """Return calculated score"""
    result = self.database.fetch_points()
    if result is not None:
        score = result.get("Points", "0")
        if score is None:
            score = "0"
        contest_points = int(score)
        mults = show_mults(self)
        return contest_points * mults
    return 0


def adif(self):
    """Call the generate ADIF function"""
    gen_adif(self, cabrillo_name, "CQ-WW-RTTY")


def cabrillo(self):
    """Generates Cabrillo file. Maybe."""
    # https://www.cqwpx.com/cabrillo.htm
    logger.debug("******Cabrillo*****")
    logger.debug("Station: %s", f"{self.station}")
    logger.debug("Contest: %s", f"{self.contest_settings}")
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = (
        str(Path.home())
        + "/"
        + f"{self.station.get('Call', '').upper()}_{cabrillo_name}_{date_time}.log"
    )
    logger.debug("%s", filename)
    log = self.database.fetch_all_contacts_asc()
    try:
        with open(filename, "w", encoding="ascii") as file_descriptor:
            print("START-OF-LOG: 3.0", end="\r\n", file=file_descriptor)
            print(
                f"CREATED-BY: Not1MM v{__version__}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"CONTEST: {cabrillo_name}",
                end="\r\n",
                file=file_descriptor,
            )
            if self.station.get("Club", ""):
                print(
                    f"CLUB: {self.station.get('Club', '').upper()}",
                    end="\r\n",
                    file=file_descriptor,
                )
            print(
                f"CALLSIGN: {self.station.get('Call','')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"LOCATION: {self.station.get('ARRLSection', '')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"CATEGORY-OPERATOR: {self.contest_settings.get('OperatorCategory','')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"CATEGORY-ASSISTED: {self.contest_settings.get('AssistedCategory','')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"CATEGORY-BAND: {self.contest_settings.get('BandCategory','')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"CATEGORY-MODE: {self.contest_settings.get('ModeCategory','')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"CATEGORY-TRANSMITTER: {self.contest_settings.get('TransmitterCategory','')}",
                end="\r\n",
                file=file_descriptor,
            )
            if self.contest_settings.get("OverlayCategory", "") != "N/A":
                print(
                    f"CATEGORY-OVERLAY: {self.contest_settings.get('OverlayCategory','')}",
                    end="\r\n",
                    file=file_descriptor,
                )
            print(
                f"GRID-LOCATOR: {self.station.get('GridSquare','')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"CATEGORY-POWER: {self.contest_settings.get('PowerCategory','')}",
                end="\r\n",
                file=file_descriptor,
            )

            print(
                f"CLAIMED-SCORE: {calc_score(self)}",
                end="\r\n",
                file=file_descriptor,
            )
            ops = f"@{self.station.get('Call','')}"
            list_of_ops = self.database.get_ops()
            for op in list_of_ops:
                ops += f", {op.get('Operator', '')}"
            print(
                f"OPERATORS: {ops}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"NAME: {self.station.get('Name', '')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"ADDRESS: {self.station.get('Street1', '')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"ADDRESS-CITY: {self.station.get('City', '')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"ADDRESS-STATE-PROVINCE: {self.station.get('State', '')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"ADDRESS-POSTALCODE: {self.station.get('Zip', '')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"ADDRESS-COUNTRY: {self.station.get('Country', '')}",
                end="\r\n",
                file=file_descriptor,
            )
            print(
                f"EMAIL: {self.station.get('Email', '')}",
                end="\r\n",
                file=file_descriptor,
            )
            for contact in log:
                the_date_and_time = contact.get("TS", "")
                themode = contact.get("Mode", "")
                if themode == "LSB" or themode == "USB":
                    themode = "PH"
                if themode.strip() in (
                        "RTTY",
                        "RTTY-R",
                        "LSB-D",
                        "USB-D",
                        "AM-D",
                        "FM-D",
                        "DIGI-U",
                        "DIGI-L",
                        "RTTYR",
                        "PKTLSB",
                        "PKTUSB",
                    ):
                    themode = "RY"
                exchange1 = contact.get('Exchange1', '')
                if exchange1 == '':
                    exchange1 = "DX"
                frequency = str(int(contact.get("Freq", "0"))).rjust(5)

                loggeddate = the_date_and_time[:10]
                loggedtime = the_date_and_time[11:13] + the_date_and_time[14:16]
                print(
                    f"QSO: {frequency} {themode} {loggeddate} {loggedtime} "
                    f"{contact.get('StationPrefix', '').ljust(13)} "
                    f"{str(contact.get('SNT', '')).ljust(3)} "
                    f"{str(contact.get('SentNr', '')).ljust(6)} "
                    f"{contact.get('Call', '').ljust(13)} "
                    f"{str(contact.get('RCV', '')).ljust(3)} "
                    f"{str(contact.get('ZN', '')).zfill(2)}",
                    f"{str(exchange1).ljust(2)}",
                    end="\r\n",
                    file=file_descriptor,
                )
            print("END-OF-LOG:", end="\r\n", file=file_descriptor)
        self.show_message_box(f"Cabrillo saved to: {filename}")
    except IOError as exception:
        logger.critical("cabrillo: IO error: %s, writing to %s", exception, filename)
        self.show_message_box(f"Error saving Cabrillo: {exception} {filename}")
        return


def recalculate_mults(self):
    """Recalculates multipliers after change in logged qso."""


def set_self(the_outie):
    """..."""
    globals()["ALTEREGO"] = the_outie


def ft8_handler(the_packet: dict):
    """Process FT8 QSO packets
    FT8
    {
        'CALL': 'KE0OG',
        'GRIDSQUARE': 'DM10AT',
        'MODE': 'FT8',
        'RST_SENT': '',
        'RST_RCVD': '',
        'QSO_DATE': '20210329',
        'TIME_ON': '183213',
        'QSO_DATE_OFF': '20210329',
        'TIME_OFF': '183213',
        'BAND': '20M',
        'FREQ': '14.074754',
        'STATION_CALLSIGN': 'K6GTE',
        'MY_GRIDSQUARE': 'DM13AT',
        'CONTEST_ID': 'ARRL-FIELD-DAY',
        'SRX_STRING': '1D UT',
        'CLASS': '1D',
        'ARRL_SECT': 'UT'
    }
    FlDigi
    {
            'FREQ': '7.029500',
            'CALL': 'DL2DSL',
            'MODE': 'RTTY',
            'NAME': 'BOB',
            'QSO_DATE': '20240904',
            'QSO_DATE_OFF': '20240904',
            'TIME_OFF': '212825',
            'TIME_ON': '212800',
            'RST_RCVD': '599',
            'RST_SENT': '599',
            'BAND': '40M',
            'COUNTRY': 'FED. REP. OF GERMANY',
            'CQZ': '14',
            'STX': '000',
            'STX_STRING': '1D ORG',
            'CLASS': '1D',
            'ARRL_SECT': 'DX',
            'TX_PWR': '0',
            'OPERATOR': 'K6GTE',
            'STATION_CALLSIGN': 'K6GTE',
            'MY_GRIDSQUARE': 'DM13AT',
            'MY_CITY': 'ANAHEIM, CA',
            'MY_STATE': 'CA'
        }

    """
    logger.debug(f"{the_packet=}")
    # {
    #   'FREQ': '7.040000', 'CALL': 'K5TUX', 'MODE': 'RTTY', 'QSO_DATE': '20240916', 'QSO_DATE_OFF': '20240916',
    #   'TIME_OFF': '235422', 'TIME_ON': '235100', 'RST_RCVD': '599', 'RST_SENT': '599', 'STATE': 'MO', 'BAND': '40M',
    #   'COUNTRY': 'USA', 'CQZ': '3', 'STX': '000', 'STX_STRING': 'DM13', 'TX_PWR': '0', 'OPERATOR': 'K6GTE',
    #   'STATION_CALLSIGN': 'K6GTE', 'MY_GRIDSQUARE': 'DM13AT', 'MY_CITY': 'ANAHEIM, CA', 'MY_STATE': 'CA'
    # }
    if ALTEREGO is not None:
        ALTEREGO.callsign.setText(the_packet.get("CALL"))
        ALTEREGO.contact["Call"] = the_packet.get("CALL", "")
        ALTEREGO.contact["SNT"] = ALTEREGO.sent.text()
        ALTEREGO.contact["RCV"] = ALTEREGO.receive.text()
        ALTEREGO.contact["Exchange1"] = f"{the_packet.get("STATE", "")}".strip()
        ALTEREGO.contact["ZN"] = the_packet.get("CQZ", "")
        ALTEREGO.contact["Mode"] = the_packet.get("MODE", "ERR")
        ALTEREGO.contact["Freq"] = round(float(the_packet.get("FREQ", "0.0")) * 1000, 2)
        ALTEREGO.contact["QSXFreq"] = round(
            float(the_packet.get("FREQ", "0.0")) * 1000, 2
        )
        ALTEREGO.contact["Band"] = get_logged_band(
            str(int(float(the_packet.get("FREQ", "0.0")) * 1000000))
        )
        logger.debug(f"{ALTEREGO.contact=}")
        ALTEREGO.other_1.setText(str(the_packet.get("CQZ", "ERR")))
        ALTEREGO.other_2.setText(f"{the_packet.get("STATE", "")}".strip())
        ALTEREGO.save_contact()
