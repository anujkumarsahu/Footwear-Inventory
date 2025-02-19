from django.db import models

# Create your models here.

class ModuleMaster (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50,)
    module_image = models.ImageField(upload_to='modules/image', null=True, blank=True)
    db_name = models.CharField(max_length=100)
    db_user = models.CharField(max_length=200)
    db_host = models.CharField(max_length=200)
    db_pass = models.CharField(max_length=50)
    description = models.TextField()
    emp_id = models.IntegerField()
    status = models.SmallIntegerField(default=1)
    stampdatetime = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = 'tbl_module_mstr'
        app_label = 'system'
        managed = False
      
    
class RoleMaster(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField()
    emp_id = models.IntegerField()
    status = models.SmallIntegerField(default=1)
    stampdatetime = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = 'tbl_role_mstr'
        app_label = 'system'
        managed = False
        verbose_name = "Role Master"
     
    
    
class MenuMaster(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50,)
    url_name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50)
    order_no = models.SmallIntegerField()
    query_string = models.CharField(max_length=50,default='cmd=clear')
    parent_menu = models.ForeignKey("self", verbose_name="parent_menu", on_delete=models.CASCADE, null=True, blank=True)    
    module = models.ForeignKey(ModuleMaster, verbose_name=("module_id"), on_delete=models.CASCADE)
    remarks = models.TextField()
    emp_id = models.IntegerField()
    status = models.SmallIntegerField(default=1)
    stampdatetime = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = 'tbl_menu_mstr'
        app_label = 'system'
        managed = False
        verbose_name = "Menu Master"
        verbose_name_plural = "Menu Master"
        ordering = ['order_no'] 
    
    
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    emp_id = models.IntegerField()
    status = models.SmallIntegerField(default=1)
    stampdatetime = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = 'tbl_user_mstr'
        app_label = 'system'
       
    
class Employee(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('resigned', 'Resigned'),('terminated', 'Terminated')]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name  = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15,unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE,default=1)
    emp_code = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    profile_picture = models.ImageField(upload_to='employees/profile_pics/', blank=True, null=True,width_field=50, height_field=50)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, null=True,blank=True)
    is_status = models.SmallIntegerField(default=1)
    emp_id = models.IntegerField()
    stampdatetime = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = 'tbl_employee_mstr'
        app_label = 'system'
        managed = False
    
class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(ModuleMaster, on_delete=models.CASCADE)
    menu = models.ForeignKey(MenuMaster, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    emp_id = models.IntegerField()
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_view = models.BooleanField(default=True)
    can_read = models.BooleanField(default=True)
    stampdatetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_permission'
        app_label = 'system'
        managed = False

        
        
#     urlpatterns = [
#     path('', views.index, name='index'),
#     path('role/<str :action>/<int:id>',views.role_alter,name="role_alter" ), #action = view,create,update,delete,etc where create with id =0
#     path('employee/<str :action>/<int:id>',views.employee_alter,name="employee_alter" ),#action = view,create,update,delete,etcwhere create with id =0
# ] 
