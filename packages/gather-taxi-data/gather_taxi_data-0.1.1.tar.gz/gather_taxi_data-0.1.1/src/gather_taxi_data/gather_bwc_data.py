from datetime import datetime, timedelta, date
from argparse import ArgumentParser
from os import getenv
from pydantic import FilePath

from taxi_data_core.database import BwcDataBase as DataBase, Driver, Taxi, Shift, Job
from taxi_data_core.blackandwhitecabs_com_au import WebSite

def gather_bwc_data(start_date: date, finish_date: date, destination: str) -> None:

    try:
        database: DataBase = DataBase(db_path = f"{destination}/bwc_data.db")
        website: WebSite = WebSite(WebSite.Structure.WEB_UI_URL)

        website.login(WebSite.Structure.WEB_UI_USERNAME, WebSite.Structure.WEB_UI_PASSWORD)
        website.close_last_login_window()

        taxis = website.get_taxi_list()
        numbers = [taxi.fleet_number for taxi in taxis]

        Driver.bulk_update(database, website.get_driver_list())
        Taxi.bulk_update(database, taxis)
        [Shift.bulk_update(database, website.get_shift_list(number, from_date = start_date, to_date = finish_date)) for number in numbers]
        [Job.bulk_update(database, website.get_job_list(number, from_date = start_date, to_date = finish_date)) for number in numbers]

    finally:
        website.browser.quit()
        database.connection.close()

def main() -> None:

    finish_date: datetime = datetime.now() - timedelta(days=1)
    start_date: datetime = finish_date - timedelta(days=7)

    parser = ArgumentParser(description='Gathers data from BWWC web portal and stores in database')
    parser.add_argument('--start_date',type=date,required=False,help="start date to get shifts and jobs from",default=start_date)
    parser.add_argument('--finish_date',type=date,required=False,help="finish date to get shifts and jobs from",default=finish_date)
    parser.add_argument('--destination',type=FilePath,required=False,help="destination folder for downloaded data",default=f"{getenv('HOME')}/test")
    args, unknown = parser.parse_known_args()

    gather_bwc_data(args.start_date, args.finish_date, args.destination)

if __name__ == '__main__':
    main()