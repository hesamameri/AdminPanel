from django.db import models
from Administrator.models import User
# Here are the models for the tickets section in the panel project
# In order to prevent confusion we will explain the purpose of each form before its code.
# Also the models that it interacts with

#HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
# Ticket :
# Description :  When panel users register requests for other departments, their requests are in the form of tickets.
# Relations: TicketSystemCategory,TicketSystemPriority,TicketSystem,TicketSystemSource,TicketSystemStatus,TicketSystemType
class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    system = models.ForeignKey('TicketSystem', models.DO_NOTHING)
    category = models.ForeignKey('TicketSystemCategory', models.DO_NOTHING)
    status = models.ForeignKey('TicketSystemStatus', models.DO_NOTHING, blank=True)
    type = models.ForeignKey('TicketSystemType', models.DO_NOTHING)
    source = models.ForeignKey('TicketSystemSource', models.DO_NOTHING)
    priority = models.ForeignKey('TicketSystemPriority', models.DO_NOTHING,null=True, blank=True)
    doer = models.IntegerField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    obj_source_id = models.IntegerField(blank=True, null=True)
    obj_source_type = models.CharField(max_length=255, blank=True, null=True)
    voip_id = models.CharField(max_length=255, blank=True, null=True)
    family = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    phone2 = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=255)
    body = models.TextField()
    flag = models.IntegerField(blank=True, null=True)
    files = models.CharField(max_length=255, blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    star = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket'

# TicketAttachment
# Description : This model is to address all the files that are attached to the tickets created or altered.
# relations: Ticket
class TicketAttachment(models.Model):
    ticket_attachment_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255)
    size = models.FloatField(blank=True, null=True)
    uploader = models.IntegerField()
    upload_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_attachment'

# TicketComentRead
# Description : This model helps to register view and register dates for all the tickets
# relations: TicketComment
class TicketComentRead(models.Model):
    ticket_coment_read = models.AutoField(primary_key=True)
    ticket_comment = models.ForeignKey('TicketComment', models.DO_NOTHING)
    user_id = models.IntegerField()
    view_dt = models.DateTimeField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_coment_read'

# TicketComent
# Description : when the user registers a commment on a ticket. This model helps to address that.
# relations: Ticket
class TicketComment(models.Model):
    ticket_comment_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    visiblity = models.CharField(max_length=7, blank=True, null=True, db_comment="If visibility equal to visible then comment's show for requester")
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_comment'

