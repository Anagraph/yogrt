import os
import subprocess


class Source:
    def __init__(self, geometry_type, table_name, download_url, is_zip=False):
        self.type = geometry_type
        self.table_name = table_name
        self.download_url = download_url
        self.downloaded_path = None
        self.is_zip = is_zip

    def __repr__(self):
        return f"Source(type={self.type}, table_name={self.table_name}, download_url={self.download_url})"

    def download(self, destination_folder, ):
        p = subprocess.Popen(["wget", self.download_url, "-P", destination_folder, "-q"])
        p.wait()
        self.downloaded_path = os.path.join(destination_folder, os.path.basename(self.download_url))

        if self.is_zip:
            p = subprocess.Popen(["unzip", self.downloaded_path, "-d", destination_folder])
            p.wait()

    def import_to_database(self, host, port, database, user, password, schema):
        cmd = f"""ogr2ogr -progress -f "PostgreSQL" PG:"host='{host}' port='{port}' dbname='{database}' user='{user}' password='{password}'" -nln {self.table_name} {self.downloaded_path} -overwrite"""
        print(cmd)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()
