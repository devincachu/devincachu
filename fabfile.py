# -*- coding: utf-8 -*-
import contextlib
import os
import sys

from fabric.api import cd, env, run, settings, sudo
from fabric.contrib import django
from fabric.utils import abort

env.root = os.path.dirname(__file__)
env.app = os.path.join(env.root, 'devincachu')
env.base_dir = '/usr/home/devincachu'
env.project_root = os.path.join(env.base_dir, 'devincachu')
env.app_root = os.path.join(env.project_root, 'devincachu')
env.virtualenv = os.path.join(env.project_root, 'env')
env.shell = '/bin/sh -c'

sys.path.insert(0, env.root)

django.project('devincachu')

from django.conf import settings as django_settings


def update_app():
    run('([ -d %(project_root)s ] && cd %(project_root)s && git pull origin master) || (cd %(base_dir)s && git clone git://github.com/devincachu/devincachu.git)' % env)


def create_virtualenv_if_need():
    run('[ -d %(virtualenv)s ] || virtualenv --no-site-packages --unzip-setuptools %(virtualenv)s' % env)


def check_csstidy():
    if run('test -f %s' % django_settings.COMPRESS_CSSTIDY_BINARY).return_code != 0:
        abort("Você deve instalar o csstidy no caminho %s!" % django_settings.COMPRESS_CSSTIDY_BINARY)


def pip_install():
    run('CFLAGS=-I/usr/local/include LDFLAGS=-L/usr/local/lib %(virtualenv)s/bin/pip install -r %(project_root)s/requirements_env.txt' % env)


def create_local_settings():
    with cd(env.project_root):
        run('%(virtualenv)s/bin/python gerar_settings_local.py %(app_root)s/settings_local.py.example' % env)


def collect_static_files():
    with cd(env.app_root):
        run('%(virtualenv)s/bin/python manage.py collectstatic -v 0 --noinput' % env)


def syncdb():
    with cd(env.app_root):
        run('%(virtualenv)s/bin/python manage.py syncdb --noinput' % env)


def start_gunicorn():
    with cd(env.app_root):
        run('%(virtualenv)s/bin/gunicorn_django --pid=gunicorn.pid --daemon --workers=3 --access-logfile=devincachu_access.log --error-logfile=devincachu_error.log' % env)


def stop_gunicorn():
    with contextlib.nested(cd(env.app_root), settings(warn_only=True)):
        run('kill -TERM `cat gunicorn.pid`')


def graceful_gunicorn():
    with contextlib.nested(cd(env.app_root), settings(warn_only=True)):
        run('kill -HUP `cat gunicorn.pid`')


def reload_nginx():
    run("su -m root -c '/usr/local/etc/rc.d/nginx reload'")


def createsuperuser():
    with cd(env.app_root):
        run("%(virtualenv)s/bin/python manage.py createsuperuser" % env)


def clean_cache():
    sudo("rm -rf /usr/local/etc/nginx/cache/data/devincachu/*")


def deploy():
    update_app()
    create_virtualenv_if_need()
    pip_install()
    check_csstidy()
    collect_static_files()