# TicketCommentAttachment
# Description : If when a user writes a comment on the ticket and also attaches a file to its comment, then this model works to address
# that
# relations: TicketComment,
class TicketCommentAttachment(models.Model):
    ticket_comment_attachment = models.AutoField(primary_key=True)
    ticket_comment = models.ForeignKey(TicketComment, models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    ext = models.CharField(max_length=10)
    type = models.CharField(max_length=100, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    upload_dt = models.DateTimeField()
    uploader = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ticket_comment_attachment'

# TicketCustomer
# Description : This model is not yet used so the explanation is not necessary!
# relations: Ticket
class TicketCustomer(models.Model):
    ticket_customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    co_name = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_customer'

# TicketDoer
# Description : This model is to register people who are to complete the tickets
# relations: Ticket
class TicketDoer(models.Model):
    ticket_doer_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    doer = models.IntegerField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    leave_dt = models.DateTimeField(blank=True, null=True)
    leave_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_doer'
        db_table_comment = 'چه افراد دیگری نیز این تیکت نقش دارند\nو چه زمانی خودشان تصمیم گرفته اند از تیکت خارج شوند'

# TicketLog
# Description : with every update on a ticket the change will be displayed by using this model
# relations: Ticket
class TicketLog(models.Model):
    ticket_status_log_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_log'
        db_table_comment = 'با هر تغییر در وضعیت تیکت یک لاگ از وضعیت و تغییر دهنده وضعیت در جدول فوق ثبت میگردد'

# TicketSystem
# Description : This is the general model that all departments will be connected to.
# relations: 
class TicketSystem(models.Model):
    ticket_system_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=25, blank=True, null=True)
    color = models.CharField(max_length=25, blank=True, null=True)
    status = models.CharField(max_length=7, blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system'

# TicketSystemCategory
# Description : These are all the departments that deal with tickets and the tickets are bound to relate to one of these departments
# relations: TicketSystem
class TicketSystemCategory(models.Model):
    ticket_system_category_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    chart_id = models.IntegerField(blank=True, null=True)
    assign_to = models.IntegerField(blank=True, null=True)
    # assign_to = models.ForeignKey(User, models.DO_NOTHING)
    approver = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    send_sms = models.IntegerField()
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_category'

# TicketSystemCity
# Description : ?????????????????????????????????????????????????
# relations: TicketSystem
class TicketSystemCity(models.Model):
    ticket_system_city = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    city_id = models.IntegerField()
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    chart_id = models.IntegerField(blank=True, null=True, db_comment='بر اساس چارت سازمانی کدام چارت سازمانی وظیفه پاسخ گویی به تیکت های مربوط به شهر انتخاب شده را دارد')

    class Meta:
        managed = False
        db_table = 'ticket_system_city'

# TicketSystemField
# Description : ?????????????????????????????????????????????????
# relations: TicketSystem
class TicketSystemField(models.Model):
    ticket_system_field_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    groupname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    default_value = models.CharField(max_length=255, blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_field'

# TicketSystemPriority
# Description : this model helps to create priorities for each ticket in terms of low ,moderate and high
# relations: TicketSystem
class TicketSystemPriority(models.Model):
    ticket_system_priority_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=100, blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_priority'

# TicketSystemSource
# Description : This model determines the channel of contact . example: email, phone, whatsapp
# relations: TicketSystem
class TicketSystemSource(models.Model):
    ticket_system_source_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=100, blank=True, null=True)
    source_type = models.CharField(max_length=100)
    server = models.CharField(max_length=255, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_source'

# TicketSystemStatus
# Description : This model let the ticket have states of execution. example: done, processing and etc. ...
# relations: TicketSystem
class TicketSystemStatus(models.Model):
    ticket_system_status_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)
    need_qc = models.CharField(max_length=3, blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_status'

# TicketSystemTeam
# Description : none
# relations: TicketSystem
class TicketSystemTeam(models.Model):
    ticket_system_team_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    owner = models.IntegerField()
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_team'

# TicketSystemTeamMember
# Description : none
# relations: TicketSystem
class TicketSystemTeamMember(models.Model):
    ticket_system_team_member_id = models.AutoField(primary_key=True)
    ticket_system_team = models.ForeignKey(TicketSystemTeam, models.DO_NOTHING)
    member_id = models.IntegerField()
    register = models.IntegerField()
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_team_member'

# TicketSystemType
# Description : This model helps to define if a ticket is to be issued what type of job it is for. example: question,fixing issues, etc
# relations: TicketSystem
class TicketSystemType(models.Model):
    ticket_system_type_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    orderby = models.IntegerField()
    chart_id = models.IntegerField(blank=True, null=True, db_comment='چه عنوان شغلی در چارت سازمانی پاسخ دهنده خواهد بود')
    user_id = models.IntegerField(blank=True, null=True, db_comment='چه کاربری به صورت مستقیم پاسخ گو تیکت های وارده به این بخش خواهد بود')
    register = models.IntegerField()
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ticket_system_type'

# TicketSystemUser
# Description : This model connects users to tickets via TicketSystem connection.
# relations: TicketSystem
class TicketSystemUser(models.Model):
    ticket_system_user_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ticket_system_user'

# TicketTodo
# Description : this is basically the main part that is currently in use. This model allows the doer of then ticket to register a 
# a comment on the ticket. example : " job done. Replaced the sections necessary for the customer."
# relations: Ticket
class TicketTodo(models.Model):
    ticket_todo_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    body = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ticket_todo'

# TicketViewer
# Description : this is currently not in use
# relations: Ticket
class TicketViewer(models.Model):
    ticket_viewer_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    user_id = models.IntegerField()
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ticket_viewer'