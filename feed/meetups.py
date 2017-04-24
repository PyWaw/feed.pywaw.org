import peewee
import peewee_async
from playhouse.fields import ManyToManyField

from feed import settings

database = peewee_async.PostgresqlDatabase(**settings.DATABASE)


class Speaker(peewee.Model):
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    photo = peewee.CharField()

    class Meta:
        database = database
        db_table = 'meetups_speaker'

    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Sponsor(peewee.Model):
    logo = peewee.CharField()

    class Meta:
        database = database
        db_table = 'meetups_sponsor'


DeferredMeetupSponsor = peewee.Proxy()


class Meetup(peewee.Model):
    number = peewee.IntegerField()
    date = peewee.DateTimeField()
    is_ready = peewee.BooleanField()
    sponsors = ManyToManyField(Sponsor, through_model=DeferredMeetupSponsor)

    class Meta:
        database = database
        db_table = 'meetups_meetup'

    def title(self):
        return 'PyWaw #{}'.format(self.number)


class MeetupSponsor(peewee.Model):
    meetup = peewee.ForeignKeyField(Meetup)
    sponsor = peewee.ForeignKeyField(Sponsor)

    class Meta:
        database = database
        db_table = 'meetups_meetup_sponsors'


DeferredMeetupSponsor.initialize(MeetupSponsor)

DeferredTalkSpeaker = peewee.Proxy()


class Talk(peewee.Model):
    id = peewee.IntegerField()
    title = peewee.CharField()
    meetup = peewee.ForeignKeyField(Meetup, related_name='talks')
    speakers = ManyToManyField(Speaker, through_model=DeferredTalkSpeaker)

    class Meta:
        database = database
        db_table = 'meetups_talk'


class TalkSpeaker(peewee.Model):
    talk = peewee.ForeignKeyField(Talk, db_column='talk_id', index=True, null=True)
    speaker = peewee.ForeignKeyField(Speaker, db_column='speaker_id', index=True, null=True)

    class Meta:
        database = database
        db_table = 'meetups_talk_speakers'


DeferredTalkSpeaker.initialize(TalkSpeaker)

manager = peewee_async.Manager(database)


async def get_latest_meetup() -> Meetup:
    return await manager.get(Meetup.select().order_by(-Meetup.number))
