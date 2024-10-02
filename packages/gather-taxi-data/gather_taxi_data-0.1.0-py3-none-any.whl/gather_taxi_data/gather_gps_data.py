from datetime import datetime, timedelta, date
from typing import List, Dict
from argparse import ArgumentParser
from os import getenv
from pydantic import FilePath

from taxi_data_core.nextechgps_com import WebSite
from taxi_data_core.database import GpsDataBase as DataBase, GpsRecord

def gather_gps_data(start_date: date, finish_date: date, destination: str) -> None:

    website: WebSite = WebSite(WebSite.Structure.WEB_UI_URL)
    database: DataBase = DataBase(db_path = f"{destination}/gps_data.db")

    try:
        

        db_records: Dict[str, GpsRecord] = {record.record_date: record for record in GpsRecord.get_all(database.cursor)}
        


        website.login(WebSite.Structure.WEB_UI_USERNAME, WebSite.Structure.WEB_UI_PASSWORD)

        website.browser.switch_to.default_content()
        website.switch_to_main_box_iframe()
        website.click_on_tracker()
   
        website.nav_to_tracking_report()
 
        gps_records: Dict[datetime.date, GpsRecord] = {}

        for date in WebSite.Actions.date_range_generator(start_date, finish_date):
            new_record: GpsRecord = GpsRecord(record_date = date, 
                                              kml_file = website.download_tracking_report(report_date = date, data_dir=destination))
            gps_records[date] = new_record


        website.browser.switch_to.default_content()

        website.open_playback()
        website.setup_playback()

        for date in website.Actions.date_range_generator(start_date, finish_date):

            if gps_records[date].kml_file is None:
                gps_records[date].kml_file = f"{destination}/{website.Structure.FILE_NAME_STRING}{date.strftime(website.Structure.DATE_TIME_YEAR_FIRST)}.kml"
 
            if gps_records[date].kml_is_valid():

                if date not in db_records:

                    website.set_playback_date(date)

                    gps_records[date].gps_data = website.get_gps_data()
                    gps_records[date].events = website.get_events()

        gps_records: List[GpsRecord] = list(gps_records.values())
        GpsRecord.bulk_update(gps_records, database)
    finally:

        website.browser.quit()
        database.connection.close()

def main() -> None:

    finish_date: datetime = datetime.now() - timedelta(days=2)
    start_date: datetime = finish_date# - timedelta(days=7)

    parser = ArgumentParser(description='Gathers data from GPS tracker web portal and stores in database')
    parser.add_argument('--start_date',type=date,required=False,help="start date to get shifts and jobs from",default=start_date)
    parser.add_argument('--finish_date',type=date,required=False,help="finish date to get shifts and jobs from",default=finish_date)
    parser.add_argument('--destination',type=FilePath,required=False,help="destination folder for downloaded data",default=f"{getenv('HOME')}/test")
    args, unknown = parser.parse_known_args()

    gather_gps_data(args.start_date, args.finish_date, args.destination)

if __name__ == '__main__':
    main()