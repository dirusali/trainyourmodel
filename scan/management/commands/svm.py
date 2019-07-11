mport os
import shutil
import csv
import zipfile
from datetime import datetime
from urllib.request import URLopener
from django.core.management.base import BaseCommand
from products.management.commands.convertcsv import load_catalog_to_db
from products.models import AutomaticProductUpdate
from thebest5_catalog_products.settings import CATALOGS_ROOT


def decompress_file(input_file, output_dir, compression_format):
    if compression_format.lower() == 'zip':
        zip_ref = zipfile.ZipFile(input_file, 'r')
        zip_ref.extractall(output_dir)
        zip_ref.close()
        return True
    return False


class Command(BaseCommand):
    help = "Downloads the last catalogs for each shop and updates 'Product' database."

    def handle(self, *args, **options):
        print("Updating catalogs..")
        update_conf_list = AutomaticProductUpdate.objects.filter(order_number=1)
        for conf in update_conf_list:
            shop_shop = conf.shop
            print("Updating catalog for shop '%s'.." % shop_shop)
            print("-------------------------------------------------------- ")
            try:
                print("Dowloading catalog file for shop '%s', from url:%s" % (shop_shop, conf.catalog_url))
                file = URLopener()
                if not os.path.exists(CATALOGS_ROOT):
                    os.makedirs(CATALOGS_ROOT)
                catalog_filename = CATALOGS_ROOT+'/%s_catalog' % shop_shop
                if conf.is_compressed:
                    extension = '.%s' % conf.compress_format
                else:
                    extension = '.csv'
                catalog_filename += extension
                file.retrieve(conf.catalog_url, catalog_filename)
                print("Catalog file retrieved for shop '%s', local path:%s" % (shop_shop, catalog_filename))
                if conf.is_compressed:
                    print("Decompressing file ...")
                    # Get a new clean tmp dir
                    tmp_dir = CATALOGS_ROOT + '/%s_tmp' % shop_shop
                    if os.path.exists(tmp_dir):
                        shutil.rmtree(tmp_dir)
                    os.makedirs(tmp_dir)
                    # Extract catalog (should be a single file inside compressed file)
                    if not decompress_file(input_file=catalog_filename,
                                           output_dir=tmp_dir,
                                           compression_format=conf.compress_format):
                        print("Decompressing file ... ERROR")
                        return -1
                    # Copy and rename the extracted catalog file
                    extracted_catalog = os.listdir(tmp_dir)[0]
                    catalog_filename = catalog_filename[:-4] + ".csv"
                    extracted_catalog_path = os.path.abspath(os.path.join(tmp_dir, extracted_catalog))
                    shutil.copyfile(extracted_catalog_path, catalog_filename)
                    print("Decompressing file ... DONE")
                    print("Cleaning and preparing CSV FILE ...")
                    output_file = CATALOGS_ROOT+'/%s' % shop_shop + ".csv"            
                    csv_file = open(catalog_filename, 'r', errors = 'ignore')
                    with open(output_file, 'w') as fh:
                        reader = csv.reader(csv_file, delimiter=';')
                        next(reader,None)
                        writer = csv.writer(fh, delimiter=';')
                        writer.writerow(("aw_deep_link","product_name","search_price","merchant_name","delivery_cost","brand_name","product_model","delivery_time","product_GTIN"))
                        for r in reader:
                            count = 0
                            for i in r:
                               a = i.count(';')
                               count += a
                            if count ==0:
                                writer.writerow((r[0],r[1],r[2],r[3].replace(" ", ""),r[4],r[5],r[6],r[7],r[8]))
                    csv_file.close()
                    fh.close()
                conf.last_update = datetime.now()
                conf.local_file = catalog_filename
                conf.save()
            except Exception as e:
                print("ERROR processing catalog %s [SKIPPED]\n%s" %(shop_shop, e))
                continue
            print("------------------------------------------------------ ")
        print("All catalogs processed.")
