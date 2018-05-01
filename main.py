import os
import json
import zipfile
import webdav.client as wc
import datetime, time


def zipdir(ziph, path):
    # ziph is zipfile handle
    start = time.time()
    print("going to zip {} items/subfolders".format(len(os.listdir(path))))
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
    end = time.time()
    delta = (end - start)/1000
    print("done zipping took {} seconds".format(delta))


def main(config):
    options = config["webdav"]
    path = config["path"]
    filename = config["filename"]
    client = wc.Client(options)
    if not client.valid():
        raise Exception("Webdav client invalid..")

    zippedfile = datetime.datetime.today().strftime('%Y-%m-%d')+"-"+filename+".zip"

    ziph = zipfile.ZipFile(zippedfile, 'w', zipfile.ZIP_DEFLATED)
    zipdir(ziph=ziph, path=path)

    size = sum(zinfo.file_size for zinfo in ziph.filelist)
    zip_mb = float(size) / 1000 / 1000  # k

    print("going to upload %s with size %.2f MB to %s" % (zippedfile, zip_mb, options["webdav_hostname"]))
    ziph.close()

    file = zippedfile
    zippedfile = "/"+zippedfile
    with open(file, "rb") as fd:
        client.upload_from(fd, zippedfile)
    os.remove(file)


if __name__ == '__main__':
    if not os.path.isfile('config.json'):
        raise Exception("cant find config.json")
    with open('config.json', 'r') as f:
        config = json.load(f)
    main(config)
