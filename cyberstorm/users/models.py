from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class TeamManager(BaseUserManager):
    def create_user(self, team_name, team_leader, team_leader_email, password=None):
        if not team_name:
            raise ValueError("Team name is required")
        
        team = self.model(
            team_name=team_name,
            team_leader=team_leader,
            team_leader_email=team_leader_email,
        )
        team.set_password(password)  # Encrypt password
        team.save(using=self._db)
        return team

    def create_superuser(self, team_name, team_leader, team_leader_email, password):
        team = self.create_user(team_name, team_leader, team_leader_email, password)
        team.is_admin = True
        team.save(using=self._db)
        return team

class Team(AbstractBaseUser, PermissionsMixin):
    team_name = models.CharField(max_length=100, unique=True, primary_key=True)
    team_leader = models.CharField(max_length=100)
    team_leader_email = models.EmailField(unique=True)
    member_names = models.TextField(blank=True)  # Store names as CSV
    member_emails = models.TextField(blank=True)  # Store emails as CSV
    cleared_round1 = models.BooleanField(default=False)
    cleared_round2 = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = TeamManager()

    USERNAME_FIELD = "team_name"  # Login via `team_name`
    REQUIRED_FIELDS = ["team_leader", "team_leader_email"]

    def __str__(self):
        return self.team_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
