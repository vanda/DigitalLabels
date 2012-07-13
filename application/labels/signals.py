from sorl.thumbnail import get_thumbnail


def get_api_data(sender, instance, **kwargs):

    if instance.id == None or instance.redownload == True:

        museum_object = instance.museumobject_json
        if museum_object:
            label_name = ''
            object_name = museum_object['fields']['object']
            object_title = museum_object['fields']['title']

            # Remove sort indicators
            object_title = object_title.replace('^', '')

            if (object_name and object_title) and (object_name !=
                                                        object_title):
                label_name = "%s (%s)" % (object_title, object_name)
            else:
                label_name = object_name

            instance.name = label_name
            instance.museum_number = museum_object['fields']['museum_number']
            instance.materials_techniques = \
                            museum_object['fields']['materials_techniques']

            instance.artist_maker = museum_object['fields']['artist']
            instance.place = museum_object['fields']['place']
            instance.date_text = museum_object['fields']['date_text']
            instance.credit_line = museum_object['fields']['credit']

            # get the first label text
            if len(museum_object['fields']['labels']) > 0:
                l = museum_object['fields']['labels'][-1]
                instance.main_text = l['fields']['label_text']

        else:
            # make note of error in title
            instance.name = "* UNABLE TO GET RECORD DATA FOR %s *" % (
                                                    instance.object_number)

        # don't redownload again
        instance.redownload = False


def get_related_api_data(sender, instance, **kwargs):
    """
    Retrieve VADAR images and individual labels as well
    """

    if instance.cmslabel_set.count() == 0:

        instance.create_cms_labels()

    if instance.image_set.count() == 0:

        instance.create_images()


def create_thumbnails(sender, instance, **kwargs):

    if instance.image_file:
        im = get_thumbnail(instance.local_filename, '540x540',
                                                    quality=85, pad=True)
        im = get_thumbnail(instance.local_filename, '128x128',
                                                    quality=85, pad=True)
        im = get_thumbnail(instance.local_filename, '222x222',
                                                    quality=85, pad=True)
        im = get_thumbnail(instance.local_filename, '44x44',
                                                    quality=85, pad=True)
        return im
