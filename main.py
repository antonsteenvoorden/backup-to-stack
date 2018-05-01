import os
import json
import zipfile
import webdav.client as wc
import datetime, time


def zipdir(ziph, path):
    # ziph is zipfile handle
    start = time.time()
    print(datetime.datetime.now(), ":going to zip {} items/subfolders".format(len(os.listdir(path))))
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
    end = time.time()
    delta = (end - start)/1000
    print(datetime.datetime.now(), ":done zipping took {} seconds".format(delta))


def main(config):
    options = config["webdav"]
    path = config["path"]
    filename = config["filename"]
    client = wc.Client(options)
    if not client.valid():
        print(datetime.datetime.now(), "Webdav client invalid..")
        raise Exception(datetime.datetime.now(), "Webdav client invalid..")

    zippedfile = datetime.datetime.today().strftime('%Y-%m-%d')+"-"+filename+".zip"

    ziph = zipfile.ZipFile(zippedfile, 'w', zipfile.ZIP_DEFLATED)
    zipdir(ziph=ziph, path=path)

    size = sum(zinfo.file_size for zinfo in ziph.filelist)
    zip_mb = float(size) / 1000 / 1000  # k

    print(datetime.datetime.now(), ":going to upload %s with size %.2f MB to %s" % (zippedfile, zip_mb, options["webdav_hostname"]))
    ziph.close()

    file = zippedfile
    zippedfile = "/"+zippedfile
    with open(file, "rb") as fd:
        client.upload_from(fd, zippedfile)
    print(datetime.datetime.now(), ":cleaning up zipped file")
    os.remove(file)


if __name__ == '__main__':
    print("\n")
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    if not os.path.isfile(os.path.join(__location__, 'config.json')):
        print(time.time(), ":cant find config.json at", os.path.join(__location__, 'config.json'))
        raise Exception(time.time(), ":cant find config.json at", os.path.join(__location__, 'config.json'))

    with open(os.path.join(__location__, 'config.json'), 'r') as f:
        config = json.load(f)
    main(config)
    print("Done")
