from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class RoleMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    description = models.CharField(max_length=200)
    stampdatetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    updatestampdatetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tbl_role_mstr'
        app_label = 'system'
        managed = False
      

class UserMaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    mobile_no = models.PositiveBigIntegerField(unique=True) 
    address = models.TextField()
    upload_file = models.FileField(upload_to='staff/Adhaar/', max_length=100)
    stampdatetime = models.DateTimeField(auto_now_add=True)
    updatestampdatetime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)

    objects = models.Manager()  # 👈 Ensure this is present

    class Meta:
        db_table = 'tbl_user_mstr'
        app_label = 'system'
        managed = False

    def __str__(self):
        return self.name


    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)
    #     self.save()


class ModuleMaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    db_name = models.CharField(max_length=50)
    db_schema_name = models.CharField(max_length=50)
    db_pass = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    module_img = models.FileField(upload_to='module/image', max_length=100)
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    stampdatetime = models.DateTimeField( auto_now=True, auto_now_add=False)
    updatestampdatetime = models.DateTimeField( auto_now=True, auto_now_add=False)
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tbl_module_mstr'
        app_label = 'system'
        managed = False

class MenuUrlMaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    menu_name = models.CharField(max_length=200)
    url = models.CharField(max_length=200,null=True,blank=True)
    parent_menu = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleMaster, verbose_name= ("module"), on_delete=models.CASCADE)
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    is_toolbar = models.BooleanField(default=False)
    menu_icon = models.CharField(max_length=50, null=True,blank=True)
    order_no = models.PositiveSmallIntegerField(default=1)
    clear_query = models.CharField(max_length=10, default="cmd=clear")
    stampdatetime = models.DateTimeField( auto_now=True, auto_now_add=False)
    updatestampdatetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.menu_name

    class Meta:
        db_table = 'tbl_menu_url_mstr'
        app_label = 'system'
        managed = False


class MenuUrlPermissionMaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    menu = models.ForeignKey(MenuUrlMaster, on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleMaster, on_delete=models.CASCADE)
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE, null=True, blank=True)
    stampdatetime = models.DateTimeField( auto_now=True, auto_now_add=False)
    updatestampdatetime = models.DateTimeField( auto_now=True, auto_now_add=False)
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.menu.menu_name

    class Meta:
        db_table = 'tbl_menu_url_permission_mstr'
        app_label = 'system'
        managed = False


class MenuUrlPermissionDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    permission = models.ForeignKey(MenuUrlPermissionMaster, on_delete=models.CASCADE)
    is_save = models.BooleanField(default=False)
    is_update = models.BooleanField(default=False)
    is_close = models.BooleanField(default=False)
    is_list = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    stampdatetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    updatestampdatetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'tbl_menu_url_permission_dtls'
        app_label = 'system'
        managed = False
    
class ViewMenuUrlPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    role_id = models.IntegerField()
    role_name = models.CharField(max_length=50)
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50)
    module_id = models.IntegerField()
    module_name = models.CharField(max_length=50)
    menu_id = models.IntegerField()
    menu_name = models.CharField(max_length=50)
    parent_menu_id = models.IntegerField()
    parent_menu_name = models.CharField(max_length=50)
    permission_id = models.IntegerField()
    permission_detail_id = models.IntegerField()
    menu_status = models.IntegerField()
    user_status = models.IntegerField()
    permisstion_status = models.IntegerField()
    permission_dtl_status = models.IntegerField()
    is_save = models.BooleanField(default=False)
    is_update = models.BooleanField(default=False)
    is_close = models.BooleanField(default=False)
    is_list = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'view_menu_url_permission'
        app_label = 'system'
        managed = False  # Since this is a view, don't create a table for it.
       