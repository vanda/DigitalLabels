"""
This file handle the database migration from the first release of the DigitalLabel to the newest one
which introduce the ManytoMany relation between the MuseumObjects, TextLabels and Portals DigitalLabels
"""
from django.db import connection, transaction
cursor = connection.cursor()

# creating new database tables
cursor.execute("CREATE TABLE labels_baserelation (id integer NOT NULL PRIMARY KEY, position integer unsigned NOT NULL);")
cursor.execute("""CREATE TABLE "labels_digitallabelobject" (
    "baserelation_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "labels_baserelation" ("id"),
    "museumobject_id" integer NOT NULL REFERENCES "labels_museumobject" ("id"),
    "digitallabel_id" integer NOT NULL REFERENCES "labels_digitallabel" ("id"),
    "gateway_object" bool NOT NULL
);""")
cursor.execute("""CREATE TABLE "labels_portalobject" (
    "baserelation_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "labels_baserelation" ("id"),
    "museumobject_id" integer NOT NULL REFERENCES "labels_museumobject" ("id"),
    "portal_id" integer NOT NULL REFERENCES "labels_portal" ("id")
);""")
cursor.execute("""CREATE TABLE "labels_portaltextlabel" (
    "baserelation_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "labels_baserelation" ("id"),
    "portal_id" integer NOT NULL REFERENCES "labels_portal" ("id"),
    "textlabel_id" integer NOT NULL REFERENCES "labels_textlabel" ("id"),
    "biography" bool NOT NULL
);""")
cursor.execute("""CREATE INDEX "labels_digitallabelobject_69d4d0b2" ON "labels_digitallabelobject" ("digitallabel_id");""")
cursor.execute("""CREATE INDEX "labels_digitallabelobject_ebf6d5d9" ON "labels_digitallabelobject" ("museumobject_id");""")
cursor.execute("""CREATE INDEX "labels_portalobject_307912e4" ON "labels_portalobject" ("portal_id");""")
cursor.execute("""CREATE INDEX "labels_portalobject_ebf6d5d9" ON "labels_portalobject" ("museumobject_id");""")
cursor.execute("""CREATE INDEX "labels_portaltextlabel_307912e4" ON "labels_portaltextlabel" ("portal_id");""")
cursor.execute("""CREATE INDEX "labels_portaltextlabel_547dc814" ON "labels_portaltextlabel" ("textlabel_id");""")
transaction.commit_unless_managed()
print "New tables successfully created"

# get all museum objects linked to a digital label
dl_mos = cursor.execute('SELECT id, digitallabel_id, dl_position, CAST(gateway_object AS int) FROM labels_museumobject WHERE digitallabel_id IS NOT NULL')

# create the DL_museumobjects relations according to the new database structure
blid = 1
for obj in dl_mos.fetchall():
    cursor.execute("INSERT INTO labels_baserelation VALUES(%s,%s);" % (blid, obj[2]))
    cursor.execute("INSERT INTO labels_digitallabelobject VALUES(%s,%s,%s,%s);" % (blid, obj[0], obj[1], obj[3]))
    transaction.commit_unless_managed()
    blid += 1
print "Digital Label museum objects successfully migrated"

# get all museum objects linked to a portal
dl_mos = cursor.execute('SELECT id, portal_id, pt_position FROM labels_museumobject WHERE portal_id IS NOT NULL')

# create the Pt_museumobjects relations according to the new database structure
for obj in dl_mos.fetchall():
    cursor.execute("INSERT INTO labels_baserelation VALUES(%s,%s);" % (blid, obj[2]))
    cursor.execute("INSERT INTO labels_portalobject VALUES(%s,%s,%s);" % (blid, obj[0], obj[1]))
    transaction.commit_unless_managed()
    blid += 1
print "Portal museum objects successfully migrated"

