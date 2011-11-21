# -*- coding: utf-8 -*-
import contextlib
import os
import sys

from fabric.api import cd, env, roles, run, settings, sudo
from fabric.contrib import django, files

env.root = os.path.dirname(__file__)
env.app = os.path.join(env.root, 'devincachu')
env.base_dir = '/home/devincachu'
env.project_root = os.path.join(env.base_dir, 'devincachu')
env.app_root = os.path.join(env.project_root, 'devincachu')
env.virtualenv = os.path.join(env.project_root, 'env')
env.user = 'devincachu'
env.roledefs = {
    'server': ['devincachu.com.br'],
}

sys.path.insert(0, env.root)

django.project('devincachu')

from django.conf import settings as django_settings


@roles('server')
def update_app():
    if files.exists(env.project_root):
        with cd(env.project_root):
            run('git pull origin master')
    else:
        with cd(env.base_dir):
            run('git clone git://github.com/devincachu/devincachu.git')


@roles('server')
def create_virtualenv_if_need():
    if not files.exists(env.virtualenv):
        run('virtualenv --no-site-packages --unzip-setuptools %(virtualenv)s' % env)


@roles('server')
def install_csstidy_if_need():
    if not files.exists(django_settings.COMPRESS_CSSTIDY_BINARY):
        with cd('/tmp'):
            run('curl -O "http://ufpr.dl.sourceforge.net/project/csstidy/CSSTidy%20%28C%2B%2B%2C%20stable%29/1.3/csstidy-source-1.4.zip"')
            with settings(warn_only=True):
                run("unzip csstidy-source-1.4.zip")

            with cd("csstidy"):
                run("sed -i 's/#include <string>/#include <string>\\n#include <cstring>/g' csspp_globals.hpp && g++ *.cpp -o csstidy")
                sudo("cp csstidy %s" %  django_settings.COMPRESS_CSSTIDY_BINARY)


@roles('server')
def pip_install():
    run('%(virtualenv)s/bin/pip install -r %(project_root)s/requirements_env.txt' % env)


@roles('server')
def create_local_settings():
    with cd(env.project_root):
        run('%(virtualenv)s/bin/python gerar_settings_local.py %(app_root)s/settings_local.py.example' % env)


@roles('server')
def collect_static_files():
    with cd(env.app_root):
        run('%(virtualenv)s/bin/python manage.py collectstatic -v 0 --noinput' % env)


@roles('server')
def syncdb():
    with cd(env.app_root):
        run('%(virtualenv)s/bin/python manage.py syncdb --noinput' % env)


@roles('server')
def start_gunicorn():
    with cd(env.app_root):
        run('%(virtualenv)s/bin/gunicorn_django -p gunicorn.pid --daemon --workers=3' % env)


@roles('server')
def stop_gunicorn():
    with contextlib.nested(cd(env.app_root), settings(warn_only=True)):
        run('kill -9 `cat gunicorn.pid`')


@roles('server')
def graceful_gunicorn():
    with contextlib.nested(cd(env.app_root), settings(warn_only=True)):
        run('kill -HUP `cat gunicorn.pid`')


@roles('server')
def start_nginx():
    sudo('service nginx start')


@roles('server')
def stop_nginx():
    sudo('service nginx stop')


@roles('server')
def restart_nginx():
    sudo('service nginx restart')


@roles('server')
def reload_nginx():
    sudo('service nginx reload')


@roles('server')
def gerar_2011():
    run("curl -H 'Host: devincachu.com.br' http://localhost:8085/gerar.php")


@roles('server')
def createsuperuser():
    with cd(env.app_root):
        run("%(virtualenv)s/bin/python manage.py createsuperuser" % env)


@roles('server')
def clean_cache():
    sudo("rm -rf /opt/nginx/cache/data/devincachu/*")


@roles('server')
def deploy(db='no', start='no', create_local='no'):
    update_app()
    create_virtualenv_if_need()
    pip_install()
    install_csstidy_if_need()

    if create_local == 'yes':
        create_local_settings()

    collect_static_files()

    if db == 'yes':
        syncdb()

    if start == 'yes':
        start_gunicorn()
    else:
        graceful_gunicorn()

    reload_nginx()
