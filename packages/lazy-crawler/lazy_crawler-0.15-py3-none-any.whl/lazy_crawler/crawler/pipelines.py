from scrapy import signals
from scrapy.exporters import CsvItemExporter
import json
from itemadapter import ItemAdapter
import openpyxl
from scrapy.utils.serialize import ScrapyJSONEncoder
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


class CSVPipeline(object):
    def __init__(self):
        self.created_time = datetime.datetime.now()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open(f"scraped_data_{self.created_time}.csv", "w+b")
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        self.created_time = datetime.datetime.now()
        self.items = []

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        file_name = f"scraped_data.json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(
                self.items, f, indent=2, cls=ScrapyJSONEncoder, ensure_ascii=False
            )

    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        return item


# GoogleSheetsPipeline
class GoogleSheetsPipeline(object):
    def __init__(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets",
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            "creds.json", scope
        )

        self.client = gspread.authorize(self.creds)

        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open("JobScrapeData").sheet1
        self.spreadsheet_key = ""  # key can find on url sections
        self.wks_name = "Sheet1"

    def _append_to_sheet(self, item):
        """Append item to spreadsheet"""
        # Add headings to the sheet if it's the first item
        if self.sheet.row_values(1) != list(item.keys()):
            values = list(item.keys())
            # append body to spreadsheet
            self.sheet.insert_row(values, index=self.sheet.row_count)

        else:
            # Add the item data to the sheet
            values = list(item.values())
            # append body to spreadsheet
            self.sheet.append_row(values)

    def process_item(self, item, spider):
        cell = self.sheet.find(item["id"])
        if cell:
            print("job is already exists in google sheet.........................!!")
        else:
            print("Now, adding jobs", item)
            time.sleep(5)
            self._append_to_sheet(item)
            return item


class ExcelWriterPipeline(object):
    def __init__(self):
        self.created_time = datetime.datetime.now()
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "Scraped Data"
        self.row_num = 1  # counter for the current row in the sheet

    def process_item(self, item, spider):
        # Add headings to the sheet if it's the first item
        if self.row_num == 1:
            self.ws.append(
                list(item.keys())
            )  # convert dict_keys to a list and use it as headings
        # Add the item data to the sheet
        self.ws.append(list(item.values()))
        self.row_num += 1  # increment the row counter
        # return ''
        return item

    def close_spider(self, spider):
        # self.wb.save(f"scraped_data_{self.created_time}.xlsx")  # save the workbook
        self.wb.save(f"scraped_data.xlsx")  # save the workbook