# handling the museum object duplicates
numbs = []
mos = cursor.execute('SELECT id, museum_number, digitallabel_id, portal_id FROM labels_museumobject')
for obj in mos.fetchall():
    if obj[1] in numbs:
        cursor.execute('DELETE FROM labels_museumobject WHERE id = %s;' % (obj[0]))
        cursor.execute('DELETE FROM labels_image WHERE museumobject_id = %s;' % (obj[0]))
        if obj[2] is not None:
            cursor.execute("""UPDATE `labels_digitallabelobject`
            SET museumobject_id = (SELECT `id` FROM `labels_museumobject` WHERE `museum_number` = "%s" LIMIT 1)
            WHERE `museumobject_id` = "%s";""" % (obj[1], obj[0]))
        elif obj[3] is not None:
            cursor.execute("""UPDATE `labels_portalobject`
            SET museumobject_id = (SELECT `id` FROM `labels_museumobject` WHERE `museum_number` = "%s" LIMIT 1)
            WHERE `museumobject_id` = "%s";""" % (obj[1], obj[0]))
        transaction.commit_unless_managed()
    numbs.append(obj[1])
print "Museum Objects duplicates successfully merged"

# workaround for altering the museum objects table
cursor.execute("""CREATE TEMPORARY TABLE "labels_museumobject_backup" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL,
    "date_text" varchar(255) NOT NULL,
    "artist_maker" varchar(255) NOT NULL,
    "restored_altered" varchar(255) NOT NULL,
    "place" text NOT NULL,
    "materials_techniques" text NOT NULL,
    "museum_number" varchar(255) NOT NULL,
    "object_number" varchar(16) NOT NULL,
    "credit_line" varchar(255) NOT NULL,
    "artfund" bool NOT NULL,
    "main_text" text NOT NULL,
    "redownload" bool NOT NULL
);""")
cursor.execute("""INSERT INTO labels_museumobject_backup SELECT
    id, name, date_text, artist_maker, restored_altered, place,
    materials_techniques, museum_number, object_number, credit_line,
    artfund, main_text, redownload FROM labels_museumobject;""")
cursor.execute('DROP TABLE labels_museumobject;')
cursor.execute("""CREATE TABLE "labels_museumobject" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL,
    "date_text" varchar(255) NOT NULL,
    "artist_maker" varchar(255) NOT NULL,
    "restored_altered" varchar(255) NOT NULL,
    "place" text NOT NULL,
    "materials_techniques" text NOT NULL,
    "museum_number" varchar(255) NOT NULL,
    "object_number" varchar(16) NOT NULL,
    "credit_line" varchar(255) NOT NULL,
    "artfund" bool NOT NULL,
    "main_text" text NOT NULL,
    "redownload" bool NOT NULL
);""")
cursor.execute("""INSERT INTO labels_museumobject SELECT
    id, name, date_text, artist_maker, restored_altered, place,
    materials_techniques, museum_number, object_number, credit_line,
    artfund, main_text, redownload FROM labels_museumobject_backup;""")
cursor.execute('DROP TABLE labels_museumobject_backup;')
cursor.execute('CREATE INDEX "labels_museumobject_197a45bd" ON "labels_museumobject" ("object_number");')
transaction.commit_unless_managed()
print "Museum object table successfully altered to the upgraded version"

# get all text labels
tls = cursor.execute('SELECT id, portal_id, position, CAST(biography AS int) FROM labels_textlabel')

# create the text label relations according to the new database structure
for obj in tls.fetchall():
    cursor.execute("INSERT INTO labels_baserelation VALUES(%s,%s);" % (blid, obj[2]))
    cursor.execute("INSERT INTO  labels_portaltextlabel VALUES(%s,%s,%s,%s);" % (blid, obj[1], obj[0], obj[3]))
    transaction.commit_unless_managed()
    blid += 1
print "Text labels successfully migrated"

# workaround for altering the text labels table
cursor.execute("""CREATE TEMPORARY TABLE "labels_textlabel_backup" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(255) NOT NULL,
    "main_text" text NOT NULL
);""")
cursor.execute("""INSERT INTO labels_textlabel_backup SELECT id, title, main_text FROM labels_textlabel;""")
cursor.execute('DROP TABLE labels_textlabel;')
cursor.execute("""CREATE TABLE "labels_textlabel" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(255) NOT NULL,
    "main_text" text NOT NULL
);""")
cursor.execute("""INSERT INTO labels_textlabel SELECT id, title, main_text FROM labels_textlabel_backup;""")
cursor.execute('DROP TABLE labels_textlabel_backup;')
transaction.commit_unless_managed()
print "Text label table successfully altered to the upgraded version"
