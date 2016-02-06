import ddgcorp.models


print None  # make new line


# add statuses
for s in ddgcorp.models.Status.Enum:
    try:
        ddgcorp.models.Status(
            name=s,
        ).save()
        print 'Status: "{}"'.format(ddgcorp.models.Status.Enum(s))
    except Exception as ex:
        print str(ex)


# add tasks
for s in ddgcorp.models.Status.Enum:
    status = ddgcorp.models.Status.objects.filter(name=s).first()
    for t in xrange(20):
        try:
            name = 'Task {}{}'.format(s, t)
            ddgcorp.models.Task(
                name=name,
                status=status,
            ).save()
            print 'Task: "{}"'.format(name)
        except Exception as ex:
            print str(ex)
